# Mr Stealth on the carrot mechanism — 2026-08-24

Received verbatim. Saved before relaying, per the standing rule.
Claims are HIS measurements, not verified here except where noted below.

## Q1 — It's the market play, and it's deliberate. Provenance proves it.

His 32 tiles were not new ground: at d20 every one of them was a standing crop — 16 strawberry + 16 wheat.
As those one-shots ripened d21–25 he harvested and replanted the spent tile with carrot instead of rotating onward:
1 tile d22 → 2 → 10 → 22 → 32 by d26, then collected down to 0 by d28 dusk, holding ~76 units, dumped d29 at $498.

The decomposition kills the coincidence theory: 76 units × $498 ≈ his entire $37.8k day; the same 76 units as wheat ≈ $2.9k.
Same tiles, same crew, same turns — the crop choice and the withholding are worth ~$35k.
And it wasn't even efficient (2.4 units/tile of 4 possible): the play has enormous slack.
He left money on the table and still beat us by $29k.

One flag your model should absorb: 16 of his converted tiles were strawberry.
Strawberry's second flush lands on d29 — converting those tiles plausibly killed his own strawberry d29 yield, and the play still paid.
The corner doesn't need to be clean; it needs to be big.

## Q2 — The missing half is "redirect the replant flow from d21", plus our own abstention

- We stall at ~14 tiles because `CARROT_SWAP_DAYS=(25,26,27)` starts too late and rewrites only already-scheduled wheat plants, which taper late-season.
  His ramp started d22.
  Your own measurement agrees: widening to d21–27 was worth $17,788 with the gate agreeing in both arms.
- Our schedule sells carrot on d21/22/24/25 — we refill the very book we'd be starving.
  Abstention must gate SELLs during accumulation, not just plant rewrites.
  That's separable, cheap, and explains most of D=975-him vs D=~850-us (we sold 11 carrots into it).
- Don't chase exactly 32 tiles.
  Volume = window-days × your planner's daily replant throughput.
  His 76 banked at 2.4/tile says precision doesn't matter; depth-of-book does.

## Q3 — Re-read daily, never latch

Latch-once-at-window-open is dead by your own table (at d21 opponent commitment is invisible → rules agree).
Re-evaluate every dawn of d21–27 on current observables:
projected-D-at-d29 minus our remaining planned supply minus 4 × their standing carrot tiles, fire/continue iff residual u > 1.3.
Their commitment becomes visible d24 (10 tiles) — a daily read reacts to it;
a hysteresis rule ("once firing, only stop when residual < 1.1") prevents whipsaw.
Already-sown tiles keep growing regardless; stopping mid-window just stops adding.

## Q4 — Elo: the mirror is positive-sum here, but size the opportunity honestly

I scanned all 1,852 downloaded games' d25 observations: carrot-drain ≥ 5 towns = 23.7% of the field;
no game anywhere had a carrot book deeper than D≈900.
So this fires roughly one game in four, the hinge quadratic makes double-cornering split the walk-down rather than self-destruct
(his own 76-unit dump moved the close only $523→$498), and Fable's `(hold, not)` dominance argument holds against a mostly-non-withholding field.
The CLAUDE.md mirror warning applies weakly here — this mirror prints money *from the town*.
The real Elo risk is misfiring on drain-2/3 towns (76% of games), which the deficit projection handles.

## Q5 — The single measurement

The one that could kill the line: per-game realized dump price on fired games across the full corpus — Fable's own wrongness condition, but run wide.
If, on real replays where the deficit projection fires, the average d29 realization is under ~3× base ($105) —
because the recorded opponents collectively refill these books more than the six-loss sample suggests —
the edge is ~$70/unit × ~50 units on a quarter of games, marginal after regressions, and effort belongs to cadence instead.
If it comes back ≥$300/unit (as the one observed instance did), ship it behind the daily re-read gate.

My bet, for what it's worth: the line survives, and the ordered program is —
abstention gate first (smallest diff, unblocks D), then daily-re-read gate, then window widening, then EGG as the second book.

---

## Notes added on receipt (not Stealth's)

**Unreconciled number.** Stealth: drain ≥ 5 towns are **23.7%** of 1,852 games.
Fable: deep carrot towns are **4.2%** of games.
These are probably different predicates (drain threshold vs projected book depth), not a contradiction,
but neither of us has stated the predicate precisely enough to check.
Do not average them. The gate that ships must be measured on its own firing rate.

**Yield disagreement.** Stealth sizes opponent supply at `4 × standing carrot tiles`.
Fable says the unfertilised ceiling is **3** (`_new_plant` starts at 1, WATER adds +1 at ages 2–3, +2 only if fertilised).
Both directions here are conservative — over-stating their supply makes us fire less —
but `corner_the_book.YIELD_PER_TILE["CARROT"]` should be the true number, and Fable's derivation is from the env source.
