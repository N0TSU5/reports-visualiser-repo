# Code analysis report

**Run:** `20260823-083410_validate_credit_risk_challenge_scattered`

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

**Consequence:** The production change to alder-2.1.0 is not supported by supplied version-specific approval and validation evidence, weakening assurance over the changed implementation.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0; unit: model version
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `docs/model_governance.md` L0019-L0031: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `tests/validation_results.json` model_version and release_note: "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"
- `tests/validation_results.json` executed_at, model_version, summary, coverage_profile, and release_note: Validation executed 2026-02-12 for alder-2.0.0; 4 tests were skipped; listed profiles had zero coverage; no rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.

**Suggested action:** Obtain and record formal approval and independent validation for alder-2.1.0, including testing of the staging and cash-flow timing changes. Reconcile the approved-version field with the actual production release and document any interim risk acceptance or rollback decision.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 98%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three required monthly monitoring cycles appear outstanding, potentially delaying detection and escalation of drift or performance deterioration. The current status and zero-exception count may understate the control gap.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07; unit: control state
- `docs/model_governance.md` L0047-L0059: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.
- `evidence/monitoring_record.json` required_frequency, completed_periods, and latest_completed_period: "required_frequency": "monthly"; completed periods are 2026-01 through 2026-04; "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` status fields: "open_exception_count": 0, "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` reporting_date, required_frequency, completed_periods, and latest_completed_period: Reporting date is 2026-07-31; frequency is monthly; completed periods are 2026-01 through 2026-04; latest completed period is 2026-04.
- `evidence/monitoring_record.json` open_exception_count and status_recorded_by_owner: "open_exception_count": 0, "status_recorded_by_owner": "current"

**Suggested action:** Complete or provide the May, June, and July 2026 monitoring evidence, investigate why the record was marked current with no open exception, and correct the status or raise and track a monitoring exception.

## Limitations

- All artefacts were supplied as untrusted case evidence. Their authenticity, provenance, approvals, and completeness were not independently verified.
- All supplied artefacts were treated as untrusted evidence and were assessed only for internal consistency; their authenticity and completeness were not independently verified.
- Assertions were extracted from a single supplied governance document and are recorded as declared evidence without independent corroboration.
- Assertions were extracted only from the explicitly fenced assertion records in docs/methodology.md.
- Narrative details not represented as fenced assertions, including the 60-month lifetime maturity cap, were not added as separate assertions.
- No approval decision, change ticket, validation report, validator identity, organisational chart, conflict assessment, or validation sign-off was supplied.
- No deployment record was supplied; alder-2.1.0 production status is inferred from the monitoring record.
- No implementation assessment, defect determination, or answer-key comparison was performed.
- No implementation assessment, defect inference, or answer-key comparison was performed.
- No underlying approval decision, change ticket, production deployment record, validation report, validator identity, or organisational-independence documentation was supplied.
- The monitoring evidence does not state the due date for a month-end monitoring cycle, creating limited uncertainty over whether July 2026 was due on 31 July; May and June remain clearly missing.
- The public-control digest is contextual only. This review does not determine regulatory, legal, accounting, PRA, EBA, IFRS 9, or other formal compliance.
- The public-control digest provides contextual governance themes but does not itself prove any case-specific control state or determine regulatory, legal, or accounting compliance.
- The validation results contain four skipped tests and zero coverage for several profiles, but the case does not provide acceptance criteria or separate assertions sufficient for definitive control conclusions on each gap.
- The validation results show zero coverage for several listed profiles and four skipped tests, but no corresponding assertions were provided against which to reach separate control decisions.
