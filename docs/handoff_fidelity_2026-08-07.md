# Handoff — tape/schedule/agent fidelity, 2026-08-07

Everything below is uncommitted.
Nothing was reverted.

## The method, which is the part that matters

Fidelity is measured **day by day on state**, never on the final bank.
Two seasons can land on similar money by completely different routes, and one end-of-season figure cannot say WHERE they parted.

A cell is exact or it is not.
`315 / 318` is not a match.
Every "near-exact" claim made in this project so far was made by reading a column of pairs and not counting them — including one I made in this session about days 0–6 of Seb's tape, which is wrong (day 1 water is `17 / 0`).
The next change to `scripts/breakdown.py` should be a `*` marker on every differing pair plus a per-day mismatch tally, so that claim cannot be made by eye again.

## Naming — read this first

- **"Seb" = the current leader.** `data/seed_scripts/top_guys/90494364.json`, team `Seb (allegedly)`.
  Schedule at `data/seed_scripts/top_guys/90494364/schedule.json`.
- **"old leader" / "new_leader" dir = an OLDER tape.** `data/seed_scripts/new_leader/90016067.json`, team `somewhere after`.
  The directory name is misleading; it is not the leader.

Seb is the target.
Where the two tapes disagree, weight Seb.

## Scripts

| script | what it answers |
|---|---|
| `scripts/fidelity.py` | day-by-day **deltas** (ours minus tape) for 8 scalars + per-product shed, plus order cadence. `--replay --team --schedule --seed --weeds` |
| `scripts/breakdown.py` | day-by-day **raw pairs** `ours/tape` for every crop, animal, product and op. `--tape seb\|oldleader --days N` |
| `scripts/why_the_land_is_bare.py` | does the extracted schedule ask for as many plants as the tape made? (needs no simulation) |
| `scripts/where_the_plants_go.py` | per-day wanted vs planted, seeds on hand, empty ground, weeds, idle crew-turns |

All runs: seed 11, `weedSpawnChance 0.0`.
Logs in `data/logs/`.

## What was established this session

### 1. The extractor is clean

`why_the_land_is_bare.py`: the schedule's `plants` rows match the tape day for day and crop for crop on **both** tapes — leader 131/131, Seb 86/86, identical per-crop splits.
So any planting deficit is the executor, not `dayplan`.

### 2. The crew is not the problem

`hands` **never parts** from the tape on either tape.
The "hired hands are idle" theory is dead: season idle crew-turns are 603 of 6,659 (9%), and in the critical window days 6–11 idle is 12, 4, 4, 18, 12, 0.

### 3. We plant 85 of 86 — but late, and the late-ness was land

The tile deficit was **not** fewer plantings.
It was one 25-tile parcel arriving ~6 days late (`owned -25` sustained days 9–15 on Seb), and the plant deficit tracked it almost unit for unit (`-26` plants against `-25` tiles on day 12).

### 4. Root cause found and fixed: `sells` was the last per-day target

`plants`, `builds` and `animals_bought` had each already been converted to cumulative targets, every time for the same reason: a row that could not be filled on the day it appeared was silently forfeited and never retried.
`sells` was still read as today's row only.

Seb sells `MELON: 18` on day 10 and asks for no melon again until day 16.
Our melons ripen one day later, so the day-10 row fired against an **empty shed**.
We then held exactly those 18 melons from day 11 to day 15 with **$2 in the bank**, could not afford the $4,000 third parcel until day 16, and farmed 25 fewer tiles for six days.

Fix in `kagg/search/schedule_agent.py`, behind `CUMULATIVE_SELLS = True`:
carry forward only the part of a past sell row the shed could never have covered, for `SELL_CARRY_DAYS = 3` days, capped per offer at `rate` (the largest single day that product is ever asked for).

Two earlier versions were tried and are recorded in the comments because both ran away:

- a cumulative `asked - sold` ledger — the fill credit under-counts whenever a DROP lands on the same turn as a fill, so `owed` never reached zero and the offer pinned at the season's largest row every turn from ~day 19 (63 strawberries at a time)
- an accumulating uncovered-remainder with no expiry — same failure, because on the old leader's plan the schedule asks to sell more than we ever produce

**Measured, paired, `CUMULATIVE_SELLS` off → on, seed 11:**

| field | Seb off → on | old leader off → on |
|---|---|---|
| money delta | −30,352 → **−13,005** | −19,407 → **−30,262** |
| `owned` | day 9 sustained → re-converges | unchanged |
| `plant` never-returns | day 7 → **day 10** | day 22 → day 22 |
| `animal` final | −1 → **0** | unchanged |
| `weed` final | −33 → **−23** | 4 → 2 |
| `shed` final | 50 → 38 | 17 → 18 |

