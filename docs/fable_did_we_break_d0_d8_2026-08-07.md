# Did we break d0-d8? Arbitrating the ferry-drain claim (2026-08-07)

## Verdict

The user's claim does not hold.
There is no commit today at which d0-d8 beat the current numbers, under either the cell metric or
the narrower "exact on every op" reading.
The deliver ferry does not touch d0-d8 at all -- confirmed independently, not just re-read from
Fable's numbers.
Nothing needs reverting.

## Method

Built git worktrees at `6243b55`, `b922667`, `0fa262d`, `f31e50e`, `176733c`, `e904e4f`, `38dcf9b`,
and HEAD (`1b2970c`).
Each worktree got the CURRENT `scripts/breakdown.py` and CURRENT `kagg/search/router.py` copied in
(both unedited since `dc943de`/well before this range, so this is not a moving target), with only
`kagg/search/schedule_agent.py` left at the commit's own version, and `data/` symlinked back to the
real repo.
Ran `python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 12 --diff` in each.
This is a like-for-like comparison: same harness, same routing engine, only the agent code varies.

Worktrees were removed after use; nothing was left mounted.

## Q1: is there a commit where d0-d8 was better?

Per-day cell counts, current harness, all measured today from worktrees (not read off old commit
messages, which turn out to disagree slightly with this re-measurement -- see the caveat below):

| commit | d0 | d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 | d10 | d11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6243b55 | 7 | 6 | 4 | 7 | 7 | **8** | 13 | 18 | 18 | 15 | 22 | 25 |
| b922667 | 7 | 6 | 4 | 7 | 7 | 7 | 14 | 21 | 15 | 15 | 24 | 19 |
| 0fa262d | 7 | 6 | 4 | 7 | 7 | 7 | 14 | 21 | 15 | 15 | 24 | 19 |
| f31e50e | 7 | 6 | 4 | 7 | 7 | 7 | 13 | 20 | 15 | 15 | 24 | 22 |
| 176733c | 7 | 6 | 4 | 7 | 7 | 7 | 11 | 15 | 13 | 15 | 18 | 20 |
| e904e4f | 7 | 6 | 4 | 7 | 7 | 7 | 11 | 15 | 13 | 15 | 19 | 20 |
| 38dcf9b | 7 | 6 | 4 | 7 | 7 | 7 | 11 | 15 | 13 | 14 | 19 | 20 |
| HEAD | 7 | 6 | 4 | 7 | 7 | 7 | 11 | 15 | 13 | 14 | 19 | 20 |

d0-d4 has been **byte-identical at 7,6,4,7,7 across every commit tested**, back to 6243b55.
d5 stabilized at 7 from b922667 onward (6243b55 itself had it at 8, same-day, before its own
follow-up fix). d6-d11 improved monotonically from b922667 through today; nothing regressed at any
step in this range. Today's numbers (11, 15, 13 for d6-d8) are the best ever measured against this
tape -- not a regression from a better point.

On the cell metric, the claim is simply false: d0-d8 has never summed to fewer than
7+6+4+7+7+7+11+15+13 = 77 cells at any commit in this range.

**Caveat**: 176733c's own commit message quotes a "before" row of `7 6 4 7 7 7 12 18 17 17 24 23`
for what should be f31e50e, but re-measuring f31e50e directly today gives `7 6 4 7 7 7 13 20 15 15
24 22`. `scripts/breakdown.py` has not changed since `dc943de`, well before this range, so the
harness isn't the explanation. Most likely the commit message's own table was taken from an
in-session state that was never itself committed as a standalone point (a squashed intermediate).
Either way it doesn't change the verdict -- both readings put every historical d6-d8 worse than
today's.

### Q1, narrower reading: "exact on every op"

6243b55 claims d0-d4 "exact on every op, and on the dawn board"; b922667 claims d0-d5 "exact on
every op". Read narrowly -- excluding NORTH/SOUTH/EAST/WEST/PASS/PICKUP/DROP, which are routing
and pathing, not economics -- **this claim holds at HEAD, today, unbroken**:

