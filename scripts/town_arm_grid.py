"""Does any TOWN want the edit? Reported per town, per opponent band -- never as one pooled mean.

Alex, 2026-08-21: *"where you just show the wins - its not showing if a certain town is better or
worse you have averaged over all and only over all people - so its unhelpful - there needs to be a
few slightly weaker people in there too and also the mirror - basically your stats are shit"*.

He is right. The previous sweep printed one pooled margin per arm across twelve strong opponents
and sixteen seed-drawn towns. A pooled mean is exactly the wrong statistic for the question being
asked, which is conditional: *is there a town where carrot pays*. Averaging over the conditioning
variable destroys the only signal worth finding, and a wash at the mean is what you get whether
carrot is useless everywhere or a $5k win on a fifth of towns and a $1k loss on the rest.

Three changes:

**The town is an explicit axis, not a lottery.** `breakdown.run` accepts a `shops` callable, so a
town is constructed rather than fished for with seeds. A shop unlocks at hour 0 of d3, d6, d9, d12,
d15, d18, d21 and d24 -- eight of them -- drawn **with replacement** from eight types, so the space
is 8**8 and enumeration is out. Towns are sampled, and each is reported with its DRAIN VECTOR: how
many times a shop-interval the town takes each product off the book. That vector, not the seed and
not the shop names, is what an arm should be conditioned on.

**The opponents span strength, not just the top.** Six strong, six middle, six weak, chosen off
median bank across the archive. A pool of leaders answers "does this beat the best", which is not
the ladder's question -- Elo pays for the whole field.

**The mirror is in.** Our own replay in the other chair. A mirror is the one opponent guaranteed to
contest exactly the products we contest, so it is the strictest test of an arm that changes what we
sell -- and `money == money` is exact, so a mirror that draws says the arm changed nothing real.

Output is three tables and no pooled headline:

    1. arm x CARROT-drain band, and arm x TOMATO-drain band -- the conditional the question needs
    2. arm x opponent band -- strong / middle / weak / mirror, separately
    3. the ten best and ten worst TOWNS for each arm, with their drain vectors

    python -u scripts/town_arm_grid.py --towns 48 --jobs 14
"""

import argparse
import collections
import functools
import json
import multiprocessing
import os
import pathlib
import random
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B                                                        # noqa: E402
import tape_edit_sweep as S                                                  # noqa: E402
from kagg.search import schedule_agent as SA                                 # noqa: E402
from kagg.search import tape_edit as E                                       # noqa: E402

#: Bands come from `data/opponent_pool_ranked.json`, which is the ARCHIVE joined to the real
#: Kaggle leaderboard -- not from median bank.
#:
#: **Banding on archive bank was wrong and produced inverted labels.** Alex, 2026-08-21: *"how on
#: earth do you think ryo and kobe are weak?? - you just goinf on money? cos ryo is nrr 1"*. He is
#: right twice over. The archive is a SELECTED sample -- he downloads losses -- so a median bank
#: taken across it measures which of a player's games got saved, not how good the player is. And
#: bank is not rating in any case: the ladder is Elo, where a $43k win and a $4k win score the same
#: (`CLAUDE.md`). The first pass put Ryo Hasegawa (rank 1), Arman Tuganbaev (3), Subramanya N (4)
#: and Kobe BRYANT (10) in "middle", ReCurSiON (13) and Eddy Despradel (45) in "weak", and its
#: best "strong" player was rank 21. Every label was scrambled.
#:
#: Rebuilt 2026-08-21 from `kaggle competitions leaderboard -c kaggriculture`, 5,724 teams:
#: top = ranks 1-7, mid = 21-45, low = 374-457. カワシギ is rank 9 and we are rank 91.

