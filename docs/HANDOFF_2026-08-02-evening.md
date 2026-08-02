# Handoff — 2026-08-02, evening

Supersedes the state sections of `HANDOFF_NEXT.md`.
Read `CLAUDE.md` first, then this.

Competition launched **2026-07-30**, deadline **2026-09-30**.
Today is **day 3 of 62**, which matters for how you read every "teacher" number below.

---

## Running right now

`league1`, systemd service `kagg-train` on the Windows box, resumed from **update 300**.
Log: `/home/alex/kagg/data/logs/run.log` — `kagg-log` follows exactly that file.

```
--curriculum-mix length:0:0.6,10:0.1,15:0.1,20:0.1,25:0.1   --curriculum-symmetric
--opponent-frac 0.45 --farm-frac 0.25 --ranch-frac 0.20 --idle-frac 0.10   (self = 0)
--pool-size 16 --pool-every 25
--hand-prior 0.05 --spend-prior 0.05 --kl-prior <mix5-20260802-120823/latest.pkl>
--ent-coef 0.01 --lr 3e-5 --batch 256 --horizon 32
```

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

**Note on `hire`, correcting the reasoning used to include it.** 5% is a *tighter* target than the
BC prior's 6.3%, and measured `hire` is 7.3%, above both.
Including `hire` neither releases nor meaningfully constrains it.
The ~0.42 a crew of ten needs will not come from either prior.

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

## The pool: a working regression check and a useless difficulty source

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
