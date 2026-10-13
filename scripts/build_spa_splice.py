"""SpaTaro's opening, then Hayashi's tapes. The join is the whole experiment.

Days 0-6 of SpaTaro are replayed verbatim, then each of the 13 Hayashi routes
continues from turn 168. All 13 share the same prefix, so the chassis's route
choice at step 144 is immaterial inside the prefix.

The known failure mode, recorded in docs (REPLAY_OPENING_DAYS, dead): a recording
spliced into machinery built for someone else overrides the rules it cannot see.
Here that is the point of the measurement -- Hayashi's turn-168 onward expects the
farm HIS opening built, and SpaTaro's 62 openings reach 37 distinct states.
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "submission" / "hay_router"
DST = ROOT / "submission" / "spa_splice"
PREFIX_EP = 107010601          # SpaTaro's best banked season in our dumps, $143,142
SPLIT = 168                    # end of day 6


def find_replay(ep):
    for d in ("data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09"):
        p = ROOT / d / f"{ep}.json"
        if p.exists():
            return p
    raise SystemExit(f"no replay for {ep}")


def main():
    r = json.loads(find_replay(PREFIX_EP).read_text())
    seat = r["info"]["TeamNames"].index("SpaTaro")
    prefix = [s[seat].get("action") for s in r["steps"][1:SPLIT+1]]
    assert len(prefix) == SPLIT, len(prefix)
    assert all(p is not None for p in prefix)

    tapes = json.loads((SRC / "actions.json").read_text())
    assert len(tapes) == 13 and all(len(t) == 719 for t in tapes)
    spliced = [prefix + t[SPLIT:] for t in tapes]
    assert all(len(t) == 719 for t in spliced), [len(t) for t in spliced]

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__", "*.tar.gz"))
    (DST / "actions.json").write_text(json.dumps(spliced, separators=(",", ":")))

    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": 11}, debug=False)
    env.run([str(DST/"main.py"), str(ROOT/"submission"/"shop0909"/"main.py")])
    bank = env.steps[-1][0]["reward"]
    assert bank > 3000, f"agent never acted: {bank}"
    print(f"wrote {DST}  prefix ep{PREFIX_EP} seat{seat} turns 0-{SPLIT-1}")
    print(f"  smoke seed 11 vs 0909: bank {bank:,.0f} "
          f"(hay_router scores 135,963 on this seed)")


if __name__ == "__main__":
    main()