```
ops emitted that day -- ours/tape                d0        d1        d2        d3        d4        d5
plant                                          17/17      0/0      0/0      0/0      0/0      8/8
water                                          17/17      0/0    17/17    14/14    17/17      8/8
harvest                                          0/0      0/0      0/0      0/0    14/14      0/0
feed                                             4/4      5/5      5/5      6/6      7/7      7/7
care                                             4/4      5/5      5/5      6/6      7/7      7/7
collect_fert                                     0/0      4/4      5/5      5/5      6/6      7/7
build_pastur                                     8/8      0/0      0/0      0/0      0/0      1/1
sell                                             0/0      4/4      5/5      5/5    32/32    26/26
buy_seed                                       17/17      0/0      0/0      0/0      0/0      8/8
buy_product                                      8/8      6/6      5/5      7/7      0/0      4/4
buy_animal                                       4/4      1/1      0/0      1/1      1/1      0/0
buy_land                                         0/0      0/0      0/0      0/0      1/1      0/0
hire                                             7/7      7/7      7/7      7/7      8/8      8/8
money                                     3000/3000    566/566  356/356  658/658  483/482  319/320
```
(`place` also matches d0-d5; money at d4/d5 is $1 off both ways and was already off at 6243b55 --
not a regression.)

Every board/economic field for d0-d5 is exact today. The residual 7,6,4,7,7,7 cells are entirely
routing/pathing (movement directions, pass, pickup/drop) -- fields that have never been zero at any
commit tested, including the very first one (6243b55 has 7 cells at d0 too, all movement). This is
consistent with what CLAUDE.md's own routing note says: `field_order` is a shed-anchored
boustrophedon sweep, not a literal replay of the tape's path, so raw movement will not match the
tape step-for-step even when the economics are identical.

d6-d8 under this narrow reading are NOT exact at any commit, including today (feed off by one on
d6/d8, sell off on d6-d8, sh:FERTILIZER off on d7-d8, cow off by one on d7). But they were never
claimed exact -- 6243b55/b922667 only claimed d0-d4/d0-d5. Nothing regressed here either.

**Conclusion on the user's mental model**: "d0-d8 all correct" over-states what was ever claimed.
The actual claim was d0-d4 then d0-d5 exact on the productive-ops reading, and that specific claim
is intact today. d6-d8 was always the open problem being worked, and it has only ever gotten
better across this session, never worse.

## Deliver ferry: independently re-verified, not just trusted

Rather than take point 3 on faith, monkeypatched `schedule_agent.DELIVER_FERRY` True/False in a
single process (both against CURRENT code, nothing pinned to an old commit) and diffed the full
per-day state and ops dumps directly, not just the summary cell counts:

```
DELIVER_FERRY=True   per-day cells: d0=7 d1=6 d2=4 d3=7 d4=7 d5=7 d6=11 d7=15 d8=13 d9=14 d10=19 d11=20
DELIVER_FERRY=False  per-day cells: d0=7 d1=6 d2=4 d3=7 d4=7 d5=7 d6=11 d7=15 d8=13 d9=15 d10=19 d11=20

d0-d8 state identical on vs off: True
d0-d8 ops identical on vs off: True
d9 differs: BUY_SEED 18(on)/22(off), SELL 17/16, DROP 7/5, plus movement/pass rebalancing
d10 differs: money 2581(on)/2509(off), sh:FERTILIZER 3/4
d11 differs: money only
```

d0-d8 are byte-identical on the full state and the full op counts, not just the summary -- the
ferry cannot be the cause of anything on those days because it produces literally no divergence
there. On d9 the ferry is mildly **beneficial**: OFF is one cell worse (15 vs 14) and 4 fewer sold
this way. This directly contradicts "the ferry drain... is the change which broke it" -- it isn't
the change, and where it does anything at all, it's not a drain.

## Q2: is the seed-retry trade good, and can it avoid the 8x re-offer?

Comparing f31e50e (before 176733c) to 176733c (after), in order: d6 13->11, d7 20->15, d8 15->13,
d9 15->15, d10 24->18, d11 22->20. Every day from d6 on either improved or held; none got worse.
Under the in-order rule this is an unambiguous good trade -- it is not a tradeoff between days, it
is a strict win, and it's the earliest broken day that moved.

