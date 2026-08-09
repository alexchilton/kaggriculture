"""Per-night shed/feed telemetry: what the rollover ACTUALLY destroyed, and what the market
ACTUALLY filled.

Records, for every game day: dawn shed per product, dusk shed, hands at dusk, herd size, animals
fed, escapes across the rollover, wheat bought and sold, and the exact rollover discard.

**Two things here are instrumented rather than inferred, and both corrections were worth several
thousand units of reported error.**

* **The discard.** `held_at_dusk - shed_at_dawn` is NOT the night's loss. Hour 23's SELL and
  BUY_PRODUCT settle in the SAME `env.step` as the rollover, so a sale counts as a discard and a
  purchase hides one. On seed 11, full season, that method reports 105-137 units destroyed and the
  env destroys 7. This patches `_drop_inventories_to_shed`, which is the only code path in the game
  that deletes product -- `PLACE` into a full shed clamps and leaves the remainder in the hand
  (`reference/kaggriculture.py:380-396`).
* **The fills.** Order quantities are re-offered every turn, so summing them inflates any row that
  retries. This patches `_commit_unit`, which returns True exactly once per unit that settles.

Usage:
    python -u scripts/probe_hold.py --seed 11 [--handover 11] [--set NAME=VALUE ...]

`--handover N` hands over from the tape at day N; `--handover 0` is the full season played by us,
which is the project's canonical surface. Note that `--handover 30` or higher means the TAPE plays
every day and nothing is being measured about our agent at all.
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")


def alive_tiles(obs, seat=0):
    return [c for r in obs["farms"][seat]["tiles"] for c in r
            if isinstance(c, dict) and "animal" in c]


#: Exact per-night discard, read off the env's own `_drop_inventories_to_shed` rather than inferred
#: from a shed delta. The delta is contaminated: hour 23's SELL/BUY_PRODUCT settle in the same step
#: as the rollover, so a shed-difference metric counts a sale as a discard. This counts what the
#: function actually deletes.
DISCARDS = []


def install_discard_probe():
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    if getattr(KG, "_probe_installed", False):
        return
    orig = KG._drop_inventories_to_shed

    def patched(private, capacity):
        before = collections.Counter()
        for inv in private["inventories"]:
            before.update({k: int(v) for k, v in inv.items() if int(v) > 0})
        shed_before = collections.Counter({k: int(v) for k, v in private["shed"].items()})
        orig(private, capacity)
        after = collections.Counter({k: int(v) for k, v in private["shed"].items()})
        lost = (before + shed_before) - after
        DISCARDS.append({k: v for k, v in lost.items() if v > 0})

    KG._drop_inventories_to_shed = patched

    #: Market FILLS, not offers. `_commit_unit` returns True exactly once per unit that settled,
    #: so this is the only honest count -- the agent re-offers a quota every turn.
    #: The env rebuilds `farms` every step, so the seat is resolved from the list `_process_market`
    #: is actually holding rather than from an id captured outside the interpreter.
    orig_commit = KG._commit_unit
    orig_market = KG._process_market
    seat_of = {}

    def patched_market(state, env_):
        seat_of.clear()
        for i, f in enumerate(state[0].observation.farms):
            seat_of[id(f)] = i
        return orig_market(state, env_)

    def patched_commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = orig_commit(op, item, price, farm, private, market, shed_capacity)
        if ok:
            FILLS.append((seat_of.get(id(farm), -1), op, item, price))
        return ok

    KG._commit_unit = patched_commit
    KG._process_market = patched_market
    KG._probe_installed = True


FILLS = []


def run(seed, handover, days, tape, overrides, weeds=0.0):
    from kaggle_environments import make

    from kagg.search import schedule_agent as SA
    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    for k, v in (overrides or {}).items():
        assert hasattr(SA, k), k
        setattr(SA, k, v)

    replay, schedule, team = TAPES[tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    raw = json.loads(pathlib.Path(replay).read_text())
    tseat = raw["info"]["TeamNames"].index(team)
    tape_act = [dict(farmer=((s[tseat] or {}).get("action") or {}).get("farmer") or ["PASS"],
                     hands=list(((s[tseat] or {}).get("action") or {}).get("hands") or []),
                     market=list(((s[tseat] or {}).get("action") or {}).get("market") or []))
                for s in raw["steps"][1:]]

    install_discard_probe()
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    rows, dusk, dawn_shed = [], None, None
    money = 0.0
    day_fills = collections.Counter()
    for t in range(24 * days - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        priv = o0.get("private") or {}
        shed = collections.Counter({k: int(v) for k, v in (priv.get("shed") or {}).items()})
        day, hour = t // 24, t % 24
        money = float(o0["farms"][0].get("money", 0))

        if hour == 0:
            dawn_shed = dict(shed)
            if dusk is not None:
                lost = dusk["discard"]
                rows.append(dict(day=dusk["day"], dawn=dusk["dawn"], shed=dusk["shed"],
                                 wheat=dusk["shed"].get("WHEAT", 0), shedtot=sum(dusk["shed"].values()),
                                 hands=dusk["hands"], alive=dusk["alive"], fed=dusk["fed"],
                                 unfed=dusk["alive"] - dusk["fed"],
                                 alive_next=len(alive_tiles(o0)),
                                 escapes=max(0, dusk["alive"] - len(alive_tiles(o0))),
                                 lost=sum(lost.values()), lost_by=lost,
                                 wbuy=dusk["wbuy"], wsell=dusk["wsell"], wcost=dusk["wcost"],
                                 wrev=dusk["wrev"],
                                 money=dusk["money"]))
                dusk = None

        a1 = opp(o1, t)
        if day < handover:
            a0 = dict(tape_act[t]) if t < len(tape_act) else {"farmer": ["PASS"], "hands": [],
                                                              "market": []}
            ours(o0)
        else:
            a0 = ours(o0)

        if hour == 23:
            hb = collections.Counter()
            for iv in (priv.get("inventories") or []):
                hb.update({k: int(v) for k, v in (iv or {}).items() if int(v) > 0})
            animals = alive_tiles(o0)
            dusk = dict(day=day, dawn=dawn_shed, shed=dict(shed), hands=sum(hb.values()),
                        hands_by_prod=dict(hb), alive=len(animals),
                        fed=sum(1 for a in animals if a.get("fed_today")), money=money)

        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        DISCARDS.clear()
        FILLS.clear()
        me = 0
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        for fid, op, item, price in FILLS:
            if fid == me:
                day_fills[(op, item)] += 1
                day_fills[("$", op, item)] += price
        if hour == 23:
            # `_drop_inventories_to_shed` is called once per farm in seat order, so seat 0 is first.
            dusk["discard"] = DISCARDS[0] if DISCARDS else {}
            dusk["wbuy"] = day_fills[("BUY_PRODUCT", "WHEAT")]
            dusk["wsell"] = day_fills[("SELL", "WHEAT")]
            dusk["wcost"] = day_fills[("$", "BUY_PRODUCT", "WHEAT")]
            dusk["wrev"] = day_fills[("$", "SELL", "WHEAT")]
            day_fills = collections.Counter()

    final = float(env.state[0].observation["farms"][0].get("money", 0))
    return rows, final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--handover", type=int, default=99)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--tape", default="seb1326")
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--label", default="")
    ap.add_argument("--json", action="store_true", help="print one JSON summary line only")
    a = ap.parse_args()

    ov = {}
    for s in a.set:
        k, _, v = s.partition("=")
        ov[k] = json.loads(v)

    rows, final = run(a.seed, a.handover, a.days, a.tape, ov, a.weeds)
    if a.json:
        print(json.dumps(dict(
            seed=a.seed, money=final,
            lost=sum(r["lost"] for r in rows),
            nights=sum(1 for r in rows if r["lost"] > 0),
            escapes=sum(r["escapes"] for r in rows),
            unfed=sum(r["unfed"] for r in rows),
            wbuy=sum(r["wbuy"] for r in rows), wsell=sum(r["wsell"] for r in rows),
            wcost=sum(r["wcost"] for r in rows), wrev=sum(r["wrev"] for r in rows),
            eaten=sum(r["fed"] for r in rows))))
        return rows, final
    print(f"== {a.label or 'run'} seed={a.seed} handover={a.handover} tape={a.tape} "
          f"overrides={ov}")
    print("    day  dawnWH  duskWH  shedTOT  hands  alive  fed  unfed  esc  wBUY  wSELL   wNET  "
          "lost  lost_by")
    for r in rows:
        lb = ",".join(f"{k}:{v}" for k, v in sorted(r["lost_by"].items(), key=lambda kv: -kv[1]))
        print("    %3d  %6d  %6d  %7d  %5d  %5d  %3d  %5d  %3d  %4d  %5d  %6.0f  %4d  %s"
              % (r["day"], r["dawn"].get("WHEAT", 0), r["wheat"], r["shedtot"], r["hands"],
                 r["alive"], r["fed"], r["unfed"], r["escapes"], r["wbuy"], r["wsell"],
                 r["wrev"] - r["wcost"], r["lost"], lb))
    nights = [r for r in rows if r["lost"] > 0]
    print(f"    TOTAL lost={sum(r['lost'] for r in rows)} over {len(nights)} nights; "
          f"escapes={sum(r['escapes'] for r in rows)}; "
          f"unfed-animal-days={sum(r['unfed'] for r in rows)}; "
          f"wheat bought={sum(r['wbuy'] for r in rows)} for ${sum(r['wcost'] for r in rows):.0f}; "
          f"eaten={sum(r['fed'] for r in rows)}; "
          f"sold={sum(r['wsell'] for r in rows)} for ${sum(r['wrev'] for r in rows):.0f}; "
          f"WHEAT_NET ${sum(r['wrev'] - r['wcost'] for r in rows):.0f}; "
          f"FINAL_MONEY {final:.0f}")
    return rows, final


if __name__ == "__main__":
    main()
