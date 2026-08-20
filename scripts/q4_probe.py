"""Measure the four-quadrant variant against the shipped agent, one OS process per measurement.

    python -u scripts/q4_probe.py --workers 6 | tee data/logs/q4_probe.log
    python -u scripts/q4_probe.py --cell --seed 3 --arm q4 --json      # one measurement

## The three arms, and why the middle one is not optional

    shipped       what ships today. Three quadrants, solved routes.
    shipped_live  what ships today, with the solved routes dropped from d12.
    q4            the fourth quadrant, which also drops the solved routes from d12.

`cover._apply_precomputed` keys a stop on `(tile, ops)` against routes solved for a 75-tile board.
On 100 tiles those routes describe a board the game never reaches, so the q4 arm HAS to plan d12-29
live. Live routing costs real money on its own -- `scripts/swap_one_crop.py` measured -$11,431 on
seed 3 -- so `q4` against `shipped` measures the parcel and the routing handicap added together,
and would read as a large loss whatever the parcel is worth. `shipped_live` pays the same handicap
and nothing else, which is what makes `q4 - shipped_live` a statement about the parcel.

## One OS process per measurement

Measured 2026-08-15: the same config run four times inside one process gave $134,665 then $94,523
three times -- the FIRST run in a process differs. An in-process loop measures run order. This
script therefore does exactly ONE measurement per `--cell` invocation and the matrix drives it from
outside, which is `scripts/swap_matrix.py`'s pattern, unchanged. Do not "optimise" it into a loop.

There is a second, independent reason here: `q4_agent` mutates `cover.PRECOMPUTED_ROUTES`, which is
process-global. Two arms in one process would contaminate each other's routing.

## The seeds are chosen, and that is the point

The branch only arms when the town draws a YARN_STORE in its first two draws, which happens on
about a sixth of boards. Running it on arbitrary seeds measures the shipped agent against itself on
five sixths of them and dilutes the answer into noise. `EARLY_YARN_SEEDS` is every seed under 70
whose real game -- not a PASS-only game, whose shop stream differs -- opens a yarn store
(`data/logs/q4_shopscan.log`). The result is therefore conditional on the trigger firing, which is
the only quantity the branch can affect. What it does NOT tell you is the season-average effect;
multiply by the base rate for that.

## A money figure without a collection rate is not interpretable

Every cell reports its per-crop collection rate off the same tile-diff instrumentation
`swap_one_crop.py` uses. A crop grown and left in the field is a routing failure wearing a money
figure, and on the live-route arms that is the failure mode to expect.
"""
import argparse
import collections
import importlib
import importlib.util
import json
import os
import pathlib
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEDULE = str(REPO / "data/seed_scripts/kawashigi/schedule.json")

#: Seeds whose town draws a YARN_STORE in its first two draws (d3 and d6), measured by playing the
#: shipped agent in both seats -- see `data/logs/q4_shopscan.log`. 11 of seeds 0-69.
EARLY_YARN_SEEDS = (3, 10, 17, 18, 22, 45, 47, 53, 60, 65, 66)

ARMS = ("shipped", "shipped_live", "q4")


