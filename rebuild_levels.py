"""Rebuild the per-level `files` arrays in data.js from the captured bundles.

Each level in data.js previously carried only `code/credit_engine.py`, so switching
level dropped the rest of the bundle (and, for `scattered`, showed a byte-identical
file at every hop count because the hop mutation lives in the sibling files).

This script repopulates every level with the full `code/` tree captured under
`tipping_verification/<mode>/level_<n>/code/`, plus the config and evidence files
that carry the two governance defects.

Usage:  python3 rebuild_levels.py
"""

import difflib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOLUTION = os.path.abspath(os.path.join(HERE, "..", "code-analysis-solution"))
TIPPING = os.path.join(SOLUTION, "tipping_verification")
BASELINE = os.path.join(
    SOLUTION, "projects/synthetic/sme_credit_risk/cases/challenge_case"
)
DATA_JS = os.path.join(HERE, "data.js")

# data.js bundle id -> (tipping_verification mode dir, level numbers in display order)
MODES = {
    "fatigue": ("fatigue", [10, 50, 100, 200, 300, 500]),
    "dilution": ("dilution", [1, 2, 3, 4, 5]),
    "scattered": ("scattered", [1, 2, 3, 4, 5]),
    "sec_authority_escalation": ("authority", [1, 2, 3, 4]),
    "sec_goal_redirection": ("goal", [1, 2, 3]),
    "sec_linguistic_confusion": ("linguistic", [1, 2, 3]),
}

# Carried on every level so the two governance findings stay clickable.
# build_verification.py only ever copied `code/`, so these come from the baseline
# case. For fatigue the evaluated run used bloated copies of these two files that
# were never captured; the defects themselves are identical, only padding differs.
EXTRA_FILES = [
    "config/governance_record.yaml",
    "evidence/monitoring_record.json",
]


def read_text(path):
    with open(path, "r", errors="replace") as handle:
        return handle.read()


def make_diff(baseline_path, content, rel_path):
    base_lines = read_text(baseline_path).splitlines(keepends=True) if os.path.exists(
        baseline_path
    ) else []
    new_lines = content.splitlines(keepends=True)
    diff = difflib.unified_diff(
        base_lines,
        new_lines,
        fromfile=f"baseline/{rel_path}",
        tofile=f"mutated/{rel_path}",
    )
    text = "".join(diff)
    if not text:
        return "No changes from baseline for this file."

    lines = text.splitlines()
    if len(lines) > 800:
        omitted = len(lines) - 800
        text = "\n".join(lines[:800]) + f"\n\n... [diff truncated, {omitted} lines omitted] ..."
    return text


def collect_level_files(mode_dir, level):
    """Return the file records for one level, in a stable display order."""
    level_dir = os.path.join(TIPPING, mode_dir, f"level_{level}")
    code_dir = os.path.join(level_dir, "code")
    if not os.path.isdir(code_dir):
        raise SystemExit(f"missing captured bundle: {code_dir}")

    rel_paths = []
    for root, _dirs, names in os.walk(code_dir):
        for name in names:
            if name.endswith(".pyc"):
                continue
            abs_path = os.path.join(root, name)
            rel_paths.append("code/" + os.path.relpath(abs_path, code_dir))

    # credit_engine.py first (it is the entry point every finding refers back to),
    # then the remaining hop/helper files alphabetically.
    rel_paths.sort(key=lambda p: (os.path.basename(p) != "credit_engine.py", p))

    files = []
    for rel_path in rel_paths + EXTRA_FILES:
        source = (
            os.path.join(level_dir, rel_path)
            if rel_path.startswith("code/")
            else os.path.join(BASELINE, rel_path)
        )
        if not os.path.exists(source):
            continue
        content = read_text(source)
        files.append(
            {
                "filename": rel_path,
                "content": content,
                "diff_content": make_diff(
                    os.path.join(BASELINE, rel_path), content, rel_path
                ),
            }
        )
    return files


def main():
    raw = read_text(DATA_JS)
    start, end = raw.index("["), raw.rindex("]") + 1
    data = json.loads(raw[start:end])

    for bundle in data:
        entry = MODES.get(bundle.get("id"))
        if not entry:
            continue
        mode_dir, levels = entry
        declared = bundle.get("levels") or []
        if len(declared) != len(levels):
            raise SystemExit(
                f"{bundle['id']}: data.js has {len(declared)} levels, "
                f"expected {len(levels)}"
            )

        for level_data, level in zip(declared, levels):
            files = collect_level_files(mode_dir, level)
            level_data["files"] = files
            print(f"  {bundle['id']:<26} {level_data['name']:<16} {len(files):>3} files")

    with open(DATA_JS, "w") as handle:
        handle.write("const reportData = ")
        handle.write(json.dumps(data, indent=2))
        handle.write(";")

    size_mb = os.path.getsize(DATA_JS) / (1024 * 1024)
    print(f"\nwrote {DATA_JS} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
