# The field passed カワシギ. What the top clones do that we do not.

Measured 2026-08-26, Mac, worktree `corner`.
Sources: 120 episodes of `kaggle/kaggriculture-episodes-2026-08-25` (pulled 2026-08-26, winner
>= $60k filter) at `data/seed_scripts/daily_2026-08-26/`, and our own 54 ladder replays at
`data/seed_scripts/ours_2026-08-26/`.
Scripts: `scripts/what_the_new_field_is_doing.py`, `scripts/where_the_clones_beat_us.py`.
Logs: `data/logs/new_field.log`, `data/logs/clones_vs_us.log`.

## カワシギ is 12th

```
      bank  tiles  crops@bell  herd            top crops                       name
   153,113     27          12  11co 4sh        whea134 stra41 carr20 melo11    Arda Ceylan
   147,576     19           3  11co 4sh        whea134 stra38 carr20 melo11    G!vIOne
   141,250     27          12  11co 4sh        whea134 stra38 carr20 melo11    UjjwalPardeshi
   139,769     28          12  11co 4sh        whea134 stra41 carr20 melo11    Tom3
   134,682     37          14  10sh 6co        whea128 stra39 carr12 melo11    Bharath Varma
   131,597     32           0  10co 4sh        whea121 stra34 melo20 carr6     カワシギ
```

The top of the field is **one script under many names** -- `whea134 stra38 carr20 melo11` on an
11co/4sh herd repeats verbatim across nine of the top twelve seats. A second cluster runs
`whea128 stra39 carr12 melo11` on 10sh/6co over 37 tiles.

They are running his shape with changes, which is what we are doing, and they are ~$20k ahead of
him. **That makes them the right comparison target, not him.** A difference against カワシギ is
confounded by everything the clones also changed.

## Matched on the shop draw

Shops unlock on a fixed 3-day cadence but the DRAW varies, and YARN_STORE is what puts a town bid
under WOOL -- so a seat that drew yarn at d6 plays a different economy from one that drew it at d24.
Comparing herds across different draws is apples to oranges.

```
   clone YARN_STORE day: d3:3  d6:3  d12:2  d15:2  d18:2  d21:3
   ours  YARN_STORE day: d3:5  d6:4  d9:5  d12:4  d15:5  d18:2  d21:3  d24:1  d99:25
```

Compared only on draws present on both sides: **15 clone seats, 23 of ours.**

## The gap

```
=== d12-d29 totals per seat, ours minus theirs
   PLANT                   114.5    120.3     -5.8
   WATER                   763.7    709.9    +53.8
   HARVEST                 346.5    371.4    -24.9
   FEED                    257.2    254.1     +3.1
   CARE                    256.0    254.2     +1.8
   FERTILIZE               119.7     82.9    +36.8
   COLLECTFERTILIZER       272.1    264.4     +7.6
   PICKUP                  171.7    202.0    -30.3
   DROP                     49.7     94.2    -44.5
   PLACE                    22.2     30.3     -8.1
   DIG                      49.2     44.1     +5.1
   PASS                    437.4    179.8   +257.5
   MOVE                   2097.0   2508.2   -411.2
```

**We idle 437 unit-turns; they idle 180.** They spend the 411 extra turns walking and convert them
into +25 harvests and nearly double the shed traffic.

Per day, and it is not spread out:

```
        PASS ours   PASS clones
  d12        46.7          21.7
  d13        57.8          20.4
  d15        53.1           5.1
  d18        50.1           7.5
  d19        32.3           3.9
```

**On d15 the whole clone crew PASSes 5 times. We PASS 53.**

## Three things they do that we do not

1. **They hire more, and later.** Crew d24 **13.5**, d26 **14.7**; ours is **12.0** flat.
   We idle the hands we have AND do not buy the ones they buy.
2. **They replant hard late.** PLANT d24 **17.5** and d26 **17.3** against our 9.5 and 10.9, paired
   with DIG 10.7 and 10.9 to clear spent ground first. We dig late (d27 12.8) and do not re-sow
   behind it.
3. **They fertilize far less** -- 82.9 against our 119.7. Same finding as against カワシギ (65 vs our
   122), now confirmed against the winners.

## Correction: standing crop is NOT our defect

```
   standing   d27    d28    d29
   clones    98.9   67.8   23.7
   ours      64.4   32.6   13.5
```

**The winners carry MORE standing crop than we do, all the way through.**
カワシギ's clean field (2.2 units on 1.5 tiles) is what made this look like our biggest problem all
day; he is 12th. The whole "we leave 6x more crop standing" thread was chasing a property of the
12th-place agent, not of the winners.

## Geese, tomato, carrot -- closed on a field that can sell

- **GOOSE: 7 of 240 seats, all in the bottom half (4%), best $108,672.** Nobody in the top decile
  places one. The deletion stands.
- **TOMATO: 8 of 240, best $120,828** (Ryo Hasegawa, 11 plants, 21st). Not a lever.
- **CARROT: 217 of 240 seats plant it, mean 19.2.** It is standard now. But the gradient matters:
  top decile plants **14.4**, bottom half **20.5**. More is not better; the bottom over-plants it.
  カワシギ plants **6** and we inherited his melon-heavy mix from the tape.

**Broken measurement, recorded so it is not mistaken for a result:** `seats that SOLD` came back
empty for every product in `data/logs/new_field.log`. The observation has no `shed` key -- farm keys
are `farmer, hands, hires_today, money, tiles, unlocked_quadrants` -- so the detector had nothing to
read. **`EGG sold by 0/240` is a bug, not a finding.** Answering the egg question needs
`kagg/analysis/fills.py`.

## Herd shape

Top decile **cow 8.67 / sheep 6.58**; bottom half **cow 9.71 / sheep 4.48**.
The winners keep more sheep and fewer cows than the field. We ship 10co/4sh, which is the
bottom-half shape.