It is a real tape-dependent trade: **+$17.3k on Seb, −$10.9k on the old leader.**
On the old leader the result is byte-identical under all three carry rules tried, because there our shed is always the binding constraint (`shed` delta negative all season), so any cumulative rule collapses to "sell the whole shed" and that tape punishes it.
Left ON because Seb is the leader.
One line to flip.

## Where it diverges NOW — Seb, seed 11

Day 7, planting slips one day and self-corrects:

```
plant    d6   3/14      d7  22/11
strawb   d7   3/11      melon d7  10/13
```

**Day 9 is the break, and it is DROP:**

```
drop         d9    0/7      <- we bank nothing all day
sell         d9    1/22     <- so there is nothing in the shed to sell
money dawn   d10   0/3104   <- broke
unit-turns   d9    70/276   <- crew collapses to ~2 units for the day
water        d9    9/31
```

Day 10 is the consequence:

```
weeds     16/0     <- 16 tiles hit consecutive_unwatered >= 2
dig       17/0     <- the next whole day spent digging them out
strawb     5/28    <- from 19/19 the day before
```

Chain: units hold the day's produce in hand → nothing reaches the shed → nothing can be sold → bank hits $0 mid-day 9 → the crew is lost → 16 tiles dry out → day 10 goes on digging instead of farming.

**Next bug: DROP timing.**
This is exactly what `OPPORTUNISTIC_DROP` was built for.
It is currently `True` and still leaves us at 0 drops on the day it matters most.
Its earlier isolated measurement was mixed (better on Seb's herd chain, worse on the old leader's harvest), which now looks like it was measuring the wrong thing — the question is not whether to drop mid-tour, it is why day 9 produces zero drops at all.

Do not re-derive the three already-reverted DROP attempts; they are written up in the comments at the return-leg block in `schedule_agent.py` and in `docs/fable_drop_timing_attempt.patch`.

## Files touched (all uncommitted)

- `kagg/search/schedule_agent.py` — the sells fix, `CUMULATIVE_SELLS`, `SELL_CARRY_DAYS`, plus earlier uncommitted work (`FEED_ORDER_CAP = None`, `OPPORTUNISTIC_DROP`, live-quote feed debit)
- `kagg/search/router.py` — the half-price survival water in `crop_ops` (`consecutive_unwatered >= 0`, thirsty tiles at full prize, slack tiles at half)
- `tests/test_router.py` — **46 passing**, including two new pinned tests:
  `test_a_sell_row_that_landed_on_an_empty_shed_is_recovered_later`
  `test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked`
- `scripts/fidelity.py`, `scripts/breakdown.py`, `scripts/why_the_land_is_bare.py`, `scripts/where_the_plants_go.py` — all untracked

## Open, in order

1. **DROP timing on day 9** — the live bug above.
2. Add the `*` mismatch marker and tally to `scripts/breakdown.py` (edit was drafted and not applied).
3. Day-0 order cadence is still unfixed: tape 41 orders over 18 distinct hours, ours 12 over 4.
   The mechanism must be *more orders at full size*, never a ceiling on the order that feeds the herd.
4. Decide `OPPORTUNISTIC_DROP` — currently `True`, measured mixed, likely subsumed by (1).
5. The wasted day-1 water on short-window crops — deferred by Alex until matching is done.
   The unimplemented refinement: offer the early water only when the tile could actually weed before its next in-window water is due.
6. Triage the wider suite — 27 failed / 8 errors outside `test_router.py`, believed to be stale RL-era tests plus env changes from PRs. Not yet verified.
7. Market adaptivity, deferred until matching is done.
   The agreed split: the schedule commits *production* (open-loop — a melon is a bet 10 days ahead); *disposal* need never be committed, so `sells` becomes a release budget and the executor walks the computed marginal curve at order time.
   `market_price(item, inventory)` is pure and exactly computable client-side; `BUY_PRODUCT` quotes at `market_price(inventory - 1)`; shops restock every 4 steps, town centre every 12, 4x from day 20.

## Standing traps

- `TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")` stripping is **inert** for the shipping agent — `schedule_agent.py` reads none of them. Only the retired `dayplan` path did.
- `RANK` in `schedule_agent.py` is **dead code** for the shipped agent; it lives in the `else:` (greedy, `router=False`) branch.
- Replay the tape from `steps[1:]`. Offset 0 gives $45,387 against a recorded $141,256; offset 1 gives $149,662.
- `env.reset()` draws a fresh seed unless one is passed explicitly. Always pass `--seed`.