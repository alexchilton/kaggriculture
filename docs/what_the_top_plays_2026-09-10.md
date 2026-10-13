# What the current number one actually plays — 2026-09-10

Source: the stored run log of `destbreso/x-ray-your-agent`, a public notebook that resolves the live rank-1 submission at run time, pulls its ladder replays and classifies the action stream.
Raw log saved at `data/logs/xray_number_one_2026-09-10.log`.
This is **someone else's measurement**, not ours. It is quoted because it reads 199 real ladder episodes, which we cannot currently fetch — the competition episode API rate-limited us after about 400 calls and now returns 404 for ids that answered minutes earlier.

## The verdict

Submission **56097405**, rank 1, rating 3,018.8, **199 ladder episodes**, ledger **W151-L47-T1**, margin median +$5,053, worst -$14,468, best +$131,198.

- **GLOBAL class: ADAPTIVE.** 86.6% of turns vary between episodes. First divergence at **t=96, which is day 4 hour 0**.
- Texture across 199 replays: **navy 78.9%** (the plan itself — farmer or hands — differs from its own modal action), amber 3.9% (market channel only), green 17.2% (plays its modal action).
- **Within-world verdict: ADAPTIVE in all 50 worlds** that had two or more episodes. A world is one shop pair, so this is the line that matters: an agent that merely routes among fixed tapes is *identical* inside a world. This one is not. Divergence inside a fixed shop draw still starts at t=96.
- 62 distinct shop pairs seen. 83 genetic groups among 199 opponents, only **1 mirror game** — almost nobody is running its lineage.

## What this means for the imported tapes

Shop Router 0909 is open-loop with **two** branch points, at step 144 and step 648, and 12 of its 13 tapes share the whole first 144 steps.
The current number one is already diverging at step 96 and keeps diverging inside a fixed shop draw.
So the tape family is structurally behind the top of the ladder, and the imports should be read as a floor to stand on, not as the ceiling.

**This does not say the top is RL.** A replay cannot separate a learned policy from online search or a deep heuristic planner — all three produce a state-dependent stream. Nothing measured here distinguishes them, and no public kernel from any of the current top eight exists to settle it.

## Our own measurement, 2026-09-10

The x-ray above is someone else's run. This section is ours, from 12 replays of 2026-09-09 pulled with `scripts/fetch_leader_episodes.sh` into `data/replays_2026-09-09/` (379 MB) and classified by `scripts/classify_ladder_agents.py`.
Full output: `data/logs/classify_0909.log`.

A replay carries the team name and the 719 actions each seat submitted, so two episodes of the same team can be diffed turn by turn.
The shop draw is the world. A router cannot vary inside one world, so the same-world comparison is what separates routing from reactivity.

| team | LB rank | episodes | first divergence between episodes | turns differing |
|---|---|---|---|---|
| SpaTaro | 1 | 7 | **turn 0 or 1** | 707-719 of 719 |
| Otter Vibe | 2 | 8 | **turn 96** (day 4 hour 0) | 572-620 of 719 |
| Matthew Huang | - | 3 | turn 7 | 87-202 of 719 |
| Mengfei Li | 11 | 2 | turn 195 | 442 of 719 |

**SpaTaro does not share an opening with itself.** Two of its games differ on 719 of 719 turns. There is no tape here at all.

**Otter Vibe plays a fixed four-day opening and then adapts.** The one same-world pair in this sample -- episodes 106960018 and 106962874, both `PET_CAFE|YARN_STORE` -- still diverges at turn 96 and differs on 595 turns. Same shop draw, different play, so it is not routing.

Matthew Huang looks like the third archetype: a fixed plan with repairs, 87 to 202 turns of deviation.
Mengfei Li's two episodes are in different worlds and diverge at 195, which is consistent with routing but cannot be told apart from adaptivity on two games.

Sample is 12 episodes from one day, one same-world pair for the only team where it was possible.
And **adaptive is not RL** -- online search and a deep heuristic planner produce the same signature.

## One number that supports the market arm

The x-ray prints the rank-1 agent's own price damage: *craters we sold into* WHEAT -$252, FERTILIZER -$197, -$147, -$116, WHEAT -$112, MELON -$72.
Even the leader is selling into holes it dug.
See `docs/improving_from_the_tars.md`, arm B.
