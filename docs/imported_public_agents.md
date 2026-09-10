# Imported public agents — 2026-09-10

Two public Kaggle notebooks were imported whole, not adapted.
Both are Apache-2.0 and both are credited in the submission description and in the bundle's own `LICENSE.txt` / `NOTICE.txt`.
Nothing in either bundle is our code.

## What they are

**Yusuke Hayashi, `yhay81/shop-router-0909`** (2026-09-09, 120 votes).
13 complete 719-turn action tapes in `actions.json`, plus a router of about 260 lines.
It picks a plan at step 144 from the first two unlocked shops, switches to plan 2 at step 648, inserts `DIG` when a weed blocks planting or building, pulls some planned sales forward one turn, and liquidates on the final turn.
Sale timing and shed projection are credited by the author to `aurax7/kaggriculture-reactive-router`.
Bundle: `submission/shop0909/`.

**Dmitrii Gluzdov, `dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800`** (2026-09-09, 61 votes).
The same tapes and the same parent router, carried verbatim as `router_parent.py`, plus a terminal planner that runs from action 712: it looks for short collect-and-return routes that still get the goods sold before the season ends.
A route is accepted only if its own-farm model preserves every worker's cumulative deliveries and loses no sold units; otherwise the parent continues.
Bundle: `submission/e182/`.

## Verification

`scripts/build_imported_submission.py` rebuilds each archive in the authors' format — USTAR, stored DEFLATE blocks, zeroed mtime — and fails the build unless every member hash matches the value published in the source notebook.

    .venv-sub/bin/python -u scripts/build_imported_submission.py e182
    .venv-sub/bin/python -u scripts/build_imported_submission.py shop0909

E182 reproduces the author's published archive **byte for byte**:
`sha256 f0a5ef344d4a195e1a3ec9c66f8856709c75cb611461b7bb71a3143b3faed3cb`, 5,192,098 bytes, all 9 members matching.
The 0909 bundle matches on all 3 members; its author published member hashes but no archive hash.

`actions.json` is the same file in both bundles, `sha256 17d503f2fd20d59f9c0f14024d1e74a8add8bb9b5561d4d908b45deecb5495ef`, and 0909's `main.py` is hash-identical to E182's `router_parent.py`.
So the E182 claim that the parent is unmodified is checked, not taken on trust.

Both archives were extracted to a clean directory and run by path on engine 1.32.7: status `DONE` on both seats, $179,870 (E182) and $179,668 (0909) against `starter` on seed 4242.
That is a format-and-import check only — `starter` sells almost nothing, so the number is roughly 2x reality and must never be used to select anything.

## Why they were imported

Our own planner bundle, built from this commit, loses to the unmodified 0909 router **16 times out of 16** over 8 seeds with seats swapped, by $28,607 to $38,827.
On the live ladder our best standing score is 1924.0 against this author's rank-9 rating of 2958.2.

## The caveat that matters

These tapes are public, so the strong agents can be tuned against them.
`pilkwang/kaggriculture-structured-economic-policy` abandoned its own fixed-schedule family for exactly this reason and now ships a fork of `kaitofukami/238-238-known-streams-v58-minimax-closed-loop`.
Expect the imported tapes to rate below their author's live agent.
How far below is not measured.
