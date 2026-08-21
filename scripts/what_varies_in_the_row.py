"""Per day, per FIELD: how much does a target row actually vary across one player's seasons?

Alex, 2026-08-21: "the numbers of animals and plants is relevant - the split tho is the dynamic
allocation - but the movement we have in our offline solver(?) the watering and harvesting is
probably important even tho they are also in the scheduler - i mean what does vary??"

Counting DISTINCT WHOLE ROWS says d18 has 174 of them and stops there. It cannot say whether that is
174 genuinely different plans or one plan with a jittery `harvests` count, because a single field
differing by one makes the whole hash differ. Blanking the herd species proved the point in the
other direction: it removed 15 rows out of 6,840, so the species was never what was splitting them.

So: distinct values per field per day, and -- the number that decides what is learnable -- how many
distinct rows remain if that one field is DROPPED. A field whose removal collapses the count is
carrying the split. A field whose removal changes nothing is already agreeing.

    python -u scripts/what_varies_in_the_row.py --targets data/target_rows_kawa_norm.json
"""

import argparse
import collections
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

#: Every key a target row carries. `hands` mirrors `hires` by construction, so it is listed but will
#: always report identically to it -- that is a check on this script, not a finding.
FIELDS = ("hands", "hires", "land", "builds", "places", "feeds", "cares", "plants",
          "harvests", "fertilises", "clears", "animals_bought", "seeds", "buys", "sells")


def key(v):
    return json.dumps(v, sort_keys=True)


def row_hash(row, drop=()):
    d = {k: v for k, v in row.items() if k not in drop}
    return hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()[:10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--days", nargs="*", type=int,
                    default=[3, 6, 9, 12, 14, 16, 18, 22, 26, 29])
    args = ap.parse_args()

    rows = json.loads(pathlib.Path(args.targets).read_text())
    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r["target"])

    print("%d day-rows\n" % len(rows))

    # A. per field, distinct values and the share held by the most common one.
    print("DISTINCT VALUES PER FIELD  (top%% = share of seasons holding the modal value)")
    hdr = "%4s %7s" % ("day", "rows")
    for f in FIELDS:
        hdr += " %>10s" % f if False else " %10s" % f[:10]
    print(hdr)
    for day in args.days:
        rs = by_day.get(day) or []
        if not rs:
            continue
        line = "%4d %7d" % (day, len(rs))
        for f in FIELDS:
            c = collections.Counter(key(r.get(f)) for r in rs)
            line += " %5d/%3.0f%%" % (len(c), 100.0 * c.most_common(1)[0][1] / len(rs))
        print(line)

    # B. drop-one: what does the whole-row count fall to without this field?
    print("\nDROP-ONE  distinct whole rows with that ONE field removed")
    print("%4s %7s %7s   %s" % ("day", "rows", "all", "  ".join("%10s" % f[:10] for f in FIELDS)))
    for day in args.days:
        rs = by_day.get(day) or []
        if not rs:
            continue
        base = len({row_hash(r) for r in rs})
        line = "%4d %7d %7d  " % (day, len(rs), base)
        for f in FIELDS:
            line += " %10d" % len({row_hash(r, drop=(f,)) for r in rs})
        print(line)

    # C. the constructive version: keep ONLY the fields that look like the plan, drop the rest.
    #    If the count collapses, the late-day cliff is jitter in the dropped fields, not new plans.
    plan_only = ("hires", "land", "builds", "places", "plants", "animals_bought", "seeds")
    print("\nKEEPING ONLY %s" % ", ".join(plan_only))
    print("%4s %7s %7s %9s %7s" % ("day", "rows", "all", "plan-only", "top"))
    for day in args.days:
        rs = by_day.get(day) or []
        if not rs:
            continue
        drop = tuple(f for f in FIELDS if f not in plan_only)
        c = collections.Counter(row_hash(r, drop=drop) for r in rs)
        print("%4d %7d %7d %9d %6.1f%%"
              % (day, len(rs), len({row_hash(r) for r in rs}), len(c),
                 100.0 * c.most_common(1)[0][1] / len(rs)))


if __name__ == "__main__":
    main()
