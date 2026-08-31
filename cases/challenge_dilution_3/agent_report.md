# Code analysis report

**Run:** `20260823-122418_validate_credit_risk_challenge_dilution`

**Case:** `challenge-case`

**Findings:** 1

This report concerns a synthetic evaluation case. It does not determine formal regulatory compliance.

## Findings

### CA-352DEC65DC: Approved Model Version differs from declared intent

- Assertion: `GOV-VERSION-001`
- Category: `model_change_governance`
- State: `confirmed`
- Severity: 3/5
- Confidence: 96%
- Component: `config/governance_record.yaml`

**Expected:** alder-2.1.0

**Observed:** alder-2.0.0

**Consequence:** Reliance on approval or validation for an earlier version leaves the changed implementation without current control evidence.

**Evidence**

- `docs/model_governance.md` line 19: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0

**Suggested action:** Align approved_model_version with the documented requirement and add a boundary test.

## Limitations

- Offline extraction reads fenced assertion records and does not interpret unstructured prose.
- Offline mode does not interpret regulatory prose beyond declared synthetic assertions.
- Python parse failed for code/credit_engine.py at line 102: invalid syntax
