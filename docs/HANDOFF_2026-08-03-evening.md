# Handoff — 2026-08-03 evening

**Supersedes `HANDOFF_2026-08-03.md` entirely.** Read `CLAUDE.md`, then this.

Competition launched 2026-07-30, deadline 2026-09-30. Day 4 of 62.

---

## Read this first: why the last handoff failed

`HANDOFF_2026-08-03.md` carried a TO DO item that had been **recommended three times and was wrong
every time** — "put day / turns-remaining features into the value function". The feature has been in
`glob` since the first commit of the per-turn policy. Nobody ran the two-line check.

The cause is now known and is a process fact, not a judgement call. Those recommendations came from
a Fable consultation whose round-1 prompt said **"Do NOT read any files or run any tools"** — and
that constraint was still in force in round 4 when the recommendation was made for the third time.
It could not have checked. **Three repetitions of an unverified claim are one claim counted three
times, not three pieces of evidence.**

Two rules fall out, and they are the only reason this handoff is structured the way it is:

1. **Every claim below carries its evidence and its status.** If a line says "measured", a number
   and a file follow. If it says "inferred", it has not been tested.
2. **Nothing lives only in a handoff.** Every finding has its own dated document. This file is an
   index with status, not the record. The previous handoff compressed four rounds of advice into
   two bullets and permanently lost the rest — it was only recovered by grepping the raw session
   transcript off disk.

---

## The document set (nothing is only here)

| document | what it holds |
|---|---|
| `critic_terminal_blindness_2026-08-03.md` | the critic cannot tell won from lost near the end; supersedes old item 3 |
| `cliff_decomposed_2026-08-03.md` | the day-10 money cliff, decomposed and root-caused; includes a self-correction |
| `fable_advice_recovered_2026-08-03.md` | four rounds of advice the last handoff lost, recovered from transcript |
| `leaderboard_snapshot_2026-08-03.md` | field position — **Alex has ruled this out of scope**, kept for the record only |

---

## Running right now

`league1`, systemd unit `kagg-train` on the Windows box. Log `/home/alex/kagg/data/logs/run.log`,
followed by `kagg-log`. Redeploy = edit the unit's `ExecStart` and `daemon-reload`.

**It is training on the curriculum identified below as the leading suspect.** Nothing here has been
deployed to it.

---

## THE PROBLEM LIST

Ordered by how much they explain, not by cost.

### P1 — The critic is blind to terminal outcomes · MEASURED · NOT FIXED

At turn 718, one turn from the end, holding **$0 against $30,000**, the critic outputs **0.169**.
The correct value is 0.0. A 3× lead on the final turn reads 0.664 instead of ~1.0. Confirmed twice
by different methods, including real self-play trajectories that rule out an out-of-distribution
artifact: in decisively lost games `V` sits in a **0.12–0.14** band (vs farm) and **0.32–0.33**
(vs idle) all the way to the last turn.

**Cause:** terminal rows are ~0.14% of a batch (`train_jax_rl.py:954`), so the critic trains almost
entirely on its own bootstrapped targets — **and a value function flat in day is perfectly
self-consistent under bootstrapping.** Same fact as `ev` 0.79 vs `ev_signal` ~0.4.

**Two mitigations already ship and are active and insufficient:** `seat_coef=1.0` and `--n-phases
12`. Seat-sum consistency is necessary but not sufficient — a critic predicting exactly 0.5/0.5
satisfies it perfectly while being useless, and the measured values do sum to ~1 at every day.

**Solution — measure before adding a third mechanism.** In order:
1. How much of the value-loss gradient actually comes from terminal-adjacent rows *with* staggering
   on. Measurement, no change. 719/32 ≈ 22, so each phase group still touches its own terminal
   about once every 22 updates.
2. Oversample or upweight terminal / near-terminal rows in the value loss.
3. Whether `vf_coef` lets the value loss get outweighted by policy and KL terms at exactly those
   rows.

**A restart is required for 2 or 3, not for 1.**

### P2 — The curriculum teaches "late day = rich farm", and the policy obeys · MEASURED · NOT FIXED

The training mix is `length:0:0.6,10:0.1,15:0.1,20:0.1,25:0.1`. What the four late rungs hand it:

