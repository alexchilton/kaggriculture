# SUPER IMPORTANT — READ THIS BEFORE TOUCHING THE AGENT

Written 2026-08-20. Everything here is measured, and every line of it cost time to learn.

---

## 1. The docstrings LIE. Read the branch, never the prose.

**Five docstrings contradicted their own code in a single session.** Every one of them sent a fix in
the wrong direction, and three of those fixes were built and measured before the lie was found.

| The prose said | The code does |
|---|---|
| `will_be_fed`: a long essay on skipping non-producing animals | an unconditional `return True` sits in front of that logic — it is UNREACHABLE |
| `WHEAT_TILES_TO_TOMATO`: "Unconditional" | the use site gated it on `melon_armed and not q4_armed` |
| `SHOP_ADAPT_CROPS` is the only draw→crop path | `STRAWBERRY_TILES_BY_DRAIN` runs OUTSIDE it |
| `_herd_through_day` re-labels every head, so a goose cannot survive | it iterates COW and SHEEP only and leaves geese alone |
| `_wheat_row_first` looked uncalled | it IS called, at the `_fit_slots` return |

**Rule: before acting on any docstring claim, grep the name the branch actually reads.** A comment is
a hypothesis. `CLAUDE.md` already says "print the name the code actually reads before any A/B" — the
docstring is not the name.

---

## 2. Measure at the DECISION, never at the season census

The single largest error of the week, made in three separate forms.

Scoring the herd rule against the **end-of-season board** hands it a day-29 shop list nobody had on
day 4. Scoring it at each placement — with the day, and the shops unlocked *at that turn* — took the
same unchanged rule from **11.5% to 55.8%**. Then scoring order-free within a day (the split returns
COUNTS; walk order comes from the schedule row) took it to **77.9%**.

**Only +9.8 points of that came from changing the agent. The other ~55 was fixing the instrument.**

Related trap, same family: **pseudo-replication.** An "opponent decides the late herd" finding
measured over 213 PLACEMENTS evaporated at the GAME level (50 games, every gap −0.05 to −0.32). A
game contributing twelve animals is one decision repeated, not twelve observations.

**Rule: name the unit before trusting an aggregate, and make sure the rule only sees what the player
saw.**

---

## 3. Gradient or mixture? Ask BEFORE fitting.

The milk-shop variable was measured **negative twice** and was right all along:

    LINE fitted on the final board          65.6% -> 46.4%
    LINE on expected final shops            65.6% -> 63.0%
    THRESHOLD at d9                         81.9% -> 88.5%

His late-yarn boards cluster at **COW 6 and COW 12**. The per-milk-count means of 6.0 … 12.0 are
averages OVER that split, not a trend within it — the fitted 8.6 is a value he essentially never
plays. **A linear fit to a bimodal response lands between both modes and matches neither, and the
mean is the worst single guess.**

A mixture wants a classifier. A gradient wants a line. Decide which you have first.

---

## 4. A unit test passing does NOT mean the season improved

Fixed the d0 ration defect. Unit test green, all three guard tests green, targeted day improved
(`feed 1/5 → 3/5`). **Season got worse and it was reverted:**

    PLANT d0-d10   67/68 -> 49/68        d9 hands  11/11 -> 7/11
    FEED  d0-d10   73/85 -> 68/85        d10 PLANT 18/19 -> 0/19
    PASS  d0-d10     911 -> 959

Feeding two extra animals on d0 ate wheat the later days needed. **Days match IN ORDER — a change
that fixes d0 and breaks d9 is a regression, however good the unit test looks.**

**Rule: every fix is judged on the full d0–d10 grid against his own recorded ops, not on its test.**

---

## 5. The golden-output grid is the only refactor lock that exists

This is the thing that makes a restructure survivable. On tetsuya's board `94345389`, seat 0,
seed `959074148`, the agent must produce:

    PLANT 212/212   BUILD 15/15
    WHEAT 164/164   STRAWBERRY 32/32   MELON 8/8   CARROT 8/8
    herd COW 6  SHEEP 5  GOOSE 3

`scratchpad/tets_grid3.py` prints it; `vs_tets.py` prints ours-vs-his ops per day. It has already
caught one silent regression (`MELON 8/8 → 0/8` from a branch overwriting the plan).

**Refactor loop: change shape → grid byte-identical → commit.** Without this pin, a 9k-line
restructure is unverifiable, which is why previous ones never stuck.

Caveat, and it matters: **the grid currently pins ONE board and ONE seed.** Before trusting it to
police a big restructure, loop it over three or four of his seeds.

---

## 6. The tape and the seed go in step

