"""Replay the games we LOST against the winner's own actions, with the strawberry fork forced on.

## The question

Five ladder losses on 2026-08-16 share one signature: ahead at d18, behind by d22, with the opponent
selling 5-6x more strawberry than us in the d18-d21 window where it trades at $200-$216. Our
strawberry first yields at d21 because 23 of 34 tiles go in on d11-d12.

We cannot simply plant strawberry earlier: the bank is empty through d8 (measured in those same
games -- d2 $174, d4 $4, d6 $9, d8 $3) and strawberry seed is the dearest at $100. The only early
strawberry we can afford is a SUBSTITUTION, and the crop occupying those d6/d7 slots is melon at $80.

`_melon_to_strawberry` already does exactly that. It is gated by
`melon_branch.arm`, which latches at `DECIDE_BY_DAY` (3) when the
opponent already shows `OPPONENT_MELON` (7) melon tiles.

**The trigger and the benefit are unrelated quantities.** The gate asks about the OPPONENT's melon;
the benefit is OUR early strawberry. Measured across the five losses, the fork fired in two and the
board differed sharply:

    fired   MELON 12  STRAWBERRY 41   16 strawberry planted by d8
    off     MELON 20  STRAWBERRY 33   9 strawberry planted by d8

So the arm here forces the gate open by setting the opponent threshold to 0, changing nothing else.

## Method

The winner's RECORDED actions hold the other seat, on the seed of the real game, so the opponent is
exactly the agent that beat us rather than a stand-in. Their tape is open-loop and cannot react to a
different us, which biases the result in OUR favour -- state that with any win.

`weedSpawnChance` is **0.005** on the ladder, not 0. Random weeds spawn on EMPTY tiles only
(`_spawn_weeds`, `reference/kaggriculture.py:836`), so a crop tile that weeds is still our own missed
watering, but the empty-ground spawns are real and must be reproduced.

One OS process per measurement: the first run in a process differs from later ones.

    python -u scripts/force_the_strawberry_mix.py --replays 93531871 93525585 93525586
"""
import argparse
import collections
import importlib
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
DOWNLOADS = pathlib.Path.home() / "Downloads"


def find_replay(eid):
    for p in (DOWNLOADS / f"{eid}.json",
              REPO / f"data/seed_scripts/ladder_2026-08-16/episode-{eid}-replay.json",
              REPO / f"data/seed_scripts/ladder_1943/episode-{eid}-replay.json"):
        if p.exists():
            return str(p)
    raise SystemExit(f"no replay for {eid}")


def tape(path, team):
    """The recorded actions of `team`, as a callable. See `scripts/breakdown.tape_policy`."""
    d = json.loads(pathlib.Path(path).read_text())
    seat = d["info"]["TeamNames"].index(team)
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[seat] or {} for step in d["steps"][1:])]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return lambda obs, t: acts[t] if t < len(acts) else idle


