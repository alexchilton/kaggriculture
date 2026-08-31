"""How are our newest submissions actually playing on the ladder, right now.

Why this exists: `fetch_replays.py` and `fetch_leader_episodes.sh` pull from the nightly public
episode datasets. Those lag a day and hold a high-rated *sample* -- they are for finding teachers,
not for grading ourselves. Measured 2026-08-24: of 354 downloaded games with us in them, 352 were
played by builds older than the 2500, so the local corpus was grading an agent we no longer ship.

What this reads, and what it deliberately does NOT read:

- `competitions.EpisodeService/ListEpisodes` returns, for every episode, each agent's `teamId`,
  `submissionId`, `reward` (the bank the seat finished on) and `updatedScore` (its rating after
  the game). That is enough for win/loss and money per submission.
- It does NOT return the replay body. Every method name I probed for one -- `GetEpisodeReplay`,
  `GetReplay`, `DownloadReplay`, `GetEpisodeReplayContent`, under both `competitions.EpisodeService`
  and `competitions.SimulationService` -- returns 404, as do the plain URL forms. So per-turn
  analysis still needs a replay downloaded from the web UI. This tool answers "is it winning",
  not "what did it do on d28".

The scan: `ListEpisodes` has no team filter (only `ids` and `submissionId`), but ids are dense --
a request for 100 consecutive ids returns 100 episodes -- and roughly 1 in 100 is ours. So this
walks the id space backwards from the newest episode in blocks of 100 and keeps ours.

    python -u scripts/pull_our_episodes.py --subs 2 --want 40

Credentials come from `~/.kaggle/kaggle.json` at runtime. They are never printed or logged.
"""

import argparse
import base64
import collections
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
OUR_TEAM = 16632291          # learned from a game we know we played; see --bootstrap
BLOCK = 100


def _tok():
    c = json.loads((pathlib.Path.home() / ".kaggle" / "kaggle.json").read_text())
    return base64.b64encode(f"{c['username']}:{c['key']}".encode()).decode()


def _list(ids, tok, retries=3):
    """`ListEpisodes` for a batch of episode ids. Returns the decoded response, or None."""
    body = json.dumps({"ids": list(ids)}).encode()
    hdr = {"Content-Type": "application/json", "Authorization": f"Basic {tok}",
           "User-Agent": "kaggle-cli"}
    for k in range(retries):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(URL, data=body, headers=hdr), timeout=120) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(5 * (k + 1))
                continue
            print(f"  HTTP {e.code} on a block of {len(ids)}", flush=True)
            return None
        except Exception as e:                                               # noqa: BLE001
            print(f"  {e!r}", flush=True)
            time.sleep(3)
    return None


def newest_episode_id(tok, start):
    """Walk forward from `start` until a block comes back empty. Returns the highest live id."""
    lo, step = start, 20_000
    while True:
        r = _list(range(lo + step, lo + step + BLOCK), tok)
        if not r or not (r.get("episodes") or []):
            break
        lo += step
        print(f"  ...alive at {lo}", flush=True)
    # Refine: halve the step until nothing further is alive.
    while step > BLOCK:
        step //= 2
        r = _list(range(lo + step, lo + step + BLOCK), tok)
        if r and (r.get("episodes") or []):
            lo += step
    return lo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subs", type=int, default=2, help="how many of our NEWEST submissions")
    ap.add_argument("--want", type=int, default=40, help="stop once each has this many games")
    ap.add_argument("--from-id", type=int, default=0, help="skip the search, scan down from here")
    ap.add_argument("--max-blocks", type=int, default=400)
    ap.add_argument("--out", default="data/logs/our_ladder_games_2026-08-24.jsonl")
    a = ap.parse_args()

    tok = _tok()
    top = a.from_id or newest_episode_id(tok, 98_335_212)
    print(f"newest episode id ~{top}\nscanning down in blocks of {BLOCK}\n", flush=True)

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")

    subs = {}                       # submissionId -> dateSubmitted
    games = collections.defaultdict(list)
    cur = top
    for b in range(a.max_blocks):
        r = _list(range(cur - BLOCK, cur), tok)
        cur -= BLOCK
        if not r:
            continue
        meta = {s["id"]: s for s in (r.get("submissions") or [])}
        for e in r.get("episodes") or []:
            ours = [x for x in (e.get("agents") or []) if x.get("teamId") == OUR_TEAM]
            if not ours:
                continue
            me = ours[0]
            them = [x for x in e["agents"] if x is not me]
            sid = me["submissionId"]
            subs.setdefault(sid, (meta.get(sid) or {}).get("dateSubmitted", "?"))
            row = {"episode": e["id"], "end": e.get("endTime"), "sub": sid,
                   "ours": me.get("reward"), "theirs": them[0].get("reward") if them else None,
                   "score_after": me.get("updatedScore")}
            games[sid].append(row)
            fh.write(json.dumps(row) + "\n")
            fh.flush()
        newest = sorted(subs, key=lambda s: subs[s], reverse=True)[: a.subs]
        if newest and all(len(games[s]) >= a.want for s in newest):
            print(f"have {a.want} games for each of the newest {a.subs} submissions", flush=True)
            break
        if b % 10 == 0:
            tot = sum(len(v) for v in games.values())
            print(f"  block {b}: id>{cur}, {tot} of our games so far", flush=True)
        time.sleep(0.4)
    fh.close()

    print(f"\n{'submissionId':>13}  {'submitted':<26} {'games':>5} {'W':>4} {'L':>4} "
          f"{'D':>3} {'win%':>6} {'our bank':>10} {'their bank':>11} {'rating':>8}")
    for sid in sorted(subs, key=lambda s: subs[s], reverse=True):
        g = [x for x in games[sid] if x["ours"] is not None and x["theirs"] is not None]
        if not g:
            continue
        w = sum(1 for x in g if x["ours"] > x["theirs"])
        loss = sum(1 for x in g if x["ours"] < x["theirs"])
        d = len(g) - w - loss
        ob = sum(x["ours"] for x in g) / len(g)
        tb = sum(x["theirs"] for x in g) / len(g)
        last = sorted(g, key=lambda x: x["end"] or "")[-1]["score_after"]
        print(f"{sid:>13}  {subs[sid]:<26} {len(g):>5} {w:>4} {loss:>4} {d:>3} "
              f"{w/len(g):>5.0%} {ob:>10,.0f} {tb:>11,.0f} {last or 0:>8.1f}")
    print(f"\nrows written to {out}")


if __name__ == "__main__":
    main()
