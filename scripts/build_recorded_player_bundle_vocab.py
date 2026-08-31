"""Build the market bundle vocabulary from a RECORDED player's own action streams.

    python -u scripts/build_recorded_player_bundle_vocab.py --team カワシギ \
        --out data/il/bundle_vocab_kawa.json

**Why a third builder.** There are two already and neither samples the right thing for a clone
trained on `scripts/bc_replay.py --team X`:

    build_bundle_vocab.py          640 LEADERBOARD games   -- the ladder's behaviour, not one player
    build_teacher_bundle_vocab.py  4 tape TEACHERS in-sim  -- our agent replaying kawa, 4 towns

Measured 2026-08-28 over 40 カワシギ seats, 14,143 traded turns (`data/logs/bc_vocab_miss.log`):

    data/il/bundle_vocab.json                     197 entries   2,045 missed   14.5%
    data/il/bundle_vocab_teacher_pre_topup.json   149 entries     425 missed    3.0%

`Vocabulary.index` returns 0 for a basket it does not hold, and 0 means "place no orders" -- so a
missed turn is taught to the student as DO NOTHING and bundle agreement then scores it as a HIT.
The 14.5% hid 5,641 HIRE and 4,894 SELL orders, and `kagg/il/bc.py:235` calls `encode_action`
without a vocab so it took the 197 by default.

**No environment stepping.** A recorded player's baskets are in the action stream; running a sim to
recover them would sample our agent's behaviour instead of his, which is the exact mistake the other
two builders each make in their own direction.
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="カワシギ")
    ap.add_argument("--out", default="data/il/bundle_vocab_kawa.json")
    ap.add_argument("--games", type=int, default=0, help="0 = every seat this team has")
    ap.add_argument("--max-size", type=int, default=None,
                    help="defaults to jax_policy.N_BUNDLES -- the head cannot express more")
    ap.add_argument("--min-coverage", type=float, default=1.0,
                    help="fraction of TRADED TURNS the kept bundles must cover, or the build "
                         "refuses. 1.0 means every basket must fit. Lowering it is an explicit, "
                         "recorded decision to teach the tail as DO NOTHING -- カワシギ's 453 "
                         "baskets against a 256-wide head cover 99.6%%, so --min-coverage 0.99 "
                         "trades 0.4%% of turns for leaving the architecture alone.")
    args = ap.parse_args()

    from kagg.il import bc, market_bundles as MB
    from kagg.rl import jax_policy as P

    max_size = args.max_size or P.N_BUNDLES
    refs = bc.rank_seats(bc.find_replays("data"), team=args.team)
    if args.games:
        refs = refs[: args.games]
    if not refs:
        raise SystemExit(f"no seats for {args.team!r}")
    print(f"{len(refs)} {args.team} seats, banks ${refs[-1].bank:,.0f}-${refs[0].bank:,.0f}",
          flush=True)

    seen = collections.Counter()
    traded = 0
    for i, r in enumerate(refs):
        doc = json.loads(pathlib.Path(r.path).read_text())
        for step in doc["steps"][1:]:
            orders = [o for o in (((step[r.seat] or {}).get("action") or {}).get("market") or []) if o]
            if not orders:
                continue
            traded += 1
            seen[tuple(MB.bundle_of(orders))] += 1
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(refs)} seats, {len(seen):,} distinct baskets", flush=True)

    ordered = [b for b, _n in seen.most_common() if b != MB.EMPTY]
    # **Index 0 is reserved for the empty bundle and is not a basket.** `Vocabulary.index` returns 0
    # for anything it does not hold, so a basket sitting there is taught on every silent turn and
    # played back on every silent turn. The first write of this file put カワシギ's commonest basket
    # (`SELL FERTILIZER`) at 0 and the row build came back with 16,600 misses of 287,600 rows --
    # 5.77% against the 0.38% predicted here. `load_vocab` now refuses such a file.
    n_baskets = max_size - 1
    print(f"\ntraded turns              {traded:,}")
    print(f"distinct bundles          {len(ordered):,}")
    print(f"head width                {max_size}  (1 reserved for the empty bundle)")

    # **A truncation here is a defect, not a trade-off.** Anything dropped becomes index 0, which
    # means "place no orders", and the student is then taught to do nothing on those turns while
    # agreement scores it correct. Refuse rather than report a percentage.
    dropped_turns = 0
    if len(ordered) > n_baskets:
        kept = [b for b, _n in seen.most_common() if b != MB.EMPTY][:n_baskets]
        kept_turns = sum(seen[b] for b in kept)
        coverage = kept_turns / traded
        if coverage < args.min_coverage:
            raise SystemExit(
                f"{len(ordered)} distinct bundles against a {max_size}-wide head. Keeping the top "
                f"{n_baskets} covers {coverage:.1%} of traded turns, below the required "
                f"{args.min_coverage:.1%}, and the rest would be silently taught as DO NOTHING. "
                f"Widen jax_policy.N_BUNDLES or coarsen bundle_of; do not truncate.")
        dropped_turns = traded - kept_turns
        print(f"\nTRUNCATING to the top {n_baskets} of {len(ordered)} baskets, by explicit "
              f"--min-coverage {args.min_coverage:.3f}")
        print(f"  covers {coverage:.2%} of traded turns; {dropped_turns:,} turns "
              f"({dropped_turns / traded:.2%}) will be labelled DO NOTHING")
        print(f"  the previous default vocabulary missed 14.5% of the same player's turns")
        ordered = kept

    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    entries = [MB.EMPTY] + ordered
    out.write_text(json.dumps([[list(p) for p in b] for b in entries]))
    print(f"\nwrote {len(entries)} entries to {out} (entry 0 is the empty bundle)")

    # Read the file back through the loader every consumer uses, and count the misses against the
    # SAME counter the build was sized from. A number produced from `ordered` in memory is a
    # different quantity from the one the row build reports, which is how the 0.38%/5.77% gap hid.
    vocab = MB.load_vocab(str(out), max_size=max_size)
    missing = sum(n for b, n in seen.items() if int(vocab.index(b)) == 0 and b != MB.EMPTY)
    print(f"coverage check via load_vocab: {vocab.size} entries, "
          f"{missing:,} of {traded:,} traded turns unexpressible ({missing / max(1, traded):.2%})")


main()
