"""What one tile of each crop is really worth, read off the engine's own yield rules.

**`max_yield` is a count of PRODUCTION EVENTS, not units per harvest.** `_end_of_day` stops at
`production_count > cd["max_yield"]` (reference/kaggriculture.py:795) and kills the tile when the
count reaches it, so an ongoing crop yields `max_yield` units over its whole life -- 4 for TOMATO,
not 4 per day. A one-shot crop accrues on WATER inside `[(max_yield_day+1)//2, max_yield_day]`
(line 441), 1 unit per watered day and 2 if fertilized, capped at `max_yield`.

Prices are the MEASURED realised ones from `scripts/crop_contest.py` over 10 seat-episodes, not the
table's base: melon realises 20% below base and wheat 54% above, which reorders the answer.

    python -u scripts/tile_value.py
"""
import sys
sys.path.insert(0, "/Users/alexchilton/DataspellProjects/kaggriculture")
import kaggle_environments.envs.kaggriculture.kaggriculture as K

REAL = {"WHEAT": 38, "CARROT": 37, "TOMATO": 81, "STRAWBERRY": 139, "MELON": 200,
        "EGG": 50, "MILK": 148, "WOOL": 141}


def crop_row(c, fert):
    d = K.CROPS[c]
    if d["ongoing"]:
        units = d["max_yield"] * (2 if fert else 1)
        units = min(units, d["max_yield"])          # cap binds: min(max_yield, +2) per event
        life = d["first_yield_day"] + d["interval"] * (d["max_yield"] - 1)
    else:
        window = d["max_yield_day"] - (d["max_yield_day"] + 1) // 2 + 1
        units = min(d["max_yield"], window * (2 if fert else 1))
        life = d["max_yield_day"] + 1
    return units, life


print("ONE TILE, whole lifecycle, at MEASURED prices\n")
for fert in (False, True):
    print(f"--- {'fertilized' if fert else 'watered only'} ---")
    print(f"{'crop':12}{'seed':>6}{'units':>7}{'life d':>8}{'revenue':>10}{'net':>9}"
          f"{'$/tile/day':>12}")
    rows = []
    for c in K.CROPS:
        units, life = crop_row(c, fert)
        rev = units * REAL[c]
        net = rev - K.CROPS[c]["seed"]
        rows.append((net / life, c, K.CROPS[c]["seed"], units, life, rev, net))
    for rate, c, seed, units, life, rev, net in sorted(rows, reverse=True):
        print(f"{c:12}{seed:>6}{units:>7}{life:>8}{rev:>10,.0f}{net:>9,.0f}{rate:>12,.0f}")
    print()

print("ONE PEN, whole season, bought day 7 (animals produce until the bell)")
print(f"{'animal':12}{'cost':>6}{'units':>7}{'events':>8}{'revenue':>10}{'net':>9}{'$/pen/day':>12}")
rows = []
for a, d in K.ANIMALS.items():
    days = 30 - 7 - d["first_yield_day"]
    if days < 0:
        continue
    events = 1 + days // max(1, d["interval"])
    units = events                                   # 1 unit per event, held up to max_held
    rev = units * REAL[d["product"]]
    net = rev - d["cost"]
    rows.append((net / (30 - 7), a, d["cost"], units, events, rev, net))
for rate, a, cost, units, events, rev, net in sorted(rows, reverse=True):
    print(f"{a:12}{cost:>6}{units:>7}{events:>8}{rev:>10,.0f}{net:>9,.0f}{rate:>12,.0f}")
