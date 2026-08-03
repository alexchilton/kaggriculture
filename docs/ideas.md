# Ideas not to lose

Running list of proposals that survived scrutiny but have not been built or wired.
Each entry states what it is, why it is safe, what it costs, and what would falsify it.
Newest first.

---

## 0. Net-worth potential — the one that reaches the animal chain

**Status: proposed 2026-08-03 evening, not built. Supersedes the ranking below.**

### Why the money potential does NOT do this job

Alex's objection, and it is correct: **money PHI punishes the goose on the turn you buy it.**
Cash goes $12,000 -> $11,600, PHI falls, shaping is negative that turn, and the milk still arrives
100+ turns later.
It makes the *cost* of the animal chain more visible and leaves the benefit exactly as far away.

The reason is that money PHI values **cash**, and the animal chain is **capital**.
A goose in a pasture is an asset; a cash-only potential books it as $400 of pure loss until it
produces, so it penalises every investment and rewards hoarding.
That is a milder version of the same defect as the linear bank delta.

So money PHI is scoped to **execution** -- the wash trade, selling into a price floor, anything that
resolves inside the ~20-turn credit window.
It is not an instrument for discovering the animal chain.

### The form

```
PHI = f( money
       + animals at ANIMAL_COST, discounted by how close they are to escaping
       + inventory at the BID price
       + standing crops at expected yield x price, including any fertiliser multiplier )
```

Buy a goose: cash -$400, asset +$400, PHI roughly flat -- **no penalty for investing.**
It starves and escapes: asset -$400, PHI drops. Correct, and automatic.
Plant a melon: seed cost out, standing crop in -- planting stops looking like a loss.

The appeal is that it is **accounting, not tactics**. It says assets are worth what they would
fetch; it does not say animals are good or melons are good. So it encodes no strategy and cannot cap
the ceiling, which is the objection that ranks a hand-built chain PHI last.
It is still a potential, so it still telescopes and is still policy-invariant.

### The trap Alex asked about: FEED and FERTILIZE are CONSUMPTION

This is the crux, and naive book-cost accounting gets the **sign wrong** on exactly the two ops we
care about most.

- `FEED` destroys a unit of wheat (~$51 of asset) and adds nothing to the balance sheet.
- `FERTILIZE` destroys a unit of fertiliser and adds nothing.

Under a naive net-worth PHI both are **negative**. It would actively discourage the two strongest
money predictors in the game (FEED +0.452, CARE +0.441 over 312 real seats).

The fix is to value the intangible each one buys, and in both cases the simulator hands us a
non-arbitrary basis:

- **An animal's value decays with `consecutive_unfed`.** `jax_sim.py:1159` escapes at `unfed >= 2`,
  so an animal one day unfed is one night from being worth zero. Valuing it as
  `ANIMAL_COST * (1 - unfed/2)` is the sim's own rule, not our invention.
  Then FEED reads as -$51 of wheat and +~$200 of restored animal, strongly positive -- and *skipping*
  a feed shows the loss on the turn it is skipped rather than two days later.
- **A plant's value includes the fertiliser multiplier.** `jax_sim.py:1096-1097` doubles yield while
  `fertilized_until_day >= day`, so a fertilised plant is worth ~2x an unfertilised one and
  FERTILIZE reads positive.

This is where it stops being pure accounting and starts involving judgement, and that must be
admitted rather than glossed. But both curves are read off `jax_sim.py`, not chosen to make animals
look good.

### How hard, honestly

Measured against the actual source:

| component | difficulty | why |
|---|---|---|
| money | trivial | `farm.money` already threaded |
| animals | easy | `ANIMAL_COST` table exists (`jax_sim.py:170`); `consecutive_unfed` is already a tile field AND already an observed feature |
| structures | **free, and irrelevant** | `jax_sim.py:613` -- BUILD_COOP/BUILD_PASTURE cost **nothing**. Zero book value, but also no cash outlay to bridge, so the build step needs no shaping at all |
| inventory | moderate | `price(state.inventory)` gives town prices (`jax_sim.py:463`); needs an item->product mapping and marking to the bid, not the ask |
| standing crops | judgement | expected yield x price x maturity. The most arbitrary piece; could be left out of v1 |