# ------------------------------------------------------------------------------------ one cell
def run_cell(seed, arm, opponent):
    """Play one season and return everything needed to interpret the money figure."""
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    Q4 = importlib.import_module("kagg.search.q4_agent")
    COVER = importlib.import_module("kagg.search.cover")
    PLAN = importlib.import_module("kagg.plan")

    sched = PLAN.load(SCHEDULE)
    if arm == "q4":
        me = Q4.make_agent(sched, me=0)
        report = me.q4_report
    else:
        if arm == "shipped_live":
            Q4._routes_go_live_from(Q4.Q4_LIVE_ROUTES_FROM)
        me = SA.make_agent(sched, me=0)
        report = None

    spec = importlib.util.spec_from_file_location("opp", opponent)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    opp = mod.agent

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)

    grown, collected = collections.Counter(), collections.Counter()
    prev = {}
    last_farm, shops = {}, []
    for t in range(719):
        o = env.state[0].observation
        farm = (o.get("farms") or [{}])[0]
        last_farm = farm
        shops = list(((o.get("town") or {}).get("unlocked_shops")) or [])
        # Tile-diff yield accounting, exactly `swap_one_crop.run`'s. A tile whose unit count fell,
        # or that lost its crop without becoming a weed, was harvested.
        cur, weed_now = {}, {}
        for y, row in enumerate(farm.get("tiles") or []):
            for x, c in enumerate(row):
                k = (x, y)
                if isinstance(c, dict) and c.get("crop"):
                    cur[k] = (c["crop"], c.get("yield_units", 0))
                elif c == "WEED" or (isinstance(c, dict) and c.get("kind") == "WEED"):
                    weed_now[k] = True
        for k, (crop, u) in cur.items():
            was = prev.get(k)
            if was and was[0] == crop:
                if u > was[1]:
                    grown[crop] += u - was[1]
                elif u < was[1]:
                    collected[crop] += was[1] - u
            elif u:
                grown[crop] += u
        for k, (crop, u) in prev.items():
            if u and cur.get(k, (None,))[0] != crop and not weed_now.get(k):
                collected[crop] += u
        prev = cur
        env.step([me(o, t), opp(env.state[1].observation, t)])
        if env.done:
            break

    quads = list(last_farm.get("unlocked_quadrants") or ["NW"])
    herd = collections.Counter()
    herd_by_quad = collections.Counter()
    planted_by_quad = collections.Counter()
    import reference.kaggriculture as KG
    n = len(last_farm.get("tiles") or [])
    for y, row in enumerate(last_farm.get("tiles") or []):
        for x, c in enumerate(row):
            if not isinstance(c, dict):
                continue
            q = KG._quadrant_of(x, y, n)
            if c.get("animal"):
                herd[c["animal"]] += 1
                herd_by_quad[q] += 1
            # Tiles still carrying a crop on the LAST turn. This is not "tiles used" -- a wheat
            # tile harvested on d27 shows up empty here -- so read it only as a floor on whether
            # the new ground was worked at all.
            if c.get("crop"):
                planted_by_quad[q] += 1

    money = env.steps[-1][0]["reward"]
    opp_money = env.steps[-1][1]["reward"]
    return dict(
        seed=seed, arm=arm, money=money, opp_money=opp_money,
        won=bool(money > opp_money), drew=bool(money == opp_money),
        quadrants=len(quads), quads=quads,
        herd=dict(herd), herd_by_quad=dict(herd_by_quad),
        planted_by_quad=dict(planted_by_quad),
        grown=dict(grown), collected=dict(collected),
        shops_first_two=shops[:2], early_yarn=("YARN_STORE" in shops[:2]),
        armed=bool(report and report["armed"]),
        bought_day=(report or {}).get("bought_day"),
        refusals=(report or {}).get("refusals") or [],
    )


# ------------------------------------------------------------------------------------ the matrix
def one(seed, arm, opponent):
    cmd = [sys.executable, "-u", "scripts/q4_probe.py", "--cell",
           "--seed", str(seed), "--arm", arm, "--opponent", opponent, "--json"]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO,
                       env={**os.environ, "PYTHONPATH": "."})
    out = (p.stdout or "").strip()
    if not out:
        return dict(seed=seed, arm=arm, failed=(p.stderr or "")[-400:])
    try:
        r = json.loads(out.splitlines()[-1])
    except json.JSONDecodeError:
        return dict(seed=seed, arm=arm, failed=out[-400:])
    r["secs"] = time.time() - t0
    r["stderr"] = (p.stderr or "").strip()[-400:]
    return r


def _rate(r, crop):
    g = r.get("grown", {}).get(crop, 0)
    return (r.get("collected", {}).get(crop, 0) / g) if g else None


def _fmt_rate(v):
    return f"{v:.0%}" if v is not None else "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", action="store_true", help="run ONE measurement and print JSON")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--arm", choices=ARMS, default="q4")
    ap.add_argument("--seeds", type=int, nargs="+", default=list(EARLY_YARN_SEEDS))
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--out", default="data/logs/q4_probe.json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    opponent = a.opponent
    if not (REPO / opponent).exists():
        opponent = "submission/main.py"

    if a.cell:
        r = run_cell(a.seed, a.arm, opponent)
        print(json.dumps(r))
        return

    jobs = [(s, arm) for s in a.seeds for arm in a.arms]
    print(f"{len(jobs)} cells = {len(a.arms)} arms x {len(a.seeds)} seeds, "
          f"{a.workers} workers, opponent {opponent}", flush=True)
    print(f"seeds {a.seeds} -- every one of these draws a YARN_STORE in its first two draws, "
          f"which is the only board the q4 branch can act on\n", flush=True)

    rows = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(one, s, arm, opponent) for s, arm in jobs]
        for f in futs:
            r = f.result()
            rows.append(r)
            if r.get("failed"):
                print(f"  seed {r['seed']:>3} {r['arm']:<13} FAILED {r['failed'][:200]}", flush=True)
            else:
                print(f"  seed {r['seed']:>3} {r['arm']:<13} ${r['money']:>10,.0f}  "
                      f"opp ${r['opp_money']:>10,.0f}  {'W' if r['won'] else 'L'}  "
                      f"quads {r['quadrants']}  herd {r['herd']}  "
                      f"armed={r['armed']} bought_d={r['bought_day']}  [{r['secs']:.0f}s]",
                      flush=True)
                for msg in r.get("refusals", []):
                    print(f"      REFUSED {msg}", flush=True)
            json.dump(rows, open(REPO / a.out, "w"), indent=1)

    _tables(rows, a.seeds, a.arms)


