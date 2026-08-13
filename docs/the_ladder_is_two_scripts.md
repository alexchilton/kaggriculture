# The top of the ladder is two shared scripts, and we are not playing either

> **Addendum 2026-08-13: the ladder is one fixed board, and the current #1 is not open-loop.**
> 16 downloaded games of the ladder's then-current #1 (カワシギ, 15-1, bank range $44.9k-$150.0k)
> plus 4 of our own games are hash-identical on world/market/tiles observation across all 20 games
> and both seats — terrain, land parcels, town positions and opening prices are constants of the
> ladder itself, not a per-seed draw. **The "seed variance ~15%" figure describes `kagg.arena`'s
> randomly drawn boards and does not apply to the ladder.** カワシギ is also, contrary to the general
> open-loop finding below, reactive from day 3: all 16 of its games are byte-identical for exactly
> the first 74 turns (through the moment before the first shop-unlock draw,
> `townShopUnlockInterval=3`), then pairwise action-vector identity drops to 26%-82% and divergence
> tracks the shop draw, not the opponent. Hour 1 stays identical across all 16 games through d23;
> hour 0 is the most divergent hour from d14 on. `SHOP_ADAPT_HERD` is our nearest analog but starts
> later (day 6) and reads only shop presence for a cow/sheep split; カワシギ's response reaches the
> whole plan from day 3. Diffing its fixed 74-turn opening op-for-op against ours is cheap and
> unexplored. Full detail: `docs/REGISTER.md` OPEN-14.
>
> **Two smaller, older field-description docs were folded in here and deleted, both explicitly
> superseded in scale by the 2,744-seat sample above but each carrying one detail not otherwise
> recorded** (see "Prior, smaller-scale field evidence" below): a 15-replay opening-cluster read
> (`the_top_five_clusters_2026-08-09.md`) and a 20-episode leader/op-census read
> (`what_the_leaders_actually_grow_2026-08-09.md`).

Measured 2026-08-11 from the official episode datasets, `kaggle/kaggriculture-episodes-2026-08-09`
and `-08-10`: 1,372 episodes, 2,744 seats, 40 GB of replays.
Extracted by `scripts/episode_index.py` (parallel, one JSONL row per seat) into
`data/episodes_2026-08-09.jsonl` and `data/episodes_2026-08-10.jsonl`.

## Where we actually stand