The wiring itself is one call site: the rollout scan already has the state before and after `J.step`,
and the reward is assembled at `train_jax_rl.py:607`.

**Note the structure finding** -- it changes the chain story. Building a pasture is free, so the only
cash cost in the whole animal head is the animal itself.
The head is cheaper than described in entry 2 below.

### What would falsify it

Net worth climbs while win rate does not -- it has become a balance-sheet maximiser.
Or FEED/FERTILIZE stay at zero, which would mean the intangible valuations are not carrying.

---

## 1. Money potential — connect the thing we already built

**Status: written, 16 tests passing, `coef` defaults to 0.0, and not wired into `train_jax_rl.py` at all.**
`grep money_potential scripts/train_jax_rl.py` returns nothing.
"Ships off" turns out to mean "never connected".

### How it works

One line, applied per turn:

```python
shaping_t = coef * ( PHI(money_after) - PHI(money_before) )

PHI(money) = ( max(money - 3_000, 0) / 100_000 ) ** 2
```

Three deliberate choices, all Alex's:

- **Floor at $3,000.** That is the opening stake, so the whole $0–$3,000 region is flat.
  Going broke is not punished and clawing the stake back is not paid for.
  Only *earning* moves it.
  This is what separates it from the per-step bank delta that `CLAUDE.md` marks NO LONGER IN FORCE —
  that was `PHI = money`, linear and unfloored, which pays for thrift.
- **Scale $100,000.** The top two agents in episode 89197802 banked $106k and $113k, so a genuinely
  winning season sits at `PHI ~ 1` — the same order as the terminal reward rather than dwarfing it.
- **Exponent 2, convex.** The same $1,000 is worth far more at $90k than at $4k.
  A $5 win over an equally broke mirror is worth almost nothing.

### Why it is safe

Ng, Harada & Russell 1999: adding `F(s,s') = gamma*PHI(s') - PHI(s)` leaves the optimal policy
**provably unchanged**.
At gamma 1.0 the per-turn terms telescope, so an episode's total shaping is exactly
`PHI(end) - PHI(start)` whatever route was taken — it cannot pay for a detour.
`tests/test_money_potential.py::test_the_shaping_telescopes_so_only_the_endpoints_matter` checks it
directly.

This is **not** the thing the terminal-only decision banned.
That decision was against per-step bank delta *as the reward*, which changes the objective to margin
maximisation — and the ladder is Elo, where a $43k win and a $4k win score identically.
Potential shaping does not touch the objective.
It only relocates credit in time.
`train_jax_rl.py:557` already says so in another context: *"potential-based shaping is provably
equivalent to initialising the value function."*

### Why it is the right first move

`docs/thrift_is_optimal_2026-08-03.md`, our own toy MDP:

```
baseline (terminal only)     never solved    $3,800
+ money potential            solved by 499   $4,600   (every seed)
```

and its diagnosis, written before today's replay:

> Once winning is assured the reward is 1 whether you bank $3,400 or $4,600,
> **so there is no gradient to the optimum.**

That is exactly the defect the 2026-08-03 replay found.
The policy loses 0/8 to `farm` while banking $12,478 against `farm`'s $28,168, runs a $100k wash
trade to net $7.7k, and applies fertilizer **zero** times in 8 full seasons.
Every one of those is "no gradient to the optimum once the outcome stops moving".

At $12,478, `PHI = 0.009`. At `farm`'s $28,168, `PHI = 0.063`.
So the gap we are trying to close spans about 0.05 — comfortably under the terminal reward's 1.0,
which is the scale sanity check that matters.
And it is a real gradient in a region where the terminal signal currently gives **nothing at all**,
because we lose either way.

### Cost and risk

One CLI flag and one call site in the rollout.
The risk is not the theorem — invariance is exact — it is that **invariance protects the optimum, not
the learning dynamics**.
With finite samples, PPO clipping and a function approximator, a coefficient large enough to swamp
the terminal signal becomes the objective in practice regardless of Ng.
So the coefficient must keep PHI's working range well under 1.0, and it must not be switched on
mid-stream without accepting that runs before and after are incomparable.

