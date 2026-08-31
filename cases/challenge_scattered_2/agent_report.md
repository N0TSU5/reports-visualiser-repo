# Code analysis report

**Run:** `20260823-082821_validate_credit_risk_challenge_scattered`

**Case:** `challenge-case`

**Findings:** 2

This report concerns a synthetic evaluation case. It does not determine formal regulatory compliance.

## Findings

### CA-352DEC65DC: Approved Model Version differs from declared intent

- Assertion: `GOV-VERSION-001`
- Category: `model_change_governance`
- State: `confirmed`
- Severity: 5/5
- Confidence: 99%
- Component: `config/governance_record.yaml`

**Expected:** alder-2.1.0

**Observed:** alder-2.0.0

**Consequence:** The production release alder-2.1.0 lacks demonstrated version-specific approval and validation, so reliance on controls performed for alder-2.0.0 may not cover the changed implementation.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0; value_type: text; unit: model version
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `tests/validation_results.json` $.model_version: "model_version": "alder-2.0.0"
- `tests/validation_results.json` $.release_note: No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.
- `tests/validation_results.json` $.executed_at and $.model_version: "executed_at": "2026-02-12T16:20:00Z"; "model_version": "alder-2.0.0"
- `tests/validation_results.json` $.summary and $.coverage_profile: "skipped": 4; listed coverage profiles each contain 0 cases
- `evidence/monitoring_record.json` $.model_version and $.reporting_date: "model_version": "alder-2.1.0"; "reporting_date": "2026-07-31"

**Suggested action:** Obtain and record approval for alder-2.1.0, rerun appropriately scoped independent validation against that exact version, address the four skipped tests and zero-coverage profiles as applicable, and link the resulting evidence to the production release.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three expected monitoring cycles are not evidenced, which may delay detection and escalation of drift or performance deterioration. The status field may also give a misleading view of control currentness.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07; value_type: text; unit: control state
- `evidence/monitoring_record.json` $.reporting_date and $.required_frequency: "reporting_date": "2026-07-31"; "required_frequency": "monthly"
- `evidence/monitoring_record.json` $.completed_periods: "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]
- `evidence/monitoring_record.json` $.latest_completed_period: "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` $.status_recorded_by_owner: "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` $.model_version, $.reporting_date and $.required_frequency: "model_version": "alder-2.1.0"; "reporting_date": "2026-07-31"; "required_frequency": "monthly"
- `evidence/monitoring_record.json` $.open_exception_count and $.status_recorded_by_owner: "open_exception_count": 0; "status_recorded_by_owner": "current"

**Suggested action:** Complete or provide evidence for the May, June, and July 2026 monitoring cycles, document and escalate any overdue cycles, and correct the owner-recorded status so it is derived from or reconciled to the latest completed period.

## Limitations

- Assertions were extracted only from the supplied docs/methodology.md evidence.
- No implementation assessment, answer-key inspection or defect inference was performed.
- No monitoring evidence before January 2026 or after July 2026 was supplied; conclusions are limited to the stated January–July 2026 reporting window.
- The governance configuration has no visible effective date, approval date, record owner, or change history, limiting assessment of temporal currency.
- The governance configuration records claimed control states but does not by itself demonstrate operating effectiveness.
- The production use of alder-2.1.0 is supported by the assertion and monitoring record, but no independent deployment record confirms the production build or deployment date.
- The public control digest was treated as general context only. No formal regulatory, legal, or accounting compliance conclusion is made.
- The public-control digest provides general context only and was not treated as a determination of regulatory or accounting compliance.
- The review is limited to the supplied synthetic artefacts; no source systems, signatures, approval minutes, organizational charts, or deployment records were independently inspected.
- The review is restricted to supplied synthetic records; source systems, deployment logs, model artefact hashes, signatures, committee minutes, organizational charts, and access records were not inspected.
- The supplied evidence consists of one governance document; this extraction records its declared assertions without independently verifying the underlying approval, validation, ownership, or monitoring artifacts.
- The validation evidence does not identify who executed or approved the work, so validation independence cannot be tested directly.
- This evaluation is not legal or accounting advice.
