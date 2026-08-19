"""The cow/sheep/goose mix, checked against tetsuya's own recorded shop draws.

The counterpart of `test_the_herd_split_answers_the_recorded_shop_draw.py`, which does this for
カワシギ. Same corpus shape, same `_herd_split` entry point, different player -- and he answers the
draw with a different function, so a rule fitted to one is not a rule for the other.

**Why this file exists.** On 2026-08-19 a schedule was extracted from ONE tetsuya replay (94345389)
and followed for a night. Against his 78 recorded games that single game is an outlier on nearly
every axis -- melon at the season minimum, carrot present where 69 of 78 games have none. A schedule
copies one draw's answer; only the corpus can separate the quantity he holds CONSTANT from the one
he moves with the draw. Measured over the 78:

    herd total          15-18   mean 15.2   sd 0.5    cv 0.03     <- the invariant
    COW                  4-12   mean  7.6   sd 2.8    cv 0.37     <- the response
    SHEEP                3-11   mean  6.4   sd 2.7    cv 0.43
    GOOSE                 0-5   mean  1.2   sd 1.4    cv 1.16

So the herd TOTAL is his constant and the SPLIT is his response. Any rule that pins the split is
pinning the only part that was ever supposed to move.

`data/logs/tets_invariants_2026-08-19.log` and `data/logs/tets_herd_vs_draw_2026-08-19.log`.
"""
import collections
import json
import pathlib

import pytest

from kagg.search import schedule_agent as SA

#: Full recordings only -- the extracted `{team, actions}` form carries no observations and so no
#: shop draw. Every folder is swept and names are de-duplicated, because the same game id appears
#: under more than one download folder.
CORPUS = "data/seed_scripts"
PLAYER = "tetsuya"
#: Below this a seat never committed to an animal strategy and its split is noise, not a choice.
#: Same threshold as the カワシギ file so the two populations are comparable.
MIN_HERD = 6


def _seats():
    """Every tetsuya seat, scored at HIS DECISIONS rather than at the final board.

    **The decision is the PLACE, and the draw is the draw as it stood at that moment.** Reading the
    end-of-season census and asking the rule about it hands the rule the day-29 shop list, which he
    did not have when he chose the species. He builds a pasture or a coop and puts an animal in it
    on a specific turn, with a specific set of shops unlocked, and that is the only state a rule
    could have used. Scoring anywhere else measures a decision nobody made.

    Returns per game: (name, first-yarn draw index at the END, placements, final herd) where
    `placements` is the ordered list of `(day, shops_then, species)` for every animal he placed.
    """
    out, seen = [], set()
    for path in sorted(pathlib.Path(CORPUS).rglob("*.json")):
        if path.name in seen:
            continue
        try:
            rec = json.loads(path.read_text())
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        steps = rec.get("steps")
        if not steps or len(steps) < 700:
            continue
        obs = steps[-1][0].get("observation")
        if not isinstance(obs, dict):
            continue
        teams = (rec.get("info") or {}).get("TeamNames") or ["?", "?"]
        seat = next((i for i, n in enumerate(teams) if PLAYER in str(n).lower()), None)
        if seat is None:
            continue
        seen.add(path.name)
        shops = (obs.get("town") or {}).get("unlocked_shops") or []
        first = next((i + 1 for i, s in enumerate(shops) if s == "YARN_STORE"), None)
        # The animals he actually put in a pen, in the order he put them there. `town` is public, so
        # seat 0's observation carries the draw for both players.
        placements = []
        for frame in steps[1:]:
            ob = (frame[0] or {}).get("observation") or {}
            act = (frame[seat] or {}).get("action") or {}
            then = list((ob.get("town") or {}).get("unlocked_shops") or [])
            day = int(ob.get("day", 0) or 0)
            for unit in [act.get("farmer")] + list(act.get("hands") or []):
                if unit and unit[0] == "PLACE" and len(unit) > 1 and unit[1] in ("COW", "SHEEP",
                                                                                "GOOSE"):
                    placements.append((day, then, unit[1]))
        herd = collections.Counter()
        for row in obs["farms"][seat]["tiles"]:
            for tile in row:
                if isinstance(tile, dict) and tile.get("animal"):
                    herd[tile["animal"]] += 1
        if len(placements) < MIN_HERD:
            continue
        out.append((path.name, first, placements, herd))
    return out


@pytest.fixture(scope="module")
def seats():
    rows = _seats()
    if len(rows) < 60:
        pytest.skip("recorded corpus not on disk (data/ is gitignored)")
    return rows


def _split(shops, total, day=9, geese=0):
    """The rule's own answer for a herd of `total`, decided on the draw `shops` as it stood.

    `geese` is handed over rather than inferred, for the same reason the total is: nothing measured
    yet says which boards get a goose, so it is part of the question, not part of the answer.
    """
    return SA._herd_split({"COW": total, "SHEEP": 0, "GOOSE": geese}, {}, day, 0, list(shops))


def _his_mix(placements):
    """What he actually put in pens this game, as a Counter over species."""
    return collections.Counter(sp for _d, _sh, sp in placements)


def test_his_herd_total_is_the_invariant(seats):
    """The premise for everything else: he fixes the SIZE and floats the mix.

    If this stops holding, the split is no longer the interesting quantity and the rest of this
    file is measuring the wrong thing.

    Counted as PLACEMENTS, not as the final census: an animal that was placed is a decision he
    made, and one that later left the board does not un-make it.
    """
    totals = [len(p) for _n, _f, p, _h in seats]
    mean = sum(totals) / len(totals)
    assert 14.0 <= mean <= 17.0, "his mean placed herd is %.2f" % mean
    assert max(totals) - min(totals) <= 6, (
        "his placed herd ranges %d, which is not an invariant" % (max(totals) - min(totals)))


