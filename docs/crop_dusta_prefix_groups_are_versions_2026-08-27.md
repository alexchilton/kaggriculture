# Crop Dusta's prefix groups are VERSIONS, not branches — clone the new one

Measured 2026-08-27. `/tmp/dusta_prefix.py`, `/tmp/dusta_lineage.py`.
Logs `data/logs/dusta_prefix.log`, `data/logs/dusta_lineage.log`.
Corpus: 150 unique Crop Dusta games found across `data/seed_scripts/*/` and `~/Downloads`.

## Why this was checked

Alex asked whether Crop Dusta "has maybe 8 tapes which would cover a high percentage of his games",
so that his opening could be cloned as an arm set and only the tail planned.

The prefix table said yes, emphatically:

```
      cut  turn  distinct    top 1    top 2    top 4    top 8   top 16
     d1h0    24         3    56.0%    98.7%   100.0%   100.0%   100.0%
     d2h0    48        10    53.3%    82.0%    93.3%    98.7%   100.0%
     d3h0    72        15    52.0%    77.3%    87.3%    94.0%   100.0%
    d3h16    88        21    42.0%    60.7%    74.0%    88.7%    96.7%
     d5h0   120        28    42.0%    52.0%    67.3%    82.0%    92.0%
     d7h0   168       122     3.3%     5.3%     9.3%    16.0%    26.7%
    d10h0   240       146     1.3%     2.7%     5.3%     8.0%    13.3%
```

63 of 150 games byte-identical through turn 120 looked like a ready-made shared prefix.

**It is not.** The 150 games span weeks and he resubmitted. A prefix group can be a *version* of his
agent rather than a branch of one, and a latch rule fitted across versions is fitting a calendar.

## The measurement

EpisodeId is monotonic in time, so the test is whether group membership tracks it.

```
=== cut turn 24 (d1h0) ===
     n      ep min      ep max   won/played
    84    94545368    97518736    65/84     77.4%    <- old version
    64    97601003   100439982    57/64     89.1%    <- new version
     2    97609790    97696699     2/2
```

The ranges are **disjoint**. The changeover sits between ep 97518736 and ep 97601003.

The 63-game "dominant lineage" at turn 120 spans `94545368..97516492` — entirely old era, 52/63.
It is his replaced agent.

## Within the new era the splits ARE branches

At turn 120 the new-era games interleave in time, which is the opposite signature:

```
     15    97637134    97710447    15/15
     13    97639412    97703592    11/13
      7    97621163    98951020     7/7
      6    98852910    98951021     4/6
      4    98898505    98951023     4/4
```

The 7-group spans 97.62M–98.95M and the 6- and 4-groups sit inside that span. Overlapping ranges
mean the same agent chose differently on different boards. Those are decisions, and a decision can
be predicted from observables; a version cannot.

## The architectural constraint this exposed

An arm set latched at turn `L` requires every arm to be **byte-identical on turns 0..L**. The eight
groups at turn 120 differ *before* turn 120 by construction, so they cannot be eight arms latched at
120. This is already asserted in `scripts/build_diment_clone.py` as `PREFIX_GATE`; the coverage table
does not satisfy it.

The latch must sit at or before the first divergence among the chosen arms. For the new era:

| latch | arms available | note |
|---|---|---|
| turn 24 (d1h0) | all 64 | board at t=24 is near-fixed, so little signal for a selector |
| turn 48 (d2h0) | ~43 | deeper shared prefix, more signal |

## Caveat on the win rates

This archive is not loss-selected — it is 122/150 wins overall, so
`project_kaggriculture_losing_narrowly` does not apply. But it is also not a uniform random sample
of his games, so 89.1% vs 77.4% is the record *in this archive*, not his ladder win rate. The gap is
z≈1.95 on a two-proportion test: suggestive, not established.

## What changes

- Any Crop Dusta clone must filter to **ep >= 97_600_000**. 64 games, not 150.
- The turn-120 coverage numbers in `data/logs/dusta_prefix.log` describe two agents averaged
  together and must not be quoted as one.
- `docs/clone_lineage_state_2026-08-26.md` reports "145 distinct full-season scripts out of 146
  games" for him — that figure also spans the version boundary.
