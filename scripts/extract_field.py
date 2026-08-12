"""Pull the bare ACTION STREAM of each ladder opponent out of a downloaded episode.

A downloaded episode is ~30 MB because it carries every observation. The action stream is a few
hundred KB, and it is the whole of what an open-loop opponent is: this competition's top agents
submit a fixed 720-turn script rather than a policy, so replaying their actions on a different board
is not an approximation of them -- it is exactly what they do on the ladder.

That is what makes a field of recorded opponents a fair harness and a MIRROR an unfair one. A mirror
puts ten cows on both sides of a milk book that no real pairing ever gluts, and then measures the
glut. Every opponent in these recordings runs COW 8 / SHEEP 6 against our COW 10 / SHEEP 4.

    python -u scripts/extract_field.py ~/Downloads/*.json
"""
import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / "data/seed_scripts/field"
ME = "alex chilton"


def extract(path, me=ME):
    d = json.loads(pathlib.Path(path).read_text())
    names = d["info"]["TeamNames"]
    if me not in names:
        return None
    us = names.index(me)
    them = 1 - us
    acts = []
    for step in d["steps"][1:]:
        a = (step[them] or {}).get("action") or {}
        acts.append([a.get("farmer") or ["PASS"],
                     list(a.get("hands") or []),
                     list(a.get("market") or [])])
    return {
        "team": names[them],
        "episode": d["info"].get("EpisodeId"),
        "seat_in_recording": them,
        "their_money": d["rewards"][them],
        "our_money": d["rewards"][us],
        "actions": acts,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    kept = []
    for p in args.episodes:
        try:
            rec = extract(p)
        except Exception as exc:                      # a partial download is not a reason to stop
            print(f"  skip {pathlib.Path(p).name}: {type(exc).__name__} {exc}", file=sys.stderr)
            continue
        if rec is None:
            print(f"  skip {pathlib.Path(p).name}: not one of our games")
            continue
        # Name by EPISODE, not by team: several of these are the same opponent on different boards,
        # and a name collision would silently drop one of them.
        dst = out / f"{rec['episode']}.json"
        dst.write_text(json.dumps(rec))
        kept.append((rec["team"], rec["episode"], rec["their_money"], rec["our_money"],
                     dst.stat().st_size / 1024))

    print(f"\n  wrote {len(kept)} opponent scripts to {out}")
    print(f"  {'team':<24}{'episode':>10}{'theirs':>10}{'ours':>10}{'KB':>8}")
    # `None` rewards happen -- an errored game still has a usable action stream, but it must not
    # crash the listing and it must be visible rather than silently sorted somewhere arbitrary.
    for team, ep, theirs, ours, kb in sorted(kept, key=lambda r: -(r[2] or 0)):
        t = f"{theirs:>10,.0f}" if theirs is not None else f"{'ERR':>10}"
        o = f"{ours:>10,.0f}" if ours is not None else f"{'ERR':>10}"
        print(f"  {team:<24}{ep:>10}{t}{o}{kb:>8.0f}")


if __name__ == "__main__":
    main()
