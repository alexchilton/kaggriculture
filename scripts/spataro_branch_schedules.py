"""SpaTaro's eight branch schedules: one base for d0-2, one plan per first shop for d3-29.

Measured on 179 seasons of submission 56114097 (`scripts/spataro_landed_schedule.py`):

    skeleton d0-2   CCSS 139 (78%), CCSSC 22, CSCS 10, CSSC 8  -- 157/179 are the same four animals
    first shop @d3  SMOOTHIE 29  YARN 26  ICE_CREAM 26  PET_CAFE 23  PIZZA 22  BAKERY 19
                    BRUNCH 18  FARMERS_MARKET 16
    d3-d5 inside    YARN -> SSS 23/26 (88%); PIZZA -> CCC 18/22; BAKERY -> CCS 15/19;
                    BRUNCH -> CC 14/18; PET_CAFE -> CCS 17/23; FARMERS -> CC 12/16

and his day-12 board differs by BRANCH, not by noise -- yarn runs 12 sheep where smoothie runs 2,
pet cafe is the only branch with carrot by d12 (14 of them), bakery runs 10 animals where smoothie
runs 16. One schedule has to be wrong on six of the eight.

Each branch plan is the best-bank season IN that branch whose d3-d5 placement sequence is the
branch's own dominant one, so a branch is represented by a season that plays the branch typically
AND plays it well. Rows come from `data/spataro_landed_rows.json` -- what his board actually did,
not what he ordered; he over-requests BUY_LAND in 162 of 179 seasons and funds exactly two parcels
in all 179.
"""
import argparse, collections, json, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
SEASON = 30


