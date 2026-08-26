"""Seed -> arm, read from a REAL game, and then the handover sweep per arm.

Alex, 2026-08-26: *"and we need the planner really from d12??? or can it be later?"*

d12 on `yarn3`/`yarn6` is a floor I picked, not a finding. `open` is measured -- its group plays
identical actions through d27 -- and on the one seed that latched it, tape-to-d27 beat tape-to-d12
by **$12,968** ($85,245 against $72,277). The same question has never been asked of the other two
arms, because until now there was no reliable way to make a seed land on them.

**`env.reset()` DRAWS A FRESH SEED.** That is a recorded lesson in this project
(`project_kaggriculture_fix_the_seed`) and the first version of this scan walked into it: it built
the env, called `reset(2)`, stepped PASS actions and read `town["unlocked_shops"]`. It reported seed
700 as `SMOOTHIE_SHOP` at d3 and d6 -- twice, `['SMOOTHIE_SHOP', 'SMOOTHIE_SHOP']`, a duplicate that
should have been read as a broken measurement on the spot. The real game draws `PET_CAFE` at d3 and
`YARN_STORE` at d6, so seed 700 latches **yarn6**, and every builder-verification number quoted that
day was a `yarn6` measurement being described as `open`.

So the shops are read out of `env.run`'s own recorded steps. Two `starter` agents keep it cheap; the
shop schedule does not depend on what either side does.
"""

import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def arm_of(shops_by_day):
    """The same rule the bundle latches on: yarn at d3 -> yarn3, at d6 -> yarn6, else open."""
    if "YARN_STORE" in shops_by_day.get(3, ()):
        return "yarn3"
    if "YARN_STORE" in shops_by_day.get(6, ()):
        return "yarn6"
    return "open"


def shops_from_a_real_game(seed):
    """`{day: frozenset(shops)}` at hour 0 of days 3 and 6, from `env.run` -- never `env.reset`."""
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(["starter", "starter"])
    out = {}
    for step in env.steps:
        o = (step[0] or {}).get("observation") or {}
        if o.get("hour") == 0 and o.get("day") in (3, 6):
            out[int(o["day"])] = frozenset((o.get("town") or {}).get("unlocked_shops") or ())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="lo", type=int, default=700)
    ap.add_argument("--to", dest="hi", type=int, default=760)
    args = ap.parse_args()

    found = collections.defaultdict(list)
    print(f"{'seed':>7}  {'d3 shops':<34}{'d6 shops':<46}{'arm':<7}")
    for seed in range(args.lo, args.hi):
        s = shops_from_a_real_game(seed)
        arm = arm_of(s)
        found[arm].append(seed)
        print(f"{seed:>7}  {','.join(sorted(s.get(3, ()))) or '-':<34}"
              f"{','.join(sorted(s.get(6, ()))) or '-':<46}{arm:<7}", flush=True)

    print()
    for arm in ("yarn3", "yarn6", "open"):
        v = found.get(arm) or []
        print(f"  {arm:<8}{len(v):>4} seeds   {v[:10]}")


if __name__ == "__main__":
    main()
