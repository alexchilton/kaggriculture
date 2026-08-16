"""Cross-entropy search over the agent's crop allocation and herd dials, scored on WIN RATE.

    python -u scripts/cem_allocation.py --gens 8 --pop 12 --seeds-per-gen 6 --workers 16

## The search space, and why each bound is the number it is

Every bound is pinned by `tests/test_the_allocation_dials_reach_the_tiles_they_claim.py`. None of
them is a guess, and two of them are not what a reading of the docstrings would suggest.

    dial   name                                     range   what fixes the bound
    fork   MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT   0..1    a flag
    m      WHEAT -> MELON      tiles                0..24   wheat stops in d12..d17
    t      WHEAT -> TOMATO     tiles                0..14   wheat stops left before d18
    c      WHEAT -> CARROT     tiles                0..24   wheat stops left before d26
    s      STRAWBERRY -> WHEAT tiles                0..7    ALL the late strawberry there is
    g      HERD_GEESE                               0..3    the dial saturates; 4 == 3

**`CROP_TILE_SHIFTS` cannot reduce melon.** The schedule plants melon on d0, d6 and d7 only, and
`LATE_CROP_FROM_DAY` is 12, so a `MELON -> WHEAT` shift moves exactly zero tiles. A search told to
"tune the melon tile count" through this dial can only ever add. That is why the **melon fork** is
in the space: `MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT` converts the d6/d7 melon rows to strawberry
once the opponent shows 7+ melon tiles, and turning it off is the only reachable way to hold
MELON 20 / STRAWBERRY 34 -- which is Kawashigi's own allocation, and the direction today's sweep
pointed (`STRAWBERRY->WHEAT x4` +$3,647, `WHEAT->MELON x2` +$2,499).

**The shifts drain in list order**, so MELON takes the earliest wheat stops, TOMATO the next and
CARROT the rest. That order is what makes the three bounds safe jointly rather than one at a time;
`test_the_far_corner_of_the_search_box_is_still_a_plantable_schedule` is the check.

## Routing

`cover.PRECOMPUTED_ROUTES` covers exactly d12-d29 -- the same days the shifts touch -- and it keys a
stop on `(tile, ops)`, so a re-crewed stop can be DROPPED from the solved route instead of adapted
to. A dropped stop is not "melon instead of wheat", it is "no tile at all", which would make every
shift look bad for a reason that has nothing to do with the crop. `scripts/swap_one_crop.py` handles
that by unsolving d12-d29 unconditionally.

Unsolving costs **3x the wall clock** (measured 2026-08-15: the same 24 pool games take 96s unsolved
against 31s solved), so the choice is worth a measurement rather than a default.
`scripts/cem_collection.py` runs the same shift both ways and reads the destination crop's
collection rate; `--unsolved` here selects the expensive regime if that measurement demands it.
Whichever is chosen is applied to **every** candidate, the all-zero vector included.

## The objective, and the opponent that had to be invented for it

**Elo expected score, `win + 0.5 * draw`**, in both seatings. The ladder is Elo: a $43k win and a
$4k win score identically, so money is reported and never selected on.

The first design scored against six pool opponents and **did not work**. Measured 2026-08-15: the
shipped agent wins **100%** of its games against every member of `pool.OPPONENTS` except `mirror`,
which it draws 100% of the time because it is the same file playing itself in a deterministic
environment. Win rate against the pool is a constant. It cannot rank anything, and a CEM run on it
would have spent three hours reporting ties.

So the field is built around a **frozen copy of the shipped agent** (`shipped`), which is the actual
bar a dial change has to clear, and which discriminates: the baseline draws it 0.50 by construction,
`fork0` scored 0.25 and `s4` 0.50 on a 4-seed probe. Freezing matters -- an opponent built from the
candidate's own dials would move with the candidate, which is the confound `pool.BASELINE` exists to
avoid.

`carrot_25` and `melon_heavy` stay in as guards, and they are not decoration. `CLAUDE.md` records
melon going 25 -> 12 -> 25 because a mirror-only sweep pointed the wrong way, on this exact dial. A
duel against ourselves answers "what is best if both sides play it"; the guards are what notice a
candidate that wins the duel and loses to a field. `melon_heavy` is also the only guard that fires
the melon fork at all, since the fork reads the opponent's melon tile count.

## Common random numbers, and resampling

Every candidate in a generation is scored on the SAME seed set, which cancels the seed variance that
otherwise swamps the effect -- the single biggest lever here, given a per-seed sd of ~$4,500 on a
config delta. The seed set is then **redrawn every generation**, because a fixed objective is how
this repo got a +40% that became +12.8% on held-out seeds.

The winner is re-scored on a fresh draw that no generation ever saw. The winner's curse is
documented in `CLAUDE.md`: 11 accepted moves in 14 generations for +1.6%.
"""
import argparse
import json
import pathlib
import random
import sys
import time

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
WORK = REPO / "data" / "cem"

