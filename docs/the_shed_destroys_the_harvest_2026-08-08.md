# The shed destroys the harvest, and the early game was never the gap

2026-08-08.
All numbers from `data/logs/handover.log`, `data/logs/waste.log`, `data/logs/graft.log` and
`data/logs/graft_window.log`.
Seed 11, weeds off, opponent is the `seb1326` replay's own opponent in every arm.

## 1. Seb's days 0-10 can be replayed exactly, and that is a usable fixture

The replay's `configuration.seed` is `None`, so his RNG stream is gone.
It does not matter.
The starting board is deterministic -- both sides open on `wheat 14, melon 3, cow 2, sheep 2` -- and
with `weedSpawnChance` at 0 the only unmatched stream is the shop unlock order.

Replaying his own actions for days 0-10 reproduces his board **field for field**:

```
day    owned      plant       pen      animal        ours/his
  0    25/25      0/0        8/8        0/0
  4    25/25     17/17       8/8        6/6
  5    50/50      3/3        8/8        7/7      parcel 1, bought d4
  7    75/75     22/22      10/10       7/7      parcel 2, bought d6
 10    75/75     44/44      16/16      10/10
 11   100/100    43/43      17/17      14/14     parcel 3, bought d10   <- handover
```

So the "baseline with the correct land buys" exists on demand.
It is not an approximation of his opening; it *is* his opening.

**This does not transplant to a later day.** Splicing days 4-10 instead of 0-10 is a wipeout --
$345 final, herd at zero by day 7, no land ever bought -- because his hand ops are
position-dependent (`["FEED"]` applies wherever that unit is standing) and by day 4 our crew is not
where his crew is. From day 0 there is no divergence to fight.

## 2. A perfect early game is worth $2,005

```
handover at d11    ours $71,976   opp $63,037   WIN
our own agent      ours $69,971   opp $82,015   LOSS
his own game                                    $128,518
```

At the handover we are level with him: **$3,950 against his $3,864**, on the same 100 tiles, with
the same pens and the same herd.
Then the whole gap opens in the following nine days.

The land timing was the thing we had been chasing, and on the money axis it is worth about 3.5% of a
~$57k gap.

**It is not worth nothing on the ladder axis**, and that distinction matters here: the handover
flips a loss into a win against this opponent, because selling into the early price curve first
denies it to them. Elo scores that the same as a $50k win.

## 3. What actually costs the season: we bin the harvest

`_drop_inventories_to_shed` (`kaggriculture.py:813`) banks every hand into the shed at the rollover
up to `shedCapacity` 100 and **discards the overflow**.
A HARVEST into a full shed loses the difference too (`kaggriculture.py:470`), invisibly, because the
shed total never moves.

From the handover fixture, `PRICE_AWARE_SELL_CAP` off:

```
day    11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28
shed   14  33  35  35  45  86 100 100 100 100 100 100 100 100 100 100  90 100
lost    0   1   2   1   0  21  13  27  23  18  42  36  28  11  41   7  10  24
```

**331 units destroyed**, and from day 17 the shed never comes off its cap.
Seb sits between 18 and 36 all season, because he never stops selling.

## 4. Why we stop selling

`schedule_agent.py:1947-2088`:

```python
for d in sorted(sched):
    for p, q in (sched[d].get("sells") or {}).items():
        if d <= day:       rate[p] = max(rate[p], int(q))   # per-OFFER cap
        elif d <= horizon: still_owed[p] += int(q)          # rest of season

allow = max(today + carry, have - still_owed[prod])
n     = min(have, allow, rate[prod])
```

Two throttles, both transcribed from **his** schedule, neither aware of **our** shed.

`have - still_owed` releases only stock above everything the remaining season's rows will ever ask
for, which stays negative until about day 25, so `allow` collapses to today's row.
And we plant **77 tiles to his 45** -- we produce far more than his rows ever named, so the surplus
has no row anywhere in the schedule to release it.

`SELL_TO_MAKE_ROOM` is already on and does not close this.
It reserves room for *tonight's* drop, reactively; it is a smaller question than "this product has
no buyer anywhere in the plan".

This is the `feedback_optimise_the_artifact` failure mode exactly: the sell row is a proxy for a
board that is not ours.

## 5. The fix, and why the pool could not see it

`PRICE_AWARE_SELL_CAP` (Fable, same day) drops the **day total** when the live price is at or above
base, and keeps the **per-offer** cap `rate[prod]`.
Keeping the second half is not optional -- dropping both cost ~30% of mean money against every
opponent, one post-harvest order walking its whole size down the curve.

On the arena pool it reads neutral: $103,932 -> $102,095, win rate 94.4% both ways.
**The pool is saturated.** 94.4% with `mirror` at 50% means every non-mirror opponent already loses
100% of the time, so no selling change can move the win rate and mean money is the only channel.

On the handover fixture, against an opponent that beats us:

```
                  final     destroyed    turns at cap
OFF             $71,976        331            12
ON              $75,866         82             2
                +$3,890        -75%
```

Now ON.

## 6. Open

- One seed. Needs a seed sweep before it is trusted at the quoted size.
- The price test is binary at `BASE_PRICE`, but Fable's own measurement says the products differ in
  *depth*, not just level: WHEAT realised $46.8/unit at 1,105 units against $47.8 at 125 -- nine
  times the volume at the same price -- while MELON, which has no shop, genuinely gluts. A per-product
  depth model is the obvious next refinement and is not built.
- 82 units are still destroyed. The residue is the router carrying product home to a shed that
  cannot take it, which no sell rule can reach -- see `SELL_TO_MAKE_ROOM`'s note and OPEN-4.
- Seb's own banking method is still not implemented: a continuous small-sell/small-buy
  working-capital cycle, funded early almost entirely by FERTILIZER (322 units a season, his largest
  single line, and the only thing he sells at all on days 1, 2, 3, 5 and 7). He carries feed in hands
  drawn at dawn, which is how he survives day 7 at $4 for eighteen straight hours.
