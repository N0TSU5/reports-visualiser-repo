# Code analysis report

**Run:** `20260823-082625_validate_credit_risk_challenge_scattered`

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

**Consequence:** The production change to alder-2.1.0 is not covered by the supplied approval and validation evidence, so reliance on those controls for the current release is unsupported.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `docs/model_governance.md` L0019-L0031: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `tests/validation_results.json` model_version and release_note: "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"
- `tests/validation_results.json` executed_at, model_version, and release_note: "executed_at": "2026-02-12T16:20:00Z"; "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."

**Suggested action:** Obtain documented approval for alder-2.1.0 and perform version-specific independent validation covering the staging and cash-flow timing change before representing the current release as approved and validated.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three required monitoring cycles are not evidenced, which could delay identification and escalation of drift or performance deterioration. The recorded “current” status and zero exceptions are unreliable without evidence for the missing periods.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07
- `docs/model_governance.md` L0047-L0059: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.
- `evidence/monitoring_record.json` required_frequency, completed_periods, and latest_completed_period: "required_frequency": "monthly"; completed periods are 2026-01 through 2026-04; "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` reporting_date, open_exception_count, and status_recorded_by_owner: "reporting_date": "2026-07-31", "open_exception_count": 0, "status_recorded_by_owner": "current"

**Suggested action:** Complete or provide the May, June, and July 2026 monitoring records for alder-2.1.0. Correct the currentness status, raise and track an exception if the cycles were missed, and document owner review and escalation.

## Limitations

- Assertions were extracted from the supplied untrusted governance record only; no implementation assessment, defect inference, or independent verification was performed.
- Assertions were extracted only from the explicitly fenced assertion records in docs/methodology.md.
- No implementation assessment, defect inference, or answer-key inspection was performed.
- No monitoring reports or execution artefacts for May, June, or July 2026 were supplied; the conclusion is based on the completed-period list in the monitoring record.
- No underlying approval minutes, change approval, deployment record, complete validation report, validator organizational information, or independent validation sign-off was supplied.
- No underlying approval minutes, complete validation report, validator organizational information, or monitoring reports for May through July 2026 were supplied.
- Severity uses a five-point reviewer scale, where 5 denotes the highest potential governance impact.
- Severity uses a five-point reviewer scale, where 5 represents the highest potential governance impact.
- The assessment is restricted to the supplied synthetic records and does not determine formal regulatory, legal, or accounting compliance.
- The governance configuration extracts for ownership, approval version, and validation independence contain no visible effective date, review date, approver, or sign-off.
- The review is limited to the supplied synthetic records and does not establish formal legal, regulatory, or accounting compliance.
- The validation evidence is dated 12 February 2026 and applies to alder-2.0.0. Production use of alder-2.1.0 is supported indirectly by the monitoring record and assertion but is not independently confirmed by deployment evidence.
