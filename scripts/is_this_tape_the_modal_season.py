"""Before blaming the executor for parting from the tape, ask whether the tape is the row we play.

`scripts/where_does_the_middle_start.py` compares a MODAL-row agent against ONE recorded season,
game 92498144. Those are two different things, and a divergence has two possible causes that the
grid cannot tell apart:

  1. our executor cannot make the row happen        -- a defect
  2. this season simply is not the modal season     -- not a defect, and not fixable by the executor

This prints, per day, whether 92498144's own row carries the label the schedule plays. Days where it
does NOT are days the grid can say nothing about our execution.

    python -u scripts/is_this_tape_the_modal_season.py
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import kawa_rows as K                                      # noqa: E402

TAPE_GAME = "92498144"


def main():
    rows = json.loads(pathlib.Path(K.LIBRARY).read_text())
    by_day = collections.defaultdict(list)
    tape = {}
    for r in rows:
        by_day[int(r["day"])].append(r["target"])
        if r["game"] == TAPE_GAME:
            tape[int(r["day"])] = r["target"]

    if not tape:
        raise SystemExit("game %s is not in %s" % (TAPE_GAME, K.LIBRARY))

    sched = K.build()
    mid = set(K.mid_season())

    print("tape game %s against the schedule the library agent plays\n" % TAPE_GAME)
    print("%4s %8s %10s %10s %8s %9s %9s"
          % ("day", "phase", "ours", "tape", "same?", "modal%", "his rank"))
    agree = total = 0
    for day in sorted(by_day):
        his = tape.get(day)
        if his is None:
            continue
        ours_label = K.label(sched[day], day)
        his_label = K.label(K.only_animals_get_placed(his), day)
        counts = collections.Counter(K.label(r, day) for r in by_day[day])
        order = [k for k, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
        rank = order.index(his_label) + 1
        same = ours_label == his_label
        phase = "greedy" if day in mid else "library"
        # In the middle the label is not what we play -- the row is wheat-filled -- so `same` there
        # describes the SCAFFOLDING (crew, market cadence, herd) only, never the planting.
        agree += same
        total += 1
        print("%4d %8s %10s %10s %8s %8.1f%% %6d/%d"
              % (day, phase, ours_label, his_label, "YES" if same else "no",
                 100.0 * counts[ours_label] / len(by_day[day]), rank, len(counts)))

    print("\nthe tape's own row is the one we play on %d of %d days" % (agree, total))
    early = [d for d in range(13) if d in tape
             and K.label(sched[d], d) == K.label(K.only_animals_get_placed(tape[d]), d)]
    print("d0-d12 (the strict phase): %d of 13 days agree -- %s" % (len(early), early))


if __name__ == "__main__":
    main()
