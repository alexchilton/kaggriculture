"""Replay one of our ladder games with the LIVE agent and grade only its last two days.

Alex, 2026-08-24: *"it needs to get in pre h23 because otherwise it cant sell"* and *"the stuff got
in should be optimised for d28 d29 final value -- not just whatever"*.

Season totals cannot see this. On game 98335212 the submitted agent banked $84,396, lost by $781,
and finished with **$732 of wool standing in a pasture** while its last market turns sold `MILK 9`
at **$1 a unit** and `WHEAT 30` at $33. It was not short of turns; it spent them on the cheapest
thing on the board.

So this prints, for d28 and d29 only:

  * every product that reached the shed, the hour it landed, and whether a sell turn remained;
  * every unit of yield still standing at the final turn, priced at what the town was paying;
  * the ratio that matters -- realised endgame revenue against what was left in the field.

`rematch_the_losses.rematch` is reused rather than reimplemented so the opponent stays their real
recorded actions and the seed stays the game's own (`info.seed`), which is what makes two runs
differ by our agent and nothing else.

    python -u scripts/what_the_last_two_days_banked.py 98335212
"""

import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
US = "alex chilton"
# `reference/kaggriculture.py:19-22`. A tile names the ANIMAL; the town pays for its PRODUCT.
ANIMAL_PRODUCT = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}


def _price(obs, item):
    return float(((obs.get("market") or {}).get("prices") or {}).get(item, 0.0))


