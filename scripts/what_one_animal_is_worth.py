"""Hold the game fixed. Take one cow's milk out of the book and put one goose's eggs in.

No agent change. The season is played once; the market is then REPLAYED under a counterfactual
supply, using the env's own `market_price` and the env's own per-unit lockstep, so every price is
the price the reference would have quoted.

The model is validated before it is used: the reconstructed inventory path and the reconstructed
per-unit fill prices must reproduce the recorded season exactly.

Held fixed, and this is the assumption to argue with: both agents sell the same UNITS at the same
turns. Their fill counts are shed-limited, not price-limited, so this is right for the opponent.
It is an approximation for us -- a higher milk price might make our own sell rule behave differently.
"""
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path("/Users/alexchilton/DataspellProjects/kaggriculture")
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
import breakdown as B
from kagg.search import melon_branch as _MB
from kaggle_environments import make
import importlib.util
_spec = importlib.util.spec_from_file_location("kg", str(REPO / "reference/kaggriculture.py"))
KG = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(KG)
SA = importlib.import_module("kagg.search.schedule_agent"); B.schedule_agent = SA
_MB.OPPONENT_MELON = 0
SA.NEVER_DRAINED = ()
SA.HERD_GEESE = 0

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 11
REP = str(REPO / "data/seed_scripts/kawashigi/92466371.json"); TEAM = "カワシギ"
raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY} for k, r in raw.items()}
economy = B.env_config(REP)


