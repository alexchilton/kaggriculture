# Fable review: the delivery node after the cost-model dead end

2026-08-07, second review of the day.
Requested: given that honestly pricing the missing DROP/depot turns makes day-matching worse
(commit e904e4f, both constants shipped at 0), is a delivery node in `build_nodes` still right;
is there a cheaper executor-side path; why d2 breaks under every arm; where the reasoning is wrong.
Read: `kagg/search/router.py` (constants and post-mortems at 200-242, `delta`/`homeward`/`cdelta`
at 700-798), `kagg/search/schedule_agent.py` (draw ferry at 754-772, tour walk, opportunistic drop,
`DELIVER_THE_SELL_ROW` at 853-862, return leg at 886-896), `docs/service_undercount_2026-08-07.md`,
`docs/idle_at_h10_2026-08-07.md`, my own earlier note.
One measurement run: d2 under `HOMEWARD_DROP_TURNS=1` via monkeypatch
(`scratchpad/d2_probe.py`, no repo edits), reported in §3.

## 0. The one new fact, measured this session

Under `HOMEWARD_DROP_TURNS=1`, d2 goes 4 -> 6 cells, and the two cells that flip are **`east` and
`west`**.
Every tile work op — plant, water, harvest, feed, care, sell — is identical in both configs on
d0-d2; the "work" row's movement is entirely pickup/drop.
Baseline d2's four differing cells are `north`, `south`, `pass`, `pickup` — also no tile work.

So the cost arms never damaged d2's plan.
They re-permuted which unit takes which node, and the compass-cell coincidences dissolved.
That reframes all four questions.

## 1. Is a delivery node in `build_nodes` still the right move? No. Withdraw it.

My earlier note said yes-after-the-stale-budget-fix.
Both halves of that are now dead, for measured reasons, and I withdraw the recommendation rather
than re-gating it.

**The prerequisite is discharged, not pending.**
The stale-budget theory from the router post-mortems was checked and found wrong: budgets are
recomputed fresh every turn, idle tours finish 6-14 turns early
(`docs/idle_at_h10_2026-08-07.md` §2a, §3).
And the residual mystery that doc left open — u1's tour overrunning its closed cost by ~2 — is
explained by the service probe: `Node.service` under-counts by 27% on field tiles and 48% at depots.
There is no remaining unexplained defect for a router fix to shelter behind.

**The under-count is not a bug awaiting a fix; it is the calibration that matches the tape.**
Your reading is right and should be said stronger.
Seb's own days overpack any honest per-stop estimate — his d10 spends 43 more moves than us to buy
8 more work ops — and the executor's stay-until-`_live_ops`-is-empty behaviour is exactly what
makes an overpacked plan executable.
`service = len(ops)` is wrong about the quantity it names (turns at the stop) and right about the
quantity that matters (how much a day can absorb before the plan stops resembling his).
The e904e4f sweep is the proof: correct prices, worse reproduction, every arm.
So the constants staying at 0 is not "a measured dead end" in the sense of a fix deferred; it is
the model, and it will not move.

**And a delivery node cannot live inside that model.**
The failure my earlier note flagged as risk (a) is now unconditional:

- Priced honestly, its prize is ~10% price drift plus the gating value of an earlier bank.
  The drift is small and the gating value is unknowable at `build_nodes` time — it depends on what
  the purchase queue does with the money hours later.
  Under prize/cost ranking against rivals that are all 11-48% too cheap, it inserts last and is
  refused.
  A node that is always refused is dead code.
- Made `mandatory`, it is placed before every optional node (`plan_routes` places the mandatory
  pool first, unconditionally), so it restructures every yielding tour's spine on every day it
  exists — including days that are currently exact.
  §3 says what that costs: any re-permutation of assignment flips compass cells, and the in-order
  metric charges those at full price on the earliest day touched.
  On slack-poor days (d0 has +1 pass, effectively zero surplus) a forced mid-tour depot stop
  displaces a real op outright.

