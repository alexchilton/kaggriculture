"""Which of his recordings, replayed into the OTHER games of its arm, reproduces the most turns?

`REPLAY_OPENING_TAPE` picked its two sources on season shape and end-of-season money. That is the
wrong criterion for a tape: a tape is replayed into 34 boards it was not recorded on, so what
matters is how typical its days are, not how good its own game was.

Measured 2026-08-24, his d8 BUY_SEED over 35 of his games, split by arm:

    MELON arm  n=15    {WHEAT 3} x12   <- 92498144, our melon tape, is in the majority
    STRAW arm  n=20    {WHEAT 3} x13   {STRAWBERRY 1, WHEAT 3} x3   {STRAWBERRY 1, WHEAT 1} x2
                       {STRAWBERRY 1} x1  <- 92466371, our strawberry tape, ALONE
                       {WHEAT 2} x1

That single outlier order is $69 spent one hour before a $131 hire block, and it costs the tenth
hire in eight strawberry-arm games -- every one of which then differs on the board at d8.

So: score every recording in an arm as a candidate tape, LEAVE-ONE-OUT, against every other game of
that arm. Compares recorded actions to recorded actions -- no simulation, so it is seconds not
minutes. Hands are truncated to the shorter of the two, because a replay is truncated to the hands
the farm owns (`schedule_agent.py:5527`).

Ranking on turns reproduced is not the same as ranking on money, and that is the point.
"""

import argparse
import collections
import glob
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DIRS = ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c", "kawa_2026-08-24",
        "leaders_2026-08-24", "losses", "top_guys", "top2", "ladder", "our_games", "new_leader")
TPD = 24
CURRENT = {"melon": "92498144", "straw": "92466371"}


def _norm(a, n_hands):
    if not isinstance(a, dict):
        return (("PASS",), (), ())
    return (tuple(a.get("farmer") or ["PASS"]),
            tuple(tuple(x) for x in (a.get("hands") or [])[:n_hands]),
            tuple(sorted(tuple(x) for x in (a.get("market") or []))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--lo", type=int, default=4)
    ap.add_argument("--hi", type=int, default=11)
    ap.add_argument("--arms", default="data/logs/branch_d4_d11.log")
    a = ap.parse_args()

    arm = {}
    for ln in open(REPO / a.arms):
        m = re.match(r"\s*(\d+)\s+(\d+)\s+\((\w+), (\w+)\)", ln)
        if m:
            arm[m.group(1)] = "straw" if m.group(3) == "True" else "melon"
    if not arm:
        sys.exit(f"no arms parsed from {a.arms} -- run scripts/is_it_the_wrong_branch.py first")

    files = {}
    for d in DIRS:
        for f in glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)

    acts, hands = {}, {}
    for ep, f in sorted(files.items()):
        if ep not in arm:
            continue
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                     # noqa: BLE001
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        steps = rec["steps"]
        seq, hn = {}, {}
        for t in range(a.lo * TPD, (a.hi + 1) * TPD):
            if t >= len(steps):
                break
            seq[t] = (steps[t][seat].get("action") or {})
            hn[t] = len(steps[t][seat]["observation"]["farms"][seat].get("hands") or [])
        acts[ep], hands[ep] = seq, hn

    n_turns = (a.hi - a.lo + 1) * TPD
    print(f"Leave-one-out: each recording scored as the tape for every OTHER game of its arm.")
    print(f"d{a.lo}-d{a.hi}, {n_turns} turns per pairing.\n")

    for which in ("melon", "straw"):
        pool = [e for e in acts if arm.get(e) == which]
        if len(pool) < 2:
            continue
        rows = []
        for cand in pool:
            tot = 0
            per = []
            for tgt in pool:
                if tgt == cand:
                    continue
                hit = 0
                for t, ta in acts[tgt].items():
                    ca = acts[cand].get(t)
                    if ca is None:
                        continue
                    n = min(hands[tgt].get(t, 0), hands[cand].get(t, 0))
                    hit += _norm(ca, n) == _norm(ta, n)
                tot += hit
                per.append(hit)
            rows.append((tot / max(1, len(per)), min(per), max(per), cand, len(per)))
        rows.sort(reverse=True)
        cur = CURRENT.get(which)
        print(f"{which.upper()} arm, {len(pool)} games "
              f"(each candidate scored against the other {len(pool) - 1})")
        print(f"   {'candidate':>10} {'mean turns':>11} {'worst':>7} {'best':>6}   of {n_turns}")
        for mean, lo, hi, cand, n in rows:
            tag = "   <-- SHIPPING NOW" if cand == cur else ""
            print(f"   {cand:>10} {mean:>11.1f} {lo:>7} {hi:>6}{tag}")
        best = rows[0]
        cur_row = next((r for r in rows if r[3] == cur), None)
        if cur_row and best[3] != cur:
            print(f"\n   best {best[3]} at {best[0]:.1f} mean turns against "
                  f"{cur} at {cur_row[0]:.1f}  ({best[0] - cur_row[0]:+.1f})")
        print()


if __name__ == "__main__":
    main()