#: **Opponents chosen to span BEHAVIOUR, not rank.** Rank was the right stratifier for the
#: leaderboard-vs-bank error and is the wrong one for the herd and crop arms: the ranked pool came
#: out 7 cow-leaning to 2 sheep-leaning, with the three strongest sheep players missing entirely
#: (StackKnight 6/12 rank 29, Bruce 6/12 rank 38, Eddy Despradel 6/8 rank 45). A cow-shift arm
#: judged against a cow-heavy field is being asked a different question than the one intended.
#:
#: This list spans cow 3-10, sheep 3-12, carrot 0-60 and tomato 0-22, while keeping the four unique
#: top agents for branch and rank coverage:
#:
#:     tetsuya          2   cow  9 shp  6   CA  0  TO  0   melon  0   arms melon/q4
#:     Arman Tuganbaev  3   cow  6 shp 11   CA 12  TO  0   melon  7   sheep end
#:     Subramanya N     4   cow  3 shp  3   CA 60  TO  5   melon  8   carrot extreme
#:     Ryo Hasegawa     1   cow  8 shp  6   CA  0  TO  0   melon 11   rank 1
#:     StackKnight     29   cow  6 shp 12   CA  1  TO  0   melon 12   sheep end
#:     Bruce           38   cow  6 shp 12   CA 10  TO  0   melon 12   sheep end
#:     Crop Dusta     410   cow  9 shp  3   CA  0  TO 22   melon  5   only tomato contester
#:     peikopon         7   cow 10 shp  4   CA  6  TO  0   melon 12   cow end
#:     Matteo123383   404   cow 10 shp  4   CA 14  TO  0   melon 12   cow end
#:     Victor @ Tufa   21   cow  9 shp  5   CA  0  TO  0   melon  5   arms melon/q4
BEHAVIOUR_SPAN = ("tetsuya", "Arman Tuganbaev", "Subramanya N", "Ryo Hasegawa",
                  "StackKnight", "Bruce", "Crop Dusta", "peikopon",
                  "Matteo123383iend", "Victor @ Tufa Labs")

#: The mirror is not a tape. It is our own agent, built the same way, in the other chair.
MIRROR = "MIRROR"

#: Products a town can drain, fixed so the raw CSV has stable columns.
DRAIN_KEYS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")

POOL_FILE = REPO / "data/opponent_pool_ranked.json"
TAPE_DIR = REPO / "data/opponent_tapes"


def load_bands():
    """`{name: (replay, seat, melon_at_d3, band, rank, rating)}` for every ranked opponent."""
    rows = json.loads(POOL_FILE.read_text())
    return {r["name"]: (str(REPO / r["replay"]), int(r["seat"]), r.get("melon_at_d3"),
                        r["band"], r["rank"], r["rating"])
            for r in rows}