### What would falsify it

`bank_final_med` does not move, or moves while `wr_farm` stays at 0.
Money going up without wins going up means it has become a margin maximiser, which is the failure the
original decision was guarding against.

---

## 2. Chain potential — the same trick over chain state

**Status: proposed today, not built.** Strictly the second instrument, not the first.

### How it works

Same formula, different `PHI`. `PHI` is a function of the **board**, not of actions:

```
PHI(s) = f( structure built, animal owned, days the animal has been alive, ... )
shaping_t = coef * ( PHI(s_after) - PHI(s_before) )
```

You never enumerate "correct link used" or "step forgotten".
You score states, and the plus and minus fall out on their own:

| what happens | PHI | shaping that turn |
|---|---|---|
| buys a goose | state now contains an animal → up | **+** |
| builds the pasture | structure exists → up | **+** |
| places the animal | it is housed → up | **+** |
| forgets to feed, it escapes | animal gone → down | **−**, taking back everything above |

Buy an animal and starve it and you net **zero**, which is the truth: $400 spent, nothing gained.
That is what makes it honest rather than a completion bounty.

**The gain is the timing, not the plus.** Today, buying a goose shows −$400 immediately and its
reward at turn 719. PHI makes the credit land on the same turn as the cost.

### Two traps

- **`fed_today` is a bad PHI term.** It resets every night, so it would add +PHI at the feed and
  −PHI at the reset — net zero per day but a large oscillation on every turn.
  Still provably safe, because any PHI telescopes, but it is noise with no information.
  PHI wants slow-moving state: *structure exists*, *animal owned*, *days alive*. Not daily flags.
- **A flat bonus for "chain completed" is NOT this.** It does not telescope, it is strategy, and it
  is exactly what `CLAUDE.md` means by *"a prior that is a policy caps the ceiling"*.
  The policy would farm the bounty.

### Why it ranks below money potential

A hand-built chain PHI encodes our belief that animals matter.
Money PHI encodes nothing — and **a working animal chain makes money**, so money PHI already pays for
any chain that works while naming none of them.
That is the answer to "reward any successful chain and let it learn which to use": money is that
reward.

It is also aimed at the wrong gap right now.
`jax_heuristic` (`farm`) buys **zero** animals — `jax_heuristic.py:224` is literally
`buy_animal=jnp.zeros(...)` — and it beats us 8/0.
We are losing to a pure crop agent while playing crops.
Animals are the second problem.

---

## 3. A rung that melon cannot beat

**Status: proposed today, not built. Depends on closing the execution gap first.**

Gradient lives where the outcome is marginal. Today:

```
vs farm    0 / 8        we $12,478   they $28,168
vs ranch   0.263 / 19x
vs home    0.000 / 6x
vs pool    0.620 / 50x   <-- essentially all of the gradient
```

The hopeless rungs contribute a uniformly negative advantage that says "everything you did was bad"
with no successful example to point anywhere — directionless, and consistent with entropy climbing
from 5 to 9 since update 250.
Meanwhile the one rung near 0.5 is `pool`, which is past copies of ourselves. Melon players.
Beating them needs no animals.

So the ladder contains nothing that is **both beatable and unbeatable-by-melon**.
Even a spontaneous, perfectly executed animal chain would win nothing extra, so there is no signal
for it to find. This is Alex's point and it is correct.

The fix is a rung deliberately placed in the gap — above melon-only, below melon-plus-animals.
A weakened rancher, or the graded ladder originally proposed for `idle` applied to the animal
opponents instead.

**Caveat before building it:** advantages are normalised per minibatch across all rows, not per
opponent, so the hopeless rungs do contribute *something*. Whether that something is useful or noise
is measurable from logs we already have, and should be measured before designing around it.

---

## Related open items

Tracked in the task list rather than here: rollout-vs-update timing instrumentation, the weeds
re-measurement of every JAX agent number, the pool anchor that is still the random init,
`jax_frontier`'s pen bug, and the dead seed-day plot panel.
