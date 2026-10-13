"""Does Hayashi's live agent still play the 13 tapes he published?

He re-records between releases: of the 4 tapes in Shop Router 0908, only one
survived unchanged into the 13 of Shop Router 0909 a day later; the other three
diverge at turn 70 and rewrite ~30% of the season. His live submission is newer
than both, so the public tapes may be a stale snapshot of a moving target.

For each of his live seasons this prints the closest published tape and how far
it differs. A live stream that matches no published tape means the tapes, not the
chassis, are what separates 2960 from the 2415 those tapes earned us.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAPES = json.loads((ROOT / "submission" / "shop0909" / "actions.json").read_text())


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return None


def main(folder):
    folder = Path(folder)
    rows = []
    for path in sorted((folder / "summaries").glob("*.summary.json")):
        rec = json.loads(path.read_text())
        for seat, team in enumerate(rec["teams"]):
            if not team.startswith("Yusuke"):
                continue
            live = [json.loads(a) for a in rec["actions"][seat]]
            best = None
            for j, tape in enumerate(TAPES):
                n = sum(1 for x, y in zip(live, tape) if x != y)
                if best is None or n < best[1]:
                    best = (j, n, first_diff(live, tape))
            rows.append((rec["episode"], rec["rewards"][seat], "|".join(rec["world"]), best))
    if not rows:
        print("no Hayashi seats in", folder)
        return
    print(f"{'episode':>10} {'bank':>10} {'world':28} {'closest tape':>12} {'differs':>9} {'first_div':>10}")
    for ep, bank, world, (j, n, d) in rows:
        print(f"{ep:>10} {bank:>10,.0f} {world[:28]:28} {j:>12} {n:>6}/719 {str(d):>10}")
    exact = sum(1 for r in rows if r[3][1] == 0)
    print(f"\n{len(rows)} live seasons, {exact} identical to a published tape.")
    print("If none are identical, the public 13 are a stale snapshot and the tape set is the gap.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/replays_2026-09-10")
