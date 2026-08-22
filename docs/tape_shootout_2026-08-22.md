# The (True, True) tape shootout — 2026-08-22

Which recording should `REPLAY_OPENING_TAPE[(True, True)]` hold — the key that governs a season
where both the melon latch and the q4 latch arm.

6,048 seasons. 48 stratified towns x 9 opponents x 3 seeds (11, 42, 7) x 6 arms, 14 jobs, 2h16m on
the Windows box.
Rows: `data/logs/tape_shootout_rows_2026-08-22b.csv` (also pulled local).
Run log on the box: `/home/alex/kaggriculture/data/logs/tape_shootout_2026-08-22b.log`.

## Answer

**`tt_straw_q4_128k`.**

Restricted to the seasons where each arm actually changed the outcome against control:

    arm                     n diff  arm win%  ctrl win%    swing  mean delta $
    tt_q4melon                   0   -- identical to control, measured nothing --
    tt_straw_q4_128k           420     90.0%      62.1%   +27.9          -822
    tt_straw_q4_136k           420     73.8%      62.1%   +11.7        -1,653
    tt_straw_q4_81k            420     64.8%      62.1%    +2.6        -3,564
    tt_straw_q3_old            420      6.0%      62.1%   -56.2       -21,835

Over all 1,008 seasons per arm, undiluted:

    arm                        n   win%  mean ours  vs control  identical
    control                 1008  54.7%     88,282          +0     100.0%
    tt_q4melon              1008  54.7%     88,282          +0     100.0%
    tt_straw_q3_old         1008  31.2%     79,184      -9,098      58.3%
    tt_straw_q4_128k        1008  66.3%     87,939        -342      58.3%
    tt_straw_q4_136k        1008  59.5%     87,593        -689      58.3%
    tt_straw_q4_81k         1008  55.8%     86,797      -1,485      58.3%

## Read this before quoting the numbers

**`tt_q4melon` is a phantom null.** Byte-identical to control on all 1,008 seasons — it never armed.
Roughly 20 minutes of the run measured nothing.
Its 54.7% is control's number, not its own.
Same shape as the null already recorded in `CLAUDE.md`: "q4-vs-q3 read +$0 on twelve seeds because
BOTH arms armed it and got identical rows."
Why it failed to arm is **open**.

**The winner banks less money and wins more games.**
`tt_straw_q4_128k` is $822/season poorer than control on the seasons it changes, and wins 27.9
points more of them.
This is precisely the case the project rule exists for: the ladder is Elo, a $43k win and a $4k win
score the same, so **select on win rate**.
Anyone re-reading this and seeing "mean ours 87,939 vs control 88,282" as a regression has read the
wrong column.

**Each arm only touches the `q4melon` tape key.**

    tt_straw_q4_128k, seasons by tape key:
        q4melon      changed  420   identical    0
        straw        changed    0   identical  588

That is the intended blast radius and it is worth confirming rather than assuming: an arm that
moved the `straw` seasons too would be rewriting rows it was not asked to.

**The ordering is not what the recordings' own banks predict.**
128k beats 136k beats 81k.
The best recording to replay is not the highest-banking one.

## Caveats

- 3 seeds. Seed variance in this project is ~15%; a 27.9-point swing is well outside that, a
  2.6-point one (`tt_straw_q4_81k`) is not.
- Win rate is against the seated opponent, not an Elo simulation.
- No release proposed. The 2,600 on the board stays.

## Next

The fourth-parcel land arms (`control land_d12 land_d13 land_d14 land_d16 land_d18`) started
automatically in the same tmux session `grids` at 11:2x and write to
`/home/alex/kaggriculture/data/logs/land_rows_2026-08-22.csv`.
