"""Every directory under `data/`, its size, and whether any code names it. Reports, deletes nothing.

    python -u scripts/what_is_data_actually_used_for.py

`data/` is 91 GB and 74 GB of that is `data/seed_scripts/`. Before any of it is pruned, the question
is which directories the SHIPPED agent, the harnesses and the tests actually name -- not which ones
look old. A recording nobody references is 30 MB of observations; a recording the agent replays is
the product.

A reference count of 0 is a candidate, not a verdict: a directory can be reached through a variable
or a glob rather than a literal path, and this script cannot see that. It prints the grep so the
call site can be read.
"""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
CODE = ["kagg", "scripts", "tests", "submission", "docs"]


def du(path):
    try:
        out = subprocess.run(["du", "-sk", str(path)], capture_output=True, text=True, timeout=600)
        return int(out.stdout.split()[0]) * 1024
    except Exception:                                                          # noqa: BLE001
        return 0


def human(n):
    for unit in ("B", "K", "M", "G", "T"):
        if n < 1024:
            return "%.0f%s" % (n, unit)
        n /= 1024.0
    return "%.0fP" % n


def refs(needle):
    """Files under CODE naming `needle`. Returns (count, first few paths)."""
    dirs = [str(REPO / d) for d in CODE if (REPO / d).exists()]
    out = subprocess.run(["grep", "-rl", "--", needle, *dirs],
                         capture_output=True, text=True)
    hits = [h for h in out.stdout.splitlines() if h.strip()]
    return len(hits), hits[:3]


def main():
    root = REPO / "data"
    rows = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        size = du(d)
        n, where = refs("data/%s" % d.name)
        rows.append((size, d.name, n, where, d))

    print("EVERY DIRECTORY UNDER data/  --  nothing is deleted by this script\n")
    print("  %8s %6s  %s" % ("size", "refs", "directory"))
    for size, name, n, _w, _p in sorted(rows, reverse=True):
        print("  %8s %6d  data/%s" % (human(size), n, name))

    seed = root / "seed_scripts"
    if seed.is_dir():
        print("\n\nINSIDE data/seed_scripts/  (%s)  --  the big one\n" % human(du(seed)))
        print("  %8s %6s  %s" % ("size", "refs", "directory"))
        sub = []
        for d in sorted(p for p in seed.iterdir() if p.is_dir()):
            n, where = refs("seed_scripts/%s" % d.name)
            sub.append((du(d), d.name, n, where))
        for size, name, n, where in sorted(sub, reverse=True):
            print("  %8s %6d  %s%s"
                  % (human(size), n, name, "" if not where else
                     "   <- " + ", ".join(w.split("/")[-1] for w in where)))

        unref = [(s, n) for s, n, r, _w in sub if r == 0]
        print("\n  %d of %d subdirectories are named by NO file under %s"
              % (len(unref), len(sub), "/".join(CODE)))
        print("  they total %s of %s" % (human(sum(s for s, _n in unref)), human(du(seed))))

    print("\n\nWHAT THE SHIPPED AGENT NEEDS -- these are not prunable")
    for lit in ("data/seed_scripts/kawashigi/schedule.json",
                "data/seed_scripts/kawashigi/92498144.json",
                "data/seed_scripts/kawashigi/92466371.json",
                "data/seed_scripts/downloads_2026-08-13/91907974.json",
                "data/seed_scripts/downloads_2026-08-13/91906088.json"):
        p = REPO / lit
        print("  %-58s %8s  %s" % (lit, human(p.stat().st_size) if p.exists() else "-",
                                   "present" if p.exists() else "MISSING"))


if __name__ == "__main__":
    main()
