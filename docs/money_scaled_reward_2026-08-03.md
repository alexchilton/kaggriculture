# Should the reward scale with money?

**Date:** 2026-08-03.
**Asked by:** Alex, immediately after proposing the graded-`idle` ladder.
**Answer:** the uniform-stake opponent already gives you the gradient a money-scaled reward would
give you, over exactly the range where it is missing, and stops giving it at exactly the point where
a money-scaled reward would start doing damage.

## The three things that could be meant

They are not the same and only one of them is dangerous.

### 1. Terminal reward proportional to final bank — `reward = money / SCALE`

**This changes the objective, and to the wrong one.**

`CLAUDE.md` records the measurement: *"Select on win rate, not money. The leaderboard is an Elo-style
rating. A $43k win and a $4k win score identically."* A money-scaled reward trains margin
maximisation, which is not what is scored. The same file records what that cost before — *"A mirror
match is not a best response... Melon went 25 → 12 → 25 because a mirror sweep pointed the wrong
way"* — a case of optimising a proxy that pointed somewhere the real objective did not.

There is a concrete failure mode here, not just a principle. `ranch` banks $12,078 and `farm` up to
$30,292, and both are currently unbeatable. Under a money-scaled reward, losing to `farm` by $30,000
is enormously worse than losing by $3,000 — so the strongest available gradient becomes *minimise the
margin of an unavoidable loss*, which is satisfied by hoarding and doing nothing. That is the
do-nothing fixed point (`train_jax_rl.py:340-343`, `:392`), and this would actively pay for it.

### 2. Per-step bank delta — the potential-based version

**Provably safe, and already overruled, and the two facts are related.**

The theoretically clean way to shape is Ng, Harada & Russell (1999): $F(s,s') = \\gamma\\Phi(s') -
\\Phi(s)$ leaves the optimal policy unchanged. With $\\Phi = \\text{money}/\\text{scale}$ and
$\\gamma = 1$, the sum telescopes to $(\\text{money}_{\\text{final}} -
\\text{money}_{\\text{initial}})/\\text{scale}$ — which **is** the per-step bank delta that
`docs/rl_feasibility.md` argues for at length and that `CLAUDE.md` marks *"NO LONGER IN FORCE"*.

The policy-invariance theorem is a double-edged result. It guarantees shaping cannot break the
objective; it equally guarantees that at convergence it adds nothing the terminal reward did not
already contain. Its entire value is **faster credit assignment**, which is a real benefit and is
exactly our complaint. So this option is defensible on the merits — it was overruled as a decision,
not refuted as a technique.

Against it: of the top finishers whose write-ups we have, four used a terminal signal (Felix Neumann
−1/+1, simjeg terminal at γ=0.995, Isaiah Pressman terminal, Ender positive-only 0/1/2 at γ=0.998)
and **none used a per-step bank delta**.

### 3. A graded opponent — no reward change at all

This is the proposal from `docs/graded_idle_ladder_2026-08-03.md`, and it is worth restating what it
achieves, because it is what option 1 is reaching for.

With the opponent's stake drawn $S \\sim U[0, 3000]$, a trainee finishing on bank $B$ gets

$$\\mathbb{E}[\\text{reward}] = P(B > S) = \\frac{B}{3{,}000} \\quad \\text{for } B \\in [0, 3{,}000]$$

**That is a reward linear in money.** Not an approximation of one — exactly one, in expectation, over
precisely the interval where the current reward is flat.

## The comparison that settles it

| | gradient over $0–$3,000 | behaviour above $3,000 | changes the objective? |
|---|---|---|---|
| terminal money-scaled | linear | **keeps scaling — pays for margin forever** | **yes, to margin** |
| per-step bank delta | linear (and dense in time) | keeps scaling | no (policy-invariant), but see below |
| **uniform-stake `idle`** | **linear** | **saturates at 1.0** | **no — it is still win probability** |

The decisive row is the middle column. A money-scaled reward cannot tell the difference between "$0
is bad" and "$30,000 beats $28,000", so it keeps paying for margin long after margin has stopped
being worth anything on an Elo ladder. The uniform stake pays exactly the same gradient across the
dead interval and then **saturates**, at which point `idle` ($3,000), `trade` ($3,368),
`carrot` ($3,410), `ranch` ($12,078) and `farm` ($30,292) take over as the next rungs — each of them
still a clean win/loss.

Put plainly: **the graded opponent is money-scaled reward with a correct upper boundary condition,
implemented as an opponent instead of as a reward.**

## The other reason to prefer the opponent

The standing lesson (`~/.claude` memory, `feedback_dont_shape_rewards`) is that when a policy is not
learning, the reflex to add reward to persuade it is usually treating a symptom — the cause is more
often delivery, plumbing, compute or exploration.

