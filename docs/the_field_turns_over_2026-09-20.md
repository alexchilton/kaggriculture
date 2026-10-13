# The field turns over, and one 120-line layer survives

2026-09-20.
Eight new notebooks landed between 2026-09-19 08:00 and 2026-09-20 04:06.
Our ratings slid overnight: `v94_rc` 2879.3 to 2755.2, `v94` 2721.0 to 2660.4.
Board position does not decide the medal, because the competition re-runs every entrant from scratch at the close, but it does say the meta moved.

All head-to-head numbers below are paired direct mirrors: fresh module import per game, both seats, 40 seeds x 2 = 80 games, `kaggle_environments` 1.32.7, entry point resolved by Kaggle's own rule.
Instrument `data/logs/mirror_all.py`.
Margin is challenger minus incumbent.

## 1. "The 2950 Peak Farm" is Dmitrii Gluzdov's layer, and its headline is false

`haideptry/the-2950-peak-farm`, published 2026-09-20 02:14.
A pure 120-line append to v94 - the 2945 Farm file is untouched above it - credited in its own source to "Dmitrii Gluzdov, 2026, Apache-2.0".
`submission/f2950/main.py`, 5,880 lines, sha256 `d5460fc2e5488e0a...`.

Its own table claims **+$1,045 at 100.0% win rate** against V50, against Tetsutani, and against the 2945 base.
The same margin against three different architectures cannot be a differential result, and it is not: that number is its own extra day-2 cash.

| build | vs | n | wins | median | t |
|---|---|---:|---:|---:|---:|
| `f2950` as published | `v94_rc` | 80 | 35 | -35 | -3.06 |
| `f2950_rc` = plus `room_guard`+`clamp_sells` | `v94_rc` | 80 | 77 | +50 | 1.65 |
| `f2950_tom` = `_ALT_MODE='TomatoInsteadOfCow'` | `v94_rc` | 80 | 0 | -3,819 | -18.98 |
| `f2950_orig` = `_ALT_MODE='Original'` | `v94` | 40 | 2 (36 ties) | 0 | 0.00 |

The published build loses.
It ships `room_guard: False, clamp_sells: False` - the fifth chassis in a row to leave those two off.
Turn them on, which isolates the opening layer, and it wins 77 of 80.

The mechanism: it rewrites the first 96 steps of the route tape so the two hands that sit `PASS` on days 0 and 2 plant, water and harvest a wheat micro-cycle on tile (2,4), the tile that later becomes the cow pasture, then rebuild the pasture in time for the cow at callback 95.
It also sets `CT_TABLE={}`.
That table is v94's opponent-fingerprint lookup, keyed on `(round(rival['money'],3), market inventory WHEAT)` at line 4088; changing the opening changes the fingerprint, so those entries could never match again and clearing them is consistent rather than arbitrary.

The `f2950_orig` row is the harness check: the mode switch restores v94 exactly, 36 ties of 40 and a mean of $0, so the layer is the only thing under measurement.

### The +$50 is deterministic

Held-out block, seeds 101-140, which chose nothing:

    f2950rc_heldout   n=40   40 wins   0 losses   mean +50   median +50   t=nan

Every game is won, and every game is won by exactly $50.
The t statistic is undefined because the variance is zero.
On banks near 100,000 that is 0.05%, and it would be nothing on a cash metric - but the ladder scores match outcomes, so a deterministic +$50 against a sibling is a guaranteed win, and the field is now largely v94 forks.

## 2. The tomato hole is closed

Tschinkel documents going 0-36 against seven of the top-10 teams, leading to day 10 and losing after day 11, with the hole in tomatoes: rivals buy about 9 seeds from day 12 and sell 71 at $114 where v9/4 sells 7 at $316.
He reports three failed attempts, all labour-bound.

The 2950 farm ships a `TomatoInsteadOfCow` mode that buys one cow instead of two and plants a tomato on the freed pasture site, with watering and harvest micro-managed from the wrapper.

