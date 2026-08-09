# The two private bots beating Kaggriculture's public meta

Shared by Alex on 2026-08-09, verbatim from a public notebook ("The Two Private Bots Beating
Kaggriculture's Public Meta").
Companion dataset: *Cracking Kaggriculture's Top-5: Opening-Move Data*.
Method: 3 recent replays per top-5 team, actions extracted from the first 48 steps, clustered by
opening signature.
Snapshot 2026-08-09.

Saved here because it is the first outside description of the field we have, and because it
answers a question this project has been guessing at for two days — what the leaders actually do.

## The three clusters

| Cluster | Teams | Ladder | Day-0 signature |
|---|---|---|---|
| `v23_fork` | three top-5 teams | 3,117 – 3,131 | 5 hires · 2 cows + 2 sheep · 7 wheat / 12 melon seeds · 0 strawberry |
| `sheep_first_hybrid` | HealthStone (rank #2) | 3,132.9 | 3 hires · 1 cow + 4 sheep · 5 wheat / 5 melon seeds · sheep-first buys |
| `counter_meta` | Seb (rank #1) | 3,201.1 | 14 hires · 3 cows + 2 sheep · 14 wheat / 3 melon seeds · aggressive labor |

Three of the top five run an **identical** opening down to seed counts: the public reference agent
`kaitofukami v23`, verified by running v23 locally in self-play and confirming byte-identical
opening actions.
That public agent is a hard ceiling at 3,117–3,131.
The two teams above it run nothing public.

## Cash on hand, days 0-5 (mean of 3 episodes per team)

| Day | HealthStone | Seb (`counter_meta`) | `v23_fork` |
|---|---|---|---|
| 0 | 3,000 | 3,000 | 3,000 |
| 1 | 14 | 562 | 22 |
| 2 | 14 | 353 | 22 |
| 3 | 18 | 656 | 152 |
| 4 | 26 | 481 | 417 |
| 5 | 214 | 766 | 694 |

* **HealthStone front-loads everything** — $14 by day 1, held there for four days, betting on CARE
  compounding from a sheep-weighted herd (sheep interval 3 days, so CARE banks +3 per yield against
  a cow's +1). Every wheat buy in week one is survival, not accumulation.
* **Seb keeps a real cushion**, $500+ through days 1-5, which funds a four-quadrant expansion.
* **`v23_fork` is in between**: broke on days 1-2, then rebuilding.

## Final state

| | `v23_fork` | HealthStone | Seb |
|---|---|---|---|
| Land quadrants | 3 | 3 | **4** |
| Cows | 8 | 8 | 9 |
| Sheep | 6 | 4 | **11** |
| Total animals | 14 | 12 | **20** |
| Avg final coins | ~$100k | ~$100k | ~$57k *(in these games; still rank 1)* |

Seb banks the **least money of the three** in the sampled episodes and is rank 1.
That is the Elo lesson in this project's own CLAUDE.md arriving from outside: a $100k win and a
$57k win score the same, and Seb wins by beating the `v23_fork` cluster consistently.

HealthStone runs the smallest herd (12 animals) and matches `v23_fork` on coins — efficiency
through CARE compounding rather than scale.

## What the notebook says the edge is

* `v23_fork` — replicable, copy the public reference, band ~3,117–3,131.
* `sheep_first_hybrid` — needs a redesign around CARE compounding on sheep. The $14-for-four-days
  cash constraint is severe, which is likely why few teams run it.
* `counter_meta` — needs to fund 4 quadrants and 20 animals. *"The cash trap is real (I hit variants
  of it four times when I tried building toward it heuristically); execution has to be tight."*
* **Detection is cheap**: the first 48 turns identify an opponent's cluster. `openings_actions.csv`
  in the companion dataset has the raw stream.
* **What v23 misses**: it is calibrated for a symmetric opponent, and loses to HealthStone and Seb
  in the sampled data.

## What this means for us — read this part with care

**Our best submission scores 1,123.5. The public meta's floor is 3,117.** We are not in a
neighbouring band; we are roughly a third of the way up. The daily episode index says the same
thing independently — `median_avg_score` on 2026-08-08 was **3,067.75**, and `top_avg_score`
3,192.89. Every "we are close, the gap is price realised per unit" reading in
`we_oversell_into_a_contested_book_2026-08-09.md` was made against a field we had mismeasured.

Three specific things to check rather than assume:

1. **Our `seb` tape is not this Seb, or not this Seb's current play.** `scripts/vs_tapes.py` has us
   beating the `seb` tape 4/4 by $40k-$110k. The Seb here is rank 1 at 3,201. Either the tape is
   an old submission of theirs, a different player, or beating a fixed replay of their actions is
   not the same as beating them.
2. **The opening we splice is worth re-deriving.** We hand over on day 11 from a recorded tape. All
   three clusters are distinguishable by day 0 and broke or nearly broke by day 2 — an aggressive
   front-load we do not do.
3. **`counter_meta` is 14 hires and 20 animals.** `scripts/what_the_others_do.py` measured our
   hires at the 14th percentile (12 against a top-quintile 12) and read it as "no headroom". Seb
   opens with 14 hires on day 0. That lever was mismeasured, not absent.

Nothing above is verified by us. It is one notebook's clustering of 15 replays, 3 per team, and the
final-coins column already shows sampling noise ($57k for a rank-1 agent). Treat the *signatures*
as leads to verify against `data/ladder/leaders_0808/`, which is 20 real episodes from the same
day, and treat the *ladder numbers* as confirmed, because the episode index agrees with them.
