# Fable on the animal economy: my headline claim was refuted by my own data

**Date:** 2026-08-03, evening.
Requested after a 64-game replay of the update-500 checkpoint suggested the animal economy was
structurally locked out. It is not.

## The correction that matters

**I claimed "FEED has never once been legal". That is false, and the refutation was in the replay
output I had just produced myself.**

`data/logs/replay.log` reports raw FEED counts of **14** (idle/seat0), **131** and **82** (ranch,
both seats), **78** and **113** (farm, both seats), **10** (carrot/seat0). FEED fired against **all
four opponents**. `play_checkpoint.py:157` counts the *resolved* op — post-mask, post-`CM.resolve` —
so a count of 131 means an animal was standing on a tile and was fed 131 times in 32 games.

I read the two zero entries and generalised from them. The mask reading itself was accurate as a
description of the rule (`jax_masks.py:96`, `jax_sim.py:428`, `jax_sim.py:885` all check out, and
there is genuinely no shop-unlock gate on animals) — but *"the rule requires an animal"* and *"an
animal has never existed"* are different claims and the second one is false.

## Three more corrections

**`buy_animal` is not zero, it is rounding.** `buy_animal_rate` over the run:

```
update      GOOSE / COW  / SHEEP
     0      0.042 / 0.035 / 0.033
    40      0.001 / 0.001 / 0.001
   160      0.000 / 0.000 / 0.000
   490      0.000 / 0.000 / 0.000   <- the log line I quoted
   560      0.004 / 0.002 / 0.003
   651      0.002 / 0.001 / 0.001
```

Sub-0.05% rounds to 0.000 at three decimals, and still fires often enough across 30 days x several
units x 32 games to produce those FEED counts.

**`--spend-prior` is a floor, not a cap — I had it backwards.** `train_jax_rl.py:882-884`, about this
exact flag on this exact failure: *"Against an inert policy a 5% shape prior is a FLOOR, not a cap:
it pulls from below, which is the direction now wanted."* `hand_prior_heads` sets the "no purchase"
bucket to `log(1 - spend_p)` and spreads the rest.

The real finding, which I missed entirely: **the PPO gradient is beating that floor by roughly an
order of magnitude and has been for 650+ updates.** buy_animal craters from ~3.5-4% at init to
0.1-0.4% by update 40 and stays there. That is evidence the policy's own rollout experience reads
buy_animal as negative-EV — not evidence of a masking deadlock.

**The wheat-collapse mechanism is unproven, and the tool has a blind spot.** `play_checkpoint.py:60`
sets `EPISODE_TURNS = 719`; `TURNS_PER_DAY = 24`; the flow table computes `n_days = 719 // 24 = 29`
and floors the trace to `keep = 696` (`:179-180`). **The last 23 turns of every game never appear in
the buy/sell table.** And "bank by day" samples `money_t[::24]`, last index 696 — the *start* of day
29 — while "policy $ median" is `final.farm.money` at turn 718. Different timestamps:

| | d29 trace (turn 696) | true final (turn 718) | gap |
|---|---:|---:|---:|
| ranch, seat 0 | $388 | **$6** | $382 |
| ranch, seat 1 | $7,906 | **$4,690** | $3,216 |
| farm, seat 0 | $10,642 | $8,872 | $1,770 |

Summing the printed day-25-28 net flows for ranch/seat0 gives −$1,374 against a d25→final drop of
**$10,648**. Most of the collapse happens where the table cannot see. On the days it *can* see, sells
($1,406-$2,001) are comparable to buys ($1,740-$2,312) — so "buys and does not sell it" is not what
the visible data says. Something bad and specific to active-trading opponents happens, concentrated
late, and **we cannot currently see what it is.** Fix the day-29 gap before diagnosing further.

## The diagnosis that replaces mine

Not "the chain never starts" but **"the chain breaks mid-walk"**, and there is independent evidence:

- `commit.py:82-88` already measured the wheat leg — `COMMIT_FEED` alone delivered a unit actually
  carrying wheat only **22.9%** of the time, which is why `COMMIT_PICKUP` was added.
- The same signature is live now: `cFEED` commit rate runs **2-3x the executed FEED rate** in every
  replay condition (ranch/seat0: 0.34% committed vs 0.16% executed).
- **`PLACE` has no commitment and no geometry feature.** `jax_obs.py:223-226` exposes `needs_water`,
  `is_ripe`, `needs_feed` and `kind==EMPTY`, but no `empty_structure`; `commit.py:95` has no
  `COMMIT_PLACE`. So a successful purchase still has to survive an unassisted walk-and-place before
  FEED/CARE/COLLECT_FERT become reachable at all.

That is the one architecturally missing link, and filling it follows the precedent `COMMIT_PICKUP`
already set rather than crossing any new line.

## Ranking

1. **`COMMIT_PLACE` + an `empty_structure` geometry feature.** Not on my list. Fills the missing link
   using the project's own established pattern.
2. **Seed the shed.** Attacks the real bottleneck — reaching the far side of an unassisted multi-step
   chain — and reuses `curriculum.py`'s existing mechanism rather than inventing one.
3. **Shape prior on buy_animal — already running and currently losing.** `--spend-prior 0.05` *is*
   the config of the run being analysed. Proposing it as a fix was proposing the status quo.
4. **Graded `idle` — right idea, wrong problem, and not two lines.** It does nothing for the animal
   economy. And `seed_states` carries one uniform `starting_money` for every seat, so a per-role
   stake needs a genuine role-conditional override on `fresh.farm.money`, not just the reordering I
   described. Moving the role draw is a necessary precondition, not the fix.
5. **HRL / fake chain — don't, and this is not a fresh call.** `commit.py:90-94` already declined to
   combine PICKUP+FEED into one macro *despite a measured 77% miss rate*, warning that "the next step
   is the seven-op animal-acquisition chain, and by then the script is the strategy." A buy→place→
   feed→care→collect→sell macro is exactly that chain. If Alex wants it, it should be an explicit
   decision to overturn prior art, not something adopted because a log looked bleak.

## The caveat that turned out to matter most

Fable flagged that the run had already moved past the update-500 checkpoint the whole review analyses,
and to pull a fresh replay before acting. That was right, and understated. At update 679:

| block | `idle` | `ranch` | `farm` | `bank_final_med` | `money_max` | HARV % | buy_animal |
|---|---:|---:|---:|---:|---:|---:|---:|
| 400–479 | 0.800 | 0.000 | 0.000 | $5,623 | $20,071 | 2.47 | 0.0009 |
| 480–559 | 0.854 | 0.006 | 0.010 | $9,370 | $28,492 | 4.60 | 0.0048 |
| 560–639 | 0.874 | **0.013** | **0.138** | **$14,866** | **$34,127** | **8.01** | **0.0048** |

First wins against `ranch` and `farm`. `money_max` above what `farm` banks. HARV up 35x from its
low. **And `buy_animal` up 5x — the aversion is reversing without any intervention.**

So the entire animal analysis, mine and Fable's, was performed on a checkpoint the policy has since
left behind. The honest conclusion is that **none of the five ranked items should be actioned yet**,
and the day's real lesson is the one that keeps recurring: every confident diagnosis today has been
drawn from a window too short to support it, and every one has inverted.

## What is worth doing regardless

Fixing `play_checkpoint.py`'s day-29 blind spot. It is a measurement bug, it silently misreports the
last 23 turns of every game, and it will mislead the next person who runs a replay whatever the
policy is doing by then.