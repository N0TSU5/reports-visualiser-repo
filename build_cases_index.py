"""Build cases.js -- the browsable index of every case bundle in cases/.

data.js only carries the handful of files each finding points at. This indexes
the whole bundle (docs, config, portfolio data, tests, answer key, run evidence)
so the dashboard can open any file the agent was actually given.

Contents are content-addressed. The baseline docs/config/data/tests are byte
identical across most bundles, so storing each distinct blob once and having the
bundles reference it keeps the file a fraction of the size of the tree.

    python3 build_cases_index.py
"""

import hashlib
import json
import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CASES = HERE / "cases"
OUT = HERE / "cases.js"

SKIP_NAMES = {".DS_Store"}
SKIP_DIRS = {"__pycache__"}
# Anything above this is truncated in the viewer; the full file stays on disk.
MAX_BYTES = 400_000


def main():
    blobs = {}
    bundles = {}

    for bundle in sorted(p for p in CASES.iterdir() if p.is_dir()):
        entries = []
        for path in sorted(bundle.rglob("*")):
            if not path.is_file() or path.name in SKIP_NAMES:
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            raw = path.read_bytes()
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            truncated = False
            if len(text) > MAX_BYTES:
                text = text[:MAX_BYTES] + "\n\n... [truncated for the viewer] ..."
                truncated = True
            digest = hashlib.sha1(text.encode()).hexdigest()[:16]
            blobs.setdefault(digest, text)
            entries.append({
                "path": str(path.relative_to(bundle)),
                "hash": digest,
                "lines": text.count("\n") + 1,
                "bytes": len(raw),
                "truncated": truncated,
            })
        bundles[bundle.name] = entries

    payload = {"blobs": blobs, "bundles": bundles}
    OUT.write_text("const caseIndex = " + json.dumps(payload) + ";")

    files = sum(len(v) for v in bundles.values())
    raw = sum(len(blobs[e["hash"]]) for v in bundles.values() for e in v)
    print(f"{len(bundles)} bundles, {files} files")
    print(f"unique blobs: {len(blobs)}  (dedup saved {(1 - len(''.join(blobs.values())) / raw) * 100:.0f}%)")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