def test_he_is_a_gradient_on_the_first_yarn_draw_not_a_step(seats):
    """**He is not カワシギ, and this is the difference that breaks the transplanted rule.**

    カワシギ is a step function: COW 6 on an early yarn store, COW 10 otherwise, and
    `WOOL_SHOP_SETS_THE_HERD` encodes exactly that. Tetsuya walks up with the draw instead --
    unanimous COW 4 on draw #1, COW 5 on draw #2, COW 6-8 on draw #3. A two-valued rule cannot
    express a monotone response, so no setting of `WOOL_SHOP_COW_CAP` / `WOOL_SHOP_NO_YARN_COW`
    can fit him.
    """
    by = collections.defaultdict(list)
    for _n, first, placements, _h in seats:
        by[first].append(_his_mix(placements)["COW"])
    for draw in (1, 2):
        assert len(by[draw]) >= 5, "too few draw-#%d seats to assert on" % draw
    early = sum(by[1]) / len(by[1])
    second = sum(by[2]) / len(by[2])
    late = [c for f, v in by.items() if f is None or f >= 6 for c in v]
    assert early < second < sum(late) / len(late), (
        "his cow count is not monotone in the draw: #1=%.2f #2=%.2f late=%.2f"
        % (early, second, sum(late) / len(late)))
    # A step function would put draw #1 and draw #2 on the same value. They are not.
    assert round(early) != round(second), (
        "draw #1 and #2 both round to COW %d, so he may be a step after all" % round(early))


def test_the_rule_picks_the_animal_he_picked_on_the_day_he_picked_it(seats):
    """**Scored at the decision, not at the census.** Every animal he put in a pen is one question.

    At his `i`-th placement the rule is handed exactly what he had: the day, the shops unlocked at
    that turn, and the `i` animals already standing. It must name the species he then placed. That
    is the only comparison where the rule and the player see the same board -- asking about the
    final herd gives the rule a day-29 shop list nobody had on day 4.

    His herd total is the invariant (~15), so it is given rather than inferred; the split is the
    thing under test.

    RED as written on 2026-08-19: `_herd_split` carries カワシギ's two-valued step function and he
    is a gradient, so it cannot follow him even with perfect information. The bar is 80% and not
    100% because his draws #4-#8 are bimodal at COW 6 and COW 12 -- a second covariate is needed
    there, and no function of the yarn draw alone reaches them.
    """
    hit = miss = 0
    examples = []
    for name, _first, placements, _h in seats:
        mix = _his_mix(placements)
        geese = mix["GOOSE"]
        total = len(placements) - geese
        standing = collections.Counter()
        # **Scored per DAY, order-free inside it, because the split decides a MIX and not a walk.**
        # `_herd_split` returns counts. Which pen a hand reaches first comes from the schedule row
        # through `_outstanding_places`, so charging the split for his sheep-first opening scores it
        # for something it does not control -- and "fixing" that inside the split would be fitting
        # the scoring proxy rather than the player.
        by_day = collections.OrderedDict()
        for day, shops, species in placements:
            by_day.setdefault((day, tuple(shops)), []).append(species)
        for (day, shops), species_today in by_day.items():
            want = _split(list(shops), total, day, geese)
            owed = {a: want.get(a, 0) - standing.get(a, 0) for a in ("COW", "SHEEP", "GOOSE")}
            # The rule's own multiset for as many animals as he placed that day, taken greedily off
            # the outstanding counts.
            ours = collections.Counter()
            for _ in species_today:
                pick = max(owed, key=lambda a: owed[a])
                ours[pick] += 1
                owed[pick] -= 1
            his = collections.Counter(species_today)
            agree = sum((ours & his).values())
            hit += agree
            miss += len(species_today) - agree
            if agree != len(species_today) and len(examples) < 6:
                examples.append((name, day, dict(his), dict(ours)))
            standing.update(his)
    rate = hit / max(hit + miss, 1)
    assert rate >= 0.80, (
        "the rule names his species on %d of %d placements = %.1f%%; first disagreements "
        "(game, day, his mix that day, ours): %s" % (hit, hit + miss, 100 * rate, examples))


def test_the_split_can_express_a_goose(seats):
    """**A structural hole, not a tuning gap.** `_herd_split` returns COW and SHEEP only.

    He finishes with at least one goose in 43 of 78 games -- 91 birds summed across the CORPUS, so
    a mean of 1.2 a game and never more than 4 in any one of them. These are birds standing on the
    final board, tiles whose `animal` is GOOSE, not eggs; eggs are a product and never appear in
    that field.

    **The hole is in the split, not downstream of it.** `_herd_through_day` iterates COW and SHEEP
    only and leaves other species to the caller, so a goose the schedule rowed does survive that
    function -- an earlier note in this repo claiming otherwise was wrong. What is missing is a
    GOOSE bucket in `_herd_split` itself: without one the caller's greedy can never name the bird,
    and every goose he places scores as a miss against a rule structurally unable to pick it.

    RED by construction until the split carries a third species.
    """
    with_geese = [r for r in seats if _his_mix(r[2])["GOOSE"]]
    assert len(with_geese) >= 20, "the goose population has changed; re-measure before asserting"
    keys = set(_split(with_geese[0][2][0][1], 15, geese=2))
    assert "GOOSE" in keys, (
        "`_herd_split` returns %s, so it cannot express the goose he runs in %d of %d games"
        % (sorted(keys), len(with_geese), len(seats)))