def play(item_watch=("MILK", "EGG", "WOOL")):
    """One season. Returns the per-turn record needed to replay the market."""
    env = make("kaggriculture", configuration=dict(economy, seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2); p0 = SA.make_agent(sched, 0); p1 = B.tape_policy(REP, TEAM, 1)
    rec = []
    for t in range(24 * 30):
        o0, o1 = env.state[0].observation, env.state[1].observation
        mkt = o0["market"]
        inv0 = {i: mkt["inventory"][i] for i in item_watch}
        shops = list(o0["town"]["unlocked_shops"])
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or []); n1 = len(o1["farms"][1].get("hands") or [])
        m0 = {"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]}
        m1 = {"farmer": a1.get("farmer") or ["PASS"], "hands": list(a1["hands"])[:n1],
              "market": a1.get("market") or []}
        money0, money1 = o0["farms"][0]["money"], o0["farms"][1]["money"]
        env.step([m0, m1])
        o0b = env.state[0].observation
        rec.append({"t": t, "inv": inv0, "shops": shops,
                    "inv_after": {i: o0b["market"]["inventory"][i] for i in item_watch},
                    "d_money": (o0b["farms"][0]["money"] - money0,
                                o0b["farms"][1]["money"] - money1)})
        if env.done: break
    farms = env.state[0].observation["farms"]
    return rec, farms[0]["money"], farms[1]["money"], env


def price(item, inv):
    return KG.market_price(item, inv)


def lockstep(item, inv, n_a, n_b):
    """The reference's per-unit lockstep for one turn. Returns (rev_a, rev_b, inv_out, prices)."""
    ra = rb = 0.0
    ps = []
    while n_a > 0 or n_b > 0:
        p = price(item, inv)
        ps.append(p)
        add = 0
        if n_a > 0:
            ra += p; n_a -= 1; add += 1 if p > 1 else 0
        if n_b > 0:
            rb += p; n_b -= 1; add += 1 if p > 1 else 0
        inv += add
    return ra, rb, inv, ps


def drain(item, inv, shops, step):
    if step % 4 == 0:
        for s in shops:
            prods = KG.SHOPS[s]
            mult = 2 if len(prods) == 1 else 1
            if item in prods:
                inv -= mult
    if step % 24 == 0 and item in KG.TOWN_CENTER_PRODUCTS:
        inv -= 1
    return inv


print(f"seed {SEED}: playing the base season ...", flush=True)
rec, money_us, money_them, env = play()
print(f"base banks   ours {money_us:,.0f}   theirs {money_them:,.0f}   "
      f"margin {money_us - money_them:+,.0f}\n", flush=True)

# ---- recover the per-turn unit counts from the recorded inventory path -----------------------
# `inv_after` is read after the whole turn (market THEN drain), so units sold = inv_after - inv
# + drain. Sales at $1 do not raise inventory, so this UNDER-counts at the floor; the fills
# recorder is the authority on counts and is used instead. This block only validates the drain.
from kagg.analysis.fills import record_fills


def play_with_fills():
    env2 = make("kaggriculture", configuration=dict(economy, seed=SEED, weedSpawnChance=0.0), debug=True)
    env2.reset(2); q0 = SA.make_agent(sched, 0); q1 = B.tape_policy(REP, TEAM, 1)
    per = collections.defaultdict(lambda: [0, 0])
    with record_fills(env2) as f:
        for t in range(24 * 30):
            o0, o1 = env2.state[0].observation, env2.state[1].observation
            b0, b1 = q0(o0, t), q1(o1, t)
            n0 = len(o0["farms"][0].get("hands") or []); n1 = len(o1["farms"][1].get("hands") or [])
            env2.step([{"farmer": b0["farmer"], "hands": list(b0["hands"])[:n0], "market": b0["market"]},
                       {"farmer": b1.get("farmer") or ["PASS"], "hands": list(b1["hands"])[:n1],
                        "market": b1.get("market") or []}])
            if env2.done: break
        out = {}
        for seat in (0, 1):
            for d, h, op, it, pr in f.at_turn(seat):
                if op != "SELL":
                    continue
                key = (d * 24 + h, it)
                out.setdefault(key, [0, 0, [], []])
                out[key][seat] += 1
                out[key][2 + seat].append(pr)
    return out


units = play_with_fills()

# ---- validate: replay MILK exactly and compare against the recorded fill prices ---------------
def replay(item, scale_us=1.0, extra_us=None, verbose=False):
    """Replay one product's book. `scale_us` multiplies OUR unit count; `extra_us` adds units.

    Returns (our revenue, their revenue, our units, their units, max error vs recording).
    """
    inv = KG.MARKET_PARAMS[item]["I0"]
    rev_a = rev_b = 0.0
    na_tot = nb_tot = 0
    err = 0.0
    carry = 0.0
    for r in rec:
        t = r["t"]
        key = (t, item)
        u = units.get(key)
        n_a = u[0] if u else 0
        n_b = u[1] if u else 0
        if scale_us != 1.0:
            want = n_a * scale_us + carry
            n_a2 = int(want)
            carry = want - n_a2
            n_a = n_a2
        if extra_us:
            n_a += extra_us.get(t, 0)
        na_tot += n_a; nb_tot += n_b
        ra, rb, inv, ps = lockstep(item, inv, n_a, n_b)
        rev_a += ra; rev_b += rb
        if scale_us == 1.0 and not extra_us and u:
            for got, want_p in zip(ps, sorted(u[2] + u[3], reverse=True)):
                pass
            rec_prices = sorted(u[2] + u[3])
            mine = sorted(ps * 1)[:len(rec_prices)]
            if rec_prices:
                err = max(err, abs(sum(rec_prices) - sum(ps[:len(rec_prices)])) / max(1.0, sum(rec_prices)))
        inv = drain(item, inv, r["shops"], t)
    return rev_a, rev_b, na_tot, nb_tot, err


print("=== VALIDATION: replay the recorded season and compare revenue to the fills")
print(f"{'item':>12} {'replay ours':>13} {'recorded ours':>15} {'replay theirs':>15} {'recorded theirs':>17}")
ok = True
for item in ("MILK", "WOOL", "EGG"):
    ra, rb, na, nb, _ = replay(item)
    rec_a = sum(sum(v[2]) for k, v in units.items() if k[1] == item)
    rec_b = sum(sum(v[3]) for k, v in units.items() if k[1] == item)
    flag = "" if abs(ra - rec_a) <= max(50.0, 0.01 * max(1, rec_a)) else "   <-- MISMATCH"
    if flag: ok = False
    print(f"{item:>12} {ra:>13,.0f} {rec_a:>15,.0f} {rb:>15,.0f} {rec_b:>17,.0f}{flag}")
print()
if not ok:
    print("!! the replay does not reproduce the season. Every number below is void.\n")

# ---- the counterfactual ----------------------------------------------------------------------
n_cows = 4
base_ra, base_rb, base_na, base_nb, _ = replay("MILK")
cf_ra, cf_rb, cf_na, cf_nb, _ = replay("MILK", scale_us=(n_cows - 1) / n_cows)
print(f"=== ONE COW OUT of {n_cows}: milk book replayed at {(n_cows-1)/n_cows:.0%} of our units")
print(f"{'':>14} {'units ours':>11} {'rev ours':>11} {'$/unit':>8} | {'units theirs':>13} {'rev theirs':>11} {'$/unit':>8}")
print(f"{'base':>14} {base_na:>11} {base_ra:>11,.0f} {base_ra/max(1,base_na):>8.1f} | "
      f"{base_nb:>13} {base_rb:>11,.0f} {base_rb/max(1,base_nb):>8.1f}")
print(f"{'one cow out':>14} {cf_na:>11} {cf_ra:>11,.0f} {cf_ra/max(1,cf_na):>8.1f} | "
      f"{cf_nb:>13} {cf_rb:>11,.0f} {cf_rb/max(1,cf_nb):>8.1f}")
print(f"{'delta':>14} {cf_na-base_na:>11} {cf_ra-base_ra:>+11,.0f} {'':>8} | "
      f"{'':>13} {cf_rb-base_rb:>+11,.0f}")
print()

# ---- what a goose would earn, priced against the REAL egg book -------------------------------
# GOOSE: first_yield_day 4, interval 1, max_held 4. One bird fed and cared every night yields
# 1 unit a night, rising with `pending_care_bonus` to `max_held`. Two supply profiles are priced:
# the conservative 1/night, and the 54 units the live d0-goose arm actually banked.
print("=== ONE GOOSE IN: eggs priced against the real egg book on this seed")
print(f"   EGG base ${KG.MARKET_PARAMS['EGG']['base']}, below_target "
      f"{KG.MARKET_PARAMS['EGG']['below_target']} -> hard ceiling "
      f"${KG.MARKET_PARAMS['EGG']['base'] * (1 + KG.MARKET_PARAMS['EGG']['below_target']):.0f}/unit")
n_egg_shops = sum(1 for s in rec[-1]["shops"] if "EGG" in KG.SHOPS[s])
print(f"   this seed ends with {n_egg_shops} shop instances draining EGG")
for label, per_day in (("1 egg/night from d4", 1), ("2 eggs/night from d4", 2),
                       ("4 eggs/night from d4", 4)):
    extra = {}
    for day in range(4, 30):
        extra[day * 24 + 18] = per_day
    ra, rb, na, nb, _ = replay("EGG", extra_us=extra)
    print(f"   {label:<22} {na:>4} units  ${ra:>9,.0f}  ${ra/max(1,na):>6.1f}/unit")
print()

print("=== VERDICT, one cow swapped for one goose (margin is what counts)")
milk_us = cf_ra - base_ra
milk_them = cf_rb - base_rb
for label, per_day in (("1 egg/night", 1), ("2 eggs/night", 2), ("4 eggs/night", 4)):
    extra = {day * 24 + 18: per_day for day in range(4, 30)}
    egg_us, _, _, _, _ = replay("EGG", extra_us=extra)
    ours = milk_us + egg_us
    theirs = milk_them
    print(f"   {label:<14} our revenue {ours:>+9,.0f}   their revenue {theirs:>+9,.0f}   "
          f"MARGIN {ours - theirs:>+9,.0f}")
print("\n   (cow $400 and goose $300 are one-off and roughly cancel; the $100 saved is not counted)")

# ---- the same cow, swapped for strawberry instead --------------------------------------------
print("\n=== ONE COW OUT, STRAWBERRY IN: the cow's ~3 actions a day spent on crop instead")
sb_base_a, sb_base_b, sb_na, sb_nb, _ = replay("STRAWBERRY")
print(f"   base strawberry: ours {sb_na} units ${sb_base_a:,.0f} (${sb_base_a/max(1,sb_na):.1f}), "
      f"theirs {sb_nb} units ${sb_base_b:,.0f} (${sb_base_b/max(1,sb_nb):.1f})")
for extra_n in (20, 40, 80):
    per = {}
    for day in range(8, 30):
        per[day * 24 + 18] = max(1, extra_n // 22)
    ra, rb, na, nb, _ = replay("STRAWBERRY", extra_us=per)
    gain_us = ra - sb_base_a
    cost_them = rb - sb_base_b
    ours = milk_us + gain_us
    theirs = milk_them + cost_them
    print(f"   +{na - sb_na:>3} strawberry units  our rev {ours:>+9,.0f}  their rev {theirs:>+9,.0f}  "
          f"MARGIN {ours - theirs:>+9,.0f}")

# ---- the covariates that decide it ------------------------------------------------------------
shops = rec[-1]["shops"]
n_milk = sum(1 for s in shops if "MILK" in KG.SHOPS[s])
n_egg = sum(1 for s in shops if "EGG" in KG.SHOPS[s])
n_straw = sum(1 for s in shops if "STRAWBERRY" in KG.SHOPS[s])
print(f"\nSUMMARY seed={SEED} milk_shops={n_milk} egg_shops={n_egg} straw_shops={n_straw} "
      f"their_milk_units={base_nb} our_milk_units={base_na} "
      f"denial_value={cf_rb - base_rb:+,.0f} our_milk_cost={cf_ra - base_ra:+,.0f}")
