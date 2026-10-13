# V46, Pipe-8, and the ladder's 90-point noise floor

2026-09-17. Engine 1.32.7. All builds hash-verified against the authors' own pinned digests
before use.

## 1. The ladder decides nothing under 90 points

`sdy623`/`jaxa623`, "[2842] Two Identical Agents, 90 Points Apart" (28 votes), submitted
**identical bytes** under two entries:

```
entry A (56272485)   91 games  W73 L18      rating 2857
entry B (56276050)  119 games  W88 L26 T4   rating 2786   (peaked ~2767 at equal game count)
```

Same sha256. About 90 points apart, because two copies are never drawn against the same field.
His rule, adopted here: **the ladder confirms nothing is broken; the offline paired same-seed
both-seats mirror decides.**

Applied to our own numbers, this sorts them:

- `v44a_room_clamp` 2790 -> 2508 is -282. Real.
- frozen `v43_openc` 2720.8 against live 2508.3 is -212. Real.
- `v44a` 2647.9 against `pipe4` 2663.2 is 15 points. **Noise.** That A/B could never have resolved,
  and it was submitted as though it could.

His independent attack-size sweep against a 70-unit opening also reproduces this project's own
figure to the dollar: n=30 gives **+1,367**, exactly what `mirror_all.py` measured for
`v45 vs open_u30` over 40 seeds x 2 seats. Two harnesses, same number. His plateau is 25-50 and
his cliff is below 10; his n=0 arm reads -1,300 because it leaves the inherited split opening in
place, which our own turn-0 matrix prices at -$61 - not a contradiction of our `open_u0`, which
replaces the list with nothing.

**Where yesterday's N choice went wrong.** N=1 was picked for being unexploitable. It avoids -$34
against pipe-7 forks and gives up +$1,367 against V45 forks. That is a 40:1 asymmetry and the
wrong side of it was taken, on evidence already in hand.

## 2. What V46 actually does

7,001 changed lines against V45, so not a parameter edit. Read from the code at
`submission/v46/main.py:3494-3523`, confirmed by playing turns 0-2:

```
u1_rc2 (ours)  t0 [BUY 1, SELL 1]         t1 [SELL WHEAT 0, BUY 5, HIRE...]  t2 []
pipe8          t0 [BUY 5]                  t1 [HIRE...]                       t2 []
v46            t0 [BUY 7, SELL 2]          t1 [BUY 30, HIRE...]               t2 [SELL 30]
```

- **Turn 0 is net +5 wheat, not a round trip.** The five feed units are taken at index 0, so the
  agent no longer has a purchase at an index a rival can pair against. This is Pipe-8's finding,
  credited.
- **Turn 1 lift.** `[BUY_PRODUCT WHEAT 30]` at index 0, unwound at turn 2, gated on
  `_OPEN_ATTACK_MIN_CASH = 2860`. Every tape in this lineage - ours included - buys its feed at
  index 1 of turn 1, so the index-0 purchase commits first and lifts their quotes. This is a
  second front our turn-0 payoff matrix never modelled.
- **Sale timing** from jaxa623's "Beyond 48-0": sales due within three turns execute as soon as
  units reach the shed; market list ordered sales, then product purchases, then fixed-price.

So the turn-0 parameter game is not won by V46, it is left. Our maximin N=1 is unexploitable at
turn 0 and defenceless at turn 1.

## 3. The same guard defect, for the third time

V46's opening layer fires only on exact list equality: `[BUY 5, BUY 10, SELL 60]` at step 0 and
`market[0]==['SELL','WHEAT',13]` at step 1. `clamp_sells` rewrites both sells (60->15, 13->0), so
switching it on **silently voids the entire V46 opening** - the agent reverts to the inherited
split and loses the turn-0 placement, the turn-1 lift and the turn-2 unwind. Its own telemetry
says so:

```
v46      t0 [BUY 7, SELL 2]          open_turns=5  open_attack=1  warehouse_extra_sales=6
v46_rc   t0 [BUY 5,BUY 10,SELL 15]   open_turns=0  open_attack=0  warehouse_extra_sales=0
v46_rcw  t0 [BUY 7, SELL 2]          open_turns=5  open_attack=1  warehouse_extra_sales=0
```

`v46_rcw` widens both guards to the shapes they were describing (no new flags): step 0 accepts any
market that buys 15 wheat in WHEAT buys and ends in a WHEAT sell; step 1 accepts any WHEAT sell in
slot 0 followed by `BUY_PRODUCT WHEAT 5`. Both effects then coexist - `room_guard` is visible in
`warehouse_projected_unresolved` 40 -> 8.

This is the third occurrence: V45's round trip, `u1_rc2`'s round trip, and now V46's whole opening.
See [[kaggriculture-exact-equality-guards]].

## 4. Measurements and what was submitted

40 seeds x both seats = 80 paired games each, fresh module import per game:

```
A        B          B wins   mean    median     t
v46      v46_rcw    74/80    +526    +379    7.25
v46      pipe8      72/80    +904    +680    8.27     (A wins; pipe8 is the loser here)
v46      u1_rc2     55/80    +321    +193    3.48     (A wins)
```

Ordering: **v46_rcw > v46 > u1_rc2 > pipe8**.

Submitted 2026-09-17 05:28, evicting both previous live agents (frozen at `u1_rc2` 2303.8 and
`v44a_room_clamp` 2508.3):

- `56295895` `v46_rcw` - candidate, agent sha `6b9d7ff8bc8018d6e728afcc6b49ef9834a6295aaa7823a1828cd9b0ffb18960`
- `56295903` `v46` - unmodified control, sha `735c370383b70d3bf3aac792f2c147e0afc99166fc9f253ede10e8a030acedb6`

The control exists because the candidate's only edits are mine, and because a gap under 90 points
between them will mean nothing either way.

## 5. Still open

- The `room_guard`+`clamp_sells` loss pattern from `wheat_microstructure_2026-09-16.md` section 8
  was never resolved: median margin declines monotonically with the world's `ICE_CREAM_SHOP` count
  and rises with `BRUNCH_SPOT`, the two shops differing by EGG (flat glut) versus MILK (steep).
  Untested on the V46 chassis, where the flags now coexist with the opening for the first time.
- Pipe-8 was pulled and measured but not otherwise studied; it loses to V46 by $680 median.
- `aurax7/shop-router-reactive-v7`, `seyitkaangunes` "2820 score" and
  `haideptry/v46-vs-pipe-8-vs-jaxa` were listed but not read.
