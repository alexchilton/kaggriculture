"""Let the clone free-run a held-out カワシギ seat and watch it come apart, day by day.

    python -u scripts/where_does_the_clone_come_off_the_rails.py \
        --ckpt data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl --rank 401

THE GAP THIS IS AIMED AT
------------------------
Measured today on seats the checkpoint never trained on:

    op agreement   77.9%      bundle top-1 on traded turns   80.6%
    money in play  ~$25 from a $3,000 start

Those two are both true, so the loss is not in the imitation. Per-turn agreement is measured
TEACHER-FORCED -- every row is scored from the board カワシギ actually stood on. A free-running clone
gets its own board from turn 1, and a 78% op rate means roughly one op in five is its own. This asks
what that costs, and when.

WHAT IT DOES
------------
Plays the clone in our seat on a held-out seat's own config and seed, against that game's RECORDED
opponent, and compares against the teacher's own recorded position at the start of every day:

    bank        money at day start, ours against his
    tiles       owned (not LOCKED) tiles, so a missed land purchase shows up
    crew        hands, so a missed hire shows up -- and the crew is re-rented every morning
    first div   the first turn at which the clone's action differs from the recording. Up to that
                turn the two are on the same board, so it is a like-for-like comparison; after it,
                the boards are different and only the day marks mean anything.

Read the FIRST day the marks separate, not the season total. An earlier day's failure is inherited
by every later one -- the project rule -- and a bank that is short at hour 22 of day 4 refuses a
land purchase that changes the remaining twenty-five days.
"""
import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

TPD = 24


def owned(farm):
    tiles = farm.get("tiles") or []
    return sum(1 for row in tiles for c in row
               if c is None or (isinstance(c, dict) and c.get("kind") != "LOCKED"))


def marks_from_replay(doc, seat, days):
    """`{day: (bank, owned, hands)}` read straight out of the recording."""
    out, steps = {}, doc["steps"]
    for d in range(days):
        i = d * TPD
        if i >= len(steps):
            break
        obs = (steps[i][0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if seat >= len(farms) or not farms[seat]:
            continue
        f = farms[seat]
        out[d] = (int(f.get("money") or 0), owned(f), len(f.get("hands") or []))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--team", default="カワシギ")
    ap.add_argument("--rank", type=int, default=401, help="1-based rank of the held-out seat")
    ap.add_argument("--days", type=int, default=17)
    ap.add_argument("--turns", type=int, default=719)
    args = ap.parse_args()

    sys.path.insert(0, str(REPO / "scripts"))
    import breakdown as B
    from kaggle_environments import make

    from kagg.agents import neural
    from kagg.il import bc

    ranked = bc.rank_seats(bc.find_replays("data"), team=args.team)
    if args.rank > len(ranked):
        raise SystemExit(f"only {len(ranked)} seats; --rank {args.rank} is out of range")
    ref = ranked[args.rank - 1]
    doc = json.loads(pathlib.Path(ref.path).read_text())
    seat = ref.seat
    print(f"seat  {pathlib.Path(ref.path).name}  seat {seat}  teacher banked ${ref.bank:,.0f}")
    print(f"rank  {args.rank} of {len(ranked)}   (checkpoint trained on the top 400)\n", flush=True)

    cfg = B.env_config(pathlib.Path(ref.path))
    cfg.pop("steps", None)
    if (doc.get("info") or {}).get("seed") is not None:
        cfg["seed"] = int(doc["info"]["seed"])
    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)

    clone = neural.make_agent(args.ckpt)
    recorded = [((s[seat] or {}).get("action") or {}) for s in doc["steps"][1:]]
    opp_rec = [((s[1 - seat] or {}).get("action") or {}) for s in doc["steps"][1:]]

    ours, first_div = {}, None
    for turn in range(args.turns):
        if env.done:
            break
        obs = env.state[seat].observation
        if turn % TPD == 0:
            f = (obs.get("farms") or [None, None])[seat] or {}
            ours[turn // TPD] = (int(f.get("money") or 0), owned(f), len(f.get("hands") or []))

        mine = clone(obs)
        if first_div is None and turn < len(recorded):
            want = recorded[turn]
            same = (list(mine.get("farmer") or []) == list(want.get("farmer") or [])
                    and [list(h) for h in (mine.get("hands") or [])]
                        == [list(h) for h in (want.get("hands") or [])]
                    and sorted(tuple(o) for o in (mine.get("market") or []))
                        == sorted(tuple(o) for o in (want.get("market") or [])))
            if not same:
                first_div = turn
                print(f"FIRST DIVERGENCE at turn {turn}  (day {turn // TPD} hour {turn % TPD})")
                # **Print the hands themselves, not their count.** The first version printed
                # `hands 5` on both sides and called it a divergence, which shows nothing: the
                # difference is inside the list. Per-slot, so the offending hand is named.
                th = [list(h) for h in (want.get("hands") or [])]
                ch = [list(h) for h in (mine.get("hands") or [])]
                print(f"  teacher  farmer {want.get('farmer')}  market {want.get('market')}")
                print(f"  clone    farmer {mine.get('farmer')}  market {mine.get('market')}")
                for i in range(max(len(th), len(ch))):
                    a = th[i] if i < len(th) else None
                    b = ch[i] if i < len(ch) else None
                    flag = "   <-- differs" if a != b else ""
                    print(f"    hand {i}   teacher {str(a):<28} clone {str(b):<28}{flag}")
                print(flush=True)

        theirs = opp_rec[turn] if turn < len(opp_rec) else {}
        acts = [None, None]
        acts[seat] = mine
        acts[1 - seat] = {"farmer": theirs.get("farmer") or ["PASS"],
                          "hands": list(theirs.get("hands") or []),
                          "market": theirs.get("market") or []}
        env.step(acts)

    if first_div is None:
        print("the clone never diverged from the recording over the compared turns\n")

    theirs_marks = marks_from_replay(doc, seat, args.days)
    print(f"  {'day':>4}{'bank ours/teacher':>26}{'tiles':>14}{'crew':>10}")
    for d in range(args.days):
        a, b = ours.get(d), theirs_marks.get(d)
        if a is None or b is None:
            continue
        print(f"  {d:>4}{f'{a[0]:,}/{b[0]:,}':>26}{f'{a[1]}/{b[1]}':>14}{f'{a[2]}/{b[2]}':>10}")

    final = int(env.state[seat].observation["farms"][seat]["money"])
    print(f"\n  final bank   ours ${final:,}   teacher ${ref.bank:,.0f}")


main()