def run(path, our_seat, seed, days=30):
    """Play the game again with the live agent, keeping every turn's observation for grading."""
    from kaggle_environments import make

    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads(pathlib.Path(path).read_text())
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    steps = rec["steps"]
    them = 1 - our_seat

    def their_action(t):
        if t + 1 < len(steps):
            a = steps[t + 1][them].get("action")
            if isinstance(a, dict):
                return a
        return {"farmer": ["PASS"], "hands": [], "market": []}

    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, our_seat)

    trace = []
    for t in range(days * TPD):
        o_us = env.state[our_seat].observation
        a_us = agent(o_us)
        a_them = their_action(t)
        n_us = len(o_us["farms"][our_seat].get("hands") or [])
        n_them = len(o_us["farms"][them].get("hands") or [])
        mine = {"farmer": a_us["farmer"], "hands": list(a_us["hands"] or [])[:n_us],
                "market": a_us["market"]}
        yours = {"farmer": a_them.get("farmer") or ["PASS"],
                 "hands": list(a_them.get("hands") or [])[:n_them],
                 "market": a_them.get("market") or []}
        # Snapshot BEFORE stepping: shed contents, money and the turn's own market orders.
        if o_us["day"] >= 28:
            # Also snapshot every pen still holding product, so "was the sheep sold" is answerable
            # tile by tile rather than inferred from a shed total.
            pens = {}
            for r, line in enumerate(o_us["farms"][our_seat]["tiles"]):
                for c, tile in enumerate(line):
                    if isinstance(tile, dict) and tile.get("animal"):
                        pens[(r, c)] = (tile["animal"], tile.get("yield_units") or 0)
            f = o_us["farms"][our_seat]
            units = [tuple(f["farmer"])] + [tuple(h) for h in f["hands"]]
            acts = [a_us["farmer"]] + list(a_us["hands"] or [])
            trace.append(dict(day=o_us["day"], hour=o_us["hour"],
                              shed=dict(o_us["private"]["shed"]),
                              money=f["money"],
                              orders=list(a_us["market"] or []),
                              carried=[dict(x) for x in o_us["private"].get("inventories") or []],
                              units=units, acts=acts,
                              pens=pens,
                              prices=dict((o_us.get("market") or {}).get("prices") or {})))
        env.step([mine, yours] if our_seat == 0 else [yours, mine])
        if env.done:
            break

    return env, trace


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "98335212"
    path = REPO / "data/seed_scripts/losses" / f"{ep}.json"
    rec = json.loads(path.read_text())
    info = rec["info"]
    seat = info["TeamNames"].index(US)
    seed = info["seed"]

    env, trace = run(str(path), seat, seed)
    obs = env.state[seat].observation
    farms = obs["farms"]
    ours, theirs = farms[seat]["money"], farms[1 - seat]["money"]

    print(f"game {ep}  seed {seed}  our seat {seat}")
    print(f"  recorded : ours ${rec['rewards'][seat]:>10,.0f}   "
          f"theirs ${rec['rewards'][1 - seat]:>10,.0f}")
    print(f"  rematch  : ours ${ours:>10,.0f}   theirs ${theirs:>10,.0f}\n")

    # ---- what the shed took in over d28-d29, and whether a sell turn was left ----------------
    print("d28-d29: product ARRIVING in the shed, and whether it could still be sold")
    print(f"  {'when':>9}  {'item':<12} {'+units':>7} {'$/unit':>8} {'value':>10}  sellable?")
    prev = {}
    banked = 0.0
    for row in trace:
        for item, n in row["shed"].items():
            gain = n - prev.get(item, 0)
            if gain > 0:
                px = row["prices"].get(item, 0.0)
                # h23 is the last turn; an order placed then still settles, so the deadline is
                # "in the shed by h23 of d29". Arriving after that is discarded by the rollover.
                ok = "yes" if not (row["day"] == 29 and row["hour"] > 23) else "NO -- too late"
                print(f"  d{row['day']} h{row['hour']:<5} {item:<12} {gain:>7} {px:>8,.0f} "
                      f"{gain * px:>10,.0f}  {ok}")
                banked += gain * px
        prev = row["shed"]

    # ---- what never made it -------------------------------------------------------------------
    print("\nstill standing in the field at the final turn")
    left = 0.0
    rows = []
    for r, line in enumerate(farms[seat]["tiles"]):
        for c, tile in enumerate(line):
            if not isinstance(tile, dict):
                continue
            u = tile.get("yield_units") or 0
            if not u:
                continue
            animal = tile.get("animal")
            product = ANIMAL_PRODUCT[animal] if animal else tile.get("crop")
            px = _price(obs, product) if product else 0.0
            rows.append((u * px, r, c, animal or tile.get("crop"), product, u, px))
    for val, r, c, what, product, u, px in sorted(rows, reverse=True):
        print(f"  ({r},{c})  {str(what):<10} -> {str(product):<10} {u:>3} x ${px:>6,.0f} "
              f"= ${val:>9,.0f}")
        left += val

    # **Offered is not filled.** A product sitting in the shed at the close is one of two very
    # different defects: never offered (a planning bug) or offered and refused (a market bug). The
    # standing rule in this project is that the order stream cannot be summed -- so print the orders
    # next to the shed level and let the pair say which it was.
    # ---- the specific animal that decided game 98335212 -------------------------------------
    # Alex, 2026-08-24: *"make sure the sheep which is in that game is sold"*. In the recording the
    # pen at (3,6) held 4 wool from d29 h0 to the final turn, worth $732 against a $781 losing
    # margin. This answers it for that pen directly instead of from a shed total.
    print("\nd29: every pen holding product, hour by hour  (0 = collected)")
    pens_seen = sorted({p for row in trace for p in row["pens"]})
    hdr = "  ".join(f"{str(p):>7}" for p in pens_seen)
    print(f"  {'hour':>5}  {hdr}")
    for row in trace:
        if row["day"] != 29 or row["hour"] % 3:
            continue
        cells = "  ".join(f"{row['pens'].get(p, ('', 0))[1]:>7}" for p in pens_seen)
        print(f"  h{row['hour']:<4}  {cells}")
    last = trace[-1]
    still = {p: v for p, v in last["pens"].items() if v[1]}
    print(f"  pens still holding at h{last['hour']}: {still or 'none -- all collected'}")

    # **Why a load is still in a hand.** `carried=38` for six hours with an empty shed says the crew
    # is not delivering, and only the per-unit view says whether that is a walk, other work, or a
    # DROP that never fires. `_drop_inventories_to_shed` runs after the final turn, so anything still
    # held here reaches the shed with no market turn left behind it.
    depots = {(5, 4), (4, 4), (5, 3), (4, 5)}     # shed-adjacent cells on this board
    print("\nd29 per-unit, h14 onward -- units holding something, with what they did")
    for row in trace:
        if row["day"] != 29 or row["hour"] < 14:
            continue
        loaded = []
        for k, pos in enumerate(row["units"]):
            inv = row["carried"][k] if k < len(row["carried"]) else {}
            n = sum(inv.values())
            if n:
                act = row["acts"][k][0] if k < len(row["acts"]) and row["acts"][k] else "-"
                loaded.append(f"u{k}@{pos}{'*' if pos in depots else ' '}x{n}:{act}")
        print(f"  h{row['hour']:<3} {'  '.join(loaded) or 'nothing held'}")
    print("  (* = standing on a shed-adjacent cell, so a DROP would land)")

    print("\nd29 SELL orders, every turn from the liquidation hour")
    for row in trace:
        if row["day"] != 29 or row["hour"] < 16:
            continue
        sells = [(o[1], o[2]) for o in row["orders"] if o and o[0] == "SELL"]
        carried = sum(sum(inv.values()) for inv in row["carried"])
        print(f"  h{row['hour']:<3} shed_total={sum(row['shed'].values()):>4} "
              f"carried={carried:>4}  sells={sells}")

    shed_left = {k: v for k, v in obs["private"]["shed"].items() if v}
    if shed_left:
        print(f"\nd29 SELL orders for what was still in the shed at the close: {list(shed_left)}")
        for row in trace:
            if row["day"] != 29:
                continue
            mine = [o for o in row["orders"] if o and o[0] == "SELL" and o[1] in shed_left]
            if mine:
                held = {k: row["shed"].get(k, 0) for k in shed_left}
                print(f"  h{row['hour']:<3} shed={held}  offers={mine}")
    print(f"\n  shed at the close : {shed_left or 'empty'}")
    print(f"  brought in d28-29 : ${banked:,.0f}")
    print(f"  left in the field : ${left:,.0f}")
    if banked + left:
        print(f"  captured          : {100 * banked / (banked + left):.1f}% of reachable endgame value")
    print(f"  margin            : ${abs(ours - theirs):,.0f} ({'loss' if ours < theirs else 'win'})")


if __name__ == "__main__":
    main()
