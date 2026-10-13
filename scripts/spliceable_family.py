"""Five tapes that can actually be spliced: pick on the SHARED BOARD, not on the bank.

Splicing five best-banking tapes at d3 banked $9,865 against starter -- under the build's own kill
threshold -- and `spa_splice` failed the same way in an earlier session. The reason is not jitter
that was left in. It is that a tape's d3 actions are HARVEST and PLANT against particular tiles, so
they only work on the crop layout they were recorded against, and the five picks had five different
d3 boards:

    milk_berry  MELO11 WHEA4        wheat  MELO12 WHEA7        berry  MELO11 WHEA6
    wool        CARR2 MELO9 WHEA7   carrot CARR2 MELO9 WHEA3

The herd IS identical across all of them (COW 2, SHEEP 2, 25 tiles) -- what varies is what he
planted on day 0, before any shop is open, which is a real decision and not noise.

So do not edit the jitter out. SELECT for it. Over 179 seasons there are 99 distinct d3 boards and
eight of them carry four or more clusters; one carries all five. A family sharing a d3 board can be
spliced there by construction, because the board the incoming tape expects is the board it gets.
"""
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.spa_targets import SHOP_CLUSTER, CLUSTERS

SEASON = 30


def board_sig(b):
    """What an incoming tape's d3 actions actually depend on: the crops, the herd, the tiles."""
    return (tuple(sorted(b["crops"].items())), tuple(sorted(b["animals"].items())), b["owned"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", type=int, default=3, help="the splice day")
    ap.add_argument("--out-dir", default="data/seed_scripts/spa_family")
    args = ap.parse_args()

    state = json.loads((ROOT / "data/spataro_state.json").read_text())
    landed = {s["ep"]: s for s in json.loads((ROOT / "data/spataro_landed_rows.json").read_text())}
    unlocks = {p["ep"]: p["unlocks"]
               for p in json.loads((ROOT / "data/spataro_plan_rows.json").read_text())}

    # **Only episodes whose REPLAY is on disk.** The state file covers 179 seasons; the replay
    # directory holds 162. A pick without its tape builds a bundle whose replay silently does
    # nothing -- the builder refuses it, which is how this was caught, but the picker should never
    # have offered it.
    have = {int(f.stem) for f in (ROOT / "data/replays_spa_sub").glob("*.json")
            if f.stem.isdigit()}
    fam = defaultdict(list)
    for s in state:
        if s["ep"] not in have:
            continue
        if str(args.day) not in s["state"]:
            continue
        first = next((sh for d, sh in sorted(unlocks.get(s["ep"]) or []) if d <= args.day), None)
        c = SHOP_CLUSTER.get(first)
        if c:
            fam[board_sig(s["state"][str(args.day)])].append((c, s["ep"], s["bank"]))

    # Most clusters covered, then most seasons. **Bank is not a criterion anywhere in this file.**
    # It answers "which season was richest", and the question here is "which season FITS" -- the
    # splice needs a board that matches and a continuation that is typical of its world. A rich
    # season that is atypical teaches the wrong continuation, and a season on the wrong board does
    # not splice at all.
    ranked = sorted(fam.items(),
                    key=lambda kv: (-len({c for c, _, _ in kv[1]}), -len(kv[1])))
    sig, members = ranked[0]
    covered = {c for c, _, _ in members}
    print(f"{len(state)} seasons -> {len(fam)} distinct d{args.day} boards")
    print(f"best family: {len(members)} seasons, {len(covered)} clusters, "
          f"board {' '.join(f'{a}{b}' for a, b in sig[0])} "
          f"{' '.join(f'{a}{b}' for a, b in sig[1])} tiles {sig[2]}\n")

    # **Within the family, the pick is the season whose LATER board is most typical of its
    # cluster** -- the median of that cluster's 179-season distribution on the axes the agent is
    # scored on, at d9 and d12. Typicality, not strength: the tape teaches a continuation, and the
    # continuation we want is the one that world usually gets.
    AXES = ("COW", "SHEEP", "WHEAT", "STRAWBERRY", "CARROT", "MELON")
    by_ep = {s["ep"]: s for s in state}
    cluster_of = {}
    for s in state:
        first = next((sh for d, sh in sorted(unlocks.get(s["ep"]) or []) if d <= args.day), None)
        c = SHOP_CLUSTER.get(first)
        if c:
            cluster_of.setdefault(c, []).append(s)

    def value(b, q):
        if q in ("COW", "SHEEP"):
            return b["animals"].get(q, 0)
        if q == "planted":
            return b["planted"]
        return b["crops"].get(q, 0)

    def median(vals):
        vals = sorted(vals)
        return vals[len(vals) // 2] if vals else 0

    target = {}
    for c, seasons in cluster_of.items():
        for day in ("9", "12"):
            for q in AXES + ("planted",):
                target[(c, day, q)] = median([value(s["state"][day], q)
                                              for s in seasons if day in s["state"]])

    def distance(ep, c):
        st = by_ep[ep]["state"]
        d = 0.0
        for day in ("9", "12"):
            if day not in st:
                return float("inf")
            for q in AXES + ("planted",):
                d += abs(value(st[day], q) - target[(c, day, q)])
        return d

    picks = {}
    for cluster in CLUSTERS:
        here = [m for m in members if m[0] == cluster]
        if here:
            picks[cluster] = min(here, key=lambda m: distance(m[1], cluster))
    # A cluster absent from the family falls back to the family member closest to THAT cluster's
    # median. A tape that fits the board is worth more than a tape that fits the world and misfires
    # on every action.
    fallback = None
    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {}
    print(f"{'cluster':12} {'episode':>11} {'bank':>10}  source")
    for cluster in CLUSTERS:
        if cluster in picks:
            c, ep, bank = picks[cluster]
            src = f"own cluster, board distance {distance(ep, cluster):.0f}"
        else:
            c, ep, bank = min(members, key=lambda m: distance(m[1], cluster))
            src = f"fallback from {c}, board distance {distance(ep, cluster):.0f}"
        rows = {str(d): {k: v for k, v in landed[ep]["rows"][str(d)].items() if k != "escapes"}
                for d in range(SEASON)}
        (out_dir / f"{cluster}.json").write_text(json.dumps(rows, indent=1))
        meta[cluster] = {"episode": ep, "bank": bank, "source": src,
                         "replay": f"data/replays_spa_sub/{ep}.json"}
        print(f"{cluster:12} {ep:>11} {bank:>10,.0f}  {src}")

    (out_dir / "meta.json").write_text(json.dumps(
        {"source": "scripts/spliceable_family.py", "splice_day": args.day,
         "shared_board": {"crops": dict(sig[0]), "animals": dict(sig[1]), "owned": sig[2]},
         "family_size": len(members), "clusters_covered": sorted(covered),
         "clusters": meta}, indent=2))
    print(f"\nwrote {out_dir}/*.json")
    print("\nREPLAY_OPENING_TAPE entries:")
    for cluster, m in meta.items():
        print(f'    "{cluster}": ("{m["replay"]}", "SpaTaro"),')


if __name__ == "__main__":
    main()
