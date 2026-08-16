"""Score カワシギ's decision points as SELECTORS, by playing his recorded tapes on our seat.

## The question

He is #1. The belief under test is that his season is a fixed tape plus a small number of binary
decisions taken on what the board shows him. This script tests one decision at a time, with our own
planner removed from the measurement entirely: every arm is a RECORDED TAPE on our seat.

Three arms per decision point, and **the arm under test is the third one**:

    always-A    play branch A's tape for the whole season
    always-B    play branch B's tape for the whole season
    selector    play A up to the decision turn, then switch to B if the rule fires

A rule that separates his 51 games perfectly and does not beat `max(always-A, always-B)` is worth
nothing. The separation table is a hypothesis, not a result; it has already been reported in this
project as though it were one. Only the `selector` row answers the question.

## The two decision points

    dp1  melon vs strawberry, decided at d3
         rule: opponent has >= DP1_MELON_TILES melon tiles at dawn of d3  ->  play the
         strawberry-heavy branch, else the melon-heavy one.
         Both branches are chosen by `--classify` from his games in
         `data/seed_scripts/downloads_2026-08-13/`, by counting his own PLANT emissions.

    dp2  three quadrants vs four, decided at d6, applied at d9
         rule: YARN_STORE unlocked by the end of d6  ->  play the four-quadrant tape from d9.
         three-quadrant: data/seed_scripts/kawashigi/92498144.json
         four-quadrant:  data/seed_scripts/downloads_2026-08-13/91907974.json

## Method, and the traps it is built around

- **Both seats.** `_process_market` walks player 0 then player 1 per unit, so a tape moved to the
  other seat loses price priority. Identical policies do not draw; they play different boards.
- **`weedSpawnChance` 0.005**, the ladder value. Several scripts in this tree default it to 0.0 and
  that is a different game.
- **One OS process per game.** The first run in a process differs from later ones, so every game is
  a `--child` subprocess. Same shape as `scripts/close_package_ablation.py`.
- **The opponent is a FROZEN BUILT BUNDLE**, `data/sweep/frozen_1186_opponent.py`, loaded by path.
  It carries its own copies of every module, so it cannot share dials with the arm under test. Never
  use another arm as the opponent.
- **Win rate is the score.** The ladder is Elo: a $43k win and a $4k win are identical. Money is
  printed as a diagnostic column and is never the verdict. The noise floor `2*sqrt(0.25/n)` is
  printed beside every result and anything inside it is a null.
- **A tape is open-loop.** It cannot react to an opponent it never met, so every arm here plays
  handicapped. A tape arm that WINS has won despite that. A tape arm that loses proves less.
- Splicing two tapes at a turn is only exact where the two agree before it. The run prints the
  prefix agreement for each pair, so the splice can be read rather than assumed.

    python -u scripts/decision_points.py --classify
    python -u scripts/decision_points.py --seeds 24 --workers 8
"""
import argparse
import collections
import hashlib
import importlib
import importlib.util
import json
import math
import multiprocessing
import os
import pathlib
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
TEAM = "カワシギ"                      # カワシギ
DOWNLOADS = REPO / "data/seed_scripts/downloads_2026-08-13"
CLASSIFY_CACHE = REPO / "data/logs/decision_points_classify.json"

TPD = 24                                                # turns per day

#: dp1. Read at DAWN of d3, which is the day `schedule_agent` latches its own copy of this rule on
#: (`MELON_YIELD_FROM_DAY = 3`). Applied from the same turn: he buys MELON 12 on d0 in every game and
#: executes the fork on d5-d6, so nothing before d3 should differ. The run prints that agreement
#: rather than assuming it.
DP1_DECIDE_TURN = 3 * TPD
DP1_APPLY_TURN = 3 * TPD
DP1_MELON_TILES = 9

