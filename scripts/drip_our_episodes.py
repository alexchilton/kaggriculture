"""Fetch our own submissions' episodes, ONE at a time, slowly.

Alex: *"be a bit more gentle than your grabbing 2000 at once drip them slowly or you overload the
server and get banned"*, and *"there is no hurry"*.

Different thing from `scripts/fetch_replays.py`, which pulls Kaggle's own published daily episode
DATASETS -- a bulk route they provide for exactly that purpose. This one hits the live
per-submission API, which is not a bulk route, so it goes one call every `--delay` seconds
(default 20), with a hard `--max` per run and every existing file skipped, so an interrupted run
resumes without re-asking for anything. A failure backs off six times the delay and three failures
stop the run: a tight retry against a rate limiter is how an IP gets blocked.

**Brotli is disabled before `kaggle` is imported, and that is not optional here.** With the stock
`Accept-Encoding: gzip,deflate,br,zstd`, every replay download fails on this machine:

    ('Received response with content-encoding: br, but failed to decode it.',
     error("brotli: decoder process called with data when 'can_accept_more_data()' is False"))

That is the urllib3-2.3 / brotlicffi-1.2 streaming interaction, not a server problem -- nothing had
even reached Kaggle's rate limiter. `pip install` is not available here, so the fix is to stop
advertising `br` rather than to upgrade the decoder.

The API is called directly rather than through the CLI, so episode ids come back as objects instead
of being scraped out of a printed table with a regex.

    python -u scripts/drip_our_episodes.py 55786408 55786494 --out data/seed_scripts/ours_2026-08-26
"""

import argparse
import pathlib
import sys
import time

# BEFORE importing kaggle: urllib3 builds its Accept-Encoding once, at import.
import urllib3.util.request as _ur                                       # noqa: E402
#: **`identity`, not `gzip`.** Dropping only `br` fixed the brotli crash and produced a second one:
#: `KeyError: 'content-length'`. With a compressed encoding the server replies chunked, and the
#: 2.0.2 downloader indexes that header unconditionally. Asking for no compression restores it.
#: The cost is bandwidth -- ~30 MB a file rather than a few -- which is the right trade when the
#: thing being protected is Kaggle's request rate, not our download size.
_ur.ACCEPT_ENCODING = "identity"

import kaggle                                                            # noqa: E402


def episode_ids(api, submission_id):
    """Episode ids this submission played, newest first, straight off the API object."""
    eps = api.competition_list_episodes(int(submission_id))
    out = []
    for e in eps or []:
        eid = getattr(e, "id", None)
        if eid is None and isinstance(e, dict):
            eid = e.get("id")
        if eid is not None:
            out.append(int(eid))
    return out



def _fetch_replay(api, episode_id, dest):
    """Write one replay, bypassing `KaggleApi.download_file`.

    **That helper cannot fetch a replay on this client.** It opens with

        size = int(response.headers["Content-Length"])

    unconditionally, and the replay endpoint answers chunked, so every call dies on
    `KeyError: 'content-length'` -- with `br`, with `gzip`, and with `identity` alike. The encoding
    was a red herring; only the brotli crash was about encoding.

    The response body IS the replay JSON, so it just gets written. `competition_episode_replay` also
    names its output `episode-<id>-replay.json`, not `<id>.json`, which is a second reason not to
    call it: the caller here keys files by bare episode id so the analysis scripts can glob them
    alongside the recorded tapes.
    """
    from kagglesdk.competitions.types.competition_api_service import ApiGetEpisodeReplayRequest
    with api.build_kaggle_client() as k:
        req = ApiGetEpisodeReplayRequest()
        req.episode_id = int(episode_id)
        resp = k.competitions.competition_api_client.get_episode_replay(req)
    body = getattr(resp, "content", None)
    if body is None:
        body = resp if isinstance(resp, (bytes, bytearray)) else str(resp).encode()
    tmp = dest.with_suffix(".part")
    tmp.write_bytes(body)
    tmp.replace(dest)                     # atomic: a killed run never leaves a half file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("submissions", nargs="+")
    ap.add_argument("--out", default="data/seed_scripts/ours_2026-08-26")
    ap.add_argument("--delay", type=float, default=20.0, help="seconds between calls")
    ap.add_argument("--max", type=int, default=20, help="hard cap on downloads this run")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    print(f"out={out}  delay={args.delay}s  max={args.max}", flush=True)
    print(f"Accept-Encoding pinned to {_ur.ACCEPT_ENCODING!r}", flush=True)

    api = kaggle.api
    wanted = []
    for sub in args.submissions:
        try:
            ids = episode_ids(api, sub)
        except Exception as e:                                            # noqa: BLE001
            print(f"  episodes {sub}: FAILED {type(e).__name__}: {e}", flush=True)
            continue
        print(f"  episodes {sub}: {len(ids)}", flush=True)
        for eid in ids:
            if eid not in wanted:
                wanted.append(eid)
        time.sleep(args.delay)

    print(f"total distinct episodes: {len(wanted)}", flush=True)
    got = skipped = fails = 0
    for eid in wanted:
        if got >= args.max:
            print(f"hit --max {args.max}; {len(wanted)-got-skipped-fails} left for the next run",
                  flush=True)
            break
        dest = out / f"{eid}.json"
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        try:
            _fetch_replay(api, int(eid), dest)
            ok = dest.exists() and dest.stat().st_size > 0
        except Exception as e:                                            # noqa: BLE001
            ok, err = False, f"{type(e).__name__}: {e}"
        else:
            err = "wrote nothing"
        if ok:
            got += 1
            print(f"  {eid} ok ({dest.stat().st_size/1e6:.1f} MB)   {got}/{args.max}", flush=True)
            time.sleep(args.delay)
        else:
            fails += 1
            print(f"  {eid} FAILED {err[:200]}", flush=True)
            print(f"  backing off {args.delay*6:.0f}s", flush=True)
            time.sleep(args.delay * 6)
            if fails >= 3:
                print("three failures; stopping rather than pushing", flush=True)
                break
    print(f"done: {got} downloaded, {skipped} already here, {fails} failed, into {out}", flush=True)


if __name__ == "__main__":
    main()