**It loses 80 of 80 at a median of -3,819, t=-18.98.**

That is the cheapest definitive negative of the week.
Trading a cow for a tomato plant does not open the tomato line, it costs about $3,800 a game.
Nobody needs to try this again.

## 3. V49 and V50

V49 measured 2026-09-19: -1,830 median against `v94_rc` and -1,796 against plain v94 over 80 games each, t about -7.3 both ways.
The two being within 34 of each other is the point - the flags are not what beats it, v94 is simply ahead.

V50 is V49 plus two layers, and it is world-conditional.
Against a V49 copy its author reports 15/5/76 on 48 general worlds and 80/0/0 at +2,526 on 40 yarn worlds, from committing the six-sheep expansion on day 11 instead of 12 when two of the three shops known on day 11 are yarn stores.
V49's deficit is too large for a yarn-world-only gain to close, so V50 was not pursued.

## 4. The arena dataset, and what it is actually good for

`destbreso/kaggriculture-donor-agents-20260902`, 28 MB, refreshed 2026-09-20 02:54, now in `data/arena/`.
83 community agents already extracted as `.py`, `arena.py`, `worlds.json`, a population weight file, a finished 15,872-game run in `examples/`, and the `kagsim` C++ engine as source.

**The engine is not the win, and the README says so plainly.**
A game costs 0.73 ms of engine, 32 ms of observation building, and 200 to 1,800 ms of one agent thinking.
A pairing of two large agents is about 1.6 seconds of Python against under a millisecond of simulator, so **a faster engine buys about two percent**.
It builds in 7 seconds and reports `ENGINE_VERSION = 1.32.7`; installed, and worth the 2%, but it does not change what is measurable.
There is also no replay shortcut: probed against two very different rivals, 80 of 83 agents changed their action stream.

What the dataset is worth is the **field**: 85 agents in 57 behaviour families, one representative per family being the honest unit, both seats, and a population weight applied at the end because a panel is not a ladder.

### Our builds against 43 agents from the week of 2026-09-13

8 worlds, both seats, 672 games per challenger:

| agent | games | win% | median margin | mean margin | median bank | weighted win% |
|---|---:|---:|---:|---:|---:|---:|
| `V94RC` | 672 | 88.1% | 4,124 | 16,218 | 92,082 | **89.8%** |
| `F2950` | 672 | 88.4% | 4,006 | 9,262 | 86,812 | 86.4% |
| `V94` | 672 | 83.6% | 3,965 | 9,037 | 87,351 | 85.0% |

`F2950` leads on raw win rate by 0.3 points and loses on the weighting by 3.4, and the author is explicit that when the two orderings disagree the raw one is the one to distrust.

**This is the first hard evidence for the two flags.** `V94RC` 89.8% against `V94` 85.0% is a 4.8 point gap on a 43-agent field.
The paired sibling mirror only ever got the same comparison to +78 median at t=2.66, inside the documented +-90 to +-100 noise floor.
A sibling mirror cannot see a 5-point effect against a population; that is not a failure of the statistic, it is the wrong question.

### Two rows that validate the harness, and one that cannot be read

    thomastschinkel-2945-farm-96-top-10   vs V94     8 games  0W 0L  8 TIES  margin 0
    dmitriigluzdov-a-smaller-market-shock vs F2950   8 games  0W 0L  8 TIES  margin 0

Eight ties at exactly zero margin means the same agent.
The first confirms `V94` is the 2945 Farm and the loader is picking up the right callable.
The second is how we know the 2950 Peak Farm is Gluzdov's "A Smaller Market Shock" republished.

    dmitriigluzdov-a-smaller-market-shock vs V94     8W 0L  median  +50
    dmitriigluzdov-a-smaller-market-shock vs V94RC   3W 5L  median  -51