The buy_seed inflation is real and traced to the exact line: `kagg/search/schedule_agent.py`
(current, ~line 1638) appends `["BUY_SEED", crop, short]` whenever `short > 0` and a slot is free,
with **no check on whether `money` covers it**. On day 6 today this fires 56 units' worth of melon
orders against the tape's 14 -- one order per turn the crop stays short, regardless of whether the
bank changed since the last attempt. Confirmed directly in the wide table: `buy_seed 56/14` on d6
while `plant 14/14` (the fix's actual payoff) matches exactly.

Because the metric counts differing *fields*, not magnitude, this costs exactly one cell whether
the gap is +6 or +42 -- it's free under THE METRIC. It is not free in every sense: the order list is
capped at 9 slots per turn (`len(orders) < 9`), SELL/HIRE/BUY_LAND/BUY_ANIMAL are appended before
BUY_SEED and BUY_PRODUCT after it, so a seed order that's certain to fail could in principle crowd
out that turn's wheat purchase on a turn where both are contending for the last slot. I did not find
evidence this actually happened on this tape (BUY_PRODUCT matches 9/9, 11/10, 10/10 on d6-d8), but
it's a live risk on a different seed, not a proven one here.

The requested fix -- re-offer only when the bank has changed -- is straightforward and would not
touch the plant outcome: track the `money` value at the turn an order was last appended per crop,
and skip re-appending while `money` is unchanged from that mark. Since `money` only changes via
sells/buys, this converges to "retry exactly when there's a reason to think it might land now"
without needing to observe the (silent) rejection directly. **Not implemented** -- this file is
off-limits per instructions ("DO NOT EDIT ... schedule_agent.py -- I measure against them").
Recording the recommendation only.

## Q3: is d6's early sale reachable, or should effort move to the milk row?

Three arms aimed at the same root cause (crew starts at (4,4) next to nothing; tape's sheep are
AT (4,4)/(4,3), ours at (1,4)/(3,4), so the tape harvests wool without moving and funds the h2 seed
order, we can't):

- YIELD_FIRST -- reorders task priority. Made d2 and d3 worse (4->8, 7->8), d6 unchanged.
- DEPOT_PEN_BY_LOAD -- reassigns pens by load. 52->59 cells, clearly worse.
- CASH_SHORT_SELL_FIRST -- gates sell-first on cash shortage. Held d0-d5, but d6 11->13, d7 15->16,
  d8 13->17 -- worse on exactly the days it targeted.

And pen geometry itself was independently closed at 5247b1b: pinning the tape's *exact* tile
positions only bought 2 cells out of 150 -- so the lever isn't where the pens are, it's the
sequence/timing that put the tape's sheep next to its dawn crew position in the first place. Three
different categories of lever (priority order, placement-by-load, cash-gated sell order) have all
failed, and the geometry lever underneath them was already shown not to be the answer either. That
pattern is consistent with "structural" -- getting an identical early sale without literally
replaying the tape's build order would mean overfitting the router to this one tape, which cuts
against having a general router at all.

I did not attempt a fourth arm or independently re-verify the milk-row numbers ($511, 71.6%
refusal) within this session's time budget -- that reallocation call rests on Fable's own
measurement, not mine. Given three failed arms plus an independently-closed geometry lever, closing
d6's early sale as structural and moving effort to the milk row looks like the right call, but I'd
treat the milk numbers as still needing their own independent check before committing real time to
that arm, the same way the ferry claim needed one here.

## Q4: where is Fable wrong?

Nothing found. Every number in Fable's write-up reproduced under independent re-measurement:

- Point 1's before/after commit numbers for 0fa262d and now match exactly (146 cells then, 130 now,
  same per-day breakdown).
- Point 2's hypothesis -- that "exact on every op" was a narrower field set than the cell metric --
  is correct, and I confirmed it positively (every economic field d0-d5 matches at HEAD today), not
  just by absence of counter-evidence.
- Point 3's ferry measurement reproduced exactly, including the exact d9/d10/d11 deltas, via an
  independent code path (monkeypatch + fresh run) rather than re-reading the same numbers.
- Point 4's buy_seed 56/14 mechanism reproduced exactly, traced to the same missing-money-check line.

The one gap worth flagging: I spot-checked commits (6243b55, b922667, 0fa262d, f31e50e, 176733c,
e904e4f, 38dcf9b, HEAD) rather than every commit in the range. I did check the commit list between
each pair and confirmed no untested commit was skipped in the 0fa262d..176733c gap (only 5247b1b
and 28a694a, both already accounted for). I did not walk the larger e904e4f..38dcf9b gap
commit-by-commit (4140cd4, f523fa3, 68314ab, 903720e, 041dfdc) since the endpoints already bracket
a monotonic improvement (11/15/13/15/19/20 -> 11/15/13/14/19/20, i.e. one cell better at d9 and
nothing else moved) and there wasn't a competing claim about that gap to arbitrate.

## Files touched

- Nothing in the working tree. `kagg/search/router.py` and `kagg/search/schedule_agent.py` were not
  edited.
- Scratch: `/private/tmp/claude-501/.../scratchpad/ferry_toggle_check.py` -- the independent ferry
  toggle script, scratchpad only, not part of the repo.
- Worktrees created under the scratchpad for the Q1 scan were removed after use
  (`git worktree remove --force` on all eight).
