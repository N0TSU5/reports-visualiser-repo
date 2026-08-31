# Code analysis report

**Run:** `20260823-083021_validate_credit_risk_challenge_scattered`

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

**Consequence:** The apparent production version has no supplied version-specific approval or completed validation evidence, so reliance on the earlier release's controls is not supported.

**Evidence**

- `docs/model_governance.md` L0019-L0030: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0; unit: model version
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `tests/validation_results.json` model_version and executed_at: "executed_at": "2026-02-12T16:20:00Z", "model_version": "alder-2.0.0"
- `tests/validation_results.json` release_note: No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"
- `tests/validation_results.json` $.executed_at and $.model_version: "executed_at": "2026-02-12T16:20:00Z", "model_version": "alder-2.0.0"
- `tests/validation_results.json` $.release_note: No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.
- `evidence/monitoring_record.json` $.model_version and $.reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"

**Suggested action:** Obtain and record approval and independent validation for alder-2.1.0, including assessment of the staging and cash-flow timing change. Reconcile the approved-version field with the deployed production version and do not represent 2.0.0 evidence as covering 2.1.0 without documented change-impact justification.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three expected monthly monitoring cycles are not evidenced, which may delay detection and escalation of drift or performance deterioration. The owner-recorded current status is inconsistent with the period-level record.

**Evidence**

- `docs/model_governance.md` L0047-L0058: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07; unit: control state
- `evidence/monitoring_record.json` required_frequency and completed_periods: "required_frequency": "monthly"; completed periods are 2026-01, 2026-02, 2026-03, and 2026-04.
- `evidence/monitoring_record.json` latest_completed_period: "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` reporting_date, open_exception_count, and status_recorded_by_owner: "reporting_date": "2026-07-31", "open_exception_count": 0, "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` $.required_frequency and $.completed_periods: "required_frequency": "monthly"; completed periods are 2026-01, 2026-02, 2026-03, and 2026-04.
- `evidence/monitoring_record.json` $.latest_completed_period: "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` $.reporting_date, $.open_exception_count, and $.status_recorded_by_owner: "reporting_date": "2026-07-31", "open_exception_count": 0, "status_recorded_by_owner": "current"

**Suggested action:** Complete or provide the May, June, and July 2026 monitoring evidence, assess whether retrospective escalation is required, and correct the recorded status and exception count if those cycles were not completed on time.

## Limitations

- Assertions were extracted from a single supplied governance document; no corroborating sources were provided.
- Assertions were extracted only from the supplied docs/methodology.md evidence and were not independently validated against an implementation, test results, or external requirements.
- No defect inference or implementation assessment was performed.
- No deployment, release-management, or production inventory record was supplied. The apparent production use of alder-2.1.0 is inferred from the monitoring record and assertion scope.
- No independent validation report, validator organizational information, conflict assessment, or formal validation sign-off was supplied.
- No monitoring procedure or due-date convention was supplied. The missing May through July periods contradict the stated completeness claim, but exact timeliness against internal deadlines cannot be assessed.
- No production deployment or release-management record was supplied; alder-2.1.0 production status is inferred from the monitoring record and the assertion's stated scope.
- No underlying approval document, validation report, validator organizational information, or formal sign-off was supplied.
- No underlying model approval document, approval date, approver identity, approval conditions, or change-impact assessment was supplied.
- The governance document largely states the assertions under review and should not be treated as independent corroboration without underlying records.
- The public-control digest is contextual only. This review does not determine formal regulatory, legal, or accounting compliance.
- The public-control digest provides general context only and does not establish compliance or alter the evidence-based decisions.
- The validation suite reports four skipped tests and zero coverage for several listed profiles. This raises a separate coverage concern, but the supplied assertions do not define expected validation coverage or permit a conclusive adequacy assessment.
- The validation suite shows four skipped tests and zero coverage for several profiles, but the supplied assertions do not ask for a conclusion on validation coverage adequacy.
- This extraction records declared assertions only and does not assess implementation, control effectiveness, or defects.
- This is a synthetic evaluation exercise and not legal or accounting advice.