#: `shipped` is injected into `pool.OPPONENTS` at run time as a path to the frozen zero-dial agent.
#: It is the only member that discriminates; the other two are guards. `starter` and `pass` are out
#: because they sell almost nothing, so every number against them is roughly 2x reality, and
#: `mirror` is out because it draws every game (measured -- see the module docstring).
FIELD = ("shipped", "carrot_25", "melon_heavy")

#: `(name, low, high)`. See the module docstring for what fixes each bound.
DIALS = (
    ("fork", 0, 1),
    ("melon", 0, 24),
    ("tomato", 0, 14),
    ("carrot", 0, 24),
    ("straw_off", 0, 7),
    ("geese", 0, 3),
)

#: The shipped agent: fork on, no shifts, no geese. Always evaluated, in every generation, so the
#: table has a reference row measured on that generation's own seeds.
BASELINE = (1, 0, 0, 0, 0, 0)

#: Centred on today's prior -- melon up, strawberry down, fork and geese genuinely open -- with a
#: standard deviation wide enough that the prior is a starting point and not a constraint. The
#: prior is one sweep on 12 usable seeds; it is not proven.
INIT_MU = (0.5, 4.0, 3.0, 4.0, 4.0, 0.7)
INIT_SD = (0.6, 6.0, 5.0, 7.0, 3.0, 1.0)

#: Below this the elite's own spread stops being informative and the search collapses onto whatever
#: two generations of noise picked. A tenth of each dial's range, floored at 0.45 so the binary
#: dials keep flipping.
SD_FLOOR = tuple(max(0.45, 0.10 * (hi - lo)) for _, lo, hi in DIALS)

#: How much of the previous distribution survives a refit. Straight replacement makes the search
#: jump on one generation of noise.
SMOOTH = 0.35


def vector_body(v, solved=True):
    """The dial assignments a candidate file makes on its PRIVATE copy of the agent module."""
    fork, melon, tomato, carrot, straw_off, geese = v
    shifts = [("WHEAT", "MELON", melon), ("WHEAT", "TOMATO", tomato),
              ("WHEAT", "CARROT", carrot), ("STRAWBERRY", "WHEAT", straw_off)]
    # Drop the zeros. A budget of 0 is already a no-op inside `_recrew`, but an all-zero tuple is
    # still truthy and would enter the shift branch, so filtering keeps "no shifts" literally that.
    shifts = tuple((a, b, int(n)) for a, b, n in shifts if n > 0)
    lines = [
        f"A.MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT = {bool(fork)}",
        f"A.CROP_TILE_SHIFTS = {shifts!r}",
        "A.LATE_CROP_FROM_DAY = 12",
        f"A.HERD_GEESE = {int(geese)}",
    ]
    if not solved:
        # Deliberately GLOBAL, unlike the dials above. The routing regime has to be the same for
        # both seats or the duel measures the regime instead of the crops, and every agent in one
        # `evaluate` call shares the worker process. The crop dials are the opposite case: they are
        # the thing being contrasted, so they must be private.
        lines += [
            "import kagg.search.cover as _C",
            "_C.UNSOLVE_DAYS = tuple(range(12, 30))",
            "_C.PRECOMPUTED_ROUTES = {d: r for d, r in _C.PRECOMPUTED_ROUTES.items() "
            "if d not in _C.UNSOLVE_DAYS}",
        ]
    return "\n".join(lines)