#: dp2. "Unlocked BY day 6" is read as "at any point up to the END of d6", so the decision turn is
#: the last turn of d6, not the first. Applied at d9, the first day the two plans disagree.
DP2_DECIDE_TURN = 6 * TPD + (TPD - 1)
DP2_APPLY_TURN = 9 * TPD
DP2_THREE_Q = "data/seed_scripts/kawashigi/92498144.json"
DP2_FOUR_Q = "data/seed_scripts/downloads_2026-08-13/91907974.json"

ARMS = ["dp1/always-melon", "dp1/always-straw", "dp1/selector",
        "dp2/always-3q", "dp2/always-4q", "dp2/selector"]

#: `decision point -> (branch A arm, branch B arm, the selector under test)`.
PAIRS = {"dp1": ("dp1/always-melon", "dp1/always-straw", "dp1/selector"),
         "dp2": ("dp2/always-3q", "dp2/always-4q", "dp2/selector")}

#: Arms that play branch B for the whole season. Everything else that is not a selector plays A.
ALWAYS_B = {"dp1/always-straw", "dp2/always-4q"}


# --------------------------------------------------------------------------- reading a replay

def _crop_tiles(farm, crop):
    return sum(1 for row in (farm.get("tiles") or []) for c in row
               if isinstance(c, dict) and c.get("crop") == crop)


def _obs(step, seat):
    return ((step[seat] or {}).get("observation") or {}) if seat < len(step) else {}


def scan_one(path):
    """One replay -> the facts both decision points need. `None` if カワシギ is not in it."""
    try:
        d = json.loads(pathlib.Path(path).read_text())
    except Exception:                                                       # noqa: BLE001
        return None
    # `91304798-0.json` and `-1.json` in this directory are bare step lists, not replay envelopes.
    # They carry no `info`, so there is no way to know which seat is his; skipped, not guessed.
    if not isinstance(d, dict):
        return None
    names = (d.get("info") or {}).get("TeamNames") or []
    if TEAM not in names:
        return None
    seat = names.index(TEAM)
    steps = d.get("steps") or []
    if len(steps) < 30 * TPD:
        return None

    # His own crop commitment: PLANT emissions. A PLANT is emitted once, so this is exact -- unlike
    # a market order, which our own agent re-posts every turn until it lands.
    plants = collections.Counter()
    per_day = collections.defaultdict(list)
    for t, st in enumerate(steps[1:]):
        a = (st[seat] or {}).get("action") if seat < len(st) else None
        if not a:
            continue
        per_day[t // TPD].append(json.dumps(a, sort_keys=True))
        for u in [a.get("farmer")] + list(a.get("hands") or []):
            if u and u[0] == "PLANT" and len(u) > 1:
                plants[u[1]] += 1

    # What each rule would have read on HIS board, at the turn it is read.
    o3 = _obs(steps[DP1_DECIDE_TURN], seat)
    farms3 = o3.get("farms") or []
    opp_melon_d3 = _crop_tiles(farms3[1 - seat], "MELON") if len(farms3) > 1 else None
    o6 = _obs(steps[DP2_DECIDE_TURN], seat)
    shops6 = list(((o6.get("town") or {}).get("unlocked_shops")) or [])

    # His herd and land at the end, so the COW 6 / SHEEP 8 claim is verified rather than assumed.
    olast = _obs(steps[-1], seat)
    farms_last = olast.get("farms") or []
    flast = farms_last[seat] if len(farms_last) > seat else {}
    herd = collections.Counter()
    tiles_owned = 0
    for row in (flast.get("tiles") or []):
        for c in row:
            if c == "LOCKED":
                continue
            tiles_owned += 1
            if isinstance(c, dict) and c.get("animal"):
                herd[c["animal"]] += 1

    rewards = d.get("rewards") or [0, 0]
    return dict(
        episode=pathlib.Path(path).stem, seat=seat, opponent=names[1 - seat],
        melon=plants.get("MELON", 0), straw=plants.get("STRAWBERRY", 0),
        wheat=plants.get("WHEAT", 0), plants=dict(plants),
        opp_melon_d3=opp_melon_d3, yarn_by_d6=("YARN_STORE" in shops6), shops_d6=len(shops6),
        herd=dict(herd), tiles_owned=tiles_owned,
        money=float(rewards[seat] or 0), opp_money=float(rewards[1 - seat] or 0),
        day_sig=[hashlib.md5("|".join(per_day[dd]).encode()).hexdigest()[:8]
                 for dd in sorted(per_day)],
    )


def classify(workers=8, refresh=False):
    """Every カワシギ game in the download set, split by his own melon/strawberry commitment."""
    if CLASSIFY_CACHE.exists() and not refresh:
        return json.loads(CLASSIFY_CACHE.read_text())
    files = sorted(str(p) for p in DOWNLOADS.glob("*.json"))
    print(f"scanning {len(files)} replays in {DOWNLOADS} on {workers} workers", flush=True)
    rows = []
    with multiprocessing.Pool(workers) as pool:
        for i, r in enumerate(pool.imap_unordered(scan_one, files, chunksize=1)):
            if r:
                rows.append(r)
            if (i + 1) % 10 == 0:
                print(f"  {i+1}/{len(files)} replays, {len(rows)} of them his", flush=True)
    rows.sort(key=lambda r: r["episode"])
    CLASSIFY_CACHE.parent.mkdir(parents=True, exist_ok=True)
    CLASSIFY_CACHE.write_text(json.dumps(rows, indent=1))
    return rows


def split_branches(rows):
    """Group his games by the `(melon, strawberry)` pair he actually planted."""
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["melon"], r["straw"])].append(r)
    return by


