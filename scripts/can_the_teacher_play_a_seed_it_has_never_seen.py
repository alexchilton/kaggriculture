"""Does the shipped agent generalise off its four tapes -- and does it if the replay is switched off?

    python -u scripts/can_the_teacher_play_a_seed_it_has_never_seen.py --seeds 6

THE QUESTION, which is Alex's
-----------------------------
*"is there any way to take the kawa agent (which theoretically plays on any seed exactly the same)
and use it to play the DAgger on any seed rather than just the 4 it learned?"*

DAgger already permits it -- `TapeTeacher.act(obs)` answers from whatever board it is handed, and
`scripts/dagger_tape.py` restricted the seeds by choice, not by capability:

    "The start state is fixed and weedSpawnChance is 0.0, so the four tapes' own seeds are the four
     games ... a tape replayed on a foreign seed is a tape played into a board its plan does not
     describe."

Whether that caution is binding is a measurement, and it has not been made. The student cloned from
this teacher banks $300 on seed 9000 (`data/logs/what_breaks_the_clone.log`). Nobody has checked
what the TEACHER banks there. If the teacher also collapses, the student is faithful and the ceiling
is the teacher -- no amount of extra seeds helps, because there is nothing correct to imitate.

TWO ARMS, and they have opposite consequences
---------------------------------------------
  replay ON   `REPLAY_OPENING_DAYS = tuple(range(30))` -- the agent sends kawa's RECORDED actions,
              keyed on turn index alone and never on the seed (`schedule_agent.py:3919, 4026`).
              On a foreign board those ops are a fixed tape played into the wrong game.

  replay OFF  the same agent falling through to its own planner and router, which read the LIVE
              board every turn and are seed-independent by construction.

If `replay OFF` banks well on fresh seeds, that is the teacher to run DAgger against, on as many
seeds as we like, and the resulting student would have no reason to memorise four trajectories.

**The switch is monkeypatched here and only here.** `REPLAY_OPENING_DAYS` is left exactly as it
ships; this process rebinds it in memory for the duration of one arm. Nothing is written, and the
shipped agent is not edited -- the point is to measure the alternative, not to adopt it.
"""
import argparse
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def play(seed, opponent, turns):
    """One full game on `seed`; returns (our bank, their bank)."""
    from kagg.il.tape_teacher import TapeTeacher
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = TapeTeacher(0)
    for t in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        n_units = 1 + len(obs["farms"][0].get("hands") or [])
        mine = me.sendable(me.act(obs), n_units)
        env.step([mine, opponent(env.state[1].observation)])
    farms = env.state[0].observation["farms"]
    return float(farms[0]["money"]), float(farms[1]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--turns", type=int, default=719)
    ap.add_argument("--base-seed", type=int, default=9000)
    args = ap.parse_args()

    from kagg.search import schedule_agent as SA

    def idle(_obs):
        """A do-nothing opponent. The question is whether the teacher FARMS, not whether it wins."""
        return {"farmer": ["PASS"], "hands": [], "market": []}

    shipped = SA.REPLAY_OPENING_DAYS
    seeds = [args.base_seed + 137 * i for i in range(args.seeds)]

    print(f"shipped REPLAY_OPENING_DAYS covers {len(shipped)} days")
    print(f"{args.seeds} fresh seeds, {args.turns} turns, idle opponent\n")
    print(f"  {'seed':>10}{'replay ON':>14}{'replay OFF':>14}")

    on, off = [], []
    for s in seeds:
        SA.REPLAY_OPENING_DAYS = shipped
        a, _ = play(s, idle, args.turns)
        SA.REPLAY_OPENING_DAYS = ()
        b, _ = play(s, idle, args.turns)
        on.append(a)
        off.append(b)
        print(f"  {s:>10}{a:>14,.0f}{b:>14,.0f}", flush=True)
    SA.REPLAY_OPENING_DAYS = shipped

    print(f"\n  {'':>10}{'replay ON':>14}{'replay OFF':>14}")
    print(f"  {'median':>10}{statistics.median(on):>14,.0f}{statistics.median(off):>14,.0f}")
    print(f"  {'min':>10}{min(on):>14,.0f}{min(off):>14,.0f}")
    print(f"  {'max':>10}{max(on):>14,.0f}{max(off):>14,.0f}")
    print("\n  reference points: the clone banks $300 on seed 9000; kawa's own recorded")
    print("  seasons run $51,737-$161,918; starting money is $3,000.")
    print("\nVERDICT")
    mo, mf = statistics.median(on), statistics.median(off)
    if mf > 40_000 and mf > 2 * mo:
        print("  The PLANNER generalises and the REPLAY is what does not. Run DAgger against the")
        print("  replay-off teacher on as many seeds as wanted -- there is real play to imitate.")
    elif mo > 40_000:
        print("  The shipped agent generalises WITH the replay on. The four-seed restriction in")
        print("  dagger_tape.py is unnecessary and can simply be widened.")
    else:
        print("  Neither arm plays on a fresh seed. The teacher is the ceiling, and more seeds")
        print("  cannot help -- report the numbers, do not pick a story.")


main()