def write_candidate(v, solved=True):
    """A candidate agent file for `pool.evaluate`, which passes a path straight to `env.run`.

    The file loads its own copy of `schedule_agent` and of every module `schedule_agent` holds dial
    state in, so two candidates can share a process without sharing dials.
    """
    WORK.mkdir(parents=True, exist_ok=True)
    tag = "_".join(str(x) for x in v) + ("_solved" if solved else "_unsolved")
    path = WORK / f"cem_{tag}.py"
    path.write_text(
        f"import importlib.util as _ilu\n"
        f"import sys\n"
        f"sys.path.insert(0, {str(REPO)!r})\n"
        f"import kagg.plan as PLAN\n"
        f"import kagg.search          # the package must exist before a module claims to be in it\n"
        f"\n"
        f"# A PRIVATE copy of the agent module, under a name unique to this candidate. A plain\n"
        f"# `import kagg.search.schedule_agent` returns the one cached module, so two candidate\n"
        f"# files in one `env.run` overwrite each other's dials and the second to load plays both\n"
        f"# seats. `__package__` is set because the module uses relative imports (`from . import\n"
        f"# cover`); those still resolve to the SHARED cover/router/routines, which is what we want,\n"
        f"# since only the dials below are per-candidate.\n"
        f"_NAME = 'kagg.search.schedule_agent__{tag}'\n"
        f"_spec = _ilu.spec_from_file_location(\n"
        f"    _NAME, {str(REPO / 'kagg/search/schedule_agent.py')!r})\n"
        f"A = _ilu.module_from_spec(_spec)\n"
        f"A.__package__ = 'kagg.search'\n"
        f"sys.modules[_NAME] = A\n"
        f"_spec.loader.exec_module(A)\n"
        f"\n"
        f"{vector_body(v, solved=solved)}\n"
        f"\n"
        f"_S = PLAN.load({str(REPO / 'data/seed_scripts/kawashigi/schedule.json')!r})\n"
        f"_A = {{}}\n"
        f"\n"
        f"\n"
        f"def agent(obs, config):\n"
        f"    seat = obs['player']\n"
        f"    if seat not in _A:\n"
        f"        _A[seat] = A.make_agent(_S, me=seat)\n"
        f"    return _A[seat](obs, obs['step'])\n"
    )
    return str(path)


def score(v, seeds, workers, solved=True, field=FIELD):
    """`(elo, win, draw, money, per_opponent)` for one dial vector on one seed set."""
    from kagg.arena import pool

    res = pool.evaluate(write_candidate(v, solved=solved), seeds, opponents=field, workers=workers)
    return (res.win_rate + 0.5 * res.draw_rate, res.win_rate, res.draw_rate, res.mean_money,
            {k: list(w) for k, w in res.per_opponent.items()})


def sample(rng, mu, sd):
    out = []
    for i, (_, lo, hi) in enumerate(DIALS):
        out.append(int(min(hi, max(lo, round(rng.gauss(mu[i], sd[i]))))))
    return tuple(out)


def refit(elite, mu, sd):
    """Mean and spread of the elite, smoothed onto the old distribution, with a variance floor."""
    n = len(elite)
    new_mu, new_sd = [], []
    for i in range(len(DIALS)):
        xs = [e[i] for e in elite]
        m = sum(xs) / n
        var = sum((x - m) ** 2 for x in xs) / max(1, n - 1)
        new_mu.append(SMOOTH * mu[i] + (1 - SMOOTH) * m)
        new_sd.append(max(SD_FLOOR[i], SMOOTH * sd[i] + (1 - SMOOTH) * var ** 0.5))
    return tuple(new_mu), tuple(new_sd)


