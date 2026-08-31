# Fable: the per-turn hybrid split cannot work, and the row seam already exists

2026-08-28. Read-only review, requested by Alex after the hybrid measured $20 median against the
planner's $165,058. Fable ran nothing; every runtime below is its estimate, and the instrumentation
numbers it reasons from (86.7%, 0.755, 42/240) were supplied in the prompt.

## Verdict

The per-turn split -- planner emits ops, the net's bundle replaces `action["market"]` -- cannot work
and should not be repaired. The $20 is overdetermined by three mechanisms, and **only the third is
the coupling Alex named**. But "the market decides first and the planner services it" already exists
in the planner at *day-row* granularity, and that is the workable join.

## Why the hybrid banks $20 -- three mechanisms

The harness does `mine["market"] = orders`
(`scripts/the_planner_drives_and_the_net_supplies_the_market.py:86-90`).

1. **Amputation.** The planner's entire economy is market orders it builds itself
   (`schedule_agent.py:4594-5900`): HIRE :5248/:5283, BUY_LAND :5304, BUY_ANIMAL :5437,
   BUY_SEED :5527, feed BUY_PRODUCT WHEAT :5761/:5820, SELL :5114. The harness discards all of it.
   A one-quadrant, one-hand, no-revenue season is ~$20 **regardless of the net**.

2. **Phantom-crew dawn plans.** `PLAN_THE_CREW_THAT_ARRIVES = True` (:240) with
   `HIRE_PINNED_DAYS = frozenset(range(30))` (:1032). The h0 solve routes the hands
   `_hires_this_turn` (:391-404) says the market phase is *about to buy*, and credits `plan_supply`
   with the `buys`/`animals_bought` rows (:1885-1890). When the net does not post those orders, the
   day is planned for a crew and a shed that never arrive -- ":402, work planned onto a unit that
   does not exist is work deleted".

3. **Ledger poisoning -- not previously named.** The planner books orders *at construction*, not at
   fill: `state["ordered"][("sold", prod)] += n` (:5115), `state["bought"][a] += 1` (:5434,
   "incremented unconditionally"), feed ledger :5766-5767/:5822-5823. In the hybrid the full
   `agent()` runs, writes all of these, and the harness then throws the orders away. Future sells
   are capped by `allow - state["ordered"][...]` (:5019) against sales that never happened; animals
   are booked owned forever and never re-ordered. **Even a perfect market head would be sabotaged.**

So the hybrid table measured the harness, not the clone.

## Q1 -- "market first, planner services": implementable?

**Per-turn: no.** The only solve is `_router_acts` :1998-2004 and ":2006 NO REPLAN, NO TOP-UP. The
day is deterministic and is planned once, at hour 0." `_router_acts` takes no external order list.
Imposing per-turn orders means bypassing the 1,300-line market block and its ledgers and rewriting
`owed_sale`/`plan_supply`/`_hires_this_turn`/`_land_this_turn` -- the most defect-dense code in the
repo (OPEN-1, -3, -8, -12 all live there).

**Per day-row: yes, and nearly free, because the schedule row IS "the market decided first."**
The dawn solve already services the row as constraints: `wanted=owed_sale` (:2003),
`fund=short_of_cash` (:1864), `plan_supply` (:1885-1890), `_hires_this_turn` (:391, including
same-turn sell proceeds :411-425).

Precedent for imposing rows mid-game already exists: `_Q4.arm` (:4115, rewrites rows 9-29 on the d6
shop draw), `swap_in_geese` (:3174), `_herd_split`/`SHOP_ADAPT_HERD` (:2929), `_adapt_crops` (:3251).

The change is ONE seam: an optional `amend(day, sched, obs)` callback in `make_agent` (:4056),
invoked in the `if day != state["day"]` rollover (:4177) before anything reads `row`; threaded
through `TapeTeacher.__init__` (`kagg/il/tape_teacher.py:69-73`).

## Q2 -- the right decomposition

**Reject autoregressive ops->market.** CLAUDE.md's own rule: judge a technique against the problem
its author built it for. Autoregressive decode was built for joint-decode explosion, which the
256-way bundle head already solved (top-1 86.7%, P(EMPTY) 2.6%). Our failure is different -- on
planner states the head collapses to its prior (P(EMPTY) 0.755, zero SELL wants despite 234 of 256
vocab entries containing SELL). Conditioning on the planner's ops adds a *second* off-distribution
input, since it trained on カワシギ's ops history.