def _tables(rows, seeds, arms):
    by = {(r["seed"], r["arm"]): r for r in rows if not r.get("failed")}
    crops = sorted({c for r in rows for c in (r.get("grown") or {})
                    if (r.get("grown") or {}).get(c, 0) > 0})

    print("\n" + "=" * 118)
    print("PER SEED -- bank, opponent, result, quadrants owned at d29, herd, per-crop collection")
    print("=" * 118)
    head = (f"{'seed':>5} {'arm':<13}{'bank':>11}{'opp':>11}  {'R':<2}{'quad':>5}"
            f"{'COW':>5}{'SHP':>5}  " + "".join(f"{c[:5]:>7}" for c in crops))
    print(head)
    for s in seeds:
        for arm in arms:
            r = by.get((s, arm))
            if not r:
                print(f"{s:>5} {arm:<13}{'FAILED':>11}")
                continue
            h = r["herd"]
            print(f"{s:>5} {arm:<13}{r['money']:>11,.0f}{r['opp_money']:>11,.0f}  "
                  f"{'W' if r['won'] else ('D' if r['drew'] else 'L'):<2}{r['quadrants']:>5}"
                  f"{h.get('COW', 0):>5}{h.get('SHEEP', 0):>5}  "
                  + "".join(f"{_fmt_rate(_rate(r, c)):>7}" for c in crops))
        print()

    print("=" * 118)
    print("PER ARM -- mean bank, wins, and the deltas that mean something")
    print("=" * 118)
    print(f"{'arm':<15}{'mean bank':>12}{'median':>12}{'wins':>8}{'mean quads':>12}"
          f"{'mean herd':>11}{'collect':>9}")
    means = {}
    for arm in arms:
        rs = [by[(s, arm)] for s in seeds if (s, arm) in by]
        if not rs:
            continue
        m = [r["money"] for r in rs]
        means[arm] = statistics.mean(m)
        tg = sum(v for r in rs for v in (r.get("grown") or {}).values())
        tc = sum(v for r in rs for v in (r.get("collected") or {}).values())
        print(f"{arm:<15}{statistics.mean(m):>12,.0f}{statistics.median(m):>12,.0f}"
              f"{sum(1 for r in rs if r['won']):>5}/{len(rs)}"
              f"{statistics.mean([r['quadrants'] for r in rs]):>12.2f}"
              f"{statistics.mean([sum(r['herd'].values()) for r in rs]):>11.2f}"
              f"{(f'{tc / tg:.0%}' if tg else '-'):>9}")

    print(f"\n{'comparison':<34}{'mean d':>12}{'median d':>12}{'seeds better':>14}{'W/L swing':>11}")
    for lo, hi, why in (("shipped", "shipped_live", "the LIVE-ROUTE handicap alone"),
                        ("shipped_live", "q4", "the PARCEL + herd, handicap paid by both"),
                        ("shipped", "q4", "what actually ships vs the variant, all-in")):
        pairs = [(by[(s, lo)], by[(s, hi)]) for s in seeds if (s, lo) in by and (s, hi) in by]
        if not pairs:
            continue
        d = [b["money"] - a_["money"] for a_, b in pairs]
        wl = sum(1 for a_, b in pairs if b["won"]) - sum(1 for a_, b in pairs if a_["won"])
        print(f"{hi + ' - ' + lo:<34}{statistics.mean(d):>+12,.0f}{statistics.median(d):>+12,.0f}"
              f"{sum(1 for x in d if x > 0):>8}/{len(d)}{wl:>+11}   {why}")

    q4s = [by[(s, 'q4')] for s in seeds if (s, 'q4') in by]
    if q4s:
        armed = sum(1 for r in q4s if r["armed"])
        got = sum(1 for r in q4s if r["quadrants"] >= 4)
        print(f"\nq4 armed on {armed}/{len(q4s)} seeds; SE actually unlocked on {got}/{len(q4s)}. "
              f"Buy days: {[r['bought_day'] for r in q4s]}")
        ref = [m for r in q4s for m in (r.get('refusals') or [])]
        print(f"refusals: {ref if ref else 'none'}")
        four = [r for r in q4s if r["quadrants"] >= 4]
        if four:
            print(f"animals standing in SE at d29: "
                  f"{[r['herd_by_quad'].get('SE', 0) for r in four]} of "
                  f"{[sum(r['herd'].values()) for r in four]} total")
            print(f"SE tiles still carrying a crop at d29: "
                  f"{[r['planted_by_quad'].get('SE', 0) for r in four]} (of 25; a floor, since a "
                  f"tile harvested before d29 reads empty here)")

    print("\nSeed range: " + ", ".join(str(s) for s in seeds) +
          " -- all early-yarn boards, so this is the CONDITIONAL effect. The trigger fires on "
          "about a sixth of boards; the season-average effect is this times that rate.")
    print("The ladder is Elo. Money is the screen; the W/L column is the thing that scores.")


if __name__ == "__main__":
    main()
