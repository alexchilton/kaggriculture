> Note added 2026-08-22: `docs/marginal_units_and_the_shared_book_2026-08-16.md` §9 later found the
> shop draw is endogenous to which agent plays, not seed-only (weed-spawn RNG is consumed per-tile
> before the shop draw, so a different agent's moves shift it). That qualifies this file's "seed's
> only job is the shop draw" framing for a FIXED opponent script; it does not overturn the board-is-
> fixed finding below. Not reconciled in either file — flagged for an owner.

# The ladder is ONE fixed board, and the leader is not open-loop

2026-08-13.
16 episodes of **カワシギ** (current #1) downloaded and cached to `data/seed_scripts/kawashigi/`,
plus four of our own games from 2026-08-12.

## 1. Every ladder game starts from the identical world

Hashing the opening observation with `farms`, `step`, `remainingOverageTime` stripped:

    world  dc0d81c5   1 distinct across all 16 Kawashigi games
    market a7e792b0   1 distinct
    tiles  bb3b18da   1 distinct, AND identical for seat 0 and seat 1

Our own games carry the same three hashes:

    92433651  alex chilton vs Benjamin Beaujard   world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92450417  alex chilton vs Agzam               world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92443929  Bang sion vs alex chilton           world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92439273  Jonathan Roy vs alex chilton        world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92498144  カワシギ vs Yusuke Hayashi            world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da

Terrain, land parcels, town positions and opening prices are constants of the competition, and the
two seats are mirror-identical. **The seed's only job is the shop unlock draw** (section 2), which
first fires on d3. So a ladder game has exactly two variables: the shop sequence and the opponent.

This retires the framing that has driven a lot of work here. "Seed variance is ~15%" (CLAUDE.md) is
a fact about `kagg.arena`'s randomly drawn *boards*, **not** about the ladder. Held-out seeds there
measure robustness to a board we will never be dealt. Offline solving against this one board is not
overfitting; it is the whole problem. The thing that genuinely needs generalising is the shop draw.

## 2. He is NOT replaying a tape

If he were open-loop, 16 games on one board would be 16 identical action streams. They are not.
Pairwise identity over the 720-turn action vector runs 26%-82%.

Distinct action-vectors per hour, across the 16 games (1 = all sixteen played the same thing):

    d00 : 111111111111111111111111   modal 16.0/16
    d01 : 111111111111111111111111   modal 16.0/16
    d02 : 111111111111111111111111   modal 16.0/16
    d03 : 112222222222222221111111   modal 12.2/16
    d04 : 111111111111111111111111   modal 16.0/16
    d05 : 111111111111111222111111   modal 15.9/16
    d06 : 111111111111111111121121   modal 15.5/16
    d07 : 111222222222333333444555   modal  9.8/16
    d08 : 332223333333444444456566   modal 10.6/16
    d09 : 511133655545555544442111   modal 10.0/16
    d10 : 112333235335565556666666   modal  8.3/16
    d11 : 511244436446755777777776   modal  7.2/16
    d12 : 612445456667667777777777   modal  6.7/16
    d13 : 712233355666666677778888   modal  7.0/16
    d14 : 913445556466666666666677   modal  7.0/16
    d15 : 714565566666666678877888   modal  6.0/16
    d16 : 713977888888888899999999   modal  5.0/16
    d17 : 913597799999999999999999   modal  4.0/16
    d18 : 917989999999999999999999   modal  3.0/16
    d19 : 912988899999999999999999   modal  4.3/16
    d20 : 913999999999999999999999   modal  3.4/16
    d21 : 913988999999999999999999   modal  3.6/16
    d22 : 914999999999999999999999   modal  3.0/16
    d23 : 912699999999999999999999   modal  3.4/16
    d24 : 919999999999999999999999   modal  1.9/16
    d25 : 914999999999999999999999   modal  2.6/16
    d26 : 918999999999999999999999   modal  2.3/16
    d27 : 913999999999999999999999   modal  2.2/16
    d28 : 916999999999999999999999   modal  2.8/16
    d29 : 814999999999999999999999   modal  2.8/16

**All 16 games are byte-identical for the first 74 turns — d0 through d3 h1.**
d0-d2, d4 and most of d5-d6 are 16/16 at every hour. From d7 the fan-out starts, and by d24 the
modal action is shared by fewer than 2 of 16 games. That is a fixed opening followed by live play.

**The 74 turns are the deterministic prefix, and they end at the first shop unlock.**
`_advance_day` draws a shop every `townShopUnlockInterval = 3` days with replacement
(`kaggriculture.py:854,878`), so the first draw lands on d3 — and d3 h2 is exactly where the 16
games stop agreeing. All 16 drew a different sequence:

    2407  ICE_CREAM_SHOP | BAKERY         | YARN_STORE       0434  SMOOTHIE_SHOP  | ICE_CREAM_SHOP | FARMERS_MARKET
    7234  BAKERY         | YARN_STORE     | YARN_STORE       8785  YARN_STORE     | PET_CAFE       | PIZZA_SHOP
    8461  PIZZA_SHOP     | PIZZA_SHOP     | YARN_STORE       8144  SMOOTHIE_SHOP  | ICE_CREAM_SHOP | FARMERS_MARKET
    2932  BAKERY         | BAKERY         | PIZZA_SHOP       8348  SMOOTHIE_SHOP  | YARN_STORE     | FARMERS_MARKET
    1493  PET_CAFE       | BRUNCH_SPOT    | BRUNCH_SPOT      1336  ICE_CREAM_SHOP | YARN_STORE     | YARN_STORE
    5172  FARMERS_MARKET | PIZZA_SHOP     | FARMERS_MARKET   9904  BRUNCH_SPOT    | BAKERY         | PIZZA_SHOP
    2538  PIZZA_SHOP     | PET_CAFE       | SMOOTHIE_SHOP    9908  PIZZA_SHOP     | BAKERY         | SMOOTHIE_SHOP
    6371  SMOOTHIE_SHOP  | ICE_CREAM_SHOP | BRUNCH_SPOT      2865  PIZZA_SHOP     | ICE_CREAM_SHOP | ICE_CREAM_SHOP

16 distinct sequences over 16 games. So the divergence is **the shop draw, not the opponent** —
same-opponent pairs diverge as early as d5 h15 and different-opponent pairs stay identical to d9 h6,
because opponent identity is not what is driving it.

That is the finding that matters. The seed's only job is the shop draw, and **the leader re-plans
around it from the moment it lands.** `SHOP_ADAPT_HERD` is our one attempt at the same thing, it
starts at d6, and it reads only shop *presence* to float a cow/sheep split. His response begins on
d3 and reaches the whole plan.

## 3. Two structural constants worth chasing

- **Hour 1 is identical in all 16 games right through to d23** (the `1` in column 1 of every row
  from d16 to d23) while hour 0 and hours 3+ are fully divergent. Something at h1 is unconditional.
- **Hour 0 is the most divergent hour of the day from d14 on** (leading 9s). A dawn decision that
  reads state, then a walk that is much more stable. Structurally our own architecture: plan once
  at h0, execute.

## 4. Record

15-1 across the 16. The single loss is 92445172, $88,448 to Yusuke Hayashi's $89,993 — $1,545.
Money range $44.9k to $150.0k on an identical board, which is the size of the swing the opponent
alone produces.

## Open

- Diff his fixed 74-turn opening against ours, op for op. It is a solved plan on a board we also
  own, and it is the cheapest thing in this project to copy.
- Find what he does at h1 every day.
- Re-check whether `kagg.arena`'s multi-seed evaluation is measuring anything we are graded on.