Independent corroboration of the +-50: Gluzdov's layer is worth about +$50 against plain v94, and the flags flip the sign.
Two different harnesses, the same magnitude.

**And a row that must not be read.** V49 and V50 both show 50.0%, which contradicts the -1,830 above.
The matrix shows why: exactly 4W/4L in all six cells, with seat 0 and seat 1 returning *identical* medians.
Identical across seats is impossible for an agent that reacts, since the market settles slot by slot with player 0 first.
Those agents are replaying a tape, so the outcome is a pure function of the shop world, and `--worlds 8` at one seed per world makes each cell eight deterministic samples.
Neither number is wrong; they measure different populations, and the arena's per-opponent cells at 8 worlds are far too thin to read.
Use 16 or 64 worlds for any per-opponent claim.

Their extraction of the 2945 Farm hashes to `4f3ca95d...`, which is the digest this project got before finding the missing trailing newline; ours, `bfee70e9...`, matches Tschinkel's own declared value.
Their arena copy is one byte short of what he submits. Behaviourally identical, but worth knowing before comparing digests.

`arena.py` also reports **5 agents whose entry point is not called `agent`** - v47, v48, alperen's first-in-line, rayk's topmeta consensus route and one more - and states the loading rule as a trap in its own docstring.
Third independent confirmation this week.

## 5. State

Live and active: `56347926` v94 at 2660.4, `56347920` v94_rc at 2755.2.
`v94_rc` remains the best build measured here, on both instruments.

`f2950_rc` is a candidate: a deterministic +$50 a game over `v94_rc`, 40/40 on a held-out block with zero variance.
Outstanding before it goes near a slot: `f2950_rc` against the field at 16 worlds, paired with `v94_rc` in one run.
`f2950` without the flags placed *behind* `v94_rc` on the weighting, so a build that beats its sibling and loses ground against the population is the specific trap being checked for.

Builds added today, each verified to compile and diffed against its parent:
`submission/f2950/` (extracted, sha verified), `submission/f2950_rc/`, `submission/f2950_tom/`, `submission/f2950_orig/`.

Logs: `data/logs/mirror_2950_v94rc.log`, `mirror_2950rc_v94rc.log`, `mirror_2950tom_v94rc.log`, `mirror_2950orig_v94.log`, `f2950rc_heldout.log`, `arena_v94.log`, `arena_matrix.csv`, `arena_games.csv`, `kagsim_build.log`.

## 6. What is left

`arena.py --probe` to find which agents ignore their rival, and `--random 12` twice as the control for a chosen panel.
Both are cheap and neither has been run.

The `V9_RACE_*` and `V9_HERD_*` constants on v94, still unswept, still the lowest-value avenue.

Not attempted: the tomato line by any route other than the one measured above.

---

# Addendum, same day, 18:00: V53 supersedes all of the above

`ahmedberatozer/kaggriculture-v53-opening-signature`, published 2026-09-20 14:00, six hours after the morning's work went live.
V51 and V52 are not in the public listing, so this is a larger jump than V50.
Extracted to `submission/v53/main.py`, 6,502 lines, sha256 `20fe549dd4573b9fd1dfb32a1782c205fa74f0edfdfd6cbe935079533e0a9d0e`, matching his declaration.
Entry point `_e363_agent`, asserted in his own notebook and confirmed by our loader.

## It beats everything we had

| matchup | seeds | n | wins | median | t |
|---|---|---:|---:|---:|---:|
| V53 vs `f2950_rc` (live) | 1-40 | 80 | 67 | +879 | 6.95 |
| V53 vs `v94_rc` (live) | 1-40 | 80 | 67 | +965 | 7.44 |
| V53 vs `f2950_rc` | 101-140 | 80 | 60 | +447 | 6.89 |

About +900 cash a game against both of the morning's slots.
The whole of this document above it - the +$50 Gluzdov layer, 155 wins of 160, 95.6% weighted - was superseded within six hours by someone else's release.
The measurement was right; it was just small.

