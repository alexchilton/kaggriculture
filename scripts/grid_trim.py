"""Trim a `grid_csv.py` grid to the columns that carry information, and foot it with totals.

Dropped because the board never contains one: TOMATO, CHICKEN, PIG. Dropped because they are tour
shape rather than work, and `matching-the-tape` exempts them from the match: DROP, PICKUP, PASS.
Dropped because it is a residue bucket with no fixed meaning: OTHER.

**Two footer rows, because a column is either a level or a flow and they do not total the same way.**
`money`, `tiles`, `pens`, `weeds`, the crop counts and the herd are the board at the END of a day --
summing thirty daily snapshots of a bank balance is a number with no referent. Those get `FINAL_d29`.
The op columns are that day's actions and do sum, so those get `SUM`. Each footer leaves the other
kind blank rather than printing a figure that would be read as comparable.

    python -u scripts/grid_trim.py data/logs/grid_new_victor.csv
"""
import argparse
import csv
import pathlib

#: Matched against the column label with the `_ours`/`_tape`/`_diff` suffix already stripped.
DROP = ("tomato", "chicken", "pig",
        "drop(offer)", "pickup(offer)", "pass(offer)", "other(offer)")

#: The board at the end of the day. Everything else in the grid is a count of that day's actions.
LEVELS = ("money", "hands", "tiles", "pens", "weeds",
          "wheat", "strawberry", "melon", "carrot", "cow", "sheep", "goose")


def _stem(col):
    for suffix in ("_ours", "_tape", "_diff"):
        if col.endswith(suffix):
            return col[: -len(suffix)]
    return col


def trim(path, out=None):
    rows = [r for r in csv.reader(open(path)) if r]
    header, body = rows[0], rows[1:]

    keep = [i for i, c in enumerate(header) if _stem(c) not in DROP]
    header = [header[i] for i in keep]
    body = [[r[i] for i in keep] for r in body]

    level = [i for i, c in enumerate(header) if _stem(c) in LEVELS]
    flow = [i for i, c in enumerate(header) if i and _stem(c) not in LEVELS]

    total = [""] * len(header)
    total[0] = "SUM"
    for i in flow:
        total[i] = sum(int(r[i]) for r in body)

    final = [""] * len(header)
    final[0] = "FINAL_d29"
    for i in level:
        final[i] = body[-1][i]

    out = pathlib.Path(out or path)
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(body)
        w.writerow(total)
        w.writerow(final)
    return out, len(rows[0]) - len(header), len(header)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--out", default=None, help="only valid with a single input")
    args = ap.parse_args()
    for p in args.csv:
        out, dropped, kept = trim(p, args.out if len(args.csv) == 1 else None)
        print("%s  dropped %d columns, kept %d, + SUM and FINAL_d29 rows" % (out, dropped, kept))


if __name__ == "__main__":
    main()
