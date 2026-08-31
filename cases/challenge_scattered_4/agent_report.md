# Code analysis report

**Run:** `20260823-083211_validate_credit_risk_challenge_scattered`

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

**Consequence:** The evidence does not establish that the apparent production version alder-2.1.0 has version-specific approval and validation. Changes introduced after alder-2.0.0 may therefore be outside the demonstrated control coverage.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0; value_type: text; unit: model version
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `tests/validation_results.json` model_version: "model_version": "alder-2.0.0"
- `tests/validation_results.json` release_note: No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.
- `evidence/monitoring_record.json` model_version: "model_version": "alder-2.1.0"
- `tests/validation_results.json` executed_at and model_version: "executed_at": "2026-02-12T16:20:00Z", "model_version": "alder-2.0.0"
- `tests/validation_results.json` summary and coverage_profile: 24 passed, 0 failed, 4 skipped; multiple stated coverage areas contain 0 cases.
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"

**Suggested action:** Reconcile the production inventory and governance record. Obtain and record approval and independent validation specifically for alder-2.1.0, including testing of the staging and cash-flow timing change, or demonstrate that production remains on alder-2.0.0 and correct the contrary records.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three expected monthly monitoring cycles are not evidenced, which may delay detection and escalation of drift or performance deterioration. The status label may also give a misleading impression of currentness.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07; value_type: text; unit: control state
- `evidence/monitoring_record.json` reporting_date and required_frequency: "reporting_date": "2026-07-31", "required_frequency": "monthly"
- `evidence/monitoring_record.json` completed_periods: "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]
- `evidence/monitoring_record.json` latest_completed_period: "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` status_recorded_by_owner: "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` open_exception_count and status_recorded_by_owner: "open_exception_count": 0, "status_recorded_by_owner": "current"

**Suggested action:** Complete or supply monitoring evidence for May, June and July 2026, document any approved exception or delay, and correct the current-status field unless the missing periods can be substantiated.

## Limitations

- Assertions were extracted from a single supplied governance document; no implementation testing, corroboration, or control assessment was performed.
- Assertions were extracted from one supplied methodology document only.
- No approval document, validation report, validator organizational record, or change-control record was supplied beyond the mapped configuration and validation-results summary.
- No approval document, validation report, validator organizational record, validation mandate or detailed change-control record was supplied.
- No implementation behavior, answer key or defect assessment was evaluated.
- No production deployment manifest was supplied. Alder-2.1.0 is treated as the apparent production version based on the assertion and July monitoring record, but actual deployment is not conclusively proven.
- No production deployment manifest was supplied; alder-2.1.0 is treated as the apparent production version because the assertion and monitoring record identify it as such.
- Test results show 24 passes and no failures, but four tests were skipped and several stated coverage areas had zero cases; these facts do not resolve the version or independence gaps.
- The assessment is limited to the supplied synthetic records and does not determine formal regulatory, legal or accounting compliance.
- The extracted records are declarations in the supplied evidence and are not independently verified.
- The governance configuration lacks visible effective dates, approval dates, record versioning and sign-off metadata, limiting assessment of currentness.
- The monitoring record does not state whether monitoring operates with an approved reporting lag. No such lag or exception was supplied, and the assertion expressly requires completion through July 2026.
- The review is limited to the supplied synthetic records and does not establish legal, regulatory or accounting compliance.
- Validation results show 24 passes and no failures, but four tests were skipped and multiple identified coverage populations had zero cases. The reasons for the skips and zero coverage are unknown.
