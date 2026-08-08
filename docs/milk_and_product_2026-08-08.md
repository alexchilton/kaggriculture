# `sh:milk +464` and `buy_product -164`: one is a measuring artifact, the other is not a loss

Baseline throughout:
`python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves`,
at `b81f04b`.
Every number below is seat 0 on that one seed unless it says otherwise.

## Verdict, up front

| row | real? | cause | costs us |
|---|---|---|---|
| `buy_product -164` | **NO -- coverage artifact** | `breakdown.py`'s clean-turn filter censors our side harder than the tape's (49% vs 68%). Exact fills are ours **402** to the tape's **379**, i.e. **+23**. | nothing |
| `sh:milk +464` | **YES -- exact, it is a state row** | We produce **+56** milk from the **same eight cows**, via **+47 cared-tile-days** feeding the `pending_care_bonus`. We also **sell +54**. The row is the area under a stock-held-longer curve, not stock never moved. | 15 units of *other* product discarded at the 100-unit shed cap on d21 and d24 |

They do **not** share a mechanism.
The hypothesis that they might -- buying wheat feeds animals, animals make milk -- is refuted at the
first step: we buy essentially the wheat the tape buys, because the schedule carries its `buys`
rows.

And the framing that led to the task is inverted on both counts.
`buy_product` was suspected of being "the single strategic play we do not make"; we make it.
`sh:milk` was suspected of being unsold stock; every unit of it is sold.

## Why `breakdown.py` cannot answer this and what replaced it

`docs/breakdown_fills_not_offers_2026-08-08.md` is explicit that `sell` / `buy_product` /
`buy_animal` are a **lower bound**: a turn with a `DROP` anywhere, or a `PICKUP`/`PLACE` for that
item, contributes zero.
The header prints the coverage, and for this run it is

    ours: buy_product=91/184 (49%)      tape: buy_product=177/260 (68%)

so the row subtracts two differently-censored counts.
That is enough on its own to make `-164` uninterpretable, and it is why the task's instruction to
establish the difference is real before explaining it was the correct instruction.

The replacement is the environment's own commit point.
`_commit_unit` (`reference/kaggriculture.py:626`) is the single place every `SELL` / `BUY_PRODUCT` /
`BUY_SEED` / `BUY_ANIMAL` unit settles, it returns `True` exactly when one unit changed hands, and it
is a module-level function, so wrapping it is ground truth with no coverage caveat at all.
`scripts/probe_market_fills.py` does that and also records the money the buyer held at the instant of
a refusal, so a refusal is attributable rather than guessed at.

Three further probes were needed because the same "a stock cannot tell you why it moved" problem
applies to every state row:

- `scripts/probe_animal_yield.py` wraps `_daily_refresh_animals` (`:774`) -- the only place an
  animal's `yield_units` grows -- and separates base production from the CARE bonus, counts what the
  `max_held` clamp throws away, and counts animals that escape for two unfed days.
- `scripts/probe_plant_yield.py` wraps `_daily_refresh_plants` (`:738`) -- the only place a crop
  grows *and* the only place a crop **dies**, in one line, with no signal anywhere in the
  observation.
- `scripts/probe_shed_overflow.py` wraps `_drop_inventories_to_shed` (`:812`), whose own docstring
  says "overflow is discarded", to measure what the dusk drop destroys.

## `buy_product`: exact fills, per day

`python -u scripts/probe_market_fills.py --op BUY_PRODUCT` (`data/logs/probe_buy_product.log`).
WHEAT is the only product either side buys.

| day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ours | 8 | 6 | 5 | 7 | 0 | 4 | 8 | 10 | 10 | 6 | 13 | 12 | 16 | 15 | 21 |
| tape | 8 | 6 | 5 | 7 | 0 | 4 | 9 | 10 | 10 | 10 | 13 | 12 | 16 | 15 | 21 |

| day | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | **total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ours | 13 | 18 | 18 | 17 | 16 | 17 | 16 | 17 | 19 | 16 | 18 | 18 | 14 | 17 | 27 | **402** |
| tape | 13 | 17 | 18 | 17 | 16 | 17 | 16 | 17 | 19 | 16 | 18 | 18 | 14 | 17 | 0 | **379** |

