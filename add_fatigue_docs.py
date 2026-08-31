"""Add the corrected fatigue-documentation experiment to data.js.

The original `fatigue` bundle measured a broken case: config/system_map.yaml kept
the baseline line numbers after injection, so reviewers were sent to the wrong
part of the file and returned insufficient_evidence, which the harness scored as
missed defects. This experiment repairs the map, replaces the numeric-dict noise
with the compliance and design documentation the report actually describes, and
escalates length and proximity together across seven levels.

    python3 add_fatigue_docs.py
"""

import collections
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SOLUTION = HERE.parent / "code-analysis-solution"
BUNDLES = SOLUTION / "fatigue_docs_bundles"
RUNS = SOLUTION / "user" / "runs"
DATA_JS = HERE / "data.js"

METH = ["METH-PD-001", "METH-SICR-001", "METH-DEFAULT-001", "METH-LIFE-001",
        "METH-LGD-001", "METH-EAD-001", "METH-ECL-001"]

# level -> (noise lines injected, mean gap to defect, final file length)
META = {1: (112, 165, 314), 2: (210, 133, 412), 3: (413, 107, 615),
        4: (714, 88, 916), 5: (1113, 58, 1315), 6: (1610, 39, 1812),
        7: (2212, 0, 2414)}

DEFECTS = {
    "METH-PD-001": ("EXP-SCENARIO-FLOOR-SEQUENCE-001", "credit_engine.py",
                    "scenario_pds applies the approved PD floor before the scenario shift, so the floor is not reapplied to the shifted result."),
    "METH-SICR-001": ("EXP-SICR-CONJUNCTION-001", "credit_engine.py",
                      "determine_stage requires all SICR triggers to fire together instead of any one of them."),
    "METH-DEFAULT-001": ("EXP-UTP-DEFAULT-001", "credit_engine.py",
                         "determine_stage ignores the unlikely-to-pay indicator, so UTP-only defaults are never staged."),
    "METH-LIFE-001": ("EXP-REMAINING-MATURITY-001", "credit_engine.py",
                      "lifetime_pd uses original_term_months rather than remaining_term_months for the horizon."),
    "METH-LGD-001": ("EXP-COLLATERAL-RECOVERY-001", "credit_engine.py",
                     "loss_given_default ignores prior-ranking liens, recovery duration and discounting of delayed recoveries."),
    "METH-EAD-001": ("EXP-PROJECTED-EAD-001", "credit_engine.py",
                     "exposure_at_default uses current drawn/undrawn balances instead of projecting to the expected default point."),
    "METH-ECL-001": ("EXP-DISCOUNT-TIMING-001", "credit_engine.py",
                     "expected_credit_loss floor-divides months by 12, truncating fractional-year discount timing."),
}

SPAN_KEY = {"METH-PD-001": "pd_floor_application", "METH-SICR-001": "sicr_rule",
            "METH-DEFAULT-001": "default_rule", "METH-LIFE-001": "lifetime_horizon_basis",
            "METH-LGD-001": "collateral_recovery_basis", "METH-EAD-001": "ead_balance_basis",
            "METH-ECL-001": "discount_timing"}

DESCRIPTION = """
    <p style="margin-bottom: 8px;">Re-run of <strong>Context Fatigue</strong> after two corrections to the original experiment.</p>
    <ul style="margin-left: 20px; line-height: 1.6; list-style-type: disc;">
        <li><strong>The case bundle was repaired.</strong> The original scripts injected noise into <code>credit_engine.py</code> but never updated <code>config/system_map.yaml</code>, so declared spans still pointed at baseline line numbers &mdash; <code>discount_timing</code> claimed lines 120:135 while the function had moved to 5424. Reviewers followed the map, found noise, and returned <em>insufficient_evidence</em>, which the harness scored as missed defects. That artifact produced the original all-or-nothing 7/7-vs-0/7 pattern.</li>
        <li><strong>The noise is now what the report describes.</strong> The old generator emitted numeric dict literals (holiday calendars, haircut tables) &mdash; 3058 dict lines against 8 prose lines. This injects IFRS 9 / CRR compliance sections and architecture design notes as markdown.</li>
        <li>Seven levels escalate length and proximity together: level 1 is short and far (112 lines, ~165 lines from the defect), level 7 is long and adjacent (2212 lines, gap 0).</li>
    </ul>
    <p style="margin-top:10px;"><strong>Result:</strong> detection is <em>not</em> monotonic in noise volume &mdash; it falls to 43% at level 5 then recovers to 86% at level 7, the level with the most noise. Across all 49 defect-observations, whether a defect is found is predicted perfectly by the width of its declared evidence span: every span &le;68 lines was caught (36/36), every span &ge;92 lines was missed (13/13).</p>
"""