| rung | money (median) | **units (median)** | land |
|---|---|---|---|
| day 0 | $476 | 7.0 | 0.0 |
| day 10 | $980 | **9.0** | **1.0** |
| day 15 | $11,688 | **11.0** | 1.0 |
| day 20 | $29,730 | **11.0** | 1.0 |
| day 25 | $58,333 | **11.0** | 1.0 |

**40% of training episodes begin at day ≥ 10 already owning a crew of 9–11 and a quadrant**, and
`day/30` is a feature the policy reads at layer one.

Tested directly — hold a poor board fixed ($3,000, one unit, no land) and move **only** `step_index`:

```
  day    P(hire)   P(buy_land)
    0     0.1605        0.0000
   10     0.1913        0.0004
   20     0.4107        0.1770
   28     0.4407        0.4767
```

**Note the correction:** this is a smooth monotone ramp, **not** a step at day 10. An earlier draft
claimed a threshold; that was wrong and is corrected in `cliff_decomposed_2026-08-03.md`. The dollar
cliff needs no behavioural cliff — `HIRE_COST` is Fibonacci, so cost is convex in crew size and a
1.2× rise in propensity becomes a 25× rise in spend.

**The damning number is `P(buy_land)` peaking at day 28 (0.48).** Buying a quadrant with two days
left is indefensible; nothing planted in it can mature. A land-buying urge rising monotonically to
the final day is very hard to explain except as inherited from rung states that are rich *because*
they are late.

**This is the same bug already found and fixed for day 0** — "trained to *continue* an elite opening
and deployed to *make* one". It was only ever fixed for the day-0 rung.

**Solutions, cheapest first:**
1. **Filter the rungs to reachable states.** `states_at_day` already accepts `min_bank` / `max_bank`
   / `top`; it currently draws from the *richest* seats by design. Capping the draw breaks the
   correlation directly. ~1 hour. **Requires restart.**
2. **Reverse-curriculum resume points** — sample start states from the policy's *own* trajectories
   just before a payoff. Structurally fixes reachability instead of filtering it. Ranked above the
   chain rung by Fable. Mastery criterion is an open design question. **Requires restart.**

**Do not ship 1 and 2 together, or with P3.** One delta at a time.

### P3 — No feature for what a crew costs to KEEP · MEASURED · NOT FIXED

There is **no upkeep in this game** — `_end_of_day` and `_night` move no money. But **`n_units`
resets to 1 every night**, so a crew is *rented daily* at `sum(HIRE_COST[:N-1])`, Fibonacci:

```
crew  8: $33/day    crew 10: $88/day    crew 12: $232/day
crew  9: $54/day    crew 11: $143/day
```

The measured hire column in the day-0 replay is **-33, -54, -54, -54, -88**. Those are not
approximately the ladder, they *are* it: crews of exactly 8, 9, 10, re-hired every morning from day
11 to the end. **Hire is the largest single drain of the season at -$1,192**, more than the land
purchase and more than everything lost trading.

`glob` carries `hire_afford` — the price of the *next* hire — and nothing for the recurring bill on
the crew it already has, because to the simulator there is no such thing.

**Solution:** a "cost to re-hire current crew, as a share of bank" feature. A fact, not a judgment;
same side of `CLAUDE.md`'s line as `land_afford`. **Trap: this changes the feature width, so
`migrate_params` must widen the input projection or no checkpoint will load** — the trap old item 3
wrongly claimed for the day feature genuinely applies here. **Requires restart.**

### P4 — The chain DOES pay. It buys more than it sells. · MEASURED · NOT FIXED

**This item said "the chain never terminates in money" for most of today. The gross split refutes
that, and the correction matters more than the original claim.** It is recorded rather than quietly
edited because the wrong version was acted on for several hours.

`play_checkpoint` starts at `J.reset` — a genuine $3,000 bare-board day-0 start, **no curriculum
seeding at all**. Everything below is self-produced.

`jax_masks.py:96`: `FEED = has_animal & ~fed & carrying_wheat`. Every FEED requires the policy to
have already built a structure, bought an animal, picked it up, placed it, obtained wheat, picked
that up, and walked there. **It fired 1,071 times (seat 0) and 1,609 (seat 1) across 32 games.**

The season, decomposed (seat 0, median over 32 games):

```
    SELL     +2,381        <-- the chain terminates in money, in 32/32 games
    buy      -3,206        <-- and it spends more than that on inputs
    hire     -1,192
    land     -1,000
                           gross sales median $2,381, max $8,648
```