def stratified_towns(n, rng_seed=20260821):
    """Towns drawn to SPAN the two things a uniform sample cannot reach in useful numbers.

    Uniform sampling failed twice on 2026-08-21 and in opposite directions:

      **q4 never armed.** `q4_branch` needs a YARN_STORE unlocked by d5 -- i.e. in the d3 or d6
      slot -- and a uniform draw puts one there about a quarter of the time, which combined with an
      opponent under `melon_branch.OPPONENT_MELON` made it 0 of 76 combinations. So the whole
      3,648-season grid, and the herd probe with it, ran on the melon and strawberry tapes only --
      and q4 is the tape that leans hardest on animals.

      **Carrot drain 6 was 3 towns of 48.** That is the only band where carrot pays (+$1,937), and
      it carried 57 of 3,648 seasons.

    A third of the sample is forced to each, and a third stays uniform so the bands remain
    comparable to the unstratified grid.
    """
    rng = random.Random(rng_seed)
    out, k = [], max(1, n // 3)

    def draw():
        return tuple(rng.choice(S.SHOP_NAMES) for _ in range(len(S.UNLOCK_DAYS)))

    while len([t for t in out if t[2] == "yarn_early"]) < k:
        d = list(draw())
        # **Slot 0 only -- the d3 unlock.** `q4_branch.DECIDE_BY_DAY = 5`, so a yarn store landing
        # in the d6 slot is read too late and the branch never arms. Seeding slot 0 or 1 put it in
        # the d6 slot half the time and the "yarn_early" stratum then armed q4 less often than the
        # uniform one did.
        d[0] = "YARN_STORE"
        d = tuple(d)
        out.append((d, S.drain_vector(d), "yarn_early"))
    tries = 0
    while len([t for t in out if t[2] == "carrot_rich"]) < k and tries < 200000:
        tries += 1
        d = draw()
        dv = S.drain_vector(d)
        if dv.get("CARROT", 0) >= 5:
            out.append((d, dv, "carrot_rich"))
    while len(out) < n:
        d = draw()
        out.append((d, S.drain_vector(d), "uniform"))
    return out


def sample_towns(n, rng_seed=20260821):
    """`[(draw, drain_vector)]` -- `n` towns drawn the way the environment draws them.

    Uniform with replacement over the eight shop types, eight unlocks. Seeded so the town list is
    identical between the Mac and the box and between runs; a grid whose rows move under it cannot
    be compared to yesterday's.
    """
    rng = random.Random(rng_seed)
    towns = []
    for _ in range(n):
        draw = tuple(rng.choice(S.SHOP_NAMES) for _ in range(len(S.UNLOCK_DAYS)))
        towns.append((draw, S.drain_vector(draw)))
    return towns


def _thin_or_replay(name, bands):
    replay, seat = bands[name][0], bands[name][1]
    cut = TAPE_DIR / ("%s_seat%d.json" % (pathlib.Path(replay).stem, seat))
    if cut.exists():
        return {"kind": "thin", "path": str(cut)}
    return {"kind": "replay", "replay": replay, "team": name, "seat": seat}


def with_step(agent):
    """Feed the agent a `step` when the observation has none. **Seat 1 has none.**

    `kaggle-environments` puts `step` only on the FIRST seat's observation:

        seat0 keys: day farms hour market player private remainingOverageTime step town
        seat1 keys: day farms hour market player private remainingOverageTime      town

    and `schedule_agent.replayed` reads `obs.get("step", 0)`. So an agent seated second reads step
    0 on every turn and replays turn 0 for the whole season: `BUILD_PASTURE`, five `HIRE`s and a
    `BUY_ANIMAL`, every turn, `hands` empty, bank 3000 -> 22 -> 1 -> 0.

    Measured 2026-08-21 against Ryo Hasegawa on one town: **seat 0 banks $128,807 and wins; seat 1
    banks $0**. That made the mirror opponent a corpse and its 100% win rate meaningless -- it was
    read here as a seat-order advantage for a while, which it is not.

    The fix belongs in the harness, not in the agent: the shipped artifact wins on both seats on
    the real ladder, so the ladder supplies what this loop does not.
    """
    def wrapped(obs, config=None):
        if obs.get("step") is None:
            obs = dict(obs)
            obs["step"] = int(obs.get("day", 0) or 0) * 24 + int(obs.get("hour", 0) or 0)
        return agent(obs, config)
    return wrapped


def build_agent(spec, thin):
    """Our agent for one `Arm`. Shared by our seat and by the mirror's seat.

    Everything the arm does comes off the ONE object: its opening edits, its runtime wrappers, and
    the crops it must offer. There is no second list to forget to update -- which is how a
    conditional arm ran a whole grid with no seller and banked $4,412 less than the static arm it
    was supposed to equal.
    """
    a = spec if isinstance(spec, S.Arm) else S.arm("adhoc", opening=tuple(spec))
    saved = SA.EMBEDDED_OPENINGS
    SA.EMBEDDED_OPENINGS = S.edited_openings(a.opening) if a.opening else {}
    try:
        agent = SA.make_agent(thin, 0, router=True)
    finally:
        SA.EMBEDDED_OPENINGS = saved

    for op in a.wrappers:
        if op[0] == "topup":
            _, days, hour, prods = op
            agent = E.top_up_at_hour(agent, prods, hour, from_day=min(days))
        elif op[0] == "herd":
            _, mode, decide_day = op
            agent = E.herd_species(agent, mode, decide_day)
        elif op[0] == "herdshift":
            _, delta, from_day = op
            agent = E.herd_shift(agent, delta, from_day)
        elif op[0] == "condcarrot":
            _, drain_min, opp_max = op
            agent = E.carrot_when_it_pays(agent, drain_min, opp_max)
        else:
            raise ValueError("unknown wrapper %r in arm %s" % (op, a.name))

    # Derived on the Arm, never recomputed here -- see `tape_edit_sweep.arm`.
    if a.sells:
        agent = E.surplus_sells(agent, list(a.sells))
    return with_step(agent)


@functools.lru_cache(maxsize=1)
def _plan():
    """`(thin_schedule, economy)`, parsed once per worker rather than once per season."""
    _, base_schedule, _ = B.TAPES["kawashigi"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(base_schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    return thin, B.env_config(B.TAPES["kawashigi"][0])


#: Module-level, and cleared at the top of every `_job`. A per-call dict captured by the wrapper
#: closure is captured ONCE per worker process, so every later season in that worker writes into the
#: FIRST season's dict -- which reported `melon` for all 72 seasons of a smoke run including ones
#: against an 11-melon opponent that must arm strawberry.
_ARMED = {}


def _install_branch_probe():
    """Wrap both latches so the season records which tape it played. Idempotent per process."""
    from kagg.search import melon_branch as MBx, q4_branch as Q4x                  # noqa: PLC0415
    if getattr(MBx.arm, "_probe", False):
        return
    om, oq = MBx.arm, Q4x.arm

    def wm(sc, st, o, d):
        r = om(sc, st, o, d)
        _ARMED["m"] = bool(st.get(MBx.BRANCH.armed_key))
        return r

    def wq(sc, st, o, d):
        r = oq(sc, st, o, d)
        _ARMED["q"] = bool(st.get(Q4x.BRANCH.armed_key))
        return r
    wm._probe = wq._probe = True
    MBx.arm, Q4x.arm = wm, wq


def _job(spec):
    """One (town, opponent, arm) season. Top level so `multiprocessing` can pickle it."""
    ti, draw, opp_name, opp, arm_name, edits, seed, weeds = spec
    thin, economy = _plan()
    _ARMED.clear()
    _install_branch_probe()
    theirs = [0]

    def mine():
        a = build_agent(edits, thin)
        return lambda o, t: a(o)

    def opponent():
        # **The mirror is the CONTROL agent, never the edited one.** An arm played against itself
        # is a symmetric change and cancels; what we want to know is what the arm does against the
        # thing we ship today.
        # `is` fails here: the spec crosses a process boundary and the string is re-created.
        p = build_agent([], thin) if opp == MIRROR else S.make_opponent(opp)

        def watched(obs, t):
            farms = obs.get("farms") or []
            seat = int(obs.get("player", 1) or 1)
            if len(farms) > seat:
                theirs[0] = int(farms[seat].get("money", 0) or 0)
            return p(obs) if opp == MIRROR else p(obs, t)

        return watched

    days, _, _, _ = B.run(mine, opponent, seed, weeds, economy=economy,
                          shops=S.town_shops(draw))
    tape = {(False, False): "melon", (True, False): "straw",
            (False, True): "q4", (True, True): "q4melon"}[
        (bool(_ARMED.get("m")), bool(_ARMED.get("q")))]
    return (ti, opp_name, arm_name, seed, days[-1]["money"], theirs[0],
            days[-1].get("weed", 0), tape)


def band_of(name, bands):
    return "mirror" if name == MIRROR else bands[name][3]


#: The columns before the drain vector. Named once so the header and the row cannot drift.
ROW_FIELDS = ("town", "stratum", "tape", "opponent", "band", "rank", "arm", "seed",
              "ours", "theirs", "weed")


def rows_header():
    return ",".join(ROW_FIELDS + tuple("drain_" + p for p in sorted(DRAIN_KEYS))) + "\n"


def rows_line(town, stratum, tape, opponent, band, rank, arm, seed, ours, theirs, weed, drains):
    """One season, as one CSV line.

    **This lived inline in `main` as a `%`-format with eleven specifiers and twelve arguments.**
    Python raises `TypeError: not all arguments converted during string formatting` -- at the point
    the file is written, which is after the last season. A 6,048-season run spent 1.7 hours and
    produced a traceback and no CSV. Building the line here, off the same `ROW_FIELDS` the header
    uses, is what makes that a test instead of a lost afternoon.

    The opponent name comes off the leaderboard and is free text, so its commas are replaced rather
    than quoted: a shifted column is read by INDEX downstream and mis-attributes every value after
    the gap, silently.
    """
    cells = [town, stratum, tape, str(opponent).replace(",", " "), band, rank, arm,
             seed, ours, theirs, weed]
    assert len(cells) == len(ROW_FIELDS), (
        f"{len(cells)} values for {len(ROW_FIELDS)} named columns")
    cells += [drains.get(p, 0) for p in sorted(DRAIN_KEYS)]
    return ",".join(str(c) for c in cells) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--towns", type=int, default=48)
    ap.add_argument("--arms", nargs="+",
                    default=["control", "carrot2_d25d27", "carrot_d25d26d27_all",
                             "tomato1", "decarrotall"])
    ap.add_argument("--seeds", type=int, nargs="+", default=[11],
                    help="the town is explicit, so the seed moves weed rolls and market noise only")
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--town-seed", type=int, default=20260821)
    ap.add_argument("--opponents", nargs="+", default=None,
                    help="subset of the ranked pool; MIRROR is always added")
    ap.add_argument("--stratified", action="store_true",
                    help="force a third yarn-early (arms q4) and a third carrot-rich")
    args = ap.parse_args()

    bands = load_bands()
    all_arms = S.build_arms()
    bad = [a for a in args.arms if a not in all_arms]
    if bad:
        ap.error("unknown arm(s) %s" % bad)
    arms = args.arms if "control" in args.arms else ["control"] + args.arms
    towns = (stratified_towns(args.towns, args.town_seed) if args.stratified
             else [(d, dv, "uniform") for d, dv in sample_towns(args.towns, args.town_seed)])
    # **Half the pool must sit under `melon_branch.OPPONENT_MELON`.** q4 needs the opponent's melon
    # under 9 AND a yarn store by d5; 13 of the 18 ranked opponents open with 12 melon tiles, which
    # is why the branch armed 0 times in 76 combinations.
    if args.opponents:
        missing = [o for o in args.opponents if o not in bands]
        if missing:
            ap.error("not in the ranked pool: %s" % missing)
        opps = list(args.opponents) + [MIRROR]
    else:
        opps = list(bands) + [MIRROR]

    print("towns      %d sampled (rng %d), shops drawn with replacement at d%s"
          % (len(towns), args.town_seed, ",d".join(map(str, S.UNLOCK_DAYS))))
    # **The bands of the opponents IN THIS RUN, not of the pool.** This counted `bands`, the whole
    # ranked pool, so a two-opponent run printed "opponents 2 = low x6, mid x6, top x6 + mirror"
    # and every line of the pool under it. The header is what gets pasted with the result, so it
    # described a run nobody had made. Same class as the `farm:0.445` win rate: a correct number
    # under a label that does not describe what was measured.
    ranked = [o for o in opps if o != MIRROR]
    byband = collections.Counter(bands[o][3] for o in ranked)
    print("opponents  %d = %s%s   (bands are Kaggle LEADERBOARD rank, not bank)"
          % (len(opps), ", ".join("%s x%d" % (b, n) for b, n in sorted(byband.items())) or "none",
             " + mirror" if MIRROR in opps else ""))
    for o in sorted(ranked, key=lambda k: bands[k][4]):
        print("             %-28s rank %4d  %7.1f  melon@d3 %2s  %s"
              % (o[:28], bands[o][4], bands[o][5], bands[o][2], bands[o][3]))
    print("arms       %s" % " ".join(arms))
    print("seeds      %s" % " ".join(map(str, args.seeds)))
    print("seasons    %d   jobs %d\n"
          % (len(towns) * len(opps) * len(arms) * len(args.seeds), args.jobs))

    jobs = []
    for ti, (draw, _dv, _st) in enumerate(towns):
        for o in opps:
            spec = MIRROR if o == MIRROR else _thin_or_replay(o, bands)
            for a in arms:
                for sd in args.seeds:
                    jobs.append((ti, draw, o, spec, a, all_arms[a], sd, args.weeds))

    # **Every season written out raw, AS IT LANDS.** Re-banding, re-conditioning and re-plotting
    # must never cost another 4,560 games -- which is exactly what the leaderboard-rank correction
    # did cost the first time round, because the previous version printed aggregates and kept
    # nothing. Every season, not just the last per key: the tables collapse seeds, the CSV must not.
    #
    # **The header goes down before the pool starts and every row is flushed on arrival.** Until
    # 2026-08-22 this block opened the file after the last season, so a run that was interrupted
    # wrote nothing at all. Measured that morning: `big_carrot` (8,448 seasons) and `carrot_seeds`
    # (21,120) each ran over an hour, were killed when the box was taken for the tape shootout, and
    # produced logs containing only their own headers -- 29,568 planned seasons, zero rows. The same
    # end-of-run write also hid a `TypeError` in `rows_line` (11 format specifiers, 12 arguments)
    # behind the entire run, so any sweep of any length ended in a traceback and no CSV.
    #
    # Rows now arrive in completion order rather than sorted -- `imap_unordered` -- which is fine
    # for every consumer, since all of them key on the columns rather than the line number.
    raw = pathlib.Path(os.environ.get("GRID_ROWS",
                                  REPO / "data/logs/town_arm_grid_rows_2026-08-21.csv"))
    print("raw rows -> %s  (written live, one line per season)\n" % raw, flush=True)

    got, t0 = {}, time.time()
    with open(raw, "w") as fh, multiprocessing.Pool(args.jobs) as mp:
        fh.write(rows_header())
        fh.flush()
        for k, (ti, o, a, sd, money, theirs, weed, tape) in enumerate(mp.imap_unordered(_job, jobs), 1):
            got[(ti, o, a, sd)] = (money, theirs, weed, tape)
            fh.write(rows_line(ti, towns[ti][2] if len(towns[ti]) > 2 else "uniform", tape, o,
                               band_of(o, bands), "-" if o == MIRROR else bands[o][4],
                               a, sd, money, theirs, weed, towns[ti][1]))
            fh.flush()
            if k % 200 == 0 or k == len(jobs):
                print("  %5d/%d  %5.0fs" % (k, len(jobs), time.time() - t0), flush=True)

    def dmargin(ti, o, a):
        """Mean delta-margin over every seed run for this (town, opponent, arm).

        Keyed on the seed as well, because a `got` keyed without it silently kept only the LAST
        seed and every multi-seed run would have reported a single-seed number.
        """
        v = [((got[(ti, o, a, sd)][0] - got[(ti, o, a, sd)][1])
              - (got[(ti, o, "control", sd)][0] - got[(ti, o, "control", sd)][1]))
             for sd in args.seeds
             if (ti, o, a, sd) in got and (ti, o, "control", sd) in got]
        return sum(v) / len(v) if v else None

    def won(ti, o, a):
        v = [got[(ti, o, a, sd)][0] > got[(ti, o, a, sd)][1]
             for sd in args.seeds if (ti, o, a, sd) in got]
        return (sum(v) / len(v)) > 0.5 if v else False

    print("\n\n=== 1. ARM x TOWN DRAIN BAND  (mean d margin, and win rate) ===")
    for product in ("CARROT", "TOMATO"):
        edges = [(0, 1), (2, 2), (3, 3), (4, 99)]
        print("\n  %s drain per shop-interval:" % product)
        hdr = "  %-24s" % "arm" + "".join("%16s" % ("%d-%d" % e if e[1] < 99 else "%d+" % e[0])
                                          for e in edges)
        print(hdr)
        print("  " + "-" * (len(hdr) - 2))
        for a in arms:
            cells = []
            for lo, hi in edges:
                idx = [ti for ti, t in enumerate(towns) if lo <= t[1].get(product, 0) <= hi]
                vals = [dmargin(ti, o, a) for ti in idx for o in opps]
                vals = [v for v in vals if v is not None]
                wins = [won(ti, o, a) for ti in idx for o in opps
                    if any((ti, o, a, sd) in got for sd in args.seeds)]
                cells.append("%+8.0f %3d%%" % (sum(vals) / len(vals),
                                               100 * sum(wins) / len(wins)) if vals else "%16s" % "-")
            print("  %-24s" % a + "".join("%16s" % c for c in cells))

    print("\n\n=== 2. ARM x OPPONENT BAND  (mean d margin, and win rate) ===")
    # Band names follow `opponent_pool_ranked.json`: leaderboard rank, not bank.
    order = ["top", "mid", "low", "mirror"]
    hdr = "  %-24s" % "arm" + "".join("%16s" % b for b in order)
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for a in arms:
        cells = []
        for b in order:
            names = [o for o in opps if band_of(o, bands) == b]
            vals = [dmargin(ti, o, a) for ti in range(len(towns)) for o in names]
            vals = [v for v in vals if v is not None]
            wins = [won(ti, o, a) for ti in range(len(towns)) for o in names
                    if any((ti, o, a, sd) in got for sd in args.seeds)]
            cells.append("%+8.0f %3d%%" % (sum(vals) / len(vals),
                                           100 * sum(wins) / len(wins)) if vals else "-")
        print("  %-24s" % a + "".join("%16s" % c for c in cells))

    print("\n\n=== 3. BEST AND WORST TOWNS PER ARM  (mean d margin over all %d opponents) ==="
          % len(opps))
    for a in arms:
        if a == "control":
            continue
        rows = []
        for ti, (draw, dv, _st) in enumerate(towns):
            vals = [dmargin(ti, o, a) for o in opps]
            vals = [v for v in vals if v is not None]
            if vals:
                rows.append((sum(vals) / len(vals), ti, dv))
        rows.sort(reverse=True)
        print("\n  %s" % a)
        for tag, sl in (("BEST ", rows[:6]), ("WORST", rows[-6:])):
            for v, ti, dv in sl:
                top = " ".join("%s%d" % (p[:2], dv[p]) for p in
                               sorted(dv, key=lambda k: -dv[k])[:6])
                print("    %s town%-3d %+9.0f   %s" % (tag, ti, v, top))


if __name__ == "__main__":
    main()
