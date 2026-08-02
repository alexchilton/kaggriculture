# Handoff — 2026-08-02, evening

Supersedes the state sections of `HANDOFF_NEXT.md`.
Read `CLAUDE.md` first, then this.

Competition launched **2026-07-30**, deadline **2026-09-30**.
Today is **day 3 of 62**, which matters for how you read every "teacher" number below.

---

## Running right now

`league1-20260802-175612`, systemd service `kagg-train` on the Windows box.
Log: `/home/alex/kagg/data/logs/run.log`, pull with `./scripts/deploy_train.sh getlog`.

```
--curriculum-mix length:0:0.6,10:0.1,15:0.1,20:0.1,25:0.1   --curriculum-symmetric
--opponent-frac 0.45 --farm-frac 0.25 --ranch-frac 0.20 --idle-frac 0.10   (self = 0)
--pool-size 16 --pool-every 25
--hand-prior 0.15 --spend-prior 0.05 --kl-prior <mix5-20260802-120823/latest.pkl>
--ent-coef 0.01 --lr 3e-5 --batch 256 --horizon 32
```

Resumed through a chain: `commit4` → `day0flip` → `day0flip2` → `ranch1` → `league1`.
Always launch via `./scripts/deploy_train.sh train`; a hand-started run gets reaped when SSH closes.

---

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