Twenty-six of the thirty days are **identical**.
The whole real difference is four cells:

- **d6 -1 and d9 -4**: the only two refusals of the season, both `money < price`.
  A refusal aborts the remainder of that order (`order_states[player_id] = None`, `:597`), which is
  why one refusal on d9 costs four units off a ten-unit order.
- **d16 +1**.
- **d29 +27**: we buy 27 wheat on the final day and the tape buys none.
  We also sell 43 wheat that day to its 21, so this is churn inside `LIQUIDATE_LAST_DAY` -- a
  round-trip the env prices to net roughly zero (`:573`) but which burns market-order slots on the
  one day the shed must clear.
  Not investigated further; flagged.

Days 0-28 alone are ours 375 to the tape's 379.
So the answer to "are we refusing buys, never offering them, or is the play absent" is **none of the
three**: we offer 407 units, 405 land, and the play is present at the tape's own scale.

## `sh:milk`: where the milk comes from and where it goes

`python -u scripts/probe_animal_yield.py --species COW` (`data/logs/probe_cow_yield.log`).
Cow counts are identical to the tape's on every single day, 2 rising to 8, and no cow ever starves.

|  | ours | tape |
|---|---|---|
| milk **made** (`yield_units` added at dusk) | 242 | 186 |
| of which **CARE bonus** | 179 | 124 |
| cared-tile-days | 194 | 147 |
| fed-tile-days | 195 | 182 |
| thrown away by the `max_held=6` clamp | 12 | 13 |
| milk **sold** (exact fills) | **233** | **179** |
| `yield_units` still on the cows at season end | 9 | 7 |

`made - sold == left-on-cow` closes **to the unit on both sides** (242 - 233 = 9; 186 - 179 = 7).
That is the whole answer to "does the milk get sold": there is no leak, no spoilage, and nothing
sits in the shed at the end.
`LIQUIDATE_LAST_DAY` clears 30 milk on d29 against the tape's 16.

The mechanism is the one CARE exists for.
`_daily_refresh_animals` banks `pending_care_bonus` only on a day the tile is **both fed and cared**
(`:798`), and spends it only on a production day that is **also fed** (`:795`).
Same eight cows, same interval-2 production days: the entire +56 is bonus (+55), not base rate.

### The `sh:milk` row is a stock curve, not a loss

Shed milk at dusk, ours / tape:

| d11 | d13 | d15 | d17 | d19 | d21 | d22 | d24 | d26 | d28 | d29 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6/6 | 17/12 | 19/7 | 22/5 | 31/2 | 50/4 | 61/12 | 64/15 | 49/17 | 30/16 | 0/0 |

The tape runs its shed near empty and sells as it goes; we let milk bank up and sell it in larger
lots.
Selling in lots turns out to be the *better* half of that: our realised price per unit is **$243.9**
against the tape's **$240.0** while selling 30% more units.
The inventory-sensitive price model did not punish the extra volume.

### The one genuine cost of the pile

`shedCapacity` is 100 and it is the **whole shed, every product together**
(`sum(shed.values())`, `:470` and `:820`), and overflow at dusk is silently destroyed.
`python -u scripts/probe_shed_overflow.py` (`data/logs/probe_shed_overflow.log`):

| day | our shed at dusk | discarded | tape shed at dusk | discarded |
|---|---|---|---|---|
| d19 | 83 | 0 | 49 | 0 |
| d21 | **100** | **9 MELON** | 46 | 0 |
| d22 | 89 | 0 | 54 | 0 |
| d24 | **100** | **4 STRAWBERRY, 2 WOOL** | 47 | 0 |

Fifteen units, worth roughly $2,600 at our own realised prices.
The tape peaks at 64 and never touches the cap.
This is a real, previously unowned cost, and it is caused directly by the milk pile crowding the
shed.
It is also small next to what the milk earns, below.

## Is it a trade -- milk for strawberry? No.

The coordinator's sharpened question was whether `sh:milk +464` and `strawb -94` / `sh:straw -78` are
two ends of one trade, and whether that trade is a good one.

**It is not a trade.**
Two independent things happen and they co-occur.