def _apply_fills(rows, ep, team, replay_dirs):
    """Replace the row's OFFERED market numbers with what the engine actually settled.

    **One step, not two.** `spataro_landed_schedule.py` reads his `BUY_PRODUCT`/`SELL` orders, and
    those are offers: d7 offers `WHEAT 48` on a world that fills 11, and our planner obeys the
    number, so the difference is spent out of the day's animal. Running this as a separate command
    afterwards is a step that gets forgotten -- by me, and it is not reasonable to ask Alex to
    remember it -- so the builder does it here and `scripts/schedule_guard.py` refuses anything that
    did not come through.

    `seeds` needs no engine run: it is the crop tally of `plants`, set in `spataro_landed_schedule`.
    """
    from scripts.tape_fills import animal_offers, tape_fills
    path = next((ROOT / d / f"{ep}.json" for d in replay_dirs
                 if (ROOT / d / f"{ep}.json").exists()), None)
    if path is None:
        raise FileNotFoundError(
            f"episode {ep} has no replay under {replay_dirs}; its market rows would stay as OFFERS")
    f = tape_fills(str(path), team)
    herd = animal_offers(str(path), team)
    out = {}
    for d, r in rows.items():
        r = dict(r)
        r["buys"] = dict(f[int(d)].get("BUY_PRODUCT", {}))
        r["sells"] = dict(f[int(d)].get("SELL", {}))
        r["animals_bought"] = dict(herd.get(str(d)) or {})
        out[d] = r
    return out, str(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--landed", default="data/spataro_landed_rows.json")
    ap.add_argument("--flows", default="data/spataro_plan_rows.json", help="carries the unlocks")
    ap.add_argument("--out", default="data/seed_scripts/spataro")
    ap.add_argument("--team", default="SpaTaro")
    #: **The default schedule is ONE season, and it must be the season the harness replays.**
    #: `scripts/breakdown.py`'s `TAPES["spataro"]` pairs a replay with this directory's schedule, and
    #: `breakdown` now refuses a pair whose episodes disagree, because a board from one season with
    #: rows from another describes ground that never existed. Picking this on BANK instead put YARN's
    #: `SSS` opening here -- 26 of 179 seasons -- against a replay of a `CCSSCC` board.
    ap.add_argument("--default-episode", type=int, default=107068412)
    ap.add_argument("--replay-dirs", nargs="+",
                    default=["data/replays_spa_sub", "data/replays_2026-09-07",
                             "data/replays_2026-09-08", "data/replays_2026-09-09"])
    args = ap.parse_args()

    L = json.loads((ROOT / args.landed).read_text())
    unlocks = {p["ep"]: p["unlocks"] for p in json.loads((ROOT / args.flows).read_text())}

    def skel(s, a, b):
        out = []
        for d in range(a, b):
            out += s["rows"][str(d)]["places"]
        return tuple(out)

    by_shop = defaultdict(list)
    for s in L:
        first = next((x[1] for x in (unlocks.get(s["ep"]) or []) if x[0] <= 3), None)
        if first:
            by_shop[first].append(s)

    # The base, d0-2: best bank among seasons on the dominant pre-shop skeleton. Identical across
    # branches by construction -- no shop is open before d3, so there is nothing to branch on.
    base_skel = Counter(skel(s, 0, 3) for s in L).most_common(1)[0][0]
    base_pool = sorted((s for s in L if skel(s, 0, 3) == base_skel), key=lambda s: -s["bank"])
    base = base_pool[0]
    print(f"base d0-2: skeleton {''.join(x[0] for x in base_skel)} "
          f"({len(base_pool)} seasons), best ep {base['ep']} ${base['bank']:,.0f}")

    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    branches, meta = {}, {}
    print(f"\n{'first shop':16} {'n':>4} {'dominant':>9} {'in it':>6} {'chosen ep':>11} {'bank':>10}")
    for shop, seasons in sorted(by_shop.items(), key=lambda kv: -len(kv[1])):
        dom = Counter(skel(s, 3, 6) for s in seasons).most_common(1)[0][0]
        pool = sorted((s for s in seasons if skel(s, 3, 6) == dom), key=lambda s: -s["bank"])
        pick = pool[0] if pool else sorted(seasons, key=lambda s: -s["bank"])[0]
        _filled, _src = _apply_fills(pick["rows"], pick["ep"], args.team, args.replay_dirs)
        branches[shop] = {str(d): _filled[str(d)] for d in range(3, SEASON)}
        meta[shop] = {"episode": pick["ep"], "bank": pick["bank"], "seed": pick["seed"],
                      "n_in_branch": len(seasons), "n_on_dominant": len(pool),
                      "dominant_d3_d5": "".join(x[0] for x in dom)}
        print(f"{shop:16} {len(seasons):>4} {''.join(x[0] for x in dom) or '-':>9} "
              f"{len(pool):>6} {pick['ep']:>11} {pick['bank']:>10,.0f}")

    # **The default is his MAJORITY OPENING, not his richest season.** The router falls back to this
    # when the first shop is none of the eight, and `REPLAY_OPENING_TAPE` replays its d0-d6, so it has
    # to be the season whose opening is the one most worlds actually see. Picking on bank put YARN's
    # `SSS` skeleton here -- 26 of 179 seasons -- and left the replay pointing at a different
    # episode's board than the rows describe, which is the one pairing this file must never break.
    #
    # His majority placement skeleton through d5 is `CCSSCC` (128 of 179); the best bank inside it is
    # ep 107068412. Derived here rather than hard-coded so a new batch of replays can move it.
    default_season = next((s for s in L if s["ep"] == args.default_episode), None)
    if default_season is None:
        raise SystemExit(f"--default-episode {args.default_episode} is not in {args.landed}")
    default_shop = next((sh for sh, m in meta.items()
                         if m["episode"] == default_season["ep"]),
                        max(meta, key=lambda k: meta[k]["bank"]))
    print(f"\ndefault season: ep {default_season['ep']} ${default_season['bank']:,.0f}")
    # **The default schedule is ONE season end to end, d0 through d29.** A base from one episode
    # spliced onto a branch from another describes a board that never existed: `REPLAY_OPENING_TAPE`
    # replays d0-d6 of a single recording, and the planner takes over at d7 with rows that have to be
    # the rows THAT board was built for. The default branch's own season supplies both halves.
    _dflt_ep = default_season["ep"]
    _dflt = default_season
    _dflt_rows, _ = _apply_fills(_dflt["rows"], _dflt_ep, args.team, args.replay_dirs)
    sched = {str(d): _dflt_rows[str(d)] for d in range(SEASON)}
    (out_dir / "schedule.json").write_text(json.dumps(sched, indent=1))
    (out_dir / "branches.json").write_text(json.dumps(branches, indent=1))
    (out_dir / "meta.json").write_text(json.dumps(
        {"submission": 56114097, "team": "SpaTaro", "seasons": len(L),
         "base_d0_2": {"episode": base["ep"], "bank": base["bank"],
                       "skeleton": "".join(x[0] for x in base_skel),
                       "n_on_skeleton": len(base_pool)},
         "default_branch": default_shop, "branches": meta,
         "source": "scripts/spataro_branch_schedules.py from data/spataro_landed_rows.json",
         # Read by `scripts/schedule_guard.py`. Written only where the fills were actually applied.
         "market": "FILLS",
         "schedule_from": {"episode": _dflt_ep, "bank": _dflt["bank"],
                           "why": "one season end to end -- the tape replays d0-d6 of THIS episode, "
                                  "so the planner must take over at d7 with its own rows"}},
        indent=1))
    print(f"\ndefault d3-29: {default_shop}")
    for f in ("schedule.json", "branches.json", "meta.json"):
        print(f"wrote {out_dir / f} ({(out_dir / f).stat().st_size:,} B)")


if __name__ == "__main__":
    main()
