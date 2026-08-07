# Fable review: DELIVER_THE_SELL_ROW, the depot as a route node, and the d10 idle gap

2026-08-07. Requested: verdict on shipping `DELIVER_THE_SELL_ROW`, whether the executor is the right
layer, the d10 idle anomaly, and any holes in the reasoning.
Read: `kagg/search/schedule_agent.py` (flags at 60-216, drop/deliver/return-leg at 754-850),
`kagg/search/router.py` (delta/homeward/cdelta at 661-759, chain pass at 776-815, the two reverted
closed-tour attempts at 688-700 and 729-736), plus the d9/d10 field tables supplied.

## 1. Ship it ON.

The honest reading of the criteria first, because they do not actually tie.

The strict cell-vector-in-order reading says OFF: both configs are identical d0-d9, and the first
day where the vectors differ is d10, where OFF is 18 and ON is 19.
But that reading only holds if d10's cells are measuring the same thing in both configs, and they
are not.
OFF's d10 sell row goes 35/35 on a backlog that happens to equal his row — your own words, and the
right ones.
That is two errors cancelling: we undersell d9 by 12, the shortfall arrives as backlog, and
`CUMULATIVE_SELLS` re-offers it on a day whose row it coincidentally completes.
The cell metric scores the coincidence as a match.
"Optimise the artifact, not a proxy" applies exactly here: preserving an accidental d10 match by
suppressing the tape's real mechanism is patching the proxy.

Three further reasons ON wins:

- **The OFF advantage is not durable.** d0-d8 still carry 4-15 differing cells each.
  Any fix to those days changes the goods flow, which changes the d9 backlog, which dissolves the
  d10 coincidence anyway.
  You would be shipping OFF to protect a match that the very next earlier-day fix will destroy.
- **The in-order criterion, applied to substance rather than to the saturated cell counter,
  favours ON.** The earliest day where the two configs differ at all is d9, and ON is strictly
  closer there: sell 10/22 -> 16/22, next-dawn bank +$957.
  The counter cannot see it because `sell` is one cell whether we ship 10 or 16 — you said this
  yourself, and it is the decisive point.
  A metric that saturates must not outvote the thing it saturated on.
- **The mechanism is the tape's, verified.** Market reads the shed; unit actions resolve before the
  market phase; his h7 holds WOOL 8 and sells WOOL 8 the same turn.
  A reproduction that structurally cannot express same-day delivery is wrong in a way that
  compounds through every bank-gated decision downstream (your own file documents the cascade:
  the COW settling at h19, the half-filled seed order).

Ship it ON, and record in the flag comment that the 9-cell season regression is a
compensating-error artifact on d10+, so a future session does not "fix" it by turning the flag
back off.
One caveat on the value 6: the sweep separates 6 from 2/3/4 by a single cell on d5, on one seed and
one tape.
That is not evidence for 6 specifically; it is evidence for "somewhere in 2-6".
Do not let the comment imply the threshold is tuned — it is barely constrained, and it is fitted to
d9's particular cargo mix.

## 2. Yes, the depot should become a node — but the executor flag is the correct interim, and there is a stated prerequisite.

The ceiling argument is the caveat you flagged yourself: the census counts units standing on a
depot, and the flag fires only on incidental visits.
ON got 16/22, not 22/22.
The missing 6 need a unit to *walk* to the depot on purpose, mid-day, and no executor rule can
create that walk — only the router can, because only the router knows which tours will be holding
owed product and when.
So the router is the right layer for the last third of the gap, and the executor flag is the right
layer for the two-thirds it already captures.

But read your own file before building it: this exact economics has been tried twice at the router
layer and reverted twice — the closed-tour-as-reserve version (homeward docstring, router.py:729-736,
d3 sell 5/5 -> 3/5) and the closed-tour-in-the-ratio version (router.py:688-700, d3 sell and d4
place both regressed).
The post-mortem there names the real defect: `budget` is `TPD - hour - 1`, only idle units replan,
so a tour committed at hour 6 is walked all day against a budget that stopped being true at hour 7.
"Any next attempt should fix the stale budget first and re-measure" — that line governs this
attempt too.
A mid-tour depot stop inserted under a stale budget will replay the day-3 failure: units accept the
detour, the closing walk no longer fits, and two units are still walking home at hour 23.

Concrete sketch, in dependency order:

1. **Stale budget first.** On each replan tick, recost every committed tour against the live
   `TPD - hour - 1` and shed a tail stop when it no longer closes.
   Measure that alone against the tape before touching the depot; it is implicated in two prior
   reverts and may move d3/d4 on its own.
2. **A DELIVERY pseudo-node, per unit, not per tile.** After the chain pass and the general
   insertion pass, for each unit whose assigned stops will yield product in `owed_sale`: build a
   synthetic node, tile = nearest owned shed cell, service = 1 (the DROP) plus 1 if the load will
   be mixed with wheat its later stops need (the re-PICKUP the executor flag already pays), prize =
   the owed units it delivers.
   Insert it by `cdelta` like any node — but see risk (a).