def most_typical(group):
    """The game whose per-day script agrees with the group's modal script on the most days.

    Not the richest game. Selecting the representative on money would put the branch's luckiest
    board into the arm, and the branch would then be credited with the board.
    """
    ndays = min(len(r["day_sig"]) for r in group)
    modal = [collections.Counter(r["day_sig"][d] for r in group).most_common(1)[0][0]
             for d in range(ndays)]
    def agree(r):
        return sum(1 for d in range(ndays) if r["day_sig"][d] == modal[d])

    # Ties broken on the episode name, as a STRING: one file in this directory is
    # `92441493 (1).json`, a re-download, and `int()` on that stem raises.
    best = sorted(group, key=lambda r: (-agree(r), r["episode"]))[0]
    return best, agree(best), ndays


def tape_actions(path, team):
    """The raw per-turn action list for `team`, for prefix comparison."""
    B = importlib.import_module("scripts.breakdown")
    pol = B.tape_policy(path, team, 0)
    return [json.dumps(pol(None, t), sort_keys=True) for t in range(719)]


def prefix_agreement(path_a, path_b, team, upto):
    a, b = tape_actions(path_a, team), tape_actions(path_b, team)
    same = sum(1 for t in range(upto) if a[t] == b[t])
    first = next((t for t in range(upto) if a[t] != b[t]), None)
    return same, upto, first


# --------------------------------------------------------------------------- the arms

def build_policy(arm, tape_a, tape_b, me):
    """The tape policy for one arm, on seat `me`. Every arm is a recorded tape; nothing plans.

    Returns `(policy, state)`. `state["pick"]` is `None` on a constant arm and `True`/`False` on a
    selector, so the report can print how often the rule actually fired -- a selector that never
    fires is `always-A` under a different name, and must not be read as a null result about the rule.
    """
    B = importlib.import_module("scripts.breakdown")
    # `tape_policy(replay, team, 0)` is the NAMED TEAM's own actions, whichever seat he held in the
    # recording. It is `0` on every arm here and never `me`: `me` is the seat WE sit in now.
    pol_a = B.tape_policy(tape_a, TEAM, 0)
    pol_b = B.tape_policy(tape_b, TEAM, 0)
    dp = arm.split("/")[0]
    decide = DP1_DECIDE_TURN if dp == "dp1" else DP2_DECIDE_TURN
    apply_at = DP1_APPLY_TURN if dp == "dp1" else DP2_APPLY_TURN
    state = {"pick": None}

    def rule(obs):
        if dp == "dp1":
            farms = obs.get("farms") or []
            if len(farms) < 2:
                return False
            return _crop_tiles(farms[1 - me], "MELON") >= DP1_MELON_TILES
        return "YARN_STORE" in list(((obs.get("town") or {}).get("unlocked_shops")) or [])

    if arm.endswith("selector"):
        def policy(obs, t):
            if t == decide:
                state["pick"] = bool(rule(obs))
            if t >= apply_at and state["pick"]:
                return pol_b(obs, t)
            return pol_a(obs, t)
        return policy, state

    src = pol_b if arm in ALWAYS_B else pol_a
    return src, state