def span_widths(level):
    text = (BUNDLES / f"challenge_fatigue_docs_L{level}" / "config" / "system_map.yaml").read_text()
    out = {}
    for defect, key in SPAN_KEY.items():
        m = re.search(rf'{key}:.*?span: "(\d+):(\d+)"', text, re.S)
        out[defect] = int(m.group(2)) - int(m.group(1)) + 1 if m else None
    return out


def level_runs(level):
    """All completed runs for one level, newest first."""
    found = []
    for d in RUNS.glob(f"*fatigue_docs_l{level}*"):
        raw = d / "outputs" / "raw_report.json"
        if raw.exists():
            found.append(d)
    return sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)


def bundle_files(level):
    root = BUNDLES / f"challenge_fatigue_docs_L{level}"
    wanted = ["code/credit_engine.py", "config/system_map.yaml",
              "config/model_config.yaml", "config/governance_record.yaml",
              "evidence/monitoring_record.json"]
    files = []
    for rel in wanted:
        p = root / rel
        if p.exists():
            files.append({"filename": rel, "content": p.read_text(),
                          "diff_content": "See the Case Bundle tab for the full directory."})
    return files


def main():
    raw = DATA_JS.read_text()
    start, end = raw.index("["), raw.rindex("]") + 1
    data = json.loads(raw[start:end])
    data = [b for b in data if b.get("id") != "fatigue_docs"]

    levels, tipping = [], []
    for lv in range(1, 8):
        runs = level_runs(lv)
        if not runs:
            continue
        widths = span_widths(lv)
        per_run, caught_sets = [], []
        for d in runs:
            ids = {f.get("assertion_id") for f in
                   json.loads((d / "outputs" / "raw_report.json").read_text()).get("findings", [])}
            caught_sets.append(ids & set(METH))
            per_run.append(len(ids & set(METH)))

        # A defect counts as found when the majority of runs found it.
        tally = collections.Counter(i for s in caught_sets for i in s)
        found_ids = [m for m in METH if tally[m] > len(runs) / 2]
        missed_ids = [m for m in METH if m not in found_ids]

        def record(defect_id):
            name, target, cause = DEFECTS[defect_id]
            return {
                "id": defect_id, "name": name,
                "target_file": target,
                "target_search": "",
                "root_cause": cause,
                "mutation_applied": (
                    f"Level {lv}: {META[lv][0]} lines of compliance/design markdown, "
                    f"mean gap {META[lv][1]} lines from the defect. "
                    f"Declared evidence span for this defect: {widths[defect_id]} lines."
                ),
            }

        nl, gap, flen = META[lv]
        rate = round(sum(per_run) / len(per_run) / 7 * 100)
        levels.append({
            "name": f"Level {lv} — {nl} lines, gap {gap}",
            "files": bundle_files(lv),
            "agent_report": (
                f"### Level {lv}\n\n"
                f"- **Noise injected:** {nl} lines of compliance / design markdown\n"
                f"- **Mean gap to defect:** {gap} lines ({gap / flen * 100:.1f}% of the {flen}-line file)\n"
                f"- **Runs:** {len(runs)} — detected {per_run}\n"
                f"- **Detection rate:** {rate}%\n\n"
                f"#### Declared evidence-span width per defect\n\n"
                "| Defect | Span width | Outcome |\n|---|---:|---|\n"
                + "\n".join(
                    f"| {m.replace('METH-','').replace('-001','')} | {widths[m]} | "
                    f"{'found' if m in found_ids else '**missed**'} |" for m in METH)
                + "\n\nSpans at or below ~68 lines were caught in every level; "
                  "spans at or above ~92 lines were missed in every level.\n"
            ),
            "found_defects": [record(m) for m in found_ids],
            "missed_defects": [record(m) for m in missed_ids],
        })
        tipping.append({
            "level": f"L{lv}",
            "detection_rate": f"{rate}%",
            "description": (
                f"{nl} lines of compliance/design markdown, mean gap {gap} lines "
                f"({gap / flen * 100:.1f}% of file). n={len(runs)}. "
                f"PD evidence span {widths['METH-PD-001']} lines."
            ),
        })

    data.append({
        "id": "fatigue_docs",
        "name": "Fatigue (Docs, corrected)",
        "description": DESCRIPTION,
        "found_defects": levels[0]["found_defects"],
        "missed_defects": levels[0]["missed_defects"],
        "agent_report": levels[0]["agent_report"],
        "files": levels[0]["files"],
        "tipping_data": tipping,
        "levels": levels,
    })

    DATA_JS.write_text("const reportData = " + json.dumps(data, indent=2) + ";")
    print(f"added fatigue_docs with {len(levels)} levels")
    for t in tipping:
        print(f"  {t['level']}: {t['detection_rate']}")
    print(f"data.js now {DATA_JS.stat().st_size / 1e6:.1f} MB, {len(data)} bundles")


if __name__ == "__main__":
    main()
