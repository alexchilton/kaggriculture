# The second cow is unbuyable, and that one missing animal is what desynchronises the crew

2026-08-22. Measured on this Mac, `.venv`, checkpoint
`data/dagger_tape/d01gate-20260822-185347/latest.pkl` round 14, vocabulary
`data/il/bundle_vocab_teacher.json` (148 entries), tape `(False, False)` seat 0, 48 turns, the
STUDENT driving every turn. Log: `data/logs/probe_greedy_playout.log`.

Same class of defect as `docs/the_vocabulary_labels_the_opening_as_nothing_2026-08-22.md`: an action
the teacher takes that the representation cannot express.

## It does hire, and the crew matches exactly

```
turn  crew(o/t)   bank(o/t)         <- greedy decode, student driving
   0    1/1      3000/3000
   1    6/6       884/13
  23    6/6       916/16
  24    1/1       916/16
```

Five hires at turn 0, six units all through day 0, and one unit on day 1 -- the tape does the same,
because the hands do not survive the day boundary and it cannot afford to re-hire until day 2.
So "does it hire and route the crew" is answered: yes, and the crew SIZE is exact.

## What it gets wrong: one cow and one sheep, not two

```
ours [BUY_SEED MELON 12, BUY_SEED WHEAT 7, BUY_PRODUCT WHEAT 6,
      BUY_ANIMAL COW 1, BUY_ANIMAL SHEEP 1, HIRE x5]
tape [HIRE x5, BUY_ANIMAL COW 2, BUY_ANIMAL SHEEP 2,
      BUY_SEED WHEAT 7, BUY_SEED MELON 12, BUY_PRODUCT WHEAT 6]
```

Identical but for the animal counts. COW is $400 and SHEEP is $500 (`reference/kaggriculture.py:21`),
so the missing pair is **$900** against an observed gap of $871 at turn 1.

## Where the quantity is lost, which is NOT where the comment says

`replays.py` blames its own `buy_animal` label:

> "**Binary, not a quantity.** The `buy_animal` head is `N_ANIMALS x 2` ... the only values it can
> express are 0 and 1."

That label is vestigial -- `buy_animal` is **not in `jax_act.ALL_HEADS`** and is never scored. The
real loss is upstream, in the bundle:

- `market_bundles.bundle_of` (`:55`) emits one `(op, item)` pair **per ORDER**. `HIRE` x5 is five
  separate orders, so its multiplicity survives. `BUY_ANIMAL COW 2` is ONE order carrying a
  quantity, so it becomes one pair and the 2 is dropped.
- `to_sim_fields` (`:165`) would recover it -- it does `buy_animal[...] += qty` from a `quantities`
  vector aligned to the bundle. But the head set is `qty_sell`, `qty_buy_product`, `qty_buy_seed`.
  **There is no `qty_buy_animal`**, so nothing ever supplies that quantity and it defaults to 1.

So the policy cannot say "buy two cows" at any width or any amount of training.

## The consequence: 0.28 unit-op agreement is a symptom, not the disease

```
unit-op agreement, student driving, greedy   46/163 = 0.2822
                                  sampled    32/163 = 0.1963
```

The mismatches concentrate in slot 3 -- the hand the tape sends for the second cow:

```
turn 1  ours slot3 PASS   tape WEST
turn 2  ours slot3 PASS   tape NORTH
turn 3  ours slot3 PASS   tape PICKUP COW 1
```

There is no second cow, so that unit has nothing to fetch and passes; its tour desynchronises and
never recovers. The top confusions are exactly that shape: `PASS->EAST 7`, `PASS->WEST 7`,
`NORTH->PASS 5`. Read as a movement failure this would send the work in entirely the wrong
direction.

## Greedy beats sampled, decisively

```
                       unit-op agreement   final money   turn-0 market
greedy                     0.2822              916       the opening, animals short
sampled                    0.1963             2988       SELL MILK 3, SELL STRAWBERRY 6,
                                                         SELL WHEAT 3, SELL WOOL 4, HIRE x5
```

The sampled decode spends **$12 of $3,000** across the whole of day 0 and tries to sell four goods
it does not own. Greedy spends $2,084. On teacher-driven states the same checkpoint reads
`greedy bundle 1.0000` against `sample bundle 0.9635`, and over a sequence that must be exact,
`0.96^719` is zero while `1.00^719` is one.

