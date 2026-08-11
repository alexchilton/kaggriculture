> **TARGET SUPERSEDED, added 2026-08-11.** Seb's tape was optimal under the OLD
> `townCenterSellInterval=12` economy; his median bank halved and he has since withdrawn from the
> ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats). The route mechanics below are
> still an accurate reading of the recorded tape — only the choice to imitate this particular herd
> and feed cadence, rather than the field's, is now in question.

# How Seb feeds seven animals on day 4

Read straight off tape 91422988, seed 11, Seb's own seat, day 4.
He scores `FEED 7`, `CARE 7`, `PLACE 1`, `COLLECT_FERTILIZER 6`.
We score `FEED 5`, `CARE 5`, `PLACE 1` from the same board.

## The shape of his day

Three pickups, all in the first two hours, on three different hands:

    h1  u1  PICKUP WHEAT 3
    h2  u2  PICKUP WHEAT 3
    h2  u6  PICKUP COW 1

Seven drops, none of them before hour 18:

    h18 u7 | h21 u2, u3, u6 | h22 u5 | h23 u0, u1

The shed runs `6 -> 3 -> 1` in the first two hours and sits on 1 until h18, when the
harvest lands. He empties it deliberately and never goes back.

## Three roles, not one

**u1 — wheat carrier A.** Draws 3 at h1, spends them walking outward.

    h1 (4,4) PICKUP W3   h2 (4,4) FEED   h4 (4,3) FEED   h7 (3,2) FEED
    h8 (3,2) CARE  h9 (3,2) COLLECT_FERTILIZER  then crop work to dusk

**u2 — wheat carrier B.** Draws 3 at h2, sweeps a different arc.

    h2 (4,4) PICKUP W3   h5 (3,3) FEED   h9 (2,2) FEED   h14 (1,3) FEED
    with CARE and COLLECT_FERTILIZER at each, then south to the shed

**u6 — animal carrier and CARE sweeper.** Draws the COW at h2 and carries it for ten
hours, doing the ITEMLESS work at every pen it passes on the way.

    h2 (4,4) PICKUP COW 1
    h3 (4,4) CARE            h4 (4,4) COLLECT_FERTILIZER
    h6 (4,3) CARE            h7 (4,3) COLLECT_FERTILIZER
    h9 (3,3) COLLECT_FERTILIZER
    h12 (1,3) PLACE COW      then walks on -- h13 (0,3) WEST, h14 WATER, h15 HARVEST

## The three rules this implies

1. **Load once, in parallel, at dawn.** Two carriers take the whole shed between them in
   hours 1 and 2. There is no second trip and no mid-day `DROP`, so no wheat is ever put
   back into a shed that another hand has already emptied.

2. **The hand with no wheat does the work that needs no item.** CARE costs nothing to
   carry, so the animal carrier pays for its long walk by caring for every pen it crosses.
   Our herd hand does FEED, CARE and COLLECT at one tile and then moves.

3. **A pen's day is SPLIT ACROSS HANDS, and the feed arrives after the placement.**
   u6 places the cow at `(1,3)` at h12. It does not feed it. **u2 feeds it at h14**, two
   hours later, on a wheat drawn at h2 for a pen that had no animal in it at the time.

## Why rule 3 matters here

`crew.cover`'s docstring states the opposite as a design principle:

> **The unit of ownership is the TILE, not the op.** A pen's whole day -- build it, put the
> animal in, feed it, care for it, take the fertilizer -- belongs to one hand.

The second justification given for it is exactly the case Seb solves differently:

> an animal placed today must be FED today, and `build_nodes` cannot emit a FEED for a tile
> until an animal is standing on it, so the feed is invisible at plan time

Seb's answer is not to give the pen to one hand. It is to send a **second** hand, already
carrying wheat, past the pen *later in the day* than the hand that filled it. The feed is
not invisible to him because it is not planned as part of the placement at all -- it is one
stop on a wheat carrier's sweep, and the sweep is timed to arrive after the placement.

Tile ownership is not wrong -- it fixed a real pairing failure (`place 3/4`, `feed 3/4`,
d3 bank $28 against $478). But it is what forces the placing hand to carry its own feed,
which is what forces the mid-tour re-supply `DROP`, which is what loses the wheat.

## What it costs us on day 4

Our herd hand u4 does all three roles alone:

    h1 PICKUP COW 1   h2 PICKUP WHEAT 4   h3 FEED (4,4)   h4 CARE
    h6 DROP           h7 PICKUP COW 1     h8 PICKUP WHEAT 1   <- asked 3, got 1
    h10 FEED (4,3)    h11 CARE            h14 PLACE COW (3,3)   <- arrives empty
    h15 walks off; the cow is never fed or cared for

`DROP` is all-or-nothing (`kaggriculture.py:333`), so the h6 re-supply dumps the cow too and
pays to pick it up again. By h8 the shed holds 1 wheat, the leftover want is deleted
(`schedule_agent_1455mh.py:1761`), and the shed is bare from h9 to h18 -- so
`FETCH_THE_FEED_AND_RETURN` cannot fire either.

Wheat ledger, both sides: 6 in the shed at dawn, 1 bought during the day, 7 animals.
**He buys exactly what we buy.** He is not better funded; he simply never spends a wheat on
a round trip.

## Open

- Seb performs 7 FEEDs having drawn only 6 wheat. u7 feeds `(2,3)` at h7 without ever
  visiting the shed, so it began the day holding wheat. Not yet confirmed whether the
  midnight sweep (`_drop_inventories_to_shed`) leaves a remainder in hand or whether the
  seventh wheat comes from somewhere else.
- Between our h6 `DROP` and our h8 re-pickup, one wheat AND the collected fertilizer both
  disappear from the shed. Either the drop overflowed shed capacity -- overflow is discarded
  outright (`kaggriculture.py:340`) -- or another hand drew them. Not yet separated, and it
  matters: if it is capacity, the round trip is destroying goods, not merely costing turns.
