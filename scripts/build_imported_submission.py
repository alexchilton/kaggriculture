"""Package an imported public agent into submission.tar.gz and check it byte-for-byte.

Both bundles are Apache-2.0 third-party work, imported 2026-09-10:
  shop0909  Yusuke Hayashi, kaggle.com/code/yhay81/shop-router-0909
  e182      Dmitrii Gluzdov, kaggle.com/code/dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800
            (the same 13 route tapes plus a terminal seven-turn collection planner)

The archive format is the authors': USTAR, stored DEFLATE blocks, zeroed mtime,
so the bytes are reproducible. Every member hash and the archive hash are
compared against the values published in the source notebook. A mismatch means
the import is not what the author ran, and the build fails.
"""
import argparse
import binascii
import hashlib
import io
import json
import re
import struct
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BUNDLES = {
    "shop0909": {
        "files": ["LICENSE.txt", "actions.json", "main.py"],
        "member_sha256": {
            "LICENSE.txt": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
            "actions.json": "17d503f2fd20d59f9c0f14024d1e74a8add8bb9b5561d4d908b45deecb5495ef",
            "main.py": "d6d74997dc5b483db63d8e39cafa1afeec0f366824e75107e109123f111e866b",
        },
        "archive_sha256": None,
    },
    "e182": {
        "files": ["LICENSE.txt", "NOTICE.txt", "actions.json", "main.py", "policy.py",
                  "router_parent.py", "settings.json", "terminal_planner.py", "unit_model.py"],
        "member_sha256": {
            "LICENSE.txt": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
            "NOTICE.txt": "6435ca240eea352abffd2cbf19b446b311e372f552a07865cab1b8bb547b1230",
            "actions.json": "17d503f2fd20d59f9c0f14024d1e74a8add8bb9b5561d4d908b45deecb5495ef",
            "main.py": "495bfa4825c9e58638e804aeeb62a9537826f6d4d869222815e1bbeefd84d3dc",
            "policy.py": "e239501d1224ba3d198aef11bc6b1b40637fbac335db7ca07205175d992f9b12",
            "router_parent.py": "d6d74997dc5b483db63d8e39cafa1afeec0f366824e75107e109123f111e866b",
            "settings.json": "e2756d366c88e627da6711f20ae708613d6a7cf5805410c6af4326dfc7a7417e",
            "terminal_planner.py": "a9d7a6d29e1fb313852dc0121d43f16544771ed12775afaf3a0480e9ab713dce",
            "unit_model.py": "c03e8c5cd10466c229ee0a44dece9a3943c10bff135d96a7822ffe75d6922724",
        },
        "archive_sha256": "f0a5ef344d4a195e1a3ec9c66f8856709c75cb611461b7bb71a3143b3faed3cb",
    },
}


def safe_root_name(name):
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,99}", name) or ".." in name:
        raise ValueError(f"Not a portable archive-root filename: {name!r}")
    return name


def archive_bytes(files):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        for name in sorted(files):
            entry = tarfile.TarInfo(safe_root_name(name))
            entry.size = len(files[name])
            entry.mtime = entry.uid = entry.gid = 0
            entry.uname = entry.gname = ""
            entry.mode = 0o644
            archive.addfile(entry, io.BytesIO(files[name]))
    raw = buffer.getvalue()
    result = bytearray(b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\xff")
    for offset in range(0, len(raw), 65535):
        chunk = raw[offset:offset + 65535]
        result.append(1 if offset + len(chunk) == len(raw) else 0)
        result.extend(struct.pack("<HH", len(chunk), len(chunk) ^ 0xffff))
        result.extend(chunk)
    result.extend(struct.pack("<II", binascii.crc32(raw) & 0xffffffff, len(raw) & 0xffffffff))
    return bytes(result)


def build(name):
    spec = BUNDLES[name]
    folder = ROOT / "submission" / name
    files = {}
    for member in spec["files"]:
        path = folder / member
        if not path.is_file():
            raise SystemExit(f"missing {path}")
        files[member] = path.read_bytes()

    got = {m: hashlib.sha256(b).hexdigest() for m, b in files.items()}
    bad = {m: (got[m], spec["member_sha256"][m]) for m in got if got[m] != spec["member_sha256"][m]}
    if bad:
        raise SystemExit(f"member hash mismatch, import is not what the author ran: {bad}")

    raw = archive_bytes(files)
    digest = hashlib.sha256(raw).hexdigest()
    if spec["archive_sha256"] and digest != spec["archive_sha256"]:
        raise SystemExit(f"archive hash {digest} != published {spec['archive_sha256']}")

    out = folder / "submission.tar.gz"
    out.write_bytes(raw)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as check:
        if check.getnames() != sorted(files):
            raise SystemExit("archive members differ from the declared files")
        for member, payload in files.items():
            if check.extractfile(member).read() != payload:
                raise SystemExit(f"archive readback failed: {member}")

    receipt = {"bundle": name, "archive": str(out), "archive_bytes": len(raw),
               "archive_sha256": digest,
               "archive_sha256_matches_published": bool(spec["archive_sha256"]) and digest == spec["archive_sha256"],
               "member_sha256": got}
    (folder / "build-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle", choices=sorted(BUNDLES))
    build(ap.parse_args().bundle)