`neural.py` refuses argmax because independent per-head marginals compose into "never sell". That
reasoning was correct for six independent market heads and does not apply to one `bundle`
categorical, which is a joint choice already. The rule has expired; this is the measurement.

## The audit that should have found all of this on day one

Finding these by symptom is the wrong method: the vocabulary blanking, then the animal count, each
discovered only after it had corrupted a run. There is one question with one answer --

> encode every teacher action to labels, decode it straight back, and compare.

A perfect student emits the label, so anything that does not survive the round trip is an action
**no policy can play at any width after any amount of training**. No network is involved.
Probe: `scratchpad/probe_roundtrip_audit.py`, logs `data/logs/probe_roundtrip_audit*.log`.

Over all 2,876 teacher turns of the four tapes:

```
                        before   after
MARKET does not survive    203 ->    4     (0.3% of 1451 trading turns)
   wrong ORDER SET         179 ->    0     the vocabulary
   wrong QUANTITY animal    20 ->    0     the second cow
   wrong QUANTITY SELL       4 ->    4     left, see below
UNIT ops                   587 ->   36
   PICKUP/PLACE quantity   551 ->    0     the bucket ladder
   DROP arity               36 ->   36     cosmetic
```

`DROP` is cosmetic: `reference/kaggriculture.py:343-355` drops the unit's entire inventory and never
reads `action[1]` or `action[2]`, so `['DROP','WHEAT',3]` and `['DROP']` are the same action.

## What was changed

- **`bundle_of`** repeats an animal pair per unit, as `HIRE` already was. `quantities_of` and
  `from_sim_fields` follow, so the documented inverse still holds.
- **`orders_from_heads` coalesces those repeats back into one order carrying the count.** This is
  the part the audit caught and the tests would not have: a turn holds TEN orders and the opening
  uses exactly ten, so emitting `COW 1` twice instead of `COW 2` pushed it to twelve and truncated
  two HIREs off the tail. The first version of this fix traded the second cow for two hands.
- **`UNIT_QTY_BUCKETS`** `[1, 2, 5, 10]` -> exact `1..16`. Its own comment called it "unexamined,
  not agreed"; examined, it cost 551 unit ops. 12 is the largest the teachers ask for.
- The vocabulary was rebuilt for the new animal symbols: **149 entries**, 149/149 coverage.

**The `qty` head changed shape**, so existing checkpoints cannot be warm-started for it. At 48 turns
a cold start is cheap; a 719-turn run would want the same by-shape head reset the vocabulary change
already uses.

**This audit covers ON-TAPE states only** -- it is collected with the teacher driving. As beta
anneals the teacher may emit bundles it never emits on-tape. That is no longer silent: `encode_action`
returns `w_bundle_miss` and `dagger_tape` aborts at round 0 on any miss.

## The SELL clamp, left deliberately

```
SELL WHEAT 72 -> 63     4 turns, all day 29 hour 0
```

`MAX_QTY = 64` and the class index IS the quantity, so raising it to 128 doubles `qty_sell`,
`qty_buy_product` and `qty_buy_seed`, and all three must then be reset and retrained. That is an
architecture change for 4 turns of 1451, costing 9 unsold wheat on the final liquidation -- order of
$200-350 against a ~$150k season. The other two gaps cost the opening and 551 unit ops. Recorded
here so the trade is visible rather than forgotten.

## The fix, two options (as considered at the time)

1. **Repeat the animal pair per unit in `bundle_of`, as `HIRE` already is.** `COW 2` becomes two
   `(BUY_ANIMAL, COW)` pairs, and `to_sim_fields`'s `+= qty` with the default of 1 then yields 2.
   No architecture change, no new head; `from_sim_fields` needs the matching `* n` so the two stay
   inverses, and `tests/test_a_market_bundle_survives_the_round_trip.py` covers that. `max_held` is
   6, so the vocabulary grows by a handful of entries at most.
2. **Add a `qty_buy_animal` head.** Symmetric with the other three, but it is a shape change: every
   checkpoint needs migrating and the head has to be trained from scratch.

(1) is cheaper, matches the existing treatment of `HIRE`, and needs no checkpoint surgery.