def label(v):
    return "fork{} m{} t{} c{} s{} g{}".format(*v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=8)
    ap.add_argument("--pop", type=int, default=12)
    ap.add_argument("--elite", type=int, default=4)
    ap.add_argument("--seeds-per-gen", type=int, default=6)
    ap.add_argument("--holdout-seeds", type=int, default=24)
    ap.add_argument("--finalists", type=int, default=2)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--rng-seed", type=int, default=20260815)
    ap.add_argument("--unsolved", action="store_true",
                    help="drop cover.PRECOMPUTED_ROUTES for d12-29. Measured 2026-08-15: NOT "
                         "needed -- shifted crops are collected at 96-100%% with the routes kept "
                         "-- and it costs 3x the wall clock and $6-15k a season. See "
                         "scripts/cem_collection.py.")
    ap.add_argument("--out", default=str(REPO / "logs" / "cem_allocation.json"))
    a = ap.parse_args()

    from kagg.arena import pool

    solved = not a.unsolved
    # The frozen bar. `pool.evaluate` resolves a name to a spec in the PARENT process and ships the
    # spec to the worker, and a path string is a spec `env.run` accepts, so a run-time key works.
    # Frozen, not mirrored: an opponent built from the candidate's own dials would move with the
    # candidate, which is the confound `pool.BASELINE` exists to avoid.
    pool.OPPONENTS["shipped"] = write_candidate(BASELINE, solved=solved)

    rng = random.Random(a.rng_seed)
    # Drawn once, up front, and partitioned: no generation ever sees a held-out seed, and no two
    # generations share a seed. A seed that appeared twice would let the search fit it.
    all_seeds = rng.sample(range(1, 100000), a.gens * a.seeds_per_gen + a.holdout_seeds)
    holdout = sorted(all_seeds[:a.holdout_seeds])
    pool_seeds = all_seeds[a.holdout_seeds:]

    games = a.seeds_per_gen * len(FIELD) * 2
    print(f"CEM over {[d[0] for d in DIALS]}", flush=True)
    print(f"  bounds        {[(d[0], d[1], d[2]) for d in DIALS]}", flush=True)
    print(f"  field         {FIELD}   routing {'SOLVED' if solved else 'UNSOLVED d12-29'}", flush=True)
    print(f"  pop {a.pop}  elite {a.elite}  gens {a.gens}  seeds/gen {a.seeds_per_gen}"
          f"  -> {games} games per candidate", flush=True)
    print(f"  holdout seeds {holdout}", flush=True)
    print(f"  init mu {INIT_MU}\n  init sd {INIT_SD}\n", flush=True)

    mu, sd = INIT_MU, INIT_SD
    history, seen = [], {}
    t_start = time.time()

    for gen in range(a.gens):
        seeds = sorted(pool_seeds[gen * a.seeds_per_gen:(gen + 1) * a.seeds_per_gen])
        # The baseline is re-scored on every generation's own seeds, so the table's reference row
        # moves with the seed draw instead of being a number from a different game.
        cands = [BASELINE] + [sample(rng, mu, sd) for _ in range(a.pop)]
        if history:                       # carry the incumbent, so a good vector cannot be lost
            cands.append(history[-1]["best"])
        uniq = list(dict.fromkeys(cands))

        print(f"=== gen {gen}  seeds {seeds}  {len(uniq)} distinct candidates "
              f"({len(cands) - len(uniq)} duplicates skipped)", flush=True)
        rows = []
        for v in uniq:
            t0 = time.time()
            elo, win, draw, money, per = score(v, seeds, a.workers, solved=solved)
            rows.append(dict(v=v, elo=elo, win=win, draw=draw, money=money, per=per))
            mark = "  <- baseline" if v == BASELINE else ""
            # `shipped` is the only column that discriminates; the guards sit at 1.00 unless a
            # candidate breaks something, which is exactly what they are there to catch.
            duel = per.get("shipped", [float("nan")])[0]
            print(f"  {label(v):<32} elo {elo:.3f}  duel {duel:.3f}  win {win:.3f}"
                  f"  ${money:>10,.0f}  [{time.time() - t0:.0f}s]{mark}", flush=True)

        rows.sort(key=lambda r: (-r["elo"], -r["money"]))
        elite = [r["v"] for r in rows[:a.elite]]
        base = next(r for r in rows if r["v"] == BASELINE)
        best = rows[0]
        mu, sd = refit(elite, mu, sd)

        history.append(dict(gen=gen, seeds=seeds, rows=rows, elite=elite,
                            best=best["v"], best_elo=best["elo"], best_money=best["money"],
                            base_elo=base["elo"], base_money=base["money"],
                            mu=list(mu), sd=list(sd)))
        print(f"  gen {gen}: best {label(best['v'])} elo {best['elo']:.3f} "
              f"(baseline {base['elo']:.3f}, delta {best['elo'] - base['elo']:+.3f})", flush=True)
        print(f"  refit mu {[round(x, 2) for x in mu]}  sd {[round(x, 2) for x in sd]}"
              f"  [{(time.time() - t_start) / 60:.1f} min elapsed]\n", flush=True)
        json.dump(dict(history=history, holdout=holdout), open(a.out, "w"), indent=1, default=str)

    # ---- held-out confirmation -------------------------------------------------------------
    # Rank every distinct vector the search ever scored by its own generation's margin over the
    # baseline measured on the SAME seeds. Raw elo across generations is not comparable: the seed
    # set changed under it.
    for h in history:
        for r in h["rows"]:
            v = tuple(r["v"])
            margin = r["elo"] - h["base_elo"]
            if v != BASELINE and margin > seen.get(v, (-9,))[0]:
                seen[v] = (margin, h["gen"])
    finalists = [v for v, _ in sorted(seen.items(), key=lambda kv: -kv[1][0])][:a.finalists]
    final_mu = tuple(int(min(hi, max(lo, round(mu[i])))) for i, (_, lo, hi) in enumerate(DIALS))
    for v in (final_mu,):
        if v not in finalists and v != BASELINE:
            finalists.append(v)

    print(f"=== held-out draw, {a.holdout_seeds} seeds never used in any generation", flush=True)
    print(f"  seeds {holdout}", flush=True)
    print(f"  {a.holdout_seeds * len(FIELD) * 2} games per row\n", flush=True)
    print(f"  {'config':<26}{'elo':>8}{'duel':>8}{'win':>8}{'money':>12}", flush=True)

    # The baseline row is the control and must draw itself 0.500 exactly. If it does not, the two
    # sides are not the same agent and every duel number above is measuring something else.
    final = [(BASELINE, "SHIPPED baseline (control: duel must be 0.500)")]
    final += [(v, "finalist") for v in finalists]

    rows_out = []
    for v, note in final:
        t0 = time.time()
        elo, win, draw, money, per = score(v, holdout, a.workers, solved=solved)
        rows_out.append(dict(v=v, note=note, solved=solved, elo=elo, win=win, draw=draw,
                             money=money, per=per))
        duel = per.get("shipped", [float("nan")])[0]
        print(f"  {label(v):<26}{elo:>8.3f}{duel:>8.3f}{win:>8.3f}{money:>12,.0f}"
              f"   {note}  [{time.time() - t0:.0f}s]", flush=True)
        json.dump(dict(history=history, holdout=holdout, final=rows_out),
                  open(a.out, "w"), indent=1, default=str)

    print("", flush=True)
    for row in rows_out:
        print(f"  per-opponent, {label(row['v']):<26} "
              + "  ".join(f"{k}:{w[0]:.2f}/${w[1]:,.0f}" for k, w in sorted(row["per"].items())),
              flush=True)
    print(f"\nwrote {a.out}   total {(time.time() - t_start) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
