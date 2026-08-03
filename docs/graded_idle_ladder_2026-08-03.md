# A poorer `idle`: grading the opponent by its starting stake

**Date:** 2026-08-03.
**Proposed by:** Alex — *"it would be possible to add idle with starting money of 100, 250, 500,
1000, 2000"*.
**Status:** design note. Not implemented. The decision point is the 30M-turn read.

## Why this is the right shape of fix

`docs/the_reward_is_a_step_function_2026-08-03.md` found that the reward is piecewise constant over
$0–$3,000, which is exactly the range the policy occupies. This closes that with no new agent, no
reward change, and no new mechanism.

**`idle` is already all-zeros.** `train_jax_rl.py:352-353`: *"`NOOP` is op 0 and bucket 0 of every
market head is quantity 0, so all-zeros* is *that agent — no network, no parameters, nothing to keep
in sync."* And `:278` records that *"There is no upkeep line in this game — `_end_of_day` and
`_night` move no money"*. So an idle farm's bank is **constant for the whole season**: it ends on
exactly what it started with. Change the starting stake and you have changed the win bar, and
nothing else.

## The bar it actually sets

The trainee still starts on $3,000. So against `idle@$X` the bar is not "earn money" — it is
**"do not burn more than $3,000 − X of your stake."**

| opponent | trainee must end above | i.e. may burn at most |
|---|---:|---:|
| `idle@100` | $100 | 96.7% of the stake |
| `idle@250` | $250 | 91.7% |
| `idle@500` | $500 | 83.3% |
| `idle@1000` | $1,000 | 66.7% |
| `idle@2000` | $2,000 | 33.3% |
| `idle` (existing) | $3,000 | 0% |

That is a smooth curriculum on precisely the axis the policy is currently failing — it ends on $0,
having burned 100% — and every rung is still a clean terminal win/loss. **No reward shaping.**

## Why it should produce a gradient where nothing else has

The policy already observes the target. `jax_obs.py:244` computes `opp_money = farm.money[:, ::-1]`,
and lines `:305-308` put **the opponent's bank and the signed difference `farm.money - opp_money`**
into the observation. The win condition is literally `that feature > 0`.

Today that feature's target is always 3,000 / 12,078 / 30,292, all unreachable, so it is a constant
the policy can safely ignore. Graded stakes turn the single most decision-relevant input in the
observation into something that varies and can be acted on.

## How it wires in

The restart path already rebuilds seat state from `seed_states`:

```python
fresh = seed_states                                             # :561
restart = just_done | truncate
nxt = nxt._replace(farm=jax.tree_util.tree_map(pick, fresh.farm, nxt.farm), ...)   # :565-568
```

and the role is re-drawn for exactly those slots twenty lines later:

```python
drawn = jax.random.categorical(krole, role_logp, shape=(batch,))
nxt_roles = jnp.where(restart, drawn, roles)                    # :633-634
```

**One ordering change is needed:** `drawn` is computed *after* `pick` runs, so the stake override has
to know the new role first. `drawn` depends only on `key` and `role_logp`, not on `nxt`, so moving
the role draw above the `pick` is safe. Then seat 1's stake is a gather on the drawn role:

```python
stake = IDLE_STAKE[drawn]                       # $3,000 for every non-graded role
fresh_money = fresh.farm.money.at[:, 1].set(stake)
```

**Separate roles, not one role with a random stake.** A single `ROLE_IDLE` with a sampled stake would
collapse all five rungs into one `wr_idle` and hide exactly the ladder we are trying to watch. Five
roles costs entries in `ROLE_NAMES`, `role_p`, the CLI fracs and the `wr_*`/`draws_*`/`games_*` log
fields — mechanical, but it is five places and `CLAUDE.md`'s rule about adding an op to `SCRIPT_OPS`
and `_dense_actions` in the same commit is the same species of rule.

## Checks that do *not* break

- **`seat_loss`.** `V(seat0) + V(seat1) = 1` still holds: one seat wins, one loses, whatever the
  stakes.
- **The "mean terminal reward is 0.5 by construction" check** (`:35`). That is a property of both
  seats being in the buffer, and asymmetric stakes do not change one-winner-one-loser. It is already
  not 0.5 over *trainable* rows against scripted opponents (it is 0.000 today), so nothing new
  breaks.
- **`idle`'s behaviour.** All-zeros is all-zeros regardless of bank; NOOP does not consult money.

## The real risk, stated plainly

**A do-nothing policy banks $3,000 and beats every rung on this ladder.** The source already names
this failure — `:340-343`, *"It was converging to do-nothing, not learning to win"* — and `:392`
notes an idle farm is a *stable fixed point* in this game, unlike Ender's.

So these rungs teach "stop burning your stake", which is necessary and is the trivial half. They
cannot teach earning, and they cap out at $3,000. The ladder above must stay in the mix to keep
pressure on:

```
$100 $250 $500 $1000 $2000   <- proposed, closes the dead interval
$3,000   idle                <- existing
$3,368   trade               <- IMPLEMENTED, currently at 0%
$3,410   carrot              <- IMPLEMENTED, currently at 0%
$12,078  ranch
$30,292  farm
```

`trade` and `carrot` are free rungs immediately above the do-nothing ceiling and are switched off
right now. Turning them on is a flag, and it is what stops $3,000 from becoming the new plateau.

The remaining gap is $3,410 → $12,078, and that one is legitimate: crossing it requires actually
farming, which is the thing we want learned rather than laddered around.

## Decision point

Do not build this yet. `docs/the_reward_is_a_step_function_2026-08-03.md` states a prediction the
live run tests for free: **`bank_final_med` climbs while `wr_idle` stays at exactly 0.000, snapping
only at $3,000.**

- If it snaps, the dead interval is real and this is the fix.
- If `wr_idle` rises *gradually*, the step-function reading is wrong and none of this is needed.

Reading it costs nothing and is due at the 30M-turn checkpoint.
