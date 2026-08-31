"""How much of the real player does our own agent actually reproduce?

    python -u scripts/probe_how_close_is_our_agent_to_the_real_player.py

Alex, 2026-08-27: *"there is a small but real difference between us and kawa ... we could probably
imitate kawa or dusta better than our planner"*.

That is the question this sizes, and it is the one that decides whether the imitation track is worth
anything. The DAgger student was cloned from `kagg/il/tape_teacher`, which wraps the SHIPPED AGENT --
our solver and planner, replaying only the opening tape. So the student's ceiling is our agent, not
the player. If our agent already reproduces the player op-for-op there is no headroom and a net
trained on the raw streams can only match it. If it diverges, that gap IS the prize: a BC on the real
recorded actions would be copying the human more faithfully than our solver does.

Money will not answer it. Our replay finishes within $58-$257 of the recorded result on all four
tapes, which looks like agreement and is not -- the bank is a season-long sum over a contested book
and two different routes can land on the same number.

So: per turn, compare our agent's action to the action actually recorded in the replay, on the board
the recording itself produced. Unit ops and market orders separately, because they fail differently.

`DROP` is compared on the op alone: `reference/kaggriculture.py:343` takes no arguments and dumps the
whole inventory, so `["DROP"]` and `["DROP","WHEAT",1]` are the same move and counting them as a
difference inflates the gap.
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def _op(u):
    if not u:
        return ("PASS",)
    if u[0] == "DROP":
        return ("DROP",)                    # arguments are ignored by the environment
    return tuple(str(z) for z in u)


def _mkt(a):
    c = collections.Counter()
    for o in (a or {}).get("market") or []:
        if o:
            c[tuple(str(z) for z in o)] += 1
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--tapes", type=int, default=4)
    ap.add_argument("--show", type=int, default=8)
    args = ap.parse_args()

    import dagger_tape as DT
    from kagg.il.tape_teacher import TapeTeacher
    from kaggle_environments import make

    print(f"{'tape':<16}{'op agree':>10}{'turns mkt':>11}{'mkt agree':>11}"
          f"{'first diff':>12}")
    for spec in DT.tape_games()[: args.tapes]:
        seat = spec["seat"]
        doc = json.loads((REPO / spec["tape_path"]).read_text())
        recorded = [((s[seat] or {}).get("action") or {}) for s in doc["steps"][1:]]

        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        ours = TapeTeacher(seat)
        op_ok = op_n = mk_ok = mk_n = 0
        first = None
        examples = []

        for turn in range(min(args.horizon, len(recorded))):
            if env.done:
                break
            obs = env.state[seat].observation
            mine = ours.act(obs)
            real = recorded[turn]

            a = [mine.get("farmer")] + list(mine.get("hands") or [])
            b = [real.get("farmer")] + list(real.get("hands") or [])
            n = max(len(a), len(b))
            for i in range(n):
                op_n += 1
                x = _op(a[i]) if i < len(a) else ("PASS",)
                y = _op(b[i]) if i < len(b) else ("PASS",)
                op_ok += int(x == y)
                if x != y and first is None:
                    first = turn
                if x != y and len(examples) < args.show:
                    examples.append(f"    turn {turn:>3} d{turn // 24:>2} h{turn % 24:>2} "
                                    f"unit {i}: REAL {' '.join(y):<22} ours {' '.join(x)}")

            if _mkt(real) or _mkt(mine):
                mk_n += 1
                mk_ok += int(_mkt(real) == _mkt(mine))

            # The RECORDED action drives, so every comparison is made on the board the real game
            # actually reached -- our agent is asked "what here?", never allowed to steer.
            opp = spec["opponent"][turn] if turn < len(spec["opponent"]) else {}
            env.step([real if p == seat else opp for p in range(2)])

        print(f"{spec['name'][:15]:<16}{100.0 * op_ok / max(1, op_n):>9.2f}%{mk_n:>11}"
              f"{100.0 * mk_ok / max(1, mk_n):>10.2f}%{str(first):>12}")
        for e in examples:
            print(e)


main()
