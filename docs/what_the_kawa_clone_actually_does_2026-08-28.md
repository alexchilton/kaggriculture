# What the kawa clone actually does, and what was measuring the harness instead

2026-08-28. Everything below is measured today. Three of my own hypotheses were killed in the
course of it and are recorded here with the measurement that killed each, because the pattern --
reaching for a mechanism before reading what the quantity counts -- cost most of the day.

## 1. The clone learns kawa, on seats it has never seen

`scripts/does_the_kawa_clone_generalise_to_a_seat_it_never_saw.py`. 423 カワシギ seats exist; the
checkpoint (`data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl`, 24 epochs) trained on the top 400
by bank, so ranks 401+ are genuine held-out data from the same teacher. Both columns masked the way
play masks.

```
  arm                                seats  bundle top-1  op agree  traded rows     slots
  IN TRAINING (ranked 1..6)              6        89.6%     81.1%        2,095    41,477
  HELD OUT (ranked 401..406)             6        80.6%     77.9%        2,274    41,491
```

It generalises on both halves, and the held-out seats are his *weakest* games, so the gap is an
over-estimate. **Generalisation across seeds is not the problem.** A retrain to give it the
unlock-date features was proposed on the strength of a guess and withdrawn on the strength of this.

## 2. It free-runs a held-out seat and earns nothing after day 0

`scripts/where_does_the_clone_come_off_the_rails.py --rank 401`, seat `93541810.json`, clone plays
our seat against that game's recorded opponent.

```
   day         bank ours/teacher         tiles      crew
     0               3,000/3,000         25/25       0/0
     1                     23/23         25/25       0/0
     2                    23/176         25/25       0/0
     7                  23/1,578         25/50       0/0
    11                 23/15,368         25/50       0/0
    16                 23/15,207        25/100       0/0
  final bank   ours $211   teacher $50,745
```

**Day 0 is exact** -- it reproduces kawa's entire $2,977 opening spend to the dollar on a seat it has
never seen. **Then the bank never moves.** $23 from day 1 to day 16 while the teacher climbs to
$15,207; tiles stay at 25 while he goes to 100. One mechanism: it never sells, so it never has cash,
so it can never buy land, seed or animals.

## 3. The shed is full and it declines to sell

`scripts/what_does_the_bundle_head_do_on_a_real_turn.py`, planner driving fully (its own market
intact), 400 turns, seed 9000.

```
  turns with ANYTHING in the shed         367  (91.8%)
  peak shed size                             63
  mean P(any SELL) when shed is stocked   0.228
  max  P(any SELL) when shed is stocked   0.999
  mean P(EMPTY)     when shed is stocked  0.668
  mask killed the first choice              0  (0.0%)
  most-wanted:  EMPTY x294,  [BUY_PRODUCT WHEAT] x40,  [SELL FERTILIZER] x14
```

234 of 256 bundles contain a SELL, so the vocabulary is not the limit, and the mask never removed
its first choice. Stock is present on 92% of turns and it still puts two thirds of its mass on doing
nothing. The only thing it ever wants to sell is FERTILIZER, the by-product -- never wheat, milk or
wool. It has copied the *feed* half of kawa's economy and none of the *harvest-and-sell* half.

`max P(sell) = 0.999` says it is not incapable. The rate is wrong, not the ability.

## 4. Naive selling is worth half the planner, and the feed reserve is worth $27,813

`scripts/what_if_we_just_sell_everything_that_hits_the_shed.py`, 3 seeds, idle opponent, planner
replay off.

```
      seed        planner   naive ADDED keep 0   naive ADDED keep 20   naive REPLACED
      9000        150,396              45,879                74,180            3,000
      9137        179,719              46,367                84,155            3,000
      9274        135,885              51,011                68,000            3,000
    median        150,396              46,367                74,180            3,000
```

- **Naive is not enough.** $74,180 against $150,396, losing on every seat. Market timing is not a
  small prize; the planner's sell logic is worth about as much again as everything else it does.
- **The feed reserve is worth $27,813** -- same rule, same ops, the only difference being whether the
  trade left the animals something to eat. Alex's "you can't have one without the other", priced.
- **Replacing the market banks exactly $3,000**, the untouched starting bank, on every seed. No seed
  bought, nothing planted, nothing harvested, money never moves.

## 5. Therefore every earlier hybrid number is void

`scripts/the_planner_drives_and_the_net_supplies_the_market.py` did `mine["market"] = orders`, which
deletes the planner's HIRE, BUY_LAND, BUY_SEED, feed buys and SELLs -- while the planner has already
booked those orders in its own ledgers (`schedule_agent.py:5115, :5434`), so its world-model is
falsified as well. Fable named this (`docs/fable_the_hybrid_split_cannot_work_2026-08-28.md`) and
row 4 above confirms it independently: an unconditional sell-everything rule, which cannot possibly
be a *market* failure, also banks the untouched $3,000 under replacement.

So the hybrid tables of $92 and $20 median measured the harness. A `--market-mode add` arm was added
and is the first valid test of the clone's market head.

## The three hypotheses that were wrong, and what killed each

1. **"The decode is discarding it."** Precedent was real -- greedy argmax over marginals emitting
   zero orders, `neural._fire` written for it. Killed by: `mean P(EMPTY)` = 2.6% offline, and
   suppressing index 0 entirely moves top-1 from 86.7% to 88.8%. No mass on EMPTY to reclaim.
2. **"Covariate shift -- it is asked about boards it was not fitted on."** Asserted without
   measurement. Killed by: the start board is IDENTICAL in every game, and §1 above shows it
   generalises to unseen seats at 80.6%/77.9%.
3. **"DAgger can query the teacher at unseen positions; kawa cannot be asked."** Killed by one grep:
   `dagger_tape.py:840` only begins annealing once agreement reaches `--anneal-after-agree 0.80`,
   and agreement is 0.4648. `beta` stays 1.0, the teacher drives every turn, and the run is plain BC.
   The capability described is not one we use.

A fourth, smaller one: a real vocabulary/mask mismatch was found and fixed in `neural._bundle_sells`
(mask built from the 197-entry default while the head decoded against the checkpoint's 256). It was
a genuine bug and it was **not on this path** -- 0 of 240 turns had a first choice masked. Keep the
fix; do not credit it with anything.
