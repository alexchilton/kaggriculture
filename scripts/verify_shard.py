"""Does a shard row actually survive `adapter.state_from_obs` -> `jax_obs.encode`?

The first round of labels stored a hand-picked summary and silently dropped `private["inventories"]`,
`market` and the opponent's farm. Nothing failed -- it would have trained a net on zeroed carry
state, and "am I holding wheat" is the entire precondition for FEED. So this does not check that
fields are PRESENT; it runs the real bridge and asserts the encoded tensors are not degenerate.

    python -u verify_shard.py /home/alex/labels_r0b/shard_000.jsonl
"""
import json
import sys

import numpy as np

from kagg.rl import adapter, jax_obs

path = sys.argv[1]
rows = []
with open(path) as fh:
    for i, line in enumerate(fh):
        if i > 200:
            break
        rows.append(json.loads(line))
print("rows read: %d" % len(rows))

need = ("step", "farms", "market", "private")
missing = [k for k in need if k not in (rows[0].get("obs") or {})]
print("missing top-level fields: %s" % (missing or "none"))
if missing:
    raise SystemExit("SHARD IS INCOMPLETE -- stop and fix the generator")

ob0 = rows[0]["obs"]
print("farms present   : %d (need 2)" % len(ob0["farms"] or []))
print("market keys     : %s" % sorted((ob0.get("market") or {}).keys())[:6])
print("private keys    : %s" % sorted((ob0.get("private") or {}).keys()))
print("inventories len : %s" % len((ob0.get("private") or {}).get("inventories") or []))

carried_seen = inv_seen = 0
encoded = 0
tile_nz = unit_nz = glob_nz = 0
for r in rows:
    ob = r["obs"]
    seat = int(r["seat"])
    privates = [None, None]
    privates[seat] = ob.get("private")
    privates[1 - seat] = adapter.agent_private_stub()
    try:
        state = adapter.state_from_obs(ob, privates)
    except Exception as exc:                                        # noqa: BLE001
        print("state_from_obs FAILED on step %s: %s: %s"
              % (ob.get("step"), type(exc).__name__, exc))
        raise SystemExit(1)
    if int(np.asarray(state.farm.carried).sum()) > 0:
        carried_seen += 1
    if int(np.asarray(state.inventory).sum()) > 0:
        inv_seen += 1
    tiles, units, glob = jax_obs.encode(state)
    encoded += 1
    tile_nz += int(np.count_nonzero(np.asarray(tiles)) > 0)
    unit_nz += int(np.count_nonzero(np.asarray(units)) > 0)
    glob_nz += int(np.count_nonzero(np.asarray(glob)) > 0)
    if not np.all(np.isfinite(np.asarray(glob))):
        raise SystemExit("NON-FINITE global features at step %s" % ob.get("step"))

print("\nencoded OK           : %d/%d" % (encoded, len(rows)))
print("rows with carry > 0  : %d   <-- MUST be > 0, this is what the last shard lost"
      % carried_seen)
print("rows with market inv : %d   <-- MUST be > 0" % inv_seen)
print("tiles/units/glob nonzero on: %d / %d / %d rows" % (tile_nz, unit_nz, glob_nz))
print("feature widths       : tile=%d unit=%d glob=%d"
      % (jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES, jax_obs.GLOBAL_FEATURES))
print("\nVERDICT: %s" % ("USABLE" if carried_seen and inv_seen and encoded == len(rows)
                         else "BROKEN -- do not train on this"))
