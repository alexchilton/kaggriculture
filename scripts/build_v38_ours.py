"""v38's policy with OUR tapes: swap the embedded routes for the live-recovered ones.

v38 carries yhay81's PUBLISHED Shop Router 0909 schedules. Our 56158924 submission carries 13 tapes
recovered from 109 replays of that same author's LIVE ladder play, and the two sets share not one
turn: they diverge at turn 0 (`BUY WHEAT 13, SELL WHEAT 13...` against `BUY WHEAT 13, BUY WHEAT
30...`), and 110 of his 114 recorded live seasons open the way ours do. The published set is his old
play; ours is what he actually runs.

So the routes are the one part of v38 worth replacing, and everything else -- the feed rule, the
fertilizer protection, the worker planning -- is the part worth having.

The payload is `{"base": <719 turns>, "patches": {rid: [[turn, action], ...]}}`, b85 of zlib of
JSON, rebuilt here in exactly that shape so the loader below it is untouched.

    python -u scripts/build_v38_ours.py
"""
import base64, json, pathlib, re, zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "submission/v38/main.py"
OURS = ROOT / "submission/hay_router2/actions.json"
OUT = ROOT / "submission/v38_ours/main.py"


def main():
    src = SRC.read_text()
    tapes = json.loads(OURS.read_text())
    assert len(tapes) == 13 and all(len(t) == 719 for t in tapes), "expected 13 x 719"

    base = tapes[0]
    patches = {}
    for rid, tape in enumerate(tapes):
        if rid == 0:
            continue
        patches[str(rid)] = [[i, a] for i, (a, b) in enumerate(zip(tape, base)) if a != b]

    payload = {"base": base, "patches": patches}
    raw = json.dumps(payload, separators=(",", ":")).encode()
    blob = base64.b85encode(zlib.compress(raw, 9)).decode()

    lines = src.splitlines()
    idx = next(i for i, l in enumerate(lines) if l.startswith("_PAYLOAD="))
    lines[idx] = f"_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('{blob}')))"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")

    # round-trip: the loader's own reconstruction must give back exactly our tapes
    d = json.loads(zlib.decompress(base64.b85decode(blob)))
    routes = {0: d["base"]}
    for rid, patch in d["patches"].items():
        t = list(d["base"])
        for i, a in patch:
            t[i] = a
        routes[int(rid)] = t
    back = [routes[i] for i in sorted(routes)]
    assert back == tapes, "round-trip mismatch -- the swapped payload does not rebuild our tapes"

    print(f"wrote {OUT}  {OUT.stat().st_size:,} bytes")
    print(f"payload {len(blob):,} chars   patches: "
          f"{ {k: len(v) for k, v in patches.items()} }")
    print("round-trip verified: 13 tapes rebuild exactly")


if __name__ == "__main__":
    main()
