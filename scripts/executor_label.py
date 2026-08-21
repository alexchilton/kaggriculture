"""Label a day with ONLY what the executor reads, and only as coarsely as it acts.

Alex, 2026-08-21: "if it is 'just' the movement that is not an issue ... i mean what does vary??"

Movement was already out. What varies is the SELL QUOTA. Measured on 228 of Kawashigi's seasons,
day 29 has 212 distinct target rows and 211 distinct `sells` dicts -- every other field on that day
holds ONE value across all 228. Dropping `sells` takes d29 to 24 rows.

`grep -o 'row.get("[a-z_]*"' kagg/search/schedule_agent.py` -- the executor reads TEN keys:
seeds, hands, buys, sells, land, plants, shed_dusk, places, hires, animals_bought. It never reads
builds, feeds, cares, harvests, fertilises or clears; the router re-derives those from the board.
Hashing them splits rows for differences that cannot reach the game.

Two knobs, so the cost of each is separable:
  --drop-derived   keep only the ten fields the executor reads
  --sell-buckets   round each sell quota to a coarse bucket instead of an exact integer
"""
import argparse, collections, hashlib, json, math, pathlib, sys
REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from scripts.extract_target_rows import normalise_herd            # noqa: E402

READS = ("seeds", "hands", "buys", "sells", "land", "plants", "places", "hires", "animals_bought")
DERIVED = ("builds", "feeds", "cares", "harvests", "fertilises", "clears")

def bucket(n):
    """Coarse sell size. The market walks the price down, so 41 and 43 are the same decision."""
    n = int(n or 0)
    return 0 if n <= 0 else int(2 ** round(math.log2(n)))

def label(row, drop_derived, sell_buckets):
    r = normalise_herd(row)
    if drop_derived:
        r = {k: v for k, v in r.items() if k in READS}
    if sell_buckets and r.get("sells"):
        r = dict(r, sells={k: bucket(v) for k, v in r["sells"].items()})
    return hashlib.md5(json.dumps(r, sort_keys=True).encode()).hexdigest()[:10]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--days", nargs="*", type=int, default=[3,6,9,12,14,16,18,20,22,26,29])
    a = ap.parse_args()
    rows = json.loads(pathlib.Path(a.targets).read_text())
    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r["target"])

    modes = (("as-is", False, False), ("-derived", True, False),
             ("-sells", True, True))
    print("distinct rows per day, 228 seasons\n")
    print("%4s %7s %10s %10s %10s %9s" % ("day","rows","as-is","-derived","-derived","top"))
    print("%4s %7s %10s %10s %10s %9s" % ("","","", "", "+bkt sells",""))
    for day in a.days:
        rs = by_day.get(day) or []
        if not rs: continue
        out, top = [], 0.0
        for _nm, dd, sb in modes:
            c = collections.Counter(label(r, dd, sb) for r in rs)
            out.append(len(c)); top = 100.0*c.most_common(1)[0][1]/len(rs)
        print("%4d %7d %10d %10d %10d %8.1f%%" % (day, len(rs), out[0], out[1], out[2], top))

if __name__ == "__main__":
    main()

# --- appended 2026-08-21 -------------------------------------------------------------------
# Alex: "the sell is only problematic in the first d0-d12 to manage to get the land and items -
# after that we found sell at h16 is better - so you can discount that and buying cadence is pretty
# irrelevant also after the land buy".
#
# So `sells` and `buys` are plan fields only while the bank is the constraint. Once the land is
# bought the executor sells at h16 on a fixed cadence, which means both fields are EXECUTION, not
# intent, from d13 on -- and hashing them there splits rows for a decision the executor already
# makes on its own.
