"""Do we actually beat Seb when we play HIM, rather than playing alongside him?

Every comparison so far has been two PARALLEL games: our agent in seat 0 against the tape's recorded
opponent, and Seb in seat 0 against that same opponent. `$121,221 vs $116,635` comes from those two
runs. The market was never contested between us -- and this project's most expensive lesson is that
an uncontested market roughly doubles every number, because nobody is lifting the book before you.

This puts us in the same game as him, both seatings, and reports who banks more.

CAVEAT, stated up front: the tape is an OPEN-LOOP script. It replays a fixed action sequence and
cannot react to us, so a contested sale it never anticipated simply fails for it. That makes this an
optimistic read of our side, not a pessimistic one -- it is the ceiling of "beats Seb", not proof of
beating a live opponent. It is still the first time the two have been in the same market at all.
"""
import json
import pathlib
import sys

sys.path.insert(0, "/Users/alexchilton/DataspellProjects/kaggriculture")

from kaggle_environments import make

from kagg.search import schedule_agent as SA
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy

SEEDS = [11, 3, 7, 19, 23]
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def play(seed, ours_seat):
    """One full game: us in `ours_seat`, Seb's tape in the other. Returns (our bank, his bank)."""
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, ours_seat, router=True)
    tape = tape_policy(replay, team, 1 - ours_seat)
    for t in range(719):
        obs = [env.state[0].observation, env.state[1].observation]
        acts = [None, None]
        acts[ours_seat] = agent(obs[ours_seat])
        acts[1 - ours_seat] = tape(obs[1 - ours_seat], t)
        payload = []
        for s in (0, 1):
            n = len(obs[0]["farms"][s].get("hands") or [])
            a = acts[s]
            payload.append({"farmer": a["farmer"], "hands": list(a["hands"])[:n],
                            "market": a["market"]})
        env.step(payload)
        if env.state[0].status == "DONE":
            break
    farms = env.state[0].observation["farms"]
    return int(farms[ours_seat]["money"]), int(farms[1 - ours_seat]["money"])


print(f"{'seed':<6}{'seat':<6}{'OURS':>12}{'SEB':>12}{'margin':>12}  result")
wins = draws = games = 0
for seed in SEEDS:
    for seat in (0, 1):
        ours, his = play(seed, seat)
        games += 1
        wins += ours > his
        draws += ours == his
        verdict = "WIN" if ours > his else ("draw" if ours == his else "LOSS")
        print(f"{seed:<6}{seat:<6}{ours:>12,}{his:>12,}{ours - his:>12,}  {verdict}", flush=True)

print(f"\n  {wins}/{games} wins, {draws} draws  ->  win rate {wins / games:.3f}")
print("  (the ladder is Elo: a $40k win and a $400 win score identically)")
