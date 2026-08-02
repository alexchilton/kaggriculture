# Handoff — 2026-08-02, evening

Supersedes the state sections of `HANDOFF_NEXT.md`.
Read `CLAUDE.md` first, then this.

Competition launched **2026-07-30**, deadline **2026-09-30**.
Today is **day 3 of 62**, which matters for how you read every "teacher" number below.

---

## Running right now

`league1`, systemd service `kagg-train` on the Windows box, resumed from **update 350**.
Log: `/home/alex/kagg/data/logs/run.log` — `kagg-log` follows exactly that file.

```
--curriculum-mix length:0:0.6,10:0.1,15:0.1,20:0.1,25:0.1   --curriculum-symmetric
--opponent-frac 0.45 --farm-frac 0.25 --ranch-frac 0.20 --idle-frac 0.05   (self = 0)
--pool-size 16 --pool-every 25
--hand-prior 0.05 --spend-prior 0 --kl-prior <mix5-20260802-120823/latest.pkl>
--ent-coef 0.01 --lr 3e-5 --batch 256 --horizon 32
```

Everything below is live as of this deploy. The startup line to check it took is
`day 0: $3,000` — it read `$623` before.

Resumed through a chain: `commit4` → `day0flip` → `day0flip2` → `ranch1` → `league1` → (this).

**Two launch paths exist and they are not the same one. This cost an hour.**

| path | mechanism | writes to | survives session loss |
|---|---|---|---|
| systemd unit `kagg-train` | `systemctl start kagg-train` | `data/logs/run.log` | yes |
| `/usr/local/bin/kagg-train` | tmux session `kagg` | `data/logs/train.log` | yes |

`kagg-log` reads `run.log`, so a run started the *other* way is invisible to it and looks dead.
The unit's `ExecStart` holds the full arg list including `--resume`, so **redeploying means editing
the unit and `daemon-reload`**, not passing new flags somewhere.
A hand-rolled `nohup` launch is a third way and is wrong twice over: it writes to neither log, and
`train_jax_rl.py` lives in `scripts/` so Python puts *that* directory on `sys.path` and `import
kagg` fails without `PYTHONPATH=/home/alex/kagg`.

---

## READ THIS FIRST: two bugs that made day-0 and the pool describe the wrong thing

Both are fixed and deployed (`f1130ca`). Both had the same shape as everything else in this file: a
number that was correct per row and was read as something it did not measure.

### The pool opponent changed identity every 32 turns

`opp_idx = pool.select(seed, it)` was drawn inside the **update** loop.
An episode is 719 turns; a `--horizon 32` update advances 32 of them.
So seat 1 was played by **~23 different frozen checkpoints per game**, swapping every 32 turns.

An opponent stitched from 23 checkpoints restarts its strategy 23 times a season and plays far
worse than any single member of the pool.
That is the whole explanation for `wr_pool 0.990`, and for every member's own record sitting at
0.01-0.15 — none of them had ever played a whole game, and `pool.record` credited whichever one
held the seat on the final update.