| | rating |
|---|---|
| THUNDER THUNDER (#1) | 3,210.9 |
| Victor @ Tufa Labs (#2) | 3,149.8 |
| median episode in the dataset | ~3,079 |
| **our best submission ever** | **1,257.9** |
| our submission of 2026-08-11 | 845.1 |

**None of our games appear in the two-day sample at all** — 0 of 2,744 seats.
This is not a tuning gap. The field is at ~3,000 and we are at ~1,000, and the ladder starts at 600.

## The field is running two scripts

Median values per player, players with 5+ games in the sample:

| player | n | bank | WHEAT | STRAW | MELON | COW | SHEEP | GOOSE | buy wheat | sell wheat |
|---|---|---|---|---|---|---|---|---|---|---|
| Haramball forever! | 5 | 97,828 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| Natalia Mawyin | 16 | 94,116 | 147 | 38 | 17 | 9 | 6 | 0 | 257 | 446 |
| Mohammed Nomaan | 23 | 94,006 | 147 | 38 | 17 | 9 | 6 | 0 | 257 | 446 |
| Dmitry Belan | 35 | 93,921 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| Ueddy | 25 | 90,219 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| THUNDER THUNDER | 111 | 90,112 | 144 | 36 | 19 | 9 | 5 | 0 | 245 | 430 |
| Efe Can Celiksoy | 53 | 87,378 | 146 | 37 | 19 | 10 | 4 | 0 | 234 | 459 |
| Changyuan Chen | 11 | 93,674 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| Mohamed abdelrazik | 32 | 91,682 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 397 |
| CemBas | 13 | 89,846 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| SHAURYA SHARMA | 32 | 89,262 | 108 | 42 | 24 | 8 | 6 | 0 | 267 | 302 |
| janson | 24 | 88,990 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| tao wu11 | 10 | 88,462 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |

Nine separate accounts report **WHEAT 108 / STRAW 42 / MELON 24 / COW 8 / SHEEP 6 / buy 266 / sell 305**
to the unit.
Seven more report **WHEAT ~144 / STRAW ~37 / MELON ~19 / COW 9 / SHEEP 4-6**.
That is not convergent evolution, it is two shared scripts.

## Timing

**Script A** (wheat ~144): 1 COW + 4 SHEEP on d0, the bulk of the cows on **d5-d8**, then a trickle
to d19. First PLANT at d0 turn 6. First SELL on d2, median sell day 21.

**Script B** (wheat 108): ~2 COW + 2 SHEEP on d0, cows on **d7-d10**, sheep on **d10-d11**.
First PLANT at d0 turn 8. First SELL on d0, median sell day 21.

## What separates us from all of them

- **Wheat.** They plant it 108-147 times a season; our schedule plants **24**. Wheat's book is
  starved in all 87 recorded tapes and closes at $40-59 against a $25 base, so it is the one product
  the market never saturates. They grow their own feed and sell the surplus; we buy 505 units.
- **Herd size and mix.** They run 13-16 head, cow-heavy (COW 8-10, SHEEP 4-6). Our schedule runs 21,
  and on the analysed loss `SHOP_ADAPT_HERD` bought **16 sheep and 5 cows**.
- **Geese.** Nobody in the top 16 owns a single goose.
- **Re-posting.** Measured by whether a SELL repeats the same `(item, qty)` on the next turn:
  the field is at **3-7%**. Ours re-posts its quota on all 24 turns of a day. We are the only agent
  in the sample that does this.

## Open-loop

Per-day action hashes, compared between games by the same player. One differing turn kills a whole
day, so this is a strict lower bound on similarity.

    Haramball forever!   24/30 days identical      Efe Can Celiksoy   18/30
    janson               21/30                     Mohamed abdelrazik 17/30
    Dmitry Belan         21/30                     SHAURYA SHARMA     11/30
    CemBas               21/30                     THUNDER THUNDER     7/30
    Mohammed Nomaan      19/30                     Ueddy               5/30

Most of the field is scripted. **THUNDER THUNDER, the #1, is the most reactive of the lot** — and on
a separate turn-by-turn diff, two of its same-seat games were only 1.2% identical, diverging at
d0h3. Victor @ Tufa Labs is the opposite extreme: 97-99% of turns identical across seven games on
both seats, with byte-identical season SELL totals.

So the top two are a reactive agent and a fixed script, at 3,210 and 3,149. Both work.

## Does the field adapt to the board? Mostly no — and the one that does, leads

Range across each player's own games. Every game is a distinct shop draw.

| player | n | COW | SHEEP | WHEAT | distinct draws |
|---|---|---|---|---|---|
| Dmitry Belan | 35 | 9..9 | 4..4 | 142..143 | 35/35 |
| Mohamed abdelrazik | 32 | 8..8 | 6..6 | 108..108 | 32/32 |
| janson | 24 | 8..8 | 6..6 | 108..108 | 24/24 |
| **THUNDER THUNDER** | 111 | **6..11** | **4..12** | **132..152** | 108/111 |
| Ueddy | 25 | 6..10 | 4..11 | 142..150 | 25/25 |
| Raiden.B | 27 | 1..15 | 5..19 | 55..120 | 27/27 |

Mohamed abdelrazik played 32 games on 32 different boards and bought exactly 8 cows and 6 sheep and
planted exactly 108 wheat in every one.
The fixed scripts sit at ~3,100; THUNDER, which floats cow/sheep, is #1 at 3,210.

**So adaptive herd is real and worth roughly 110 rating points. The gap from us to a fixed script is
2,255.** Do the base plan first.

## Why our schedule is the wrong target: Seb was optimal under the OLD economy

`townCenterSellInterval` went 12 -> 24 on 2026-08-08, cutting the town's drain ~8x.
Seb's 16 recorded games, split by the economy they were played under:

| | games | median bank | COW | SHEEP | WHEAT | STRAW | MELON |
|---|---|---|---|---|---|---|---|
| interval 12 (old) | 5 | **$137,747** | 5..9 | 10..15 | 19..28 | 41..45 | 18..24 |
| interval 24 (now) | 11 | **$77,737** | 5..13 | 5..20 | 20..36 | 38..43 | 14..25 |

His bank halved while he kept the same low-wheat shape, and he has since withdrawn from the ladder.
The field's answer to the new economy is the thing he does not do: plant 108-147 wheat.

**`data/seed_scripts/top_guys/90976060/schedule.json` — the plan this repo matches op-for-op — is
his interval-12 shape, asking for WHEAT 24 / STRAWBERRY 41 / MELON 17.**
That is the 845-vs-3,100 gap. It is not the planner, the watering or the market logic; it is the
target. Note also that Seb floats COW 5..13 and SHEEP 5..20 — he adapts more than the current field.

## Best tape to rebase on

**Dmitry Belan** (35 games, `COW 9..9 SHEEP 4..4 WHEAT 142..143 STRAW 36..37`) — near-zero variance
makes it a pure script, so the plan reads noise-free.
**Efe Can Celiksoy** (53 games, WHEAT 143..146) is an equally clean second source for cross-checking.
Not THUNDER: it is reactive (7/30 days identical; 1.2% on one same-seat pair), so there is no fixed
plan to extract — it is a sparring opponent and the evidence that adaptive cow/sheep pays.

## What was tried on the crop dynamic, and why all of it is off

`SHOP_ADAPT_CROPS` in `kagg/search/schedule_agent_1455mh.py` carries the full record. Summary:

- **`WHEAT<->CARROT` and `TOMATO<->STRAWBERRY`** — shipped, measured 0.806 vs HEAD's 0.871 over 232
  matched games. They swap toward crops the ladder plants 0.2% and 0.0% of the time.
- **`STRAWBERRY<->MELON`** — produces an identical 54/4 split on every board tested. No shop carries
  melon, so its drain is 29 everywhere; a pair with one board-independent member cannot adapt.
- The shared cause: **the headroom model treats the town's drain as a cliff when the price curve is
  a slope.** A melon past its drain still fetches $229 at +50 and $166 at +100. Any rule scoring on
  "units the town will eat" under-plants every steep-curve, low-drain product. The fix is to price
  the marginal unit off `market_price`, and it is unbuilt.
- **Correction, 2026-08-13: the `WHEAT<->CARROT` 0.806 figure above was measured before the
  SELLABLE fix (`c99a8a5`) — our own agent could not sell CARROT at all at measurement time, so the
  swap's carrot side banked $0 by construction.** Treat as UNVERIFIED, not re-affirmed. See
  `docs/REGISTER.md` C-23 and `docs/the_market.md` §7 for the carrot pool-verdict-void flag more
  generally.

## Prior, smaller-scale field evidence (superseded in scale, not fully redundant)

**A public Kaggle notebook** (shared 2026-08-09, 3 replays per top-5 team, opening-cluster analysis)
found three day-0 signatures: `v23_fork` (3 teams, 3,117-3,131, a byte-identical clone of the public
`kaitofukami v23` reference), `sheep_first_hybrid` (HealthStone, 3,132.9, front-loads to $14 cash
held days 1-4 on sheep CARE compounding), and `counter_meta` (Seb, 3,201.1, keeps a $500+ cushion
days 1-5, funds 4 land quadrants and 20 animals by season end). Seb banked the least money of the
three sampled builds (~$57k vs ~$100k for the other two) yet ranked 1 — an early external
confirmation that money is not the selection criterion.

**20 real leader episodes** from `data/ladder/leaders_0808` (2026-08-08, the day of the
`townCenterSellInterval` switch — treat dollar figures as possibly-old-economy) plus our two losses
showed **18 of 20 episodes are one public reference script (`kaitofukami`-shaped) mirroring itself**,
identical signature WHEAT~103-109/STRAW42/MELON24/COW8/SHEEP6, identical hire ramp — reconfirming
that most of the visible "field" is one script. Only Seb (2 rows) diverged, running sheep-heavy
(SHEEP15/COW7 and SHEEP10/COW9). Two op-census findings not carried elsewhere: our PASS share is
21.6% against the leader average 15.0%, and our WATER share is 7.7% against 13.2% — idle capacity,
not a crop-mix problem. Neither of our two actual losses (Shivam_2212, an exact mirror-baseline
signature, 34% margin; As Wasti, a CARROT/TOMATO five-crop build appearing in zero of the 40 leader
rows, 9% margin) resembled Seb, so beating Seb's tape never implied beating the field.

## Loss forensics: given a loss, why, and how big

**MELON is a fixed pot won by whoever sells first, not a per-tile yield.** 10 downloaded ladder
losses (2026-08-11, `kaggle_environments 1.32.6`, `weedSpawnChance=0.005`) found MELON is drained by
zero of the 8 town shops (closes $4-$25 against a $250 base in 10/10 games). On episode `92077611`
(lost by $1,386) our second melon wave (9 tiles, d10-d20, 66 units for $4,758, ~$72/unit) denied the
opponent's later wave but they still out-volumed us 138 units to 96 and the game was lost anyway —
the fix is ripening earlier (plant d8, not d10), not planting less. We plant MELON 69 on every one of
6 sampled seeds regardless of town composition, because `router.py`'s crop list is copied off one
leader's schedule rather than being town-responsive. **We never plant CARROT or TOMATO despite both
closing above base in 10/10 games** (CARROT $40-42/base $35, TOMATO $77-118/base $60) — this
recommendation predates the 2026-08-13 SELLABLE fix (`c99a8a5`) which had been blocking
CARROT/TOMATO/EGG sales entirely; the price observation is sound, the recommendation was not
actionable when written and should be re-evaluated now that SELLABLE is fixed. On `92077611` we
spent $4,424 more than the opponent despite outselling them by $3,038 in revenue, in a game lost by
only $1,386 — an unmeasured lead (closing-week buy counts run 15-67/day for the opponent against our
fixed 4).

**Given a loss, how big is it — and don't compute a win rate from a losses-only sample.** 60
downloaded games of our own ladder agent (`data/seed_scripts/ours_ladder/`, 2026-08-13) were
downloaded *because* they were losses; an earlier pass computed a win rate from them ("0.085",
"5-54") and that figure was removed as worthless selection bias, per the project's `farm:0.445`
lesson (`CLAUDE.md`). What's unbiased **within** the loss-only sample: 54 losses have median -$8,900,
mean -$11,600, with 6 inside $600, 11 inside $2,100, 23 inside $6,000, 31 inside $10,000 — two losses
were inside $150 (-$70 and -$135). Ruled out as causes: stranded unsold stock (shed empty at season
end) and a single bad matchup (54 distinct opponents, no repeats). Separately, one self-play
validation episode (`91304798`, seed 0) timed out at step 531/720 — flagged as an unquantified
failure mode with no current per-turn latency measurement.