def one(seed, arm, seat, opponent, tape_a, tape_b, weeds):
    """One season, in its own process. The first run in a process differs from later ones."""
    from kaggle_environments import make

    me, mine_state = build_policy(arm, tape_a, tape_b, seat)

    sp = importlib.util.spec_from_file_location("frozen_opponent", opponent)
    opp_mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(opp_mod)

    env = make("kaggriculture",
               configuration={"seed": seed, "weedSpawnChance": weeds}, debug=False)
    env.reset(2)
    for t in range(719):
        acts = [None, None]
        acts[seat] = me(env.state[seat].observation, t)
        acts[1 - seat] = opp_mod.agent(env.state[1 - seat].observation, t)
        env.step(acts)
        if env.done:
            break
    fin = env.steps[-1]
    return dict(seed=seed, arm=arm, seat=seat,
                mine=fin[seat]["reward"], theirs=fin[1 - seat]["reward"],
                picked=mine_state.get("pick"))


# --------------------------------------------------------------------------- reporting

def report(rows, arms, seeds, out_path):
    by = collections.defaultdict(dict)                  # arm -> (seed, seat) -> row
    fails = []
    for r in rows:
        if r.get("failed"):
            fails.append(r)
            continue
        by[r["arm"]][(r["seed"], r["seat"])] = r
    for f in fails:
        print(f"FAILED {f['arm']} seed {f['seed']} seat {f['seat']}\n{f['failed']}")

    print()
    print(f"{'arm':<20}{'games':>7}{'WIN':>8}{'draw':>7}{'loss':>7}"
          f"{'mean $ (diag)':>15}{'mean margin':>13}{'B fired':>9}")
    print("-" * 86)
    summary = {}
    for arm in arms:
        rs = list(by.get(arm, {}).values())
        if not rs:
            continue
        n = len(rs)
        w = sum(1 for r in rs if r["mine"] > r["theirs"]) / n
        d = sum(1 for r in rs if r["mine"] == r["theirs"]) / n
        m = statistics.mean(r["mine"] for r in rs)
        marg = statistics.mean(r["mine"] - r["theirs"] for r in rs)
        fired = [r for r in rs if r.get("picked") is not None]
        fr = (sum(1 for r in fired if r["picked"]) / len(fired)) if fired else None
        print(f"{arm:<20}{n:>7}{w:>8.1%}{d:>7.1%}{1 - w - d:>7.1%}{m:>15,.0f}{marg:>+13,.0f}"
              f"{('' if fr is None else f'{fr:.0%}'):>9}")
        summary[arm] = dict(n=n, win=w, draw=d, money=m, margin=marg, fired=fr)

    n_any = max((s["n"] for s in summary.values()), default=0)
    floor = 2 * (0.25 / n_any) ** 0.5 if n_any else float("nan")
    print(f"\nnoise floor 2*sqrt(0.25/n) at n={n_any} is {floor:.1%}. "
          f"Anything smaller than that is a NULL, not a small effect.")
    print("Money is a diagnostic column only. The ladder is Elo: a $43k win and a $4k win score "
          "the same.")

    print(f"\n{'point':<7}{'better constant':<20}{'its WIN':>9}{'selector WIN':>14}"
          f"{'delta':>9}{'paired W-L':>12}{'sign p':>9}  does the selector beat it?")
    print("-" * 112)
    verdicts = {}
    for dp, (arm_a, arm_b, arm_s) in PAIRS.items():
        if not all(x in summary for x in (arm_a, arm_b, arm_s)):
            continue
        better = arm_a if summary[arm_a]["win"] >= summary[arm_b]["win"] else arm_b
        delta = summary[arm_s]["win"] - summary[better]["win"]
        keys = set(by[arm_s]) & set(by[better])
        wins = losses = 0
        for k in keys:
            s_w = by[arm_s][k]["mine"] > by[arm_s][k]["theirs"]
            b_w = by[better][k]["mine"] > by[better][k]["theirs"]
            wins += int(s_w and not b_w)
            losses += int(b_w and not s_w)
        fr = summary[arm_s]["fired"]
        # **A selector that fires on every game, or on none, is a CONSTANT wearing a rule's name.**
        # It cannot differ from one of the two arms it is being compared with, so a delta of 0.0 here
        # is a fact about the opponent, not evidence about the rule. Said out loud, because a 0.0 in
        # this column reads exactly like a measured null.
        degenerate = fr is not None and fr in (0.0, 1.0)
        beat = ("YES" if delta > floor else
                "NO -- inside the noise floor, a null" if abs(delta) <= floor else
                "NO -- the selector is WORSE than the constant")
        if degenerate:
            beat = (f"NO -- and UNTESTED: the rule fired on {fr:.0%} of games, so the selector is "
                    f"identical to a constant")
        # Exact two-sided sign test on the DISCORDANT pairs only. Secondary to the noise floor, and
        # said so: the two arms share every seed and every seat and are byte-identical wherever the
        # rule did not fire, so an unpaired floor computed on all `n` games is the wrong yardstick
        # for them -- but a sign test on a handful of discordant pairs is not proof either.
        nd = wins + losses
        p = (min(1.0, 2 * sum(math.comb(nd, k) for k in range(wins, nd + 1)) / 2 ** nd)
             if nd else 1.0)
        print(f"{dp:<7}{better:<20}{summary[better]['win']:>9.1%}"
              f"{summary[arm_s]['win']:>14.1%}{delta:>+9.1%}{f'{wins}-{losses}':>12}"
              f"{p:>9.3f}  {beat}")
        verdicts[dp] = dict(better=better, better_win=summary[better]["win"],
                            selector_win=summary[arm_s]["win"], delta=delta,
                            paired_w=wins, paired_l=losses, sign_p=p, beats=beat,
                            fired=fr, degenerate=degenerate)

    # **The subset the rule actually touches.** A selector is identical to `always-A` on every game
    # where its rule did not fire, so a whole-set win rate DILUTES the effect by exactly the share of
    # games it never touched -- and then gets compared with a noise floor computed on the whole set.
    # The rows below are the only games where the three arms can differ at all.
    for dp, (arm_a, arm_b, arm_s) in PAIRS.items():
        if not all(x in by for x in (arm_a, arm_b, arm_s)):
            continue
        fired = {k for k, r in by[arm_s].items() if r.get("picked")}
        held = {k for k, r in by[arm_s].items() if r.get("picked") is False}
        if not fired or not held:
            continue
        print(f"\n{dp}: split by whether the rule fired. The selector plays branch A on the "
              f"'did not fire' rows,\nso it is IDENTICAL to {arm_a} there by construction; only the "
              f"'fired' rows carry information.")
        print(f"{'subset':<14}{'games':>7}{'  ':2}" + "".join(f"{x.split('/')[1]:>16}"
                                                             for x in (arm_a, arm_b, arm_s)))
        for label, keys in (("fired", fired), ("did not fire", held)):
            cells = []
            for arm in (arm_a, arm_b, arm_s):
                ks = [k for k in keys if k in by[arm]]
                w = sum(1 for k in ks if by[arm][k]["mine"] > by[arm][k]["theirs"])
                cells.append(f"{w}/{len(ks)} = {w / max(1, len(ks)):.0%}")
            print(f"{label:<14}{len(keys):>7}  " + "".join(f"{c:>16}" for c in cells))

    print("\nEvery arm is an OPEN-LOOP tape. It cannot react to an opponent it never met, so all "
          "three arms\nplay handicapped. A tape arm that WINS has won despite that handicap; a tape "
          "arm that loses\nproves less. The comparison BETWEEN arms is still fair -- the handicap "
          "is the same for all three.")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(dict(summary=summary, verdicts=verdicts,
                                        noise_floor=floor, seeds=seeds,
                                        rows=[r for r in rows if not r.get("failed")]), indent=1))
    print(f"\nwritten: {out_path}")