`CLAUDE.md` already names this exact failure for the per-opponent win rate ("the opponent was
re-drawn every update while a game spans ~22.5 of them").
Sticky roles fixed it for the opponent **type** and left the member identity redrawn — the same bug
survived in the same file, half fixed.

`Pool.select` now takes `hold=`, and the loop derives it from the horizon: `league.hold_updates` is
`ceil(719 / horizon)` = 23.
**Residual, stated rather than hidden:** a game straddling a window boundary still sees two
opponents, not one. Exact would need per-slot opponent parameters, and the rollout applies one
parameter set to the whole batch, so that costs either a forward pass per member or a batch-sized
copy of the params. Two-at-worst for free is the trade.

### Day 0 was somebody else's opening, not ours

`states_at_day(.., day=0)` snapshots a **recorded elite replay** at a turn drawn from
`_turn_indices(.., 0)` = turns **1..48**, median ~turn 24 — a full game-day in.
And `lo = max(1, (0 - DAY_WINDOW) * 24)` means **turn 0 was never drawn at all**.
Measured at startup, that rung began on **$623**, because by turn ~24 the recorded player had
converted ~$2,400 of its $3,000 into seed and put it in the ground.

**Symmetric seats made this fair, and fairness was never the problem.** Both sides get the same
position and whoever ends richer wins; the training signal was sound.
What was missing is **coverage**. The competition starts at turn 0 with $3,000 and bare tiles, and
**78% of slots are the day-0 rung** — so the policy was trained to *continue* an elite opening and
deployed to *make* one.

Both measurements were right and disagreed for that reason:

| | measures | reads |
|---|---|---|
| day-0 rung `wr` | continue a position, fairly | 0.59-0.72 |
| `eval_policy` from `J.reset` | make the opening yourself | $3,000 -> **$1,104** |

It also made `vs idle` unreadable at that rung: idle inherits $623, sits on it, and its unwatered
crops die — so "beat idle" meant "extract more than $0 from an inherited half-built farm", not
"turn $3,000 into more than $3,000".

Day 0 is now `J.reset`: $3,000, bare tiles, turn 0.
`mirror`, `behind` and `symmetric` are no-ops on it by construction — a pristine board is already
identical on both seats.

**Open consequence, decide deliberately.** All 200 day-0 slots now start at turn 0 together, so
they terminate together: terminal rewards may arrive in bursts every ~23 updates rather than spread
out. `J.reset` takes a `phase` argument that would stagger them, but a phased pristine board is
"day 10, empty farm" — a different and much harder state, not the opening. Not chosen either way
yet; watch whether the bursting actually hurts before acting.

### State at the first update after the deploy (351), so drift is measurable from here

```
[  351]  klP 3.119   ent 5.8 (op 0.20)   term 0   wr nan/0x   bank med $2,899   V 0.868  sum 1.736
   commit 24.29% = cWATER:4.62% cHARV:2.95% cFEED:3.01% cPLANT:3.20% cPICK:10.51%   move:56%
   buyanimal GOOSE:0.000  COW:0.000  SHEEP:0.001
   spend seed:0.021  hire:0.167  land:0.000
```

- `bank med $2,899` confirms the day-0 rung is a real start end to end.
- `klP` jumped 0.41 -> 3.119: the spend heads are now far from their new uniform prior, so the KL is
  pulling hard on exactly the heads that need to move. That is the mechanism; it needs updates.
- `seat_sum 1.736` against a target of 1.0 is the value head being wrong about a board distribution
  it has never seen. Expect it to come back; if it does not, the critic is not learning the new
  rung.
- **`term 0` and `wr nan/0x` are the burst, arriving immediately.** No terminal episodes and no win
  rates for ~23 updates, so predictions 1 and 2 below cannot be read before then. Do not conclude
  anything from `n/a`.
- Buys have **not** moved yet. One update is not evidence either way.

## WHAT TO WATCH, WITH PREDICTIONS

Written as predictions on purpose, so the next session can tell a fix from a story.
If one of these does not move, the diagnosis behind it was wrong and should be dropped rather than
explained away.

| # | watch | prediction | if it does not happen |
|---|---|---|---|
| 1 | `vs pool` | falls **hard** from 0.990 | the chimera bug was not the explanation; the 0.990 needs a different cause and the `hold=` change bought nothing |
| 2 | `wr` at day 0 | drops a long way from 0.59-0.72 | the new rung is not actually harder, so the replay-vs-reset gap was not the train/deploy mismatch it looks like |
| 3 | `spend land:` / `buyanimal` | **> 0 at all**, ever | removing the 5% shared target did not free them, so the binding constraint is not the prior — look at whether the *advantage* for buying is genuinely negative (an unfed animal is a certain loss, not a bad bet) |
| 4 | `spend seed:` and `hire:` | rise toward the leader's 7.1% and 42% | same as 3 |
| 5 | `bank med` on day-0 | starts near $3,000; direction from there is the real signal | if it collapses immediately the policy is destroying the stake in the opening, which is the thing the whole rung exists to expose |
| 6 | `commit N.NN%` vs `move:` | commit rises **while** move falls, same window | either alone is ambiguous; commit flat and move >=70% after 50 updates means the prior is not binding and the problem is credit assignment, so do **not** push the prior weight higher |
| 7 | `ent (op N.NN)` | stays off the floor | it read 0.24 nats against `ln(23) = 3.14` before the deploy — near-deterministic. Collapse here with commit share spiking is the overcorrection case, i.e. a new policy fragment |
| 8 | `terminal_ret_std` | non-zero on most updates | it was **0 on 45% of updates** before — every finished game that update had the same outcome, so no outcome signal at all |

**Signal budget, measured before the deploy, and the reason items 1 and 8 matter most.**
Bernoulli variance `p(1-p)` times share of games:

| opponent | wr | var | share | share of all signal |
|---|---|---|---|---|
| farm | 0.215 | 0.169 | 25% | 46.0% |
| ranch | 0.263 | 0.194 | 20% | 42.3% |
| idle | 0.854 | 0.125 | 5% | 6.8% |
| pool | 0.990 | 0.010 | 45% | **4.9%** |

**pool + idle were 50% of the games producing 12% of the signal.**
If item 1 lands, the pool's 45% starts paying for itself; if it does not, that 45% should be moved
to farm/ranch, which is a `--opponent-frac` change and nothing more.

**The stop-everything guard cannot see any of this.** It reads
`if games > 50 and row["ret_std"] == 0.0`, and `ret_std` is over *all* rows and sits near 0.055
because bootstrapped values vary. The variable that was actually zero on 45% of updates is
`terminal_ret_std`. Same species of bug as the rest: correct per row, watching the wrong thing.
Worth pointing the guard at `terminal_ret_std` before trusting it again.

## LATER THE SAME EVENING: three measurement bugs, and what they invalidate

All three are the same species already named in `CLAUDE.md` — a number correct per row whose label
does not describe what it is being read as.
All three now have a failing-first test in `tests/test_train_metrics.py` (22 pass).

### 1. The op census dropped every COMMIT token, from the moment they were introduced

`op_counts` one-hotted the **policy** op over `O.N_OPS`.
Policy op space is `commit.N_POLICY_OPS = O.N_OPS + 5`, and `jax.nn.one_hot` returns a zero row for
an out-of-range index rather than raising.
So tokens 18-22 — the five `COMMIT_*` macros, the entire behaviour under test — were counted as
nothing at all.

**What this invalidates.** `total_ops` normalises by the sum of the census, so every op percentage
this project has printed since commitments landed is a *share of primitive draws*, not a share of
unit-turns.
The "movement + NOOP is 79%" figure in the section below, and the 84% measured later, are both
inflated by however much commit share actually existed.
The post-commit result table below (`HARVEST 0.44% -> 6.2%` and the rest) counted **resolved
arrival ops only** and never once saw a commit draw.

Fixed by `op_census()`, which takes the width as a named argument so a test can pin it, and the
printed line now carries `commit N.NN% = cWATER: cHARV: cFEED: cPLANT: cPICK:`.

### 2. `--spend-prior` was silently inert whenever `--kl-prior` was set

When both priors are supplied the merge kept the hand prior for `op` **and discarded it for every
other head**, so all four `SPEND_HEADS` fell through to the BC prior.
A run could pass `--spend-prior 0.05`, have it echoed back in its own args line, and have it govern
nothing.
Extracted to `merge_priors()` for that reason: as an inline dict comprehension the choice was
invisible and unassertable.

Measured against the BC prior's implied P(act), which is where it matters:

| head | BC prior | measured | genuinely pinned? |
|---|---|---|---|
| `buy_land` | 0.0% | 0.000 | **yes** |
| `buy_animal` | 0.1% | 0.0002 | **yes** |
| `buy_seed` | 0.9% | 0.012 | no — already drifting above |
| `hire` | 6.3% | 0.073 | no — already above |

So only land and animals were actually held at zero, and KL taxes mass where the prior has none —
the policy was being charged for *trying* to buy land.
`HAND_PRIOR_HEADS_WITH_BC` is now `("op",) + SPEND_HEADS`.

**Why this is not the known-bad entry below re-suggested.** `--spend-prior` was rejected "as a
bankruptcy fix on an *inert* policy" when the failure was hyperactivity.
The failure has inverted again: against an inert policy a 5% shape prior is a **floor**, pulling
from below.
Third instance of "a decision to skip a fix can expire when the problem changes".

**Superseded within the hour: there is no shared spend rate, so `--spend-prior` is now `0`.**
See "The crew, and why one spend rate cannot fit four heads" below.

### 3. Logged `entropy` is summed over every head

So it cannot separate "commit share rising as intended" from "the op head collapsing onto one
commit token it now spams" — both move the total the same way.
`op_entropy` is now computed and logged separately.
It is a metric only and is not in the objective.

### Prior values changed, with the argument

- `--hand-prior` **0.15 -> 0.05**. Measured noop is 5-6%, already *below* the 0.15 target, so the
  KL was spending part of its budget pulling the policy back **up** toward more noop. Deliberately
  *not* moved toward Ender's 0.9: his 0.9 is safe because his game punishes standing still, and
  here an idle farm banks its opening money and can win outright, so a high noop prior pushes into
  the same basin the spend bug was already pushing into. Expect no direct effect on the movement
  figure — noop is 5-6 of those points, the rest is movement.
- `COMMIT_PRIOR_SHARE = 0.40` of non-noop mass when at least one commit is legal, primitives split
  the remaining 60%, unchanged when no commit is legal. **A class split, not a per-op marginal** —
  it says nothing about which commit or which primitive, so there is no strategy in it to inherit.
  Rests on `MAX_COMMIT_TURNS = 4` (one commit draw stands in for up to four primitive draws whose
  intermediate turns are excluded from the PPO density) and on legality asymmetry (movement is
  legal nearly every turn, a commit only when a target is in range) — both structural, both
  pushing the same way. 0.40 against a raw flat share of 5/23 = 21.7%; the multiplier should
  eventually come from measured realised walk length rather than assertion.

Flat-over-legal is the "mostly walk" fragment at the opposite frequency extreme to the one the
known-bad list already names: nobody wrote "prefer walking", the legality shape wrote it.
Reweighting *within* primitives to fix that would be the forbidden per-op marginal relabelled, so
the class boundary is the only place the correction belongs.

**Pass/revert, over ~50 updates.** Pass: commit share rises toward 15-25% *while* move share falls
in the same window — either alone is ambiguous.
Revert-as-no-effect: commit flat and move still >=70%, meaning the prior is not the binding
constraint and the problem is credit assignment (`ev_signal` 0.27-0.38 failing to propagate across
the four-turn delay) — do **not** respond by pushing the prior weight higher.
Revert-as-overcorrection: commit share past 40% or `op_entropy` collapsing without feed/care rising.

## The crew, and why one spend rate cannot fit four heads

**Crew is not cost-limited. It never was.**
`_hire_cost(n) = FARM_HAND_COST_MULT * fib(n)` with `mult = 1`, so the nth hire of the day costs
`1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233`.
**A crew of ten costs $143 for the whole day**, against a median bank of $2,400-6,000, and hands
are dismissed each night with no ongoing wage — that is the entire cost.
The scripted farmer runs ten and banks $23,783, so it plainly pays.

The constraint is the action space's arithmetic and nothing else.
HIRE is **atomic, one per turn** by the reference rule; a day is 24 turns; `hires_today` and
`n_units` both reset nightly, so the crew is rebuilt from scratch daily.
Crew of ten therefore *requires* HIRE on ten of 24 turns — `hire_rate = 0.42`.

### Measured off a leader replay, which settles the prior question

`prvsiyan/kaggle-frontier-lab-strategy-improvement` cell 11 embeds `ACTION_SUMMARY_ROWS`, a per-day
verb census from public episode **89517103**.
HIRE per day: `4, 6, 6, 6, 6, 7, 6, 8, 10, 11, 12, 12, 12 ... 12, 11, 10, 9` — mean 10.1, plateau
12, **implied `hire_rate` 0.422**, confirming the arithmetic above from an actual winner.
Note the ramp: 4-8/day through day 7, plateau by day 10.

Converted to per-turn rates over 720 turns, against the flat 5% that was briefly live:

| head | leader, per turn | flat prior | error |
|---|---|---|---|
| `hire` | **42%** | 5% | **8x too low** |
| `buy_seed` | 7.1% (51/game) | 5% | about right |
| `buy_animal` | 1.9% (14/game) | 5% | 2.6x too high |
| `buy_land` | **0.3% (2/game)** | 5% | **17x too high** |

`BUY_LAND` happens **twice in an entire 30-day game** — three unlocked quadrants, and `N_LAND = 3`
with `LAND_PRICES = [1000, 2000, 4000]` bounds it anyway, so a 5% prior cannot run away there; it
only buys them earlier.
So a single rate is wrong in *both* directions and off by ~140x between the extremes.
**A shared 5% is not a neutral shape — it is a strong and false claim that the four transact
alike.**

**The fix is `--spend-prior 0`, not per-head numbers.**
With `spend_p = 0` the four heads fall to *uniform*, which encodes no target at all:
`KL(p||uniform) = -H(p) + const`, so each keeps exactly the plain entropy regularisation it would
otherwise have and PPO finds the rates itself.
Writing the leader's measured rates in instead would be reading numbers off a replay and calling
them a prior — the policy-prior `CLAUDE.md` forbids, and what capped the ceiling in Orbit Wars.
This works **only because** `HAND_PRIOR_HEADS_WITH_BC` now contains `SPEND_HEADS`: without that,
`--spend-prior 0` silently means "use the day-2 clone" (`buy_land` 0.0%, `buy_animal` 0.1%), a
*tighter* cap than the one being removed, arriving with no flag to explain it.
Pinned by `test_spend_heads_take_no_shared_target_and_do_not_fall_back_to_the_clone`.

### The same census, on the op mix

Leader per-command shares against ours:

| | leader | ours |
|---|---|---|
| movement N/W/S/E | **48.0%** | ~75% |
| WATER | 9.48% | 3.9% |
| FEED | 3.88% | **0.11-0.31%** |
| COLLECT_FERTILIZER | 3.82% | 0.24-0.78% |
| CARE | 3.73% | 0.19-0.50% |
| HARVEST | 3.62% | 0.46-1.5% |
| PLANT | 1.19% | 0.16-0.9% |

Two readings.
Elite movement is **48%, not near zero** — so 84% walking is bad but the achievable target is ~48%,
and any plan predicated on driving movement to single digits is aiming at the wrong number.
And **PLANT is the one op already in range**: the entire gap is in the maintenance ops that need a
walk (FEED 12-35x, CARE 7-20x, COLLFERT 5-16x), which is exactly the temporal problem `commit.py`
exists for and exactly what `COMMIT_PRIOR_SHARE` is aimed at.

Caveats: one replay of the eight, day-2-of-62 meta, and their per-command shares are not the same
unit as our per-turn market rates.
Running the census across all eight tapes for a spread rather than a point estimate is not done.

## SUPERSEDED — The pool: a working regression check and a useless difficulty source

> **This conclusion was wrong, and the section is kept only so the reasoning is not re-run.**
> The day-0 cross-tab below is real and the numbers are real, but the explanation is not: `wr_pool
> 0.990` was the chimera bug at the top of this file — seat 1 played by ~23 different checkpoints
> per game — not a genuine skill gap between the policy and its own history. Prediction 1 in "What
> to watch" is the test. If `vs pool` does not fall after the `hold=` fix, come back here.
>
> Two other readings in this section were also wrong and are corrected above: seat advantage is
> marginal (both seats quote from the same pre-commit inventory; seat order decides only atomic
> `HIRE`/`BUY_LAND` and exhaustion), and "everything destroys value so a win means burning slower"
> over-reached — the $1,104-from-$3,000 result is real but it is a *separate* finding about the
> train/deploy mismatch, not the explanation for 0.990.


Both readings were in play — "the league cannot teach" versus "beating old selves is a regression
check and is supposed to pass".
The opponent x seed-day cross-tab settles it, because it removes the curriculum confound.

At **day 0**, the hard rung, matched difficulty:

| opponent | day-0 win rate |
|---|---|
| pool | **1.00 / 14** |
| idle | 1.00 / 5 |
| farm | 0.50 / 4 |
| ranch | **0.22 / 9** |

We beat every past self on the hard rung and lose 78% to a hand-written ranch bot on the same rung.
Both are true, neither is a bug, and the pool is therefore doing the job it can do and not the one
it was hoped to do.
Counts are small; this firms up as the cross-tab accumulates.

**Seat advantage: investigated and largely dismissed. Do not re-run this.**
`play_checkpoint.py`'s docstring says seat 0 wins every contested tie, which reads alarming because
`train_jax_rl.py` never swaps seats — the live policy is always seat 0.
But `_process_market` states plainly that *"Both seats quoted from the same pre-commit inventory,
before either commits"*, so there is **no price advantage**; seat order decides only the atomic
orders (`HIRE`, `BUY_LAND`, which "resolve once, in seat order, and then the slot is spent") and
exhaustion cases.
With `land_rate` at 0.000 and per-product sell rates of 0.6-6%, contested slots are rare — and this
file already records 300 full-length episodes in which both players never once sold the same
product.
It also cannot explain any *between-opponent* gap, because pool, farm, ranch and idle all sit in
seat 1 and any seat effect cancels.

## Corrected op mix (the previous numbers used a mislabelled name table)

`O_NAMES` order is `noop, N, S, E, W, water, harv, plant, dig, pick, drop, place, feed, care, ...`
— `water`/`plant` and `pick`/`drop` are not in the order they are often assumed to be.

Over updates 101-224, as a share of primitive draws:

| op | upd 101 | upd 224 | correlation with money (312 seats) |
|---|---|---|---|
| water | 11.2% | 3.9% | **-0.276** |
| plant | 1.6% | 0.16% | **-0.358** |
| feed | 1.35% | **0.26%** | **+0.452** |
| care | 1.25% | **0.50%** | **+0.441** |

The work budget goes to the two ops that anti-correlate with winning, and the two that correlate
most have **drifted down 5x and 2.5x** over the run.
That answers item 4 of "what to check next" below with a clear no.
`harv/plant` reads 8.52, above the 4.05 recorded below, but the HARVEST mask is
`ripe_plant | (has_animal & units_held > 0)` so animal collection counts as harvest.

## Known-failing test, pre-existing, unrelated

`tests/test_curriculum.py::test_the_behind_dial_actually_puts_the_trainee_in_the_poorer_seat`
fails: trainee bank **behind=32,616 is not below ahead=25,498**, i.e. the `--curriculum-behind` dial
is inverted and puts the trainee in the *richer* seat.
`--curriculum-behind` is not in the live args, so it cannot affect the current run.
Not fixed — out of scope for this session, but it should not be discovered a third time.

## THE FINDING: the failure was temporal, and it was in the codebase all along

Every *maintenance* action — WATER, HARVEST, FEED, CARE, COLLECT_FERT — needs a walk back to a tile
on a later turn.
And `jax_sim._end_of_day` returns every unit to spawn, **dismisses every hired hand** and **empties
every unit's inventory**.
So the walk is re-motivated from scratch every dawn: four independent draws that must all land, for
a payoff days away, judged by a critic at `ev_signal < 0.3`.

`jax_obs.py` had the numbers the whole time: over **412,992 owned-unit actions the policy placed
4,591 animals and FED 12**, planted 13,439 crops and **harvested 98**.

Setup ops (PLANT, PLACE — one action, on the tile you already stand on) the policy did *more* than
the teacher.
Every op needing a walk collapsed to zero.
**It never failed to learn farming; it learned exactly the subset of farming that survives a
one-step credit horizon.**

What killed the "it can't do them" theory: on day-25 boards — 83% of finished episodes at the time —
COLLFERT is legal on **15.1%** of unit-slots and CARE on **11.2%**.
The policy had chosen COLLFERT **zero times in 23,684 episodes**.
Legal often, never taken.

The *spatial* half of this had already been tried and failed: `jax_obs` hands the policy direction
and distance to the nearest job, on Ender's precomputed-geometry argument.
Knowing where the job is does not make four turns of zero reward survive a noisy advantage.

---

## The fix: `kagg/rl/commit.py`

A `COMMIT_*` token in the same categorical as every primitive op.
Drawn, it freezes a target; the unit walks it and fires the arrival op on contact.
**Intermediate unit-turns are excluded from the PPO density** — not scored as probability 1 —
reusing the mask `active_unit_heads` already applies, so `exp(0-0) = 1` for those slots by
construction.
`tests/test_commit.py` pins the ratio, plus a guard that the decision mask is not silently ignored.

Five categories, one per `_target()` geometry feature: WATER, HARVEST, FEED, PLANT, PICKUP.
**Offered uniformly on purpose** — picking only the ops with dramatic gaps is selective attention,
which is the quality judgment `CLAUDE.md` forbids.
`COMMIT_PICKUP` exists because of a measurement: with `COMMIT_FEED` alone, FEED fired 629 times and
only **144 units (22.9%) carried the wheat FEED consumes**.

It lives **outside `jax_sim`** — putting it in `Farm` would change the simulator whose whole value
is matching the reference field-for-field over 300 episodes.

### Result

| op | before | after |
|---|---|---|
| COLLFERT / FERTIL | **0.00%**, never once | ~2.4% |
| CARE | 0.07% | ~3.7% |
| HARVEST | 0.44% | ~6.2% |
| PICKUP | 0.63% | ~3.7% |
| FEED | 0.02% | ~1.5% |
| harv/plant | 0.18 | 4.05 |

Seeded `vs farm` 0.589 → **0.707**, and all five curriculum rungs above chance for the first time
(`mix5d` had four sitting at ~0.50).
On empty day-0 boards it now builds the whole seven-step animal chain — coop → buy → place →
pickup → feed — which no previous run did once.

### And the turn-0 replay is still 0/0/32

Bank $3,000 → $2,150 against the farmer's $30,292.
**Fourth time the seeded aggregate and the replay have disagreed.**
`harv/plant 4.05` is cheap: most of it is harvesting day-25 crops the policy never had to grow.

---

## THE BOTTLENECK NOW: production scale, not the market

Measured over a full turn-0 season:

```
              planted tiles   shed products   final bank
our policy         4.8              9.4          $1,517
scripted farmer   16.0              0.0         $23,783   (sells everything)
```

There is nothing to sell.
A 10.6% wheat sell rate is a fine rate at which to sell almost nothing — the sell-side numbers were
a red herring.

Two measured causes:

- **Crew.** Farmer peaks at **10 units**, teacher ~12, ours **2.9–4.8**. `n_units` resets to 1 every
  night, and HIRE is **atomic — one per turn, by reference rule** (`"Atomic orders (HIRE, BUY_LAND):
  handle once, in player order"`), so the crew must be rebuilt daily. Our `hire_rate` ~0.15 × 24
  turns ≈ 3.6 hires/day ≈ crew 4.6, which matches exactly. Crew 10 needs `hire_rate ≈ 0.42`.
  **This is learnable, not an action-space limit** — do not try to batch HIRE, it would break parity.
- **Turn budget.** Movement + NOOP is still **79%** of every unit's life (74–77% on day-0 boards).
  Commitment fixed whether a walk *completes*; it did not reduce how much time is spent walking.

---

## Traps found today — all four are metric-labelling failures

`CLAUDE.md` already names this class ("a metric can be correct per row and still meaningless if its
label is unstable over the thing it describes"). It happened four more times.

1. **`vs idle` averages five different games.** Under symmetric seats the idle opponent holds its
   opening money all episode, and openings span **$623 (day 0) to $54,031 (day 25)** — an 87×
   spread. Now printed at startup.
2. **The seeded day-0 board is not a real game start.** It is a recorded seat that has already spent
   ~$2,400 of its $3,000 on seed, so it starts at **$623 holding 7.5 seeds**; a real Kaggle game
   starts at **$3,000 holding none**. So the policy can read `vs idle 1.000` while a turn-0 replay of
   the same checkpoint ends *below* its starting money. Both true simultaneously.
3. **The day-0 RUNG is not the turn-0 REPLAY.** The rung (0.608) is a *symmetric mirror match* —
   beating a clone of itself. The replay (0/32) is against the scripted farmer from an empty farm.
4. **Seven of the nine `buy` zeros are structural.** Only WHEAT and FERTILIZER are in `jax_sim.BUYABLE`.
   Printed as a bare list it read as "refuses to buy seven products" when it *cannot*.

**From here the turn-0 replay gates every claim of progress.** Seeded rates are a regression floor.

---

## Prior architecture — read before touching any prior flag

`hand_prior_heads` shapes **only the `op` head**.
Every other head gets a **uniform** prior, and `KL(p||uniform) = -H(p) + const`, so those heads are
actively pushed toward maximum spread. Implied P(act) on a day-25 board:

| head | BC prior | uniform (`--hand-prior` alone) |
|---|---|---|
| buy_seed | 0.9% | **75.0%** |
| buy_product | 0.4% | **40.0%** |
| buy_animal | 0.1% | **50.0%** |
| hire | 6.3% | **50.0%** |
| buy_land | 0.0% | **46.7%** |
| sell | 6.6% | **27.3%** |

That emptied a $53,373 inherited farm to **$14** and lost to an opponent doing nothing.
`--spend-prior` covers only four of the six; `buy_product` and `sell` are not in `SPEND_HEADS`.

**Current design: hand prior on `op`, BC prior on every other head.**
Neither is right everywhere — the BC prior predates commitments, so its zero-padded commit logits
hold **2.4%** of op mass against 21.7% uniform, a 9× suppression of the behaviour under test.

**`--init` is not optional with a KL prior.** At `reg_coef = ent_coef = 0.01` the KL is a *tether*,
not an *attractor*: it holds you near where you started and cannot drag you 4.4 nats back to
somewhere you have never been. Three runs were lost to dropping `--init` alongside `--kl-prior`.

**`--kl-anneal` is unset and that is deliberate.** Ender's KL was a *separate* coefficient from his
entropy term, so annealing relaxed a prior. Here the KL **replaces** entropy and shares `reg_coef`,
so annealing to zero removes *all* regularisation — the state that already destroyed a run
(entropy 13.35 → 26.70, win rate 0.525 → 0.291). Doing it properly means **decoupling the two
coefficients first**, which is its own delta and is now the strongest candidate, because a flat KL
to a **day-2 checkpoint** is a permanent ceiling over a 62-day competition.

---

## Opponents — the oldest open item, now closed

`jax_rancher` has been JAX-native and jit-safe since 2026-08-01 and was wired only into `bc_dagger`.
It is now `--ranch-frac`.

```
jax_heuristic (the only farming opponent until today):  $23,783   FEED 0.00% CARE 0.00% COLLFERT 0.00%
jax_rancher:                                            $12,078   FEED 0.72% CARE 0.76% COLLFERT 0.68%
```

It is the **weaker** opponent and that is not the point: nothing the policy had ever faced was
punished for ignoring the animal economy, which `CLAUDE.md` measures as the half that wins
(FEED +0.452, CARE +0.441 over 312 seats).

**`rancher`/`converter`/`contrarian` cannot be added** — they are dict-based Python agents and cannot
run inside the jitted `lax.scan`. That is why `jax_heuristic` exists. Porting one is a real job.

**`self` was never an agent.** `ROLE_SELF` appears twice: in the enum, and as
`role_p[ROLE_SELF] = 1.0 - role_p[1:].sum()`. There is no `use_self` in the rollout — it is the
fall-through, so seat 1 keeps the live policy's own actions. Shared params make a mutual draw a
stable outcome no gradient pushes against, which is exactly what the pool was introduced to escape.
It has been folded into `pool` (an *old* version of self, which is what was wanted).

---

## The op-axis decode (`condition_on_op`): measured, no effect, kept anyway

Two BC runs per architecture, seeds 0 and 1, held-out NLL on `item`/`qty`:

| | seed 0 | seed 1 |
|---|---|---|
| `item` | +0.015 worse | −0.028 better |
| `qty` | +0.079 worse | −0.041 better |

Sign flips between seeds; seed spread (0.037–0.079) is as large as the effect. **No detectable
difference.** `crop` is inert by construction — only PLANT reads it and `active_unit_heads` already
confined it there.

Kept because it is cost-neutral and the scaffolding is the durable part: the `ratio == 1.0` gate,
and `migrate_params`, which now also widens the op head so pre-commitment checkpoints still load.

---

## What to check next, in order

0. **Turn-0 replay on `latest.pkl`.** `scripts/play_checkpoint.py <ckpt> --games 16`. It gates
   everything and has overturned four conclusions.
1. **`vs ranch` against `vs farm`.** First time the animal gap is a number rather than an inference.
2. **The pool summary line.** Members sat at `0.04/22` — if newer ones reach 0.3–0.5 the league is
   generating difficulty; if all stay near 0.04 the policy outruns its own history and the pool still
   cannot teach.
3. **`hire_rate`.** Needs ~0.42 for a crew of 10; sitting at ~0.15. The single most direct lever on
   the 4.8-vs-16 tile gap, and it is one binary decision taken 24 times a day.
4. **Whether FEED/CARE stop drifting down** now something punishes ignoring them.

## Known-bad, do not re-suggest

- `--spend-prior` alone as a bankruptcy fix on an *inert* policy (falsified 2026-08-01) — but it IS
  right on a hyperactive one. The problem changed; re-read why a thing was rejected.
- Batching HIRE into quantity buckets — atomic by reference rule.
- Annealing the shared `reg_coef` to zero — no regulariser at all.
- A per-op-marginal prior over the whole op head — FEED/CARE/COLLFERT are legal so rarely that a flat
  marginal concentrates huge relative pressure into rare windows, behaving like a policy fragment.
- Day-0 truncated at day 5 — a competent farmer is BEHIND a do-nothing agent until **day 11**
  (crossover $3,706 vs $3,000), so scoring at day 5 trains "do not farm".

## Repo

`https://github.com/alexchilton/kaggriculture`, branch `animal-economy-and-rl-measurement-fixes`.
Today's commits: `25a0b50` … `e00731e`. `data/*` is gitignored.