Per-day, the sales are real and sustained from day 14 on: **+63, +70, +39, +40, +165**.

**So the chain is not broken at the end. It closes. The farm is simply run at a loss** — inputs
$3,206 against output $2,381, before a $1,192 wage bill and a $1,000 quadrant it cannot use.

That is a different failure from the one assumed all day, and it points somewhere else:

- **It is not "cannot reach the payoff".** It reaches it every game.
- **It is a unit-economics failure**, which is exactly what a critic that cannot value an outcome
  would fail to correct. Nothing tells the policy that $3,206 of seed and stock returning $2,381 is
  a losing trade, because the only signal that would say so is terminal — see P1.
- **The buying spike is days 11–13** (-$220, -$240, -$71), the same window as the hire ramp. P2 and
  P3 are buying the inputs; P4 is failing to make them pay.

**P1 and P4 remain very likely the same problem from two ends**, but the end that is broken is
*valuation*, not *execution*.

Instrument: `step_accounted` reports gross `sell` and `buy` separately, cross-checked against the
independently-recovered net (`sell - buy == trade`) so neither half can be quietly wrong.
`data/logs/gross_sales.log`.

### P2b — THE AGREED FIX: reverse-curriculum resume points · AGREED 2026-08-03 · NOT BUILT

**Alex's call, made explicitly**, on Fable's recommendation (which ranked this *above* the chain
rung, not as a nice-to-have — see `fable_advice_recovered_2026-08-03.md` §2):

> "i like the idea of fable by the way - that way we get the training effect without feature risk -
> those game states can just be the same as the base game then moved forward and with a harvestable
> and a feed etc"

**Why this is the right fix and not merely a good one:**

1. **No feature risk.** It changes the *initial state distribution* and never the observation. No
   width change, no `migrate_params` widening, no checkpoint invalidated — and the `--kl-prior`
   anchor survives. P3's crew-cost feature cannot promise any of that.
2. **It fixes P2 at the root rather than patching it.** The current rungs are drawn from *elite
   replays*, so `day` and `wealth` are correlated in the training data and the policy learned the
   correlation (P2's ramp). If states are the base game rolled forward, money and crew are whatever
   actually accumulated, and **the correlation cannot form because it is not there.**
3. **Today's measurement makes it feasible, and it would not have been a week ago.** The policy
   already builds the chain prefix unaided — 1,071–1,609 FEEDs per 32 games from a bare board — and
   FEED is masked on `has_animal & ~fed & carrying_wheat`, so each one proves the seven-step prefix
   landed. **States with a feedable animal and a harvestable crop already occur in its own
   rollouts. They can be harvested rather than authored.**

**The one catch, and it is not optional: this must REPLACE the elite rungs, not sit beside them.**
Adding reachable resume points at 10% while leaving `10:0.1,15:0.1,20:0.1,25:0.1` in place keeps the
poison and merely dilutes it. The mix has to lose the elite rungs in the same change.

**Open design questions, both genuine:**

- **Who rolls the state forward.** The policy's own trajectories (guaranteed reachable, improves as
  it does, needs periodic refresh or it goes stale) versus a scripted agent (more reliable states,
  but that is gifting in a thinner disguise). **Recommendation: the policy's own — that is the whole
  point.**
- **The mastery criterion is missing.** Fable gave the reverse-curriculum pattern — walk the resume
  point earlier as the tail stops failing — and no threshold. Something like "FEED or HARVEST fires
  within N turns of the resume point in ≥X% of episodes over a rolling window" needs designing.

**Honest caveat on the P1 benefit.** Short episodes raise terminal density, which is why the day-25
chain rung looked attractive for the critic. But if the chain states occur around **day 10–14**,
episodes are ~430–500 turns — only **1.4–1.7× denser, not the 5–6×** a day-25 start gives. This
helps P2 a great deal and **P1 much less than the chain rung would.** Do not buy it expecting to fix
the critic.

**Requires a restart.** Do not ship it together with P3.

### P5 — `curriculum.states_at_day(0)` is still broken · MEASURED · NOT FIXED

Returns $476, 7 units, `step_index` median 24 — that is **day 1, not a game start**. Training
special-cases day 0 to `J.reset`, so the live run is fine and the function was never actually fixed.
The next caller gets the original bug.

**Solution:** fix the function. Small, isolated, **no restart needed** (nothing calls the broken
path).