Running a schedule on a foreign seed gives the wrong shop draws, which drives the herd and crop
logic off a draw the plan never saw. tetsuya's game is `data/seed_scripts/downloads_2026-08-19/
94345389.json`, **seed 959074148, seat 0**.

Never quote a q3-arm number against a q4-arm number as a strategy comparison — different boards.

---

## 7. One schedule is not a rule. We hold 78 of his games.

The whole tetsuya pivot began by extracting a schedule from ONE replay. Against his 78 recorded
games that replay is an **outlier on nearly every axis** — melon at the season minimum, carrot
present where 69 of 78 games have none.

    herd total       15-18   mean 15.2   sd 0.5   cv 0.03   <- the INVARIANT: pin it
    COW               4-12   cv 0.37                        <- the RESPONSE: adapt it
    SHEEP             3-11   cv 0.43
    GOOSE              0-5   cv 1.16
    straw + melon    32-65   cv 0.12                        <- invariant
    CARROT            0-65   cv 4.07   present in  9/78     <- pure draw response
    TOMATO            0-22   cv 4.64   present in  4/78

**Pin the total, adapt the split.** Fit the invariant plus the response — and only a corpus can tell
those apart.

---

## 8. Things that are DEAD and must not be resurrected

- **The kawashigi tape replay** (`REPLAY_OPENING_DAYS`). Every tape in `REPLAY_OPENING_TAPE` is a
  カワシギ game. It covered d4–d11 — **620 of 1187 placements, 52%** — silently overriding the herd
  rule. There is no tetsuya tape to swap in: his opening is a PLAN, not a recording.
- **`_Q4.arm` and `_MB.arm`.** `Branch.install` does `target.clear(); target.update(row)` — it wipes
  every row from its split day and substitutes kawa's plan. Measured deleting his melon outright:
  `MELON 8 → 0`.
- **The milk LINE** (both variants). See §3.
- **The `ORDER_SLOTS` gate change.** Null: d0 feed 1/5 byte-for-byte, PASS 911 → 959.
- **The arrival-ration fix.** See §4.

Kawashigi's own tests are `xfail(strict=True)`, NOT deleted — they record his shape, and strict
means they fail loudly if the rule is ever pointed back at him. **Do not "fix" them.**

---

## 9. Code health — the honest state

9k lines across three files, **145 module constants, 29 booleans**. Known violations:

- **DRY:** `DRAWN = ("FEED", "FERTILIZE", "PLACE", "BUILD")` defined identically TWICE —
  `cover.py:69` and `router.py:215`.
- **SRP:** `schedule_agent.py` is 5,762 lines doing market orders, herd logic, crop logic, replay,
  routing glue and slot arbitration.
- **Open/closed:** every behaviour change has been made by ADDING a flag rather than extending a
  type. That is how 145 constants happened — each is a fossilised A/B nobody deleted.

**No new flags.** A measured win deletes the old code. A measured null gets reverted, with the number
in the commit message.

---

## 10. Where the agent actually stands

Herd rule matches tetsuya on **88.5%** of his 1187 recorded placements (function-level).
Live season follows his plan exactly on crops and builds.

Still open:

- **PASS 911 vs his 679 over d0–d10** — we idle 232 turns more with the same crew. Biggest number
  on the board.
- **FEED 73/76, CARE 76/85.** **Corrected 2026-08-20 — the old figure here was `FEED 73/85`, and
  the 85 was never achievable.** Nine of his 85 d0–d10 FEED ops never landed: `FEED` takes a WHEAT
  from the acting unit's CARRIED inventory (`reference/kaggriculture.py:505`, `inv =
  _farmer_inventory` at `:321`) and returns silently when it has none. On d0 he submits five and
  lands **zero** — he buys 5 wheat at h1, sells all 5 back at h2, and no unit ever carries any.
  CARE has no input cost, so its 76/85 is real and is now the LARGER gap of the two.
  Full measurement: `docs/feed_is_measured_against_ops_he_wasted_2026-08-20.md`.

  Two consequences. The FEED shortfall is three ops, not twelve, so it is no longer the biggest
  thing on the board. And d0 is not a day to copy: matching him there means wasting five turns.

- **The schedule row is internally inconsistent, and this is the live bug.** Every field
  `extract_leader_schedule.py` writes is a raw op count from the action stream — `feeds`, `cares`,
  `places`, `plants`, `builds`, `hires` — except `buys`/`sells`, which are wash-netted afterwards
  (`:201-243`). tetsuya's d0 row therefore reads `feeds=5` **and** `buys={}`: five rations demanded,
  no wheat bought. **No executor can satisfy that row.**

  The netting is arithmetically correct (his d0 buy-5-sell-5 is a genuine wash) and every other op
  lands 100/100 on this board — `PLANT 90/90, HIRE 146/146, BUILD 15/15, PLACE 15/15`. FEED is the
  only op with a consumable input he does not manage, so it is the only field the mismatch bites.

  **The fix Alex specified:** size the dawn wheat order from the day's ration demand minus wheat on
  hand — `row["feeds"] - on_hand - ordered` — rather than from `buys` (netted to zero) or from
  `alive` (which is 0 at hour 0, before any pen exists). The demand is already in the row: his
  `feeds` equals the standing herd on every day measured. Keep `BUY_DRIP`; the comment at
  `schedule_agent.py:5291` records that a single large block walks `market_price` up the curve and
  fills LESS, and the tape places sixteen separate buys of 1–6 across h1–h22.

  Not yet implemented. Write the test red first, and judge it on the d0–d10 grid, not the test —
  §4 above is exactly this fix's two predecessors.
- **d13 at 55.2%** is the weakest herd day.
- **CARROT has no predictor.** Non-monotone in drain count — pinned in a test so nobody fits a line
  to it. See §3.
- **Route tables are STALE.** They were solved for the d4–d11 tape opening that no longer happens.
  Any money number from this branch is meaningless until `resolve_days.py` is re-run.
