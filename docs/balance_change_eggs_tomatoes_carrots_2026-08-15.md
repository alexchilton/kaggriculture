# Balance change — eggs, tomatoes, carrots (2026-08-15)

Posted by the competition organisers.
Verbatim, because the percentages are the whole content and a paraphrase would lose them.

> Small balance change
>
> I'm adding a small change to eggs, tomatoes and carrots, such that their price will increase
> significantly if there is a large shop demand and no production.
>
> Since the shop demand is randomized, each of these products will start to see the levels of prices
> increases (assuming NO production):
>
> tomatoes => 50% of games
> carrot => 26% of games
> eggs => 22% of games
>
> The intent of these changes it to roughly preserve the existing market dynamcs, but make these
> products viable in some situations, not universally. This should lead to more interesting end game
> decisions.
>
> Details here: https://github.com/Kaggle/kaggle-environments/pull/1399
>
> This should be the last change, excepting game breaking bugs.
>
> This should roll out shortly. You should update to >=1.32.7 a new change

## What it changes for us

**Required version is now `kaggle-environments >= 1.32.7`.**
`CLAUDE.md` still says `>= 1.32.2`; that is the version that first contained the env at all, and it
is no longer the version the ladder runs.

**Every baseline in this repo predates this.**
The 29-day kawashigi grid, the mirror gate's win rate, the build's `ours == repo` dollar identity and
the schedule rows themselves were all measured against the old price curve.
None of them are wrong, but none of them describe the game being played after the rollout.

## Why this lands on exactly our sorest spot

The three products buffed are **the three this agent could not sell at all** until 2026-08-13.

- `SELLABLE` listed 6 of 9 products and omitted `CARROT`, `TOMATO` and `EGG`
  (`project_kaggriculture_sellable_blocked_three_products`).
  Four carrot arms were measured and rejected while carrot revenue was structurally zero.
- **The goose verdict is downstream of that same bug.**
  Geese were switched off in `c9c1c18` ("Geese lose to the mirror and to the field") and deleted in
  `7a88d30`, on evidence gathered while `EGG` could never reach the market.
  `project_kaggriculture_animals_verdict` already records that "animals don't pay" has been an
  artifact four separate times; this would be the fifth, and now the payoff side is being raised too.

So the correct reading is not "a small buff to three crops we ignore".
It is: a mechanic we wrongly measured as dead is being made **more** live, in 22–50% of games.

## What this does NOT say

- It is **not** universal. Tomato fires in half of games, carrot in a quarter, eggs in a fifth, and
  only when shop demand is high **and nobody is producing**. A fixed schedule that always plants
  tomato is not what this rewards; a conditional one is.
- "No production" is doing a lot of work in that sentence. If both farms plant tomato the premium
  presumably does not appear — which makes this the same **contention** question as the
  melon/strawberry split, where カワシギ reads the opponent's board at d5 and yields the crop the
  other side is flooding (`MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`, REGISTER C-23a).
  That rule is the shape this wants, pointed at a different crop.

## Open, in order

1. Upgrade the local env to `>= 1.32.7` and re-measure the grid before trusting any prior number.
2. Read PR #1399 for the actual price formula — the percentages are outcomes, not the mechanism, and
   the mechanism is what a plan can be built against.
3. Re-open the goose/EGG question, stating plainly that the prior verdict was taken under a bug.
4. Ask whether the endgame should carry a conditional tomato/carrot block at all, given the schedule
   is read off a tape recorded under the old curve.