def one(eid, arm, weeds):
    from kaggle_environments import make

    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")

    path = find_replay(eid)
    d = json.loads(pathlib.Path(path).read_text())
    names = d["info"]["TeamNames"]
    seed = d["info"].get("seed", 0)
    us = next((i for i, n in enumerate(names) if "alex" in (n or "").lower()), 0)
    winner = names[1 - us]

    if arm == "forced":
        A.OPPONENT_MELON = 0     # the gate opens whatever the opponent grows
    opp = tape(path, winner)

    # **Both agents keep the seat they actually held.** Market orders settle in SEAT order
    # (`_process_market` walks players 0 then 1 per unit), so moving the winner from seat 0 to seat 1
    # strips their price priority -- and their tape is open-loop and cannot adapt to the refusals
    # that follow. Measured: with the seats swapped, Saud banked $39,371 against $104,080 in the
    # real game, which makes every money column meaningless.
    env = make("kaggriculture",
               configuration={"seed": seed, "weedSpawnChance": weeds}, debug=False)
    env.reset(2)
    me = A.make_agent(PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json")), me=us)

    sold = collections.defaultdict(collections.Counter)
    prev = collections.Counter()
    tiles = collections.defaultdict(set)
    for t in range(719):
        o = env.state[us].observation
        shed = collections.Counter((o.get("private") or {}).get("shed") or {})
        for k, v in prev.items():
            if shed.get(k, 0) < v:
                sold[t // 24][k] += v - shed.get(k, 0)
        prev = shed
        for y, row in enumerate(o["farms"][us]["tiles"]):
            for x, c in enumerate(row):
                if isinstance(c, dict) and c.get("crop"):
                    tiles[c["crop"]].add((x, y, c.get("planted_day")))
        acts = [None, None]
        acts[us] = me(o, t)
        acts[1 - us] = opp(env.state[1 - us].observation, t)
        env.step(acts)
        if env.done:
            break

    st = sum(c["STRAWBERRY"] for c in sold.values())
    early = sum(c["STRAWBERRY"] for day, c in sold.items() if day <= 21)
    fin = env.steps[-1]
    return dict(eid=eid, arm=arm, seed=seed, winner=winner, seat=us,
                mine=fin[us]["reward"], theirs=fin[1 - us]["reward"],
                melon=len(tiles["MELON"]), straw=len(tiles["STRAWBERRY"]),
                straw_by_d8=sum(1 for (_x, _y, pd) in tiles["STRAWBERRY"]
                                if pd is not None and pd <= 8),
                sold=st, early=early)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replays", nargs="+", required=True)
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--child", nargs=2, default=None)
    a = ap.parse_args()

    if a.child:
        print(json.dumps(one(a.child[0], a.child[1], a.weeds)))
        return

    print(f"the winner's recorded actions hold seat 1; weedSpawnChance {a.weeds} (the ladder value)\n")
    print(f"{'episode':>10}  {'winner':<20}{'arm':>8}{'ours $':>11}{'theirs $':>11}{'margin':>10}"
          f"{'melon':>7}{'straw':>7}{'by d8':>7}{'sold':>6}{'<=d21':>7}")
    got = collections.defaultdict(dict)
    for eid in a.replays:
        for arm in ("shipped", "forced"):
            p = subprocess.run([sys.executable, "-u", __file__, "--child", eid, arm,
                                "--replays", eid, "--weeds", str(a.weeds)],
                               capture_output=True, text=True, cwd=REPO,
                               env={**__import__("os").environ, "PYTHONPATH": "."})
            try:
                r = json.loads(p.stdout.strip().splitlines()[-1])
            except Exception:
                print(f"{eid:>10}  {arm} FAILED {(p.stderr or p.stdout)[-200:]}")
                continue
            got[eid][arm] = r
            print(f"{r['eid']:>10}  {r['winner'][:19]:<20}{arm:>8}{r['mine']:>11,.0f}"
                  f"{r['theirs']:>11,.0f}{r['mine'] - r['theirs']:>+10,.0f}"
                  f"{r['melon']:>7}{r['straw']:>7}{r['straw_by_d8']:>7}{r['sold']:>6}"
                  f"{r['early']:>7}", flush=True)
    print()
    flips = 0
    for eid, arms in got.items():
        if "shipped" in arms and "forced" in arms:
            s, f = arms["shipped"], arms["forced"]
            sm, fm = s["mine"] - s["theirs"], f["mine"] - f["theirs"]
            flip = sm < 0 <= fm
            flips += flip
            print(f"{eid}: shipped {sm:+,.0f} -> forced {fm:+,.0f}   "
                  f"({f['mine'] - s['mine']:+,.0f} on our bank)"
                  f"{'   *** FLIPS THE LOSS ***' if flip else ''}")
    print(f"\nlosses flipped: {flips}/{len(got)}")
    print("The winner's tape cannot react to a different us, so it plays handicapped -- read a win "
          "here as necessary, not sufficient.")


if __name__ == "__main__":
    main()