**The right join: the net emits day-row DELTAS at dawn; the planner services them.** Two caveats
Fable raises itself:

- The schedule rows already *are* カワシギ's day-aggregates on the fixed board, so a net predicting
  his rows adds nothing over the static schedule **except** his response to the shop-unlock draw --
  which OPEN-14 measured is exactly where his games diverge (identical for 74 turns, then divergence
  tracks the shop draw, not the opponent). The learnable object is small: row *adjustments*
  conditioned on the unlock draw. `SHOP_ADAPT_HERD` hand-codes this for one axis, `_Q4.arm` for
  another. **This is a retraining target, not a reuse of the per-turn bundle head.**
- The current checkpoint cannot be salvaged into that role.

Fallback if the row-delta net is not built: abandon the split and tune the planner's own market
parameters -- the never-run OPEN-CLI item, CMA-ES on the JAX sim over a direct market policy,
targeting OPEN-14's -$22,323 strawberry dump.

## Q3 -- decisions genuinely NOT coupled to unit ops

1. **SELL timing/quantity of shed stock above the feed reserve.** "The market reads the shed and
   nothing else" (:1834); reserve is `feed_days(day) * hungry` (:1855). Backward-coupled,
   forward-free. This is where the money is -- and the clone assigns ~zero mass to any SELL bundle
   on our boards, so it specifically cannot be the delegate for the one safely delegable decision.
2. **BUY_PRODUCT WHEAT restock.** Lands in the shed; existing FEED cadence services it; worst case
   is wasted cash. It is also the net's only persistent want (23 of 42 trading turns), and OPEN-3
   flags it as "the one strategic play we never make" -- the tape buys +164 product units and the
   winner drew ~83% of revenue converting bought wheat to milk/wool.
3. **HIRE count at h0 only.** Serviceable, but the schedule already fixes it. Low value.

Everything else -- BUY_ANIMAL, BUY_SEED, BUY_LAND -- is coupled at day-to-season scale and must go
through the row so the h0 solve can see it.

## Q4 -- three cheap discriminating experiments

- **E1, sell-mass probe (~5 min, first).** Add to `what_does_the_bundle_head_do_on_a_real_turn.py` a
  per-turn total probability mass on SELL-containing bundles, alongside shed contents and prices.
  If P(any SELL) stays ~0 even with a full shed at above-base prices, "delegate sells to the net" is
  dead without a season run.
- **E2, additive arm, BUY_PRODUCT only (~10-15 min).** Change the harness from replace to **append**:
  keep `mine["market"]` and add only the net's BUY_PRODUCT orders, under `MAX_MARKET_ORDERS` (:3840).
  The planner's ledger stays truthful -- no mechanism 3. Tests the entire transferable value of the
  checkpoint in the only safe join, and OPEN-3's buy-wheat hypothesis at the same time. Restricting
  to BUY_PRODUCT avoids `_uncap_sells` (`neural.py:105`) dumping reserved feed wheat.
- **E3, netless row imposition (~15 min).** No training: mutate `sched[day]["buys"]["WHEAT"] += N`
  on d5-d15 (row dicts are shared by reference through the shallow copy at :4064) and run 4 seeds.
  If the planner absorbs an externally dictated buy row, the `amend` seam is validated before any
  net is retrained. Precedent warning: the herd-ratio scaler generalisation halved the money
  (`170b8ef`, reverted) -- 4 seeds minimum, judge at the target days.

Decision table: E1 ~0 **and** E2 ~ baseline -> no transferable market signal; build the row-delta net
or tune the planner directly. E2 > baseline -> ship the additive wheat buy as a rule (the net was the
detector, not the mechanism), then build the row hook. E3 fails -> the row seam has a bug to find
first.

## Not verified (Fable's own list)

- It ran nothing; runtimes are estimates.
- Whether `masks_for`/`_bundle_sells` ever blocks BUY_LAND bundles in play.
- Whether `TapeTeacher`'s closure holds other state the order-replacement corrupts.
- `_process_market` fill semantics were read from code comments (:5108, :1868), not from
  `reference/kaggriculture.py`.