## The two mods transfer, and one was predicted

V53 ships `room_guard: False, clamp_sells: False` at line 948.
Sixth consecutive chassis. The switches have now measured positive on every one: +379, +432, +78, +505, +50, and here +23 median at t=4.71 over 80 games.

`_ADV_LOOK=3` at line 3539, with **one** call site, `for off in range(1,_ADV_LOOK+1)`.
V53 has dropped the `_e346_funded` guard that consumed the same value in V49, so the dual-purpose damping that held V49's gain to +173 does not apply and this is the V48 situation, where 3 to 22 measured +735.
Predicted the V48 magnitude before running it. Measured **+676 median, 80 wins of 80, t=15.60**.
First time this week a claim about a constant was made ahead of the data and survived.

| build | vs | seeds | n | wins | median | t |
|---|---|---|---:|---:|---:|---:|
| `v53_rc` (flags) | `v53` | 1-40 | 80 | 49 | +23 | 4.71 |
| `v53_look22` (horizon) | `v53` | 1-40 | 80 | 80 | +676 | 15.60 |
| `v53_rcl` (both) | `v53` | 1-40 | 80 | 78 | +808 | 15.97 |
| `v53_rcl` | `v53` | 101-140 | 80 | 75 | +372 | 10.86 |

The held-out block gives back 54% of the discovery margin.
Still t=10.86, but the first block flattered it, and both numbers belong in the record.

## The finding that matters most today: non-transitivity

On the same held-out seeds against the same third-party opponent:

    unmodified V53 vs f2950_rc   60/80 (75.0%)  median +447  mean +823  t=6.89
    v53_rcl        vs f2950_rc   46/80 (57.5%)  median +666  mean +604  t=5.14

while `v53_rcl` beats `v53` 75/80 head to head.
A beats B, and B beats C more reliably than A beats C.

`clamp_sells` and a longer sale horizon change *how* the agent trades, and that interacts with whoever is quoting on the other side of the market.
**A sibling mirror will rank two builds at t above 10 and point at the wrong one.**
Acting on the head-to-head alone would have put the weaker file in the slot.

## The field settles it, and reverses it back

destbreso's arena, 43 agents published 2026-09-13 to 2026-09-20, 16 shop worlds, both seats, 1,344 games per challenger, all three in one paired run, population weighted:

| agent | games | win% | median margin | mean margin | median bank | weighted win% |
|---|---:|---:|---:|---:|---:|---:|
| `V53RCL` | 1344 | 97.2% | 3,102 | 11,975 | 91,545 | **97.4%** |
| `V53` | 1344 | 96.4% | 3,571 | 10,597 | 88,806 | 97.1% |
| `F2950RC` | 1344 | 94.6% | 3,511 | 8,794 | 87,119 | 95.6% |

Against the field the stack wins more games *and* banks more, so the head-to-head reversal does not carry.

**Instrument check:** `F2950RC` returned exactly 94.6% raw and 95.6% weighted in two independent arena runs hours apart.
The harness is reproducible, which is why its answer was taken over the mirror's.

Also worth recording: the arena's throughput estimate is misleading early.
It opened at 4.6 games/s and settled at 1.1/s once it reached the pairs involving the large agents, so a 4,032-game run is about an hour, not the fifteen minutes the early rate implies.

## Submitted 2026-09-20 17:55 and 17:56

`56403045` `v53_rcl` - V53 with two lines changed, flags on and `_ADV_LOOK=22`.
`56403055` `v53` - unmodified, byte-identical to his declared hash.
Both active; `v94_rc` froze at 2452.0 and `f2950_rc` at 2667.5.
Running both so the ladder judges the two-line difference on an identical chassis, since 97.4 against 97.1 is inside what one rating can resolve.
1 submission remaining today.

Ahmed shipped V49, V50 and V53 inside two days.
Expect a V54 before Wednesday.