The strawberry side, from `python -u scripts/probe_plant_yield.py`
(`data/logs/probe_plant_yield.log`, `data/logs/probe_deaths.log`):

|  | ours | tape |
|---|---|---|
| strawberry **made** | 242 | 308 |
| tiles **dead of thirst** | **12** | **0** |
| unwatered-tile-days | 297 | 328 |
| crop tile-days | 615 | 697 |

We do not water *less carefully* than the tape in aggregate -- our unwatered rate is 48% to its 47%.
We water in a pattern that lets twelve tiles take two dry days in a row, and
`_daily_refresh_plants:752` turns a plant into a `WEED` at exactly that point.
That, not planting, is the whole of `strawb -94`: the tape's tile count only ever falls to natural
end-of-life, ours falls by deaths first.
It also explains `dig +35` and `weeds -174` -- we dig up the corpses.

The claim that this is the *price* of the milk fails on the turn budget.
Idle unit-turns, ours / tape, on the six days a tile died:

| d11 | d13 | d15 | d16 | d21 | d22 |
|---|---|---|---|---|---|
| 15/5 | 12/12 | 13/0 | 16/2 | 29/0 | 28/0 |

Season totals: **idle 1,426 / 999**, move 3,445 / 4,025, work 2,818 / 2,703.
We do *more* work than the tape, walk far less, and still finish with 427 more idle unit-turns.
There was spare capacity on every day a strawberry died.
Nothing was traded away.

And the router already prices these correctly.
`router.crop_ops` offers a survival `WATER` at `_crop_remaining`, and evaluated on the exact tiles at
dawn on the day they died it was worth **$360-$480 each** -- the highest prize on the board that day.
The valuation is right; the assignment never reached them.
`tests/test_a_thirsty_tile_outranks_everything.py` passes throughout, which is this repo's recurring
lesson again: a gate only tests what it exercises, and a unit-level ranking test cannot see a
season-level reachability failure.

## Would it have been a good trade anyway? Yes, overwhelmingly.

Realised revenue, from the exact fills (`data/logs/revenue_by_product.log`) -- money that actually
entered the bank, not shed stock:

| product | ours n | ours $ | ours $/u | tape n | tape $ | tape $/u | d n | d $ |
|---|---|---|---|---|---|---|---|---|
| MILK | 233 | 56,820 | 243.9 | 179 | 42,961 | 240.0 | +54 | **+13,859** |
| STRAWBERRY | 225 | 49,259 | 218.9 | 308 | 50,803 | 164.9 | -83 | **-1,544** |
| WOOL | 194 | 18,475 | 95.2 | 230 | 25,693 | 111.7 | -36 | -7,218 |
| FERTILIZER | 314 | 16,356 | 52.1 | 299 | 16,173 | 54.1 | +15 | +183 |
| MELON | 126 | 21,185 | 168.1 | 132 | 21,880 | 165.8 | -6 | -695 |
| WHEAT | 93 | 4,084 | 43.9 | 71 | 2,854 | 40.2 | +22 | +1,230 |
| **TOTAL** | 1,185 | **166,179** | | 1,219 | **160,364** | | -34 | **+5,815** |

Milk earns **+$13,859**; strawberry loses **-$1,544**.
The strawberry line is the interesting one: we sell 27% fewer units for 3% less money, because the
tape dumps all 308 and crushes its own price to $164.9 while we get $218.9.
So even if a trade *had* to be made, milk is the right side of it by roughly nine to one -- and the
action cost is 42 CARE unit-turns drawn from 1,426 idle ones, about **$330 per unit-turn**.

Final banks on this seed: **ours $121,221, tape $116,635**.
We finish **$4,586 ahead**.
The `money` row's season total of `-103,724` is the *area* between two bank curves, i.e. a
consequence of the same hoarding, and it should not be read as a deficit.

### The suspicious-result check

CLAUDE.md records four occasions where a negative verdict on animals was a measurement artifact, so
the standing instruction is to state what could make an animal conclusion wrong.
This conclusion is **positive** on animals, so that particular failure mode does not apply -- but the
symmetric one does, and here it is:

- One seed, one tape, weeds off.
  The milk advantage could be seed-specific, and seed variance in this project is ~15%.