So yes to your conclusion, and further: it is not that a mandatory node "would just displace real
work", it is that *any* `plan_routes` change — node, constant, or marginal — pays the permutation
tax at d2 before it can show value at d6+.
The router is effectively frozen by the metric, and the intervention channel that remains is the
one that leaves the dawn assignment untouched: the executor.

## 2. The cheaper intervention: a mid-tour deliver ferry, mirroring the draw ferry

The executor already contains the exact shape needed, pointing the other way.
The draw branch (`schedule_agent.py:754-772`) preempts a committed tour: if the tour's `draw` is
unsatisfied and the unit is off-depot, it steps toward home, does the depot action on arrival, and
resumes the tour.
Nothing about that touches `plan_routes`.

The missing piece is one branch of the same shape:

    if (a threshold of the load is owed to today's sell row) and pos not in depots
            and the detour fits in slack:
        step toward nearest depot

On arrival, **no new depot code is needed**: the tour walk chooses a MOVE back toward the next
stop, and `DELIVER_THE_SELL_ROW` (855: `act[0] in STEP ... and pos in depots`) fires as it stands —
DROP, `owed_sale` decrement, capacity guard, and the draw branch re-draws any wheat the
all-or-nothing DROP dumped.
The flag stops being able to fire only on incidental visits, which was the 16/22 ceiling in my
earlier note, without the router learning anything.

Concrete conditions, in the order they should gate:

- **Census: reuse `deliverable`** exactly as at line 853 — `min(q, owed_sale[it])` summed —
  with the same `MIN_SELL_ROW_DROP` floor.
  This inherits the wheat-only-ferry exclusion for free.
- **Slack, not value.** Your framing "remaining route worth less than the load" is the wrong test.
  The route is not abandoned — it is resumed after the drop — so the comparison is never
  load-value vs route-value; it is detour cost vs spare turns.
  `slack = (TPD - hour - 1) - est_remaining(route)` where `est_remaining` is the leg distances
  plus `n.service` plus the homeward reserve; divert iff
  `dist(pos, home) + 1 + dist(home, next_stop) - dist(pos, next_stop) <= slack - MARGIN`.
  Because `service` under-counts ~27%, `MARGIN` must exist; start at 2-3 turns flat rather than a
  multiplier, and let the d0-d3 gate set it.
  Only when slack is insufficient does a value question even arise, and there the answer is almost
  always "keep the route": the load sells overnight at ~-10% while an abandoned FEED can cost the
  animal.
  So: divert on spare slack only, never abandon.
- **Do not widen the return leg's `not st["route"]`.**
  The divert branch supersedes it for carrying units mid-tour; the return leg keeps its current
  meaning (tour done, walk in, drop) and the empty-hands walk-home from
  `docs/idle_at_h10_2026-08-07.md` Fix A stays a separate, orthogonal change.
- **Placement in `_router_acts`:** after the tour walk chooses `act` (so a real op at the current
  tile always wins), before the opportunistic drop.
  It replaces a MOVE with a different MOVE — it can never delete a work op on the turn it fires.

Why this can pass the gate that killed every router arm: it does not touch dawn assignment, it
fires only mid-tour with owed sellables in hand and measured spare slack, and early days are both
slack-poor and sell-row-small, so it should be near-inert on d0-d3.
The regression sentinel is the same as ever — run `--days 12 --diff` and read d0-d3 before
looking at d6+.
If d2 flips a compass cell, tighten the `deliverable` floor or raise `MARGIN`; do not add an
hour dial.

The pytest, per the house rule: build a unit mid-tour, off-depot, holding `MELON 12` with
`owed_sale["MELON"] >= 12`, remaining route short against budget; assert the emitted act is a step
toward the depot, not the step toward the next stop.
Red today.
Guard assertion: same state with slack below the detour, assert it steps toward the next stop —
green before and after, so the fix cannot over-fire.

## 3. d2 is not fragile. It is finished, and it is measuring churn.

The targeted look (one run, `HOMEWARD_DROP_TURNS=1` monkeypatched, days 0-2):

    baseline d2 cells:   north -7, south -5, pass +8, pickup +1        (4)
    homeward=1 d2 cells: north -8, south -4, pass +13, pickup +2,
                         east -4, west -2                              (6)

    tile work ops (plant, water, harvest, feed, care, sell): identical in BOTH configs, d0-d2.

d2 at 4 cells has no work left to lose on the board — its entire residual is walk geometry plus
one pickup.
`east 0` and `west 0` in the baseline are coincidences of the current assignment permutation:
cheapest-insertion happens to distribute nodes so the compass sums match his.
Any change to any insertion cost re-permutes the assignment and the coincidence dissolves —
which is why *every* arm breaks d2, and why the breakage carries no information about whether the
arm helped or hurt the plan.

Two consequences worth recording:

- **d2's remaining 4 cells are probably irreducible by router means.**
  Matching his compass counts cell-for-cell requires matching his actual tour geometry, which
  cheapest-insertion reproduces only by accident.
  Fixing d2 further is a different project (imitate his tours, not his day totals) and should not
  be a side-quest of the delivery work.
- **d2 is a churn detector, and it is useful as exactly that.**
  A change that leaves d2 at 4 has left the dawn permutation alone; a change that moves d2 has
  perturbed it, whatever else it did.
  For *judging* router changes it would be worth printing work-cells and walk-cells as separate
  counts — the official metric stays the scoreboard, but a d5 sell cell gained should not be
  vetoed by a d2 west cell lost without at least seeing the split.
  Suggestion only; the metric is yours.

## 4. Where you are wrong, bluntly

- **"Systematically ~11-48% too cheap for everything else" is the wrong description going
  forward.**
  It was the right measurement and the wrong conclusion-shape: it implies a debt to be repaid.
  The e904e4f sweep repaid it and got a worse reproduction, because the tape overpacks too and the
  executor absorbs the overrun.
  Call it what it now is — the packing calibration that matches the tape — or a future session
  will read the probe numbers, "fix" the constants, and re-run the dead end.
  The comment block at router.py:231-236 already says most of this; it should also say the d2
  mechanism (§3), because "every arm regresses d2" without the compass-cell fact still reads like
  the arms damaged the plan.
- **"Anything adding a stop must EARN its turns" — half right.**
  Right as a principle, wrong about the ledger.
  Earning in `plan_routes`' prize/cost ranking is impossible for a delivery stop: its prize is
  gating value, which is not computable at plan time (§1).
  Earning against the executor's live slack is computable every turn, and §2 is that test.
- **d6/d7/d8 improving under homeward=1 is not "the direction has something in it".**
  Three mid-days improving while d2/d5 regress and d10/d11 worsen is what permutation churn looks
  like: reshuffles help some days and hurt others, and the in-order metric just decides which you
  read first.
  §3 shows the mechanism is churn on the day it was measured.
  Do not bank the direction; the deliver ferry stands on its own argument, not on that row.
- **My own earlier note is the fourth thing wrong here.**
  It gated the delivery node on a stale-budget fix that turned out to chase a defect that does not
  exist, and it sketched the node itself (per-unit synthetic node, precedence via chain-style
  assignment) inside a cost model the same note admitted was miscalibrated.
  The opus investigation and the e904e4f sweep between them retire both halves.
  The census caveat from that note survives — a rule that only fires at the depot cannot send a
  unit there — and §2 is now the answer to it, at the executor, where the last third of the gap
  can actually be reached without paying the d2 tax.

## Verdict in one line

No delivery node in `build_nodes` — the router is frozen by a metric that charges permutation
churn at full price on d2, and the cost model it would price against is now known to be
calibrated-wrong-on-purpose; put the walk in the executor instead, as a mid-tour deliver ferry
mirroring the draw ferry at `schedule_agent.py:754`, gated on spare slack (never load-vs-route
value, never abandonment), landing on the existing `DELIVER_THE_SELL_ROW` branch for the drop
itself, with d0-d3 cells unchanged as the acceptance test.