Here we have a diagnosis, and it is none of those and it is also not reward *design*: the reward
function is correct, and the **opponent set** makes it constant over the occupied range
(`docs/the_reward_is_a_step_function_2026-08-03.md`). The fix belongs where the fault is.

That also makes it cheap to reverse. A stake distribution is a flag; a changed reward function is a
changed loss, a new failing test, and every prior run made incomparable.

## "0 for 0 and much much more for 100k"

Alex's clarification, and it targets something the analysis above understates.

**He is right that a $5 win is a fake win.** The pool win rate of 0.473 is earned by ending a season
on $5 against a frozen copy that ended on $0. That result transfers to nothing: the agents this
competition is actually scored against banked **$106k and $113k** (`CLAUDE.md`, episode 89197802).
A reward that cannot tell $5 from $100,000 is indifferent between a policy that will be crushed and
one that will win — which is precisely Fable's finding that nothing in this pipeline ever plays the
real field. Money is the available proxy for "would this beat the $106k agents".

So the question is how to get a strongly convex reward-versus-money curve. **It turns out not to
require touching the reward at all.**

### The reward curve *is* the opponent's stake distribution

For a trainee finishing on bank $B$ against an opponent whose stake is drawn $S \sim \mathcal{D}$:

$$\mathbb{E}[\text{reward} \mid B] = P(B > S) = F_{\mathcal{D}}(B)$$

**Whatever reward-versus-money curve you want, choose the stake distribution whose CDF is that
curve.** It remains a strictly terminal win/loss reward against a real opponent — nothing is shaped,
`won = money > money[:, ::-1]` is untouched.

Uniform stakes give a straight line because a uniform CDF is a straight line. For "0 at 0 and much
much more at 100k", take a power law:

$$S = M \cdot U^{1/k}, \quad U \sim U[0,1] \qquad \Longrightarrow \qquad
\mathbb{E}[\text{reward} \mid B] = \left(\frac{B}{M}\right)^{k}$$

With $M = 100{,}000$: $k=1$ is linear, $k=2$ quadratic, $k=3$ cubic. **One exponent is the entire
convexity knob**, and every draw is still a legitimate game with a win and a loss.

### Why a *fixed* convex curve is the wrong version, and what to do instead

A convex curve is flat near zero. At $k=2$, $M=100{,}000$, a policy finishing on $3,000 earns
$(0.03)^2 = 0.0009$ — it has reintroduced the dead zone at exactly the place the policy currently
occupies. The convexity that correctly devalues a $5 win also destroys the gradient that would get
us off $0.

The fix is to stop choosing a curve at all and let the bar track the policy:

**Draw the stake from the trainee's own recent final banks.** Keep a running buffer of
`bank_final` values and sample $S$ from it — or from a quantile modestly above it. Then the trainee
always faces a roughly even bar, so $F_{\mathcal{D}}(B)$ is steepest exactly where the policy sits,
and the gradient is maximal at every stage instead of at one. As the policy improves the distribution
walks up behind it: $0 \to \$3{,}000 \to \$12{,}000 \to \$100{,}000$, with no rung chosen by hand
and no dead interval ever.

That is prioritised fictitious self-play applied to the money axis rather than to whole opponents,
and it is the same principle as the frozen-checkpoint pool — *always play something a little better
than you* — expressed on the axis where this policy is actually failing.

It also delivers Alex's requirement as an **emergent trajectory** rather than a fixed curve: $0
stays worth 0, $100k ends up worth far more, and the policy is never asked to climb a wall it cannot
see the bottom of.

## Recommendation

1. **Do not scale the terminal reward with money.** It optimises margin, which the ladder does not
   score, and it pays for hoarding against opponents we cannot yet beat.
2. **Use a graded-stake `idle` instead** if the 30M read shows the step function is real. Start with
   uniform $[0, 3000]$ because it is one line and closes the measured gap; move to a stake drawn from
   the trainee's own recent `bank_final` if and when $3,000 becomes the new plateau. Same gradient a
   money-scaled reward would give, correct saturation, no change to the loss, reversible by a flag.
3. **Keep per-step bank delta in reserve, not off the table.** It is policy-invariant and the
   objection to it is a decision rather than a refutation. If the graded opponent lands and the
   policy still cannot cross $3,410 → $12,078 — the gap that needs real farming — a potential-based
   money term over that interval is the next thing worth arguing about, and it should be argued then,
   with the graded-opponent result in hand.

This is Alex's decision to revisit; `CLAUDE.md` records the terminal-reward rule as his call, made
explicitly, and nothing here is a reason he could not overrule it. The argument above is that he
should not need to.