- Realised price is contested-market-dependent.
  The opponent here is the `seb` replay in seat 1; against a field that also sells milk, $243.9/unit
  would fall.
- The 15 units lost to the shed cap are the visible cost of hoarding.
  There may be an invisible one: a full shed also silently truncates the mid-day `DROP` op (`:470`)
  and `PICKUP`'s room check (`:333`).
  The probe counts a blocked `DROP` and found none this season, but it is a live hazard that scales
  with the pile.

## The wool loss is a third, separate thing -- and it is a starvation

Found by the correctness-floor check the task mandated, not by looking for it.
`python -u scripts/probe_animal_yield.py --species SHEEP` (`data/logs/probe_sheep_yield.log`):

**two sheep starve at d15/d16** -- two consecutive unfed days, `_daily_refresh_animals:786` -- and
the herd stays at 9 against the tape's 11 for the remaining thirteen days.

Animals standing in pens, ours / tape:

| species | d10 | d12 | d14 | d16 | d18 | d20 | d22 | d24 | d26 | d28 |
|---|---|---|---|---|---|---|---|---|---|---|
| COW | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 |
| SHEEP | 5/5 | 8/8 | 11/11 | **9/11** | **9/11** | **9/11** | **9/11** | **9/11** | **9/11** | **9/11** |

Wool made 202 to the tape's 234; wool sold 194 to 230; **-$7,218** realised.
On d15 we fed 9 of 11 sheep and finished the day with 13 idle unit-turns; on d16, 16 idle.
Same shape as the thirst deaths: a mandatory upkeep op missed while units idle.
This is the `sheep -2` state row in the baseline, and it is a bigger dollar loss than the strawberry.

## What changed in the repo

Nothing that alters agent behaviour.
No arm was run.
Both of the assigned rows turned out not to be losses, and the two real losses this uncovered
(twelve thirst deaths, two starved sheep) live in `kagg/search/router.py`'s task assignment, which
other agents are editing concurrently, so they are handed over rather than patched here.

Added:

- `scripts/probe_market_fills.py`, `scripts/probe_animal_yield.py`, `scripts/probe_plant_yield.py`,
  `scripts/probe_shed_overflow.py` -- four env-level probes, all read-only wrappers.
- `tests/test_milk_and_product_rows.py` -- five passing pins on the diagnoses and **two
  `xfail(strict=True)`** carrying the open bugs, so the suite stays green now and goes loudly red the
  moment either is fixed.

The three load-bearing passing assertions were inverted and confirmed to go red, per the
"revert the fix and confirm the test goes red" rule.

## What I did NOT check

- **Any seed but 11, any tape but `seb`, and weeds only at 0.0.**
  Every number here is one game.
- **The opposite seat.** All measurement is seat 0.
- **Whether fixing the twelve thirst deaths or the two starved sheep actually pays.**
  Both are stated as production and revenue *losses*; neither was armed, so neither has a per-day
  before/after table.
  In particular, selling ~66 more strawberries would move the price, and the marginal unit is worth
  much less than our current $218.9.
- **The d29 `BUY_PRODUCT` of 27 wheat.** Named, priced at roughly break-even by the env's own
  quoting rule, not investigated.
- **`HIRE` and `BUY_LAND`**, which are still raw offer counts in `breakdown.py` with the same
  silent-refusal caveat `BUY_SEED` used to have.
- **`sh:ferti +143`, `sh:wheat -139`, `sell +123`, `pass +427`, `move -580`** and every other row in
  the baseline diff.
  `sell +123` in particular is still a lower-bound row and should not be read before someone puts
  the exact-fill numbers in this document's revenue table next to it.
- **Whether the milk hoard is optimal or merely better than the tape.** Selling later beat selling
  early here; no schedule between the two was tried.
- **`SELL_SURPLUS_HORIZON` and the inert `shed-target` arm** from commit `cdac079`.
  The task asked whether the shed-target arm is the right home for the milk surplus.
  On this evidence the question is malformed: there is no surplus to release -- all 242 units are
  sold and the residue is 9 units sitting on the cows, which no sell rule can reach.
  What the pile actually costs is 15 units of shed capacity on two days, which is a *capacity*
  problem, not a selling one.