3. **Precedence.** The delivery node is worthless before the yields that fill the hand.
   Cheapest-insertion has no order representation — router.py:776-781 says this in as many words
   for the animal chain, and solved it by assigning the chain whole.
   Do the same shape: restrict insertion positions to indices after the last owed-yield stop, and
   make `_two_opt` refuse reorderings that move it earlier (a validity predicate alongside
   `keep_prefix`).

Risks, named:
(a) prize double-counting — the yield stop already carries the harvest prize; the delivery node's
prize must be the *sale* margin of same-day settlement, which is small (~10% price drift plus the
gating value), so under plain prize-sorted insertion it inserts last and gets refused; it likely
needs to be mandatory-for-yielding-tours rather than prize-ranked.
(b) interaction with `depot_at[u]`: a tour can now touch the depot twice (draw stop at front,
delivery mid/late) and `delta`'s `off = 1` bookkeeping assumes one.
(c) the executor re-derives ops from the live board via `_live_ops`, which is tile-state-driven;
DROP is not a tile op, so the delivery node needs its own execution path — probably reusing the
existing DELIVER_THE_SELL_ROW branch, which then stops being a heuristic and becomes the executor
of a planned stop.
(d) day-3 is the regression sentinel: both prior attempts broke d3 sell 5/5 specifically; gate any
router change on d0-d3 cells unchanged before reading anything later.

## 3. d10 idle is probably the same defect, not a new one — prove it before investigating.

The signature: work 90/98 (close), move 132/175 (-43), idle 72/23 (+49), drop 9/16, pickup 11/13.
He does nearly the same tile-work but spends ~43 more turns walking and ~7 more shed round trips.
That is what a day full of mid-day delivery legs looks like: move-DROP-PICKUP cycles that our tours,
which visit the depot once at the front and once at the end, simply do not contain.
Our units finish shorter tours and sit.
Some of it is also money: $1,552 poorer at dawn gates errands into nonexistence (place 2/3,
pens 14/15 — something bank-gated slipped).

So the first measurement is free: rerun d10 with `DELIVER_THE_SELL_ROW` ON and recount
idle/move/drop.
If idle falls materially toward 23, it was the same defect and needs no separate line of inquiry.
If it stays near 72, then measure the per-hour, per-unit idle histogram next: a cluster at dusk
means tours are genuinely too short (nodes exhausted or unaffordable — a `left`-is-empty question
for the router), while idle spread through the day means units boxed or waiting, which is an
executor question.
Only after that histogram is it worth diffing his moving turns hour by hour.
Do not start with the hour-by-hour diff; it is the expensive measurement and the cheap one may
close the question.

## 4. Where I think you are wrong, or under-defended.

- **"Selling late costs ~10%, not selling costs 100%" is the wrong frame for this bug.**
  The 12 undelivered units are not unsold, they are sold a day late — the direct revenue cost is
  the ~10% drift, small.
  The real cost is entirely the gating: what the $1,552-poorer d10 dawn failed to buy or place.
  Your own d10 row shows it (place 2/3, pens 14/15).
  The price measurement is correct and beside the point; the flag's value should be argued from the
  gating cascade, not from price drift, or someone will one day divide $957 by the season and
  conclude the flag is marginal.
- **The threshold sweep is overfit and under-powered** — one seed, one tape, and the 6-vs-2
  separation is a single d5 cell.
  Said above; repeating it because the comment block currently presents 6 as "best" without that
  qualifier.
- **The 25 buy_seed retries are not automatically noise.** `FIT_ORDER_SLOTS` exists because order
  overflow silently deleted BUY_ANIMALs from day 11 while their bookkeeping stood.
  Sixteen single-unit retries are sixteen extra order-slot claimants; on any turn where they
  coexist with SELLs, HIREs, or a BUY_ANIMAL, they compete for ten slots.
  d9's own rows happen to balance, but check one thing before filing it as noise: on the retry
  turns, count the orders built.
  If any turn exceeds ten, the retries are displacing something and the "fix" from 176733c has a
  side effect on exactly the failure class this file has met before.
- **The depot-census caveat you flagged is the load-bearing fact of the whole question**, and it
  deserves promotion from caveat to headline: it is *why* 16/22 is the executor ceiling and *why*
  question 2's answer is yes.
  A census conditioned on being at the depot cannot observe the units that needed to be sent there.
- **One thing you got right that the file should keep saying loudly:** refusing to re-measure the
  broad -$15,272 arm and instead narrowing the trigger to the sell row was the correct move, and
  the narrowing really is the whole claim.
  The broad arm dumped feed a unit was carrying for its own stops; this one cannot touch a
  wheat-only ferry.
  They are different rules, and the twelve-seed number against the old one does not transfer.

## Verdict in one line

Turn `DELIVER_THE_SELL_ROW` ON (d10's cell win is two bugs cancelling and will not survive earlier-day
fixes); build the depot-as-node in the router *after* the stale-budget fix, with precedence handled
the way the chain pass already does it; and spend the first d10-idle measurement on simply rerunning
d10 with the flag on.
