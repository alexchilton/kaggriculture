"""Optional potential-based money shaping: zero at the starting stake, convex above it.

**Status: built, tested, and not wired into anything. `coef` defaults to 0.0, which is byte-exactly
off.** Whether to use it is an open decision -- see the trade-off at the bottom.

**The idea is Alex's**, in three parts: put the zero at $3,000 so hoarding earns nothing, scale with
money above that, and make the scaling convex so "$5 more than a broke mirror" is worth almost
nothing while a real farm is worth a lot.

**The form is what makes it safe.** Adding `f(final_bank)` to the terminal reward would change the
optimum to margin maximisation, which an Elo ladder does not score -- `CLAUDE.md`: *"A $43k win and a
$4k win score identically."* Adding `F(s, s') = gamma * PHI(s') - PHI(s)` per step instead leaves the
optimal policy **provably unchanged** (Ng, Harada & Russell 1999). Its entire effect is to relocate
credit in time, which is the actual complaint rather than a wish about the objective.

**The problem it addresses.** To plant a melon the policy spends seed money now and sells the crop
~240 turns later. With `--horizon 32` and `--gae-lambda 0.95` the credit window is ~20 turns, so the
*cost* lands inside it and the *benefit* lands far outside. The policy experiences the spend and
never the payoff, which is consistent with everything measured: it ends every season on $0
(`docs/bankrupt_every_game_2026-08-03.md`) while HARVEST runs 0.18-0.24% of ops. Per-step differences
put both halves on the turns they happen.

**Why it is not simply the per-step bank delta** that `CLAUDE.md` marks *"NO LONGER IN FORCE"*. That
was `PHI = money` -- linear, unfloored, and therefore paying for thrift, since clawing back the stake
raises it. Flooring at the opening stake makes the whole $0-$3,000 region flat, so going broke is not
punished and hoarding is not rewarded; only *earning* moves it. The convex exponent then does the
rest of Alex's requirement.

**It composes with P2b rather than replacing it** (`kagg/rl/opportunity.py`). P2b resumes the episode
next to a ripening crop, but the episode still runs to day 30, so credit from the harvest to the
terminal win still has to flow through the critic -- the one component this project has not verified.
This term makes the harvest pay on its own turn without depending on the critic at all.

**The trade-off, stated so it can be weighed rather than assumed.** For: bounded downside, since
policy-invariance is a theorem and not a judgement call; and it does not need the critic to work.
Against: one more hyperparameter (`coef`) that nobody can set a priori, and switching it on mid-stream
makes runs incomparable. The natural decision point is the 30M-turn read -- if `bank_final_med` is
still $0 then, the critic is not carrying credit and this is the cheapest thing that does not rely on
it.
"""

import jax.numpy as jnp

# **Was $3,000, the opening stake. Moved to 0 on 2026-08-03, and the reason is measured.**
#
# The floor existed so hoarding earns nothing: clawing the stake back is thrift, not production. That
# reason is right and the mechanism was wrong, because the **convexity already does it**, far more
# sharply than a hard floor. At `EXPONENT = 2` a $3,000 bank is worth 1.1% of a $28,168 season and a
# $1,856 bank is worth 0.4%. Thrift is already worthless.
#
# What the hard floor added was a **dead zone**. `day0-long-20260803-200350` saw `bank_final_med` fall
# $20,655 -> $1,856 over 300 updates, so the policy spends whole seasons entirely below $3,000 where
# `PHI` is identically zero -- no gradient in precisely the region that needs one. Alex's requirement
# was "0 for 0, much much more for 100k", and `FLOOR = 0` satisfies it literally.
FLOOR = 0.0

# **The cap.** `PHI` was unbounded, so at $110,000 it read 1.21 and at `--shaping-coef 6` contributed
# 7.3 against a terminal reward of 1.0. Invariance does not protect against that: Ng's theorem fixes
# the optimum, not what PPO does with a term that swamps the objective, and the sigmoid value head
# cannot represent it either. `SCALE` was already chosen so a top-of-leaderboard season lands near 1.0,
# so the cap binds nowhere we can currently reach and makes `--value-margin` computable rather than
# guessed. Clipping is safe: `F = gamma*PHI(s') - PHI(s)` telescopes for *any* PHI.
CAP = 1.0

# $100,000 above the stake, close to the $106k and $113k the top two agents banked in episode
# 89197802 (`CLAUDE.md`). Normalising there puts a realistic winning season at PHI ~ 1, the same
# order as the terminal reward, rather than dwarfing it.
SCALE = 100_000.0

# > 1 makes it convex: the same $1,000 is worth far more at $90k than at $4k, which is what
# separates a real farm from a $5 win against an equally broke mirror.
EXPONENT = 2.0

# **Off.** A run with this at 0 is byte-identical to a run made before the term existed.
DEFAULT_COEF = 0.0


def potential(money, floor=FLOOR, scale=SCALE, k=EXPONENT):
    """`PHI(s)` -- zero at or below `floor`, convex above it, reaching 1.0 at `floor + scale`.

    Clipped rather than signed. A signed potential would pay the policy for clawing its stake back
    toward $3,000, and recovering the stake is thrift, not production -- the incentive Alex objected
    to in the graded-opponent proposal and the reason that proposal was dropped below $3,000.
    """
    above = jnp.maximum(jnp.asarray(money, jnp.float32) - floor, 0.0)
    return jnp.minimum((above / scale) ** k, CAP)


def shaping(money_before, money_after, coef=DEFAULT_COEF, **kw):
    """`PHI(after) - PHI(before)`, elementwise, preserving shape.

    `gamma` is 1.0 throughout this project (`CLAUDE.md`, and `--gamma-per-day 1.0` on every current
    run), so the discount factor in `gamma * PHI(s') - PHI(s)` is the identity and is omitted rather
    than threaded through. If a discount ever returns, it belongs here.

    The terms telescope, so an episode's total shaping is `PHI(end) - PHI(start)` whatever path was
    taken -- which is what makes it unable to pay for a detour, and is checked directly in
    `test_the_shaping_telescopes_so_only_the_endpoints_matter`.
    """
    return coef * (potential(money_after, **kw) - potential(money_before, **kw))
