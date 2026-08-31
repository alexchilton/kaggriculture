# Crop Dusta: 7 day-plans clone days 0-4 exactly, and his branches are a spend rule

Measured 2026-08-27. Scripts `/tmp/dusta_prefix.py`, `/tmp/dusta_lineage.py`, `/tmp/dusta_fanout.py`,
`/tmp/dusta_dt_exact.py`, `/tmp/dusta_do_they_work.py`, `/tmp/dusta_canon.py`,
`/tmp/dusta_daylevel.py`.
Logs under `data/logs/dusta_*.log`.

Corpus: **66 new-era games**, ep >= 97_600_000. See
`docs/crop_dusta_prefix_groups_are_versions_2026-08-27.md` for why the other 87 games are a
different agent; they now sit in `data/seed_scripts/_retired_dusta_oldver_2026-08-27/`.

## The result

Hashing the **per-day multiset of work ops** instead of the per-turn action stream:

```
  view                          thru d2  thru d4  thru d6  thru d9  season   (top-8 of 66)
  D0 day: all ops (multiset)        98%      88%      27%      17%     14%
  D1 day: work ops (multiset)      100%     100%      32%      17%     14%
  D2 day: work op TYPES only       100%     100%      42%      17%     14%

  per-day distinct plans (work multiset)
   day  distinct   sizes
     0         1   [66]
     1         4   [43, 19, 3, 1]
     2         3   [43, 20, 3]
     3         3   [43, 20, 3]
     4         5   [58, 4, 2, 1, 1]
     5        14   [22, 16, 13, 4, 2, 1, 1, 1]
     6        52   [5, 3, 3, 2, 2, 2, 2, 2]
```

**Seven day-plans reproduce days 0-4 for all 66 games.** Day 6 is the wall: 52 distinct plans across
66 games.

## Why the per-turn view was wrong

Alex: *"if we can ignore stupid shit that does nothing we can get a better coverage"*. Correct, and
it is worth 20 points at d5.

Canonicalising **inside the turn** does almost nothing:

```
  view                     d3h0   d5h0   d7h0  d10h0     (top-8 of 66, per-turn hash)
  L0 raw                    97%    80%    27%    15%
  L1 drop PASS              97%    80%    27%    15%
  L3 work ops only          98%    91%    27%    17%
```

Dropping PASS changes literally nothing. The divergence is not idle ops -- it is the **hour** at
which an order is posted. Two of the four "decisions" found by the exact-divergence scan have
identical day totals:

```
  d2h1 branches [38, 5]      both:  day-2 HIREs 4, BUY_SEED 4, PLANTs 4
  d3h1 branches [28, 8, 2]   all:   day-3 HIREs 4, BUY_SEED 0, PLANTs 0
```

Same four hires, posted in different hours. A per-turn hash calls that a divergence on every turn of
the day. A per-day hash calls it one plan.

## The one real branch: a spend rule at h1

Fitted at the EXACT first-divergence turn, features read from `steps[T-1]` so nothing is downstream
of the branch. (The first fit read features 2 turns late and its winning feature, `seed_WHEAT`, was
just the result of the `BUY_SEED` it was predicting. That fit is void.)

```
d1h1  t25  n=64  majority 67.2%   depth-2 LOO-CV 98.4%
    money <= 51.00              -> 3 hires, BUY_SEED WHEAT 2     (3 games,  3/3)
    51 < money <= 60.50         -> 3 hires, BUY_SEED WHEAT 3     (43,      40/43)
    money > 60.50, oppWheat<=6  -> 4 hires, BUY_SEED WHEAT 4     (13,      11/13)
    money > 60.50, oppWheat> 6  -> 3 hires, BUY_SEED WHEAT 4     (5,        3/5)

d2h1  t49  n=43  majority 88.4%   depth-1 LOO-CV 100.0%   money <= 20.50 -> 1 HIRE else 2
d3h1  t73  n=38  majority 73.7%   depth-2 LOO-CV  97.4%   money_gap <= -28 ...
```

Every branch is at **hour 1**, and every one is *how many hands can I afford*. The SELL and the
farmer op are identical across branches; only HIRE count and seed quantity move.

## His extras are used. Diment's were not.

The check Alex asked for, after Diment's opening bought 19 WHEAT at turn 1 and hired 2 hands that
PASSed all day:

```
d1h1 branch    HIREs  BUY_SEED  PLANTs     marginal hand
  n=43            3        3        3      hand3: 6 work ops
  n=13            4        4        4      hand4: 6 work ops (hands 2,3 do 3 each)
  n= 5            3        4        4      hand3: 6 work ops
  n= 3            3        2        2      hand3: 4 work ops
```

`BUY_SEED == PLANTs` in every branch on every day. No hand PASSes its whole day. Nothing here is
the dead-weight opening Diment ships.

## Why this matters for the cash bug

Hire cost is `FARM_HAND_COST_MULT * fib(hires_today)` (`reference/kaggriculture.py:698`) and
`_do_hire` fails **silently** on a thin bank (`:702`). A fixed tape replaying `HIRE, HIRE` at d2h1 on
$19 eats one silent refusal and runs a hand short for the rest of the day. Dusta sizes the order to
the bank, so it cannot happen to him.

That is the measured mechanism behind Alex's *"it doesn't happen to diment - so it is a case of
something going wrong"*.

## Proposed build

```
d0        1 plan,  all 66 games
d1        4 plans, selected at h1 by bank      LOO-CV 98.4%
d2, d3    3 plans each  [43, 20, 3]
d4        5 plans, top plan 58/66 = 88%
d5       14 plans, top 3 = 51/66 = 77%
d6+       planner
```

Not an 8-tape arm set and not a `PREFIX_GATE` cascade. One day-plan table plus an affordability rule
at h1, with the planner ordering the day's work.

## Caveats

- 66 games is not a random sample of his ladder games. The per-branch records (40/43, 11/13, ...)
  describe this archive only.
- The d1h1 tree is 98.4% LOO-CV on n=64 with four classes, two of which have 5 and 3 members. The
  two big classes are solid; the small ones are three and five games.
- The money thresholds ($51.00, $60.50, $20.50) are fitted constants. They are almost certainly
  proxies for the hire-cost ladder, and an implementation should compute affordability from
  `_hire_cost` rather than hard-code them.
- Day totals being equal does NOT prove the boards are equal -- ordering can matter for what a walk
  reaches. It is strong evidence the plans are the same, not proof.