### P6 — The 6-member league is unjustified surface area · ADVICE, NOT MEASURED

Fable, never recorded in any handoff until today: *"Shrink the 6-member league… More league members
is more surface area for the next version of that bug \[the pool-identity chimera\], for a return
you've already established isn't the constraint."*

**Solution:** shrink it. **Raise with Alex first — this is a suggestion, not a finding.**

### P7 — The chain rung is built, committed, and still not deployed · DECISION PENDING

`curriculum.chain_states()`, a hand-built half-farm at day 25.

**The recorded reason to hold has an expiry date and the last handoff hid that.** The real reason
was *"get one clean baseline under the just-corrected day-0 curriculum first"* — which lapses once
a clean baseline exists. Fable never argued to kill it.

**The no-op control is nearly the whole experiment, not an expensive extra arm:** *"if feed doesn't
fire in days 1-3, that's close to sufficient on its own"*.

**New consideration:** a day-25 start collapses episodes from ~719 turns to ~120, raising terminal
density roughly 5–6×. So both this and P2's reverse-curriculum are candidate *treatments for P1* —
a use nobody considered because P1 did not exist yet. **This promotes the reverse-curriculum
version specifically**, because it gets the same terminal density without the state-gifting
confound. If run for that purpose the metric is **not** bank or win rate — it is whether `V` starts
spreading toward 0/1 on the denser terminal rows.

**Do not let the two questions merge.**

---

## Done today, with evidence

| change | status |
|---|---|
| `jax_sim.step_accounted` — exact per-turn hire/land/trade + gross sell/buy | **done**, invariant asserted at `atol=0`, parity 54/54 green |
| `play_checkpoint` money-flow-per-day output | **done** |
| `--kl-anneal` hands over to entropy instead of zeroing all regularisation | **done**, 13 tests, failed-first |
| Old item 3 (day features) struck and superseded | **done** |
| Fable's lost advice recovered from transcript | **done** |

`step` is unchanged and delegates to `step_accounted`; XLA eliminates the accounting when unused, so
the training hot path is untouched. `--kl-anneal 0` is byte-identical to the old code, **so the live
run is unaffected by everything above.**

---

## Metric warnings — unchanged and still load-bearing

- **`money_med` is not an outcome.** Use `bank_final_med` (`END $x`).
- **`ev` is not `ev_signal`.** `ev` is mostly the critic predicting its own bootstrap. Never quote
  an endpoint.
- **`ev_signal` reads n/a when every finished game had the same outcome.** The gaps are the
  information.
- **Day-0 results arrive in a burst.** Still unfixed.
- **Plot before concluding:** `python3 scripts/plot_run.py <run>/log.jsonl -o out.png`.
- **Prefer a replay to an aggregate whenever the aggregate could be a tie.**

---

## Settled — do not relitigate

- **Seat advantage is marginal.** Mirror match 54% over 48 games. Fable argued the opposite across
  two rounds and retracted it: *"the seat-advantage call was wrong"*. Keep the mirror-match method,
  discard the hypothesis.
- **`commit.py` and the op-head class-split prior are load-bearing in the right direction.**
- **"It learnt capital preservation, not production" is DEAD.** That described an earlier
  checkpoint. Update 1800 spends **$2,840 of its $3,000** and finishes on $220, 0/0/32 both
  seatings. It is dormant for ten days and then buys a farm it cannot run.
- **"FEED fires ZERO times" is DEAD.** It fires 1,071–1,609 times per 32 games.
- **"It never harvests or sells" is DEAD, and it was mine, from earlier today.** It sells **$2,381
  gross in 32/32 games**. The failure is unit economics — $3,206 of inputs for $2,381 of output —
  not a missing final link. See P4.

---

## Recommended order

1. **P5** — free, no restart, removes a live trap.
2. ~~P4 gross-sales number~~ — **done**, and it refuted the item it was measuring. See P4.
3. **P1 step 1** — measure terminal-row gradient share. No restart, no risk.
4. **P2b — build the resume-point sampler.** Agreed by Alex. The elite rungs come out in the same
   change. Restart.

**P2b and P3 must not ship together.** Both plausibly move the same numbers, and `CLAUDE.md`'s
one-delta-at-a-time rule exists because that exact confound has already cost this project days.

**P2 solution 1 (filter the rungs by bank) is now a fallback, not the plan** — P2b subsumes it and
fixes the cause rather than capping the symptom.
