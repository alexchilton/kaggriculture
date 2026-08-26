"""Sweep the handover day per arm, over SHOP SYSTEMS rather than seeds.

Alex, 2026-08-26: *"i want you to sweep over a few shops - you have that possibility now - not seeds
shop types"*, following *"and we need the planner really from d12??? or can it be later??"*

**A seed does not choose the arm.** Measured the same day: seed 700 played `starter` vs `starter`
unlocks BRUNCH_SPOT at d3 and BAKERY at d6 (arm `open`), and the same seed played by our agent
against `starter` unlocks PET_CAFE at d3 and YARN_STORE at d6 (arm `yarn6`). The shop draw moves
with the game, so no seed -> arm table exists and sweeping seeds cannot target an arm.

Injecting a RECORDED shop schedule does target it, exactly as `scripts/how_far_does_a_bare_tape_hold.py`
does: each turn, `town["unlocked_shops"]` is overwritten with what that recording had unlocked. The
draw is then a real ladder draw rather than a synthetic one, and the arm is whatever the latch reads
off it -- the shipped rule, not a shortcut past it.

The handover day is moved WITHOUT rebuilding: the bundle's `_OPENINGS[arm]` is truncated to
`stop * 24` turns and `_ARM_STOP[arm]` set to match, which is precisely what a rebuild at that stop
day would emit. One process per row would cost a build each; this costs a slice.

    ours        our bank at the end of the season
    arm         which arm the injected draw latched -- printed, never assumed

**`starter` is the opponent and it is a WEAK one**: it sells almost nothing, so the market is never
contested and every absolute number here reads roughly 2x a real game. That is tolerable for a
comparison ACROSS stop days on one draw, which is what this measures, and it is not a quality
number. Ranking two agents on it would be the mistake this project has recorded since day one.
"""

import argparse
import collections
import importlib.util
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
#: Recorded shop draws to borrow, by the day YARN_STORE lands: d3, d6, d12, d15.
#: `(recording, the author's team name)` -- the team is needed to seat the tape, and taking
#: `TeamNames[0]` instead would seat the OPPONENT on two of these four.
DRAWS = {
    "yarn_d3": ("data/seed_scripts/clone_yarn3/98889302.json", "WeAreFarmers"),
    "yarn_d6": ("data/seed_scripts/clone_yarn6/98857364.json", "Bharath Varma"),
    "yarn_d12": ("data/seed_scripts/clone_late/98898511.json", "G!vIOne"),
    "yarn_d15": ("data/seed_scripts/clone_open/98907591.json", "UjjwalPardeshi"),
}

#: The tape each ARM replays. **The reference is the tape we would actually play on that draw, not
#: the recording the draw was borrowed from.** On `yarn_d12` the latch reads no yarn at d3 or d6 and
#: picks `open`, so the tape being cloned there is `clone_open` -- comparing against `clone_late`
#: would measure a tape this agent never replays on any draw.
ARM_TAPES = {
    "yarn3": ("data/seed_scripts/clone_yarn3/98889302.json", "WeAreFarmers"),
    "yarn6": ("data/seed_scripts/clone_yarn6/98857364.json", "Bharath Varma"),
    "open": ("data/seed_scripts/clone_open/98907591.json", "UjjwalPardeshi"),
}


def arm_for(shops):
    """The shipped latch rule, applied to an injected shop schedule: yarn at d3, at d6, or neither."""
    at = lambda d: set(shops(d * TPD) or ())                                   # noqa: E731
    if "YARN_STORE" in at(3):
        return "yarn3"
    if "YARN_STORE" in at(6):
        return "yarn6"
    return "open"


def yarn_day(shops):
    """The day YARN_STORE first appears, or None. Shops unlock on a 3-day cadence from d3."""
    for d in range(3, 30, 3):
        if "YARN_STORE" in set(shops(d * TPD) or ()):
            return d
    return None


def signature(shops):
    """The shop DRAW as a comparable key: the unlock order over the season.

    Two recordings with the same order are the same shop system for our purposes, and sweeping both
    would cost a season each to re-measure one draw. This is what makes "all the shops" a set of
    distinct draws rather than a list of files.
    """
    seen, order = set(), []
    for d in range(3, 30, 3):
        for s in sorted(set(shops(d * TPD) or ())):
            if s not in seen:
                seen.add(s)
                order.append(s)
    return tuple(order)