# --------------------------------------------------------------------------- main

def print_classification(rows):
    by = split_branches(rows)
    print(f"\n{len(rows)} カワシギ games found in {DOWNLOADS.name}\n")
    print(f"{'MELON':>7}{'STRAW':>7}{'WHEAT':>14}{'games':>7}   episodes")
    for k in sorted(by, key=lambda k: -len(by[k])):
        g = by[k]
        wh = [r["wheat"] for r in g]
        print(f"{k[0]:>7}{k[1]:>7}{f'{min(wh)}-{max(wh)}':>14}{len(g):>7}   "
              f"{' '.join(r['episode'] for r in g[:6])}{' ...' if len(g) > 6 else ''}")

    print(f"\nwhat the two rules would have read on his own boards "
          f"(dp1 threshold: opponent MELON >= {DP1_MELON_TILES} at dawn of d3):")
    print(f"{'MELON/STRAW':>13}{'games':>7}{'opp melon d3 min':>18}{'max':>6}"
          f"{'>= thr':>8}{'YARN by d6':>12}")
    for k in sorted(by, key=lambda k: -len(by[k])):
        g = [r for r in by[k] if r["opp_melon_d3"] is not None]
        if not g:
            continue
        v = [r["opp_melon_d3"] for r in g]
        fires = sum(1 for x in v if x >= DP1_MELON_TILES)
        yarn = sum(1 for r in by[k] if r["yarn_by_d6"])
        print(f"{f'{k[0]}/{k[1]}':>13}{len(g):>7}{min(v):>18}{max(v):>6}"
              f"{fires:>8}{f'{yarn}/{len(by[k])}':>12}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--weeds", type=float, default=0.005,
                    help="the LADDER value. 0.0 is a different game.")
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--arms", nargs="+", default=ARMS)
    ap.add_argument("--classify", action="store_true", help="print the branch table and stop")
    ap.add_argument("--refresh", action="store_true", help="rescan the replays")
    ap.add_argument("--out", default="data/logs/decision_points.json")
    ap.add_argument("--child", nargs=3, default=None)
    ap.add_argument("--tape-a", default=None)
    ap.add_argument("--tape-b", default=None)
    a = ap.parse_args()

    if a.child:
        print(json.dumps(one(int(a.child[0]), a.child[1], int(a.child[2]),
                             a.opponent, a.tape_a, a.tape_b, a.weeds)))
        return

    rows = classify(a.workers, a.refresh)
    print_classification(rows)

    by = split_branches(rows)
    ranked = sorted(by, key=lambda k: -len(by[k]))
    if len(ranked) < 2:
        raise SystemExit("fewer than two branches found; nothing to select between")
    a_key, b_key = sorted(ranked[:2], key=lambda k: -k[0])       # A = the melon-heavier of the two
    rep_a, agree_a, nd_a = most_typical(by[a_key])
    rep_b, agree_b, nd_b = most_typical(by[b_key])
    dp1_a = str(DOWNLOADS / f"{rep_a['episode']}.json")
    dp1_b = str(DOWNLOADS / f"{rep_b['episode']}.json")

    print(f"\ndp1 branch A (melon-heavy, MELON {a_key[0]} / STRAW {a_key[1]}, "
          f"{len(by[a_key])} games): episode {rep_a['episode']}")
    print(f"     chosen because it agrees with the class's modal day script on {agree_a}/{nd_a} "
          f"days; he sat {rep_a['seat']}, ${rep_a['money']:,.0f} vs ${rep_a['opp_money']:,.0f}, "
          f"opponent melon at d3 = {rep_a['opp_melon_d3']}")
    print(f"dp1 branch B (straw-heavy,  MELON {b_key[0]} / STRAW {b_key[1]}, "
          f"{len(by[b_key])} games): episode {rep_b['episode']}")
    print(f"     chosen because it agrees with the class's modal day script on {agree_b}/{nd_b} "
          f"days; he sat {rep_b['seat']}, ${rep_b['money']:,.0f} vs ${rep_b['opp_money']:,.0f}, "
          f"opponent melon at d3 = {rep_b['opp_melon_d3']}")

    q4 = next((r for r in rows if r["episode"] == pathlib.Path(DP2_FOUR_Q).stem), None)
    if q4:
        print(f"\ndp2 four-quadrant tape {q4['episode']}: herd {q4['herd']} (VERIFY the COW 6 / "
              f"SHEEP 8 claim against this), {q4['tiles_owned']} tiles owned at the end,")
        print(f"     he sat {q4['seat']}, ${q4['money']:,.0f} vs ${q4['opp_money']:,.0f}, "
              f"YARN_STORE by d6 = {q4['yarn_by_d6']}, crops {q4['plants']}")

    s1, n1, f1 = prefix_agreement(dp1_a, dp1_b, TEAM, DP1_APPLY_TURN)
    s2, n2, f2 = prefix_agreement(str(REPO / DP2_THREE_Q), str(REPO / DP2_FOUR_Q),
                                  TEAM, DP2_APPLY_TURN)
    print("\nsplice validity -- turns byte-identical between the two tapes BEFORE the switch:")
    print(f"  dp1  {s1}/{n1} identical, first difference at turn {f1} "
          f"(day {'-' if f1 is None else f1 // TPD})")
    print(f"  dp2  {s2}/{n2} identical, first difference at turn {f2} "
          f"(day {'-' if f2 is None else f2 // TPD})")
    print("  A low number here means the selector is a hybrid of two seasons rather than one season "
          "with a\n  fork in it, and the selector arm carries that as an EXTRA handicap the two "
          "constants do not have.")

    if a.classify:
        return

    tapes = {"dp1": (dp1_a, dp1_b),
             "dp2": (str(REPO / DP2_THREE_Q), str(REPO / DP2_FOUR_Q))}
    seeds = list(range(1, a.seeds + 1))
    jobs = [(s, arm, seat) for arm in a.arms for s in seeds for seat in (0, 1)]
    print(f"\n{len(jobs)} games = {len(a.arms)} arms x {len(seeds)} seeds x 2 seats")
    print(f"opponent {a.opponent} (frozen built bundle), weedSpawnChance {a.weeds}, "
          f"one OS process per game\n", flush=True)

    def child(job):
        s, arm, seat = job
        ta, tb = tapes[arm.split("/")[0]]
        p = subprocess.run([sys.executable, "-u", __file__, "--child", str(s), arm, str(seat),
                            "--opponent", a.opponent, "--tape-a", ta, "--tape-b", tb,
                            "--weeds", str(a.weeds)],
                           capture_output=True, text=True, cwd=REPO,
                           env={**os.environ, "PYTHONPATH": "."})
        try:
            return json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:                                                   # noqa: BLE001
            return dict(seed=s, arm=arm, seat=seat, failed=(p.stderr or p.stdout))

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        rows_out = list(ex.map(child, jobs))

    report(rows_out, a.arms, seeds, REPO / a.out)


if __name__ == "__main__":
    main()
