# Second review brief: answers to your first pass, and what is actually on the ladder

Repo: `/Users/alexchilton/DataspellProjects/kaggriculture`
Worktree for the release branches: `.claude/worktrees/e2500`
Read `docs/handoff_for_review_2026-08-24.md` first — it is the background and it still stands
except where corrected below.

You reviewed this agent earlier today.
Four of your points are now answered with measurements.
One of them came back **against** your hypothesis, and that is the most useful part of this file.
Two of your points are still open and unfixed.

Same rules as last time: I want disagreement, not agreement.
Where a number below does not support the conclusion I drew from it, say so.

---

## 1. Your mind-changer test was run. It says the market is NOT the problem.

You proposed: *"compute realized $/unit per product for our seat vs their seat in every downloaded
game. If we're below ~70% on any major product, sell cadence and sizing is the biggest lever in the
repo. If we're within 90%+, the endgame line stands as the main effort."*

`scripts/what_we_actually_get_paid.py`, 100 games, **both seats in the same game on the same book**,
so the comparison is controlled — any difference is cadence and sizing, not draw luck.
Fills are inferred from `shed + carried` deltas, never from the action stream.

    product      ours/theirs $/unit
    MILK                96%
    WOOL               111%
    MELON              158%
    STRAWBERRY          94%
    CARROT             122%
    EGG                  0%
    TOMATO               0%

Nothing is below 70%. Four of five products traded are at or above parity.

**Two caveats I want you to attack.**

1. **EGG and TOMATO are 0% because we sell literally none of either.** That is not a bad price,
   it is an absent product. Whether that is a missing revenue line or a correct decision is
   untested. It is the one thing in this table I would call a live lead.
2. **This contradicts a standing finding in the project notes** that milk was floored at $1-$5 for a
   whole season while other agents realised $223/unit. Both are true and they measure different
   things: that finding came from 3-5 individually-read *losing* games, this is a 100-game mean.
   The flooding is real and episodic; it is not the average case. I do not know which one predicts
   Elo. Tell me how you would find out.

## 2. What is actually on the ladder — I got this wrong twice today, here it is verified from the files

Every row below was confirmed by grepping the *built artifact*, not the branch.

    submitted 2026-08-24   gate CARROT_DRAIN_MIN=5   shop-price fix   REPLAY_OPENING_DAYS   score
    e2500_carrot.py        YES                        no              (4..11)               1628.0
    shed_clear.py          YES                        no              range(30)  (all tape) 1348.3
    "retry the good"       Kaggle re-upload of the 2500 base, not built locally             1688.7
    e2500_shopprice.py     no                         YES             (4..11)               1292.1

For reference the same base scored **2472.7** on 2026-08-18. These four are still converging and
I would not read the ordering yet.

**The combination has never been submitted.** No artifact has both the carrot gate and the
shop-price endgame fix. It exists as commit `4649af9` on branch `e2500-carrot` and was never
bundled. That is the obvious next build and I want to know if you think it is worth a slot.

## 3. The `LAST_DAY_SELL_TURNS` contradiction you caught was real

You were right. `LAST_DAY_SELL_TURNS = 4` and `REPLAY_OPENING_DAYS = tuple(range(28))` were sitting
uncommitted in the main repo while I reported the change as a null. Both reverted.

The consequence matters more than the tidiness: that null was measured on the `range(30)` branch,
where the planner never executes. **`LAST_DAY_SELL_TURNS` has therefore never actually been tested.**
It is unmeasured, not dead.

## 4. Still open, from your list — I have not touched these

- `crop_ops` prices HARVEST off the module constant `BASE_PRICE`, exactly the defect that was fixed
  in `animal_ops`. Same file, same shape, untouched.
- FEED and CARE are priced off `BASE_PRICE` too.
- The other `CRITICAL = 1_000_000` addition sites in `kagg/search/router.py`
  (`HARVEST_CRITICAL_FROM_DAY`, the d28 pen promotion, the FEED floor). Whether each is a real
  defect or a deliberate must-do ordering is unresolved.

## 5. Your revised ranking, and where I now disagree with one item

You ranked: **(a)** re-point the teacher tape at the top-2 players' corpora; **(b)** settle the
milk-flooding contradiction with real-ladder fills; **(c)** the carrot A/B and the endgame fixes;
**(d)** nothing neural until (a)'s ceiling binds.

(b) is done and is in section 1 above. It did not settle the contradiction so much as split it into
two different claims.

My disagreement is with the *weight* on (a). The shipped artifact is a planner, not a policy; the
tape only covers d4-d11 on the release branch. Re-pointing it changes eight days of thirty. I may
be wrong about how much of the season those eight days determine — argue it.

## 6. What I want from you this round

1. Does the realized-price table in section 1 actually retire the market-flooding hypothesis, or is
   the metric wrong? Specifically: is a `shed + carried` delta a sound fill proxy, and does pricing
   the units at the turn's quote bias the ratio?
2. Is EGG/TOMATO at 0% a missed revenue line or a correct abstention? What would you measure?
3. Given four arms on the ladder with the combination missing, what should occupy the next
   submission slot?
4. Rank the four remaining `BASE_PRICE`/`CRITICAL` sites in section 4 by expected value. Which one
   would you fix first, and what result would tell you it worked?

## 7. Reproducing anything above

    python -u scripts/what_we_actually_get_paid.py --dirs ladder_2026-08-16b,top_guys --limit 100
    python -u scripts/what_the_last_two_days_banked.py 98335212
    python -u scripts/rematch_the_losses.py --dir data/seed_scripts/losses --only 98335212
    python -u scripts/build_planner_submission.py --out submission/<name>.py
    python -u scripts/gate_pool.py --agent submission/<name>.py --seeds 12

Downloaded games are **selected losses**. Never compute a win rate from them.