def discover(root, limit, per_class=0):
    """`{name: (path, team)}` -- recordings sampled by YARN DAY, which is what the latch reads.

    **Deduplicating on the full unlock order collapses nothing**: all 120 recordings in
    `daily_2026-08-26` have a distinct order, so `signature` returns 120 groups and a sweep over
    "every distinct shop system" is 120 draws. Measured 2026-08-26.

    The latch does not read the order. It reads whether YARN_STORE has arrived by d3 or d6, and the
    stop table splits `open` further on whether it arrives by d12. That leaves nine classes, sized:

        d3 21   d6 12   d9 9   d12 9   d15 15   d18 7   d21 8   d24 4   never 35

    So `per_class` samples N draws from each, which measures the quantity the table is keyed on and
    averages out the single-draw noise that made two `open` draws point opposite ways.
    """
    import scripts.breakdown as B

    out, seen = {}, set()
    taken = collections.Counter()
    for f in sorted(pathlib.Path(root).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            rep = json.loads(f.read_text())
            team = (rep.get("info") or {}).get("TeamNames", [None])[0]
            shops = B.recorded_shops(str(f))
        except Exception:                                                      # noqa: BLE001
            continue
        sig = signature(shops)
        if not sig or sig in seen:
            continue
        seen.add(sig)
        if per_class:
            k = yarn_day(shops)
            if taken[k] >= per_class:
                continue
            taken[k] += 1
        y = yarn_day(shops)
        # **The yarn day is not a unique name.** Several draws share one, and keying on it alone
        # silently overwrote them -- ten distinct shop systems collapsing to four rows would read as
        # "there are only four draws". The stem disambiguates; the yarn day stays in the label
        # because it is what the latch reads.
        base = f"yarn_d{y}" if y else "yarn_none"
        out[f"{base}_{f.stem[-4:]}"] = (str(f), team)
        if len(out) >= limit:
            break
    return out


def load(path):
    spec = importlib.util.spec_from_file_location("arm_bundle", pathlib.Path(path).resolve())
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="submission/main_perarm.py")
    ap.add_argument("--stops", default="12,16,20,24,28")
    ap.add_argument("--draws", default=",".join(DRAWS))
    ap.add_argument("--draw-dir", default=None,
                    help="sweep every DISTINCT shop draw found under this directory instead")
    ap.add_argument("--max-draws", type=int, default=12)
    ap.add_argument("--per-class", type=int, default=0,
                    help="sample N draws from each YARN-DAY class instead of the first N files")
    ap.add_argument("--seed", type=int, default=123641874)
    ap.add_argument("--csv", default="data/logs/handover_sweep.csv")
    args = ap.parse_args()

    from kaggle_environments import make
    import scripts.breakdown as B

    stops = [int(s) for s in args.stops.split(",")]
    if args.draw_dir:
        DRAWS.clear()
        DRAWS.update(discover(args.draw_dir, args.max_draws, args.per_class))
        print(f"{len(DRAWS)} distinct shop draws under {args.draw_dir}\n")
    names = [d for d in (DRAWS if args.draw_dir else args.draws.split(",")) if d in DRAWS]

    csv = pathlib.Path(args.csv)
    csv.parent.mkdir(parents=True, exist_ok=True)
    # Header before the pool, one flush per row: a sweep that writes only at the end loses
    # everything when it is killed.
    fh = csv.open("w")
    fh.write("draw,arm,stop,ours\n")
    fh.flush()

    def season(path, team, shops, economy, play0):
        """One full season on an injected shop draw. `play0` drives our seat; the tape drives theirs."""
        env = make("kaggriculture", configuration=dict(economy, seed=args.seed), debug=False)
        env.reset(2)
        opp = B.tape_policy(path, team, 0)
        for t in range(719):
            env.state[0].observation.town["unlocked_shops"] = list(shops(t))
            env.state[1].observation.town["unlocked_shops"] = list(shops(t))
            env.step([play0(env.state[0].observation, t), opp(env.state[1].observation, t)])
        return float(env.state[0].observation["farms"][0]["money"])

    head = "".join(f"{'d' + str(s):>12}" for s in stops)
    print(f"{'draw':<10}{'arm':<8}{'TAPE':>12}{head}   best")
    try:
        for name in names:
            rel, team = DRAWS[name]
            # `rel` is repo-relative for the hand-listed draws and already a path for discovered
            # ones; `REPO / absolute` returns the absolute path unchanged, so this handles both.
            path = str(REPO / rel)
            economy = B.env_config(path)
            shops = B.recorded_shops(path)

            # **The ARM's tape, all thirty days, same draw and same opponent.** This is the
            # reference the handover is judged against: our engine has to be worth more than the
            # tape days it replaces, not merely positive.
            arm_rel, arm_team = ARM_TAPES[arm_for(shops)]
            tape_only = B.tape_policy(str(REPO / arm_rel), arm_team, 0)
            tape_money = season(path, team, shops, economy, lambda o, t: tape_only(o, t))
            fh.write(f"{name},tape,30,{tape_money:.0f}\n")
            fh.flush()

            row, arm_seen = {}, "?"
            for stop in stops:
                m = load(args.agent)
                full = dict(m._OPENINGS)
                # Truncate every arm to this stop day; `_ARM_STOP` feeds `start_day`, so it has to
                # move with the opening or the planner catches up from the wrong day.
                m._OPENINGS = {a: op[:stop * TPD] for a, op in full.items()}
                m._ARM_STOP = {a: min(stop, v) for a, v in m._ARM_STOP.items()}
                ours = season(path, team, shops, economy,
                              lambda o, _t, _m=m: _m.agent(o, None))
                arm_seen = m._ARM.get(0, "?")
                row[stop] = ours
                fh.write(f"{name},{arm_seen},{stop},{ours:.0f}\n")
                fh.flush()
            best = max(row, key=row.get) if row else 0
            print(f"{name:<10}{arm_seen:<8}{tape_money:>12,.0f}"
                  + "".join(f"{row.get(s, 0):>12,.0f}" for s in stops)
                  + f"   d{best} {row.get(best, 0) - tape_money:+,.0f} vs tape", flush=True)
    finally:
        fh.close()
    print(f"\nrows written to {csv}")


if __name__ == "__main__":
    main()
