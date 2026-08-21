# The FEED target counts ops tetsuya submitted, not ops that landed

Measured 2026-08-20 on `data/seed_scripts/downloads_2026-08-19/94345389.json`, tetsuya seat 0,
seed 959074148.
Read straight out of the replay: `fed_today` / `cared_today` on every animal tile at hour 23 of
each day, against the `FEED`/`CARE` ops in his own `farmer` and `hands` action lists.

## The finding

`FEED` takes a WHEAT from the acting unit's **carried** inventory, not from the shed
(`reference/kaggriculture.py:505-513`, `inv = _farmer_inventory(private, idx)` at `:321`).
If the unit carries none, the op returns silently and the animal stays unfed.

Nine of his FEED ops in the first sixteen days do exactly that.

     day | FEED sub  FEED landed | CARE sub  CARE landed
     d0  |     5         0       |     5         5
     d1  |     5         5       |     5         5
     d2  |     5         5       |     5         5
     d3  |     6         5       |     6         6
     d4  |     8         6       |     8         8
     d5  |     8         8       |     8         8
     d6  |     8         8       |     8         8
     d7  |     9         8       |     9         9
     d8  |     9         9       |     9         9
     d9  |    11        11       |    11        11
     d10 |    11        11       |    11        11
     d11 |    13        13       |    13        13
     d12 |    15        15       |    15        15
     d13 |    15        15       |    15        15
     d14 |    15        15       |    15        15
     d15 |    15        15       |    15        15
    -----+-----------------------+----------------------
    0-15 |   158       149       |   158       158

**On d0 he submits five FEEDs and lands none of them.**
He buys 5 WHEAT at h1 and sells all 5 back at h2; the shed reads 0 for the remaining
twenty-two hours and no unit ever picks any up.
His five animals finish d0 `fed_today=False` and `cared_today=True`.

CARE has no input cost, so submitted and landed are equal on every single day.

## What this corrects

The d0–d10 grid compares OUR submitted ops against HIS submitted ops:

    FEED  73/85       <- 85 is what he sent; 76 is what he achieved
    CARE  76/85       <- 85 is real; CARE never fails

So the FEED gap is **73 against 76, not 73 against 85**. Three ops, not twelve.
The CARE gap of nine is real and is now the larger of the two.

This also retires the wheat-supply theory for d0. There is nothing to copy there: matching him
exactly on d0 means wasting five turns. Feeding the d0 arrivals is a place we can **beat** him,
not a place we are behind.

## What it does not correct

The `d0 FEED 3/5` shortfall in our own run is still measured against ops we submit, so our own
landed count is unknown and is `<= 3`. Measure ours the same way — `fed_today` at h23 — before
sizing any fix.

## The general rule this is an instance of

`docs/SUPER_IMPORTANT_READ_THIS_FIRST.md` §2: measure at the decision, not at the census.
This is the same failure one layer down. An op counted from the action stream is an *intention*.
The env drops PLANT on a short seed bag, HIRE on a thin bank, FEED on an empty hand — all
silently. Any target read off a leader's action stream is an upper bound on what he achieved,
and the gap is not always small.

Related: `feedback_offers_are_not_fills` — never sum offers, the agent re-posts each order 24x a
day. Same shape: submitted is not settled.
