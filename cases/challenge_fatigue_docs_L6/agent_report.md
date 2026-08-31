# Code analysis report

**Run:** `20260831-221039_validate_credit_risk_fatigue_docs_l6`

**Case:** `challenge-case`

**Findings:** 6

This report concerns a synthetic evaluation case. It does not determine formal regulatory compliance.

## Findings

### CA-75B675DD6F: Default Rule differs from declared intent

- Assertion: `METH-DEFAULT-001`
- Category: `default_definition`
- State: `unresolved`
- Severity: 5/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** default_flag_or_utp_or_90_dpd

**Observed:** default_flag_or_utp_or_90_dpd

**Consequence:** An SME facility marked unlikely to pay, but without a default flag or sufficient days past due, will remain in Stage 1 or may enter Stage 2 rather than Stage 3, potentially understating expected credit loss.

**Evidence**

- `docs/methodology.md` L0071-L0083: id: METH-DEFAULT-001; statement: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment; expected: default_flag_or_utp_or_90_dpd.
- `config/model_config.yaml` line 16: default_rule: default_flag_or_utp_or_90_dpd
- `config/system_map.yaml` line 12: default_rule:
- `docs/methodology.md` L0071-L0083: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.
- `code/credit_engine.py` 988:1004: unlikely_to_pay: bool, ... if default_flag or days_past_due >= config["default_days_past_due"]: return 3

**Suggested action:** Include unlikely_to_pay in the Stage 3 condition, for example: if default_flag or unlikely_to_pay or days_past_due >= config["default_days_past_due"]: return 3. Also verify that default_days_past_due is configured as 90 and add tests covering each trigger independently.

### CA-352DEC65DC: Approved Model Version differs from declared intent

- Assertion: `GOV-VERSION-001`
- Category: `model_change_governance`
- State: `confirmed`
- Severity: 5/5
- Confidence: 99%
- Component: `config/governance_record.yaml`

**Expected:** alder-2.1.0

**Observed:** alder-2.0.0

**Consequence:** The supplied approval and validation evidence cannot be relied upon as version-specific control evidence for alder-2.1.0. The changed production implementation may therefore lack current approval and validation support.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0; unit: model version
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `docs/model_governance.md` L0019-L0031: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `tests/validation_results.json` model_version and release_note: "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version: "model_version": "alder-2.1.0"
- `tests/validation_results.json` executed_at, model_version, and release_note: Executed at 2026-02-12T16:20:00Z for alder-2.0.0; no rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.
- `evidence/monitoring_record.json` model_version and reporting_date: model_version is alder-2.1.0 and reporting_date is 2026-07-31.

**Suggested action:** Obtain documented approval for alder-2.1.0 and rerun appropriately scoped independent validation against that exact version, including the staging and cash-flow timing changes. Reconcile the approved-version field before representing the release as approved and validated.

### CA-2FCD2F821B: Ead Balance Basis differs from declared intent

- Assertion: `METH-EAD-001`
- Category: `exposure_at_default`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** projected_at_default

**Observed:** projected_at_default

**Consequence:** EAD and expected credit loss can be overstated or otherwise misstated when drawn principal or available limits decline before the expected default date, despite the configuration declaring projected-at-default treatment.

**Evidence**

- `docs/methodology.md` L0135-L0147: id: METH-EAD-001; statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date; expected: projected_at_default.
- `config/model_config.yaml` line 29: ead_balance_basis: projected_at_default
- `config/system_map.yaml` line 27: ead_balance_basis:
- `docs/methodology.md` L0135-L0147: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date; expected: projected_at_default.
- `code/credit_engine.py` 1721:1727: def exposure_at_default(balance: float, undrawn: float, months_to_expected_default: int, config: dict[str, Any]) -> float: return balance + (config["ccf"] * undrawn)
- `config/system_map.yaml` line 27: ead_balance_basis maps to exposure_at_default in code/credit_engine.py, span 1721:1727, with consequences for exposure_at_default and expected_credit_loss.
- `code/credit_engine.py` 1721:1727: def exposure_at_default(balance, undrawn, months_to_expected_default, config): ... return balance + (config["ccf"] * undrawn)

**Suggested action:** Project the drawn balance and remaining available commitment through months_to_expected_default, including contractual amortisation and limit reductions, before applying the CCF and calculating EAD. Add tests showing that EAD changes appropriately as the expected default date changes.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three required monthly monitoring cycles—May, June, and July 2026—are not evidenced as completed, potentially delaying detection and escalation of model drift or performance deterioration.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07; unit: control state
- `docs/model_governance.md` L0047-L0059: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.
- `evidence/monitoring_record.json` required_frequency, completed_periods, and latest_completed_period: "required_frequency": "monthly"; completed periods are 2026-01 through 2026-04; "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` reporting_date, open_exception_count, and status_recorded_by_owner: "reporting_date": "2026-07-31"; "open_exception_count": 0; "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` required_frequency, completed_periods, and latest_completed_period: required_frequency is monthly; completed periods are 2026-01 through 2026-04; latest_completed_period is 2026-04.
- `evidence/monitoring_record.json` reporting_date, open_exception_count, and status_recorded_by_owner: reporting_date is 2026-07-31; open_exception_count is 0; status_recorded_by_owner is current.

**Suggested action:** Complete or provide the May–July 2026 monitoring evidence, assess whether missed cycles require escalation, and correct the current status and exception count until all required periods are supported.

### CA-D2E091D62B: Discount Timing differs from declared intent

- Assertion: `METH-ECL-001`
- Category: `discounting`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** monthly_fractional

**Observed:** monthly_fractional

**Consequence:** Cash shortfalls within the first 12 months receive no discounting, while later non-integer-year horizons are discounted for too short a period, overstating the present value of expected credit loss relative to the declared methodology.

**Evidence**

- `docs/methodology.md` L0163-L0175: id: METH-ECL-001; statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years; expected: monthly_fractional.
- `config/model_config.yaml` line 34: discount_timing: monthly_fractional
- `config/system_map.yaml` line 32: discount_timing:
- `docs/methodology.md` L0163-L0175: Expected credit loss is discounted using fractional monthly timing rather than completed whole years; expected: monthly_fractional.
- `code/credit_engine.py` 1738:1744: if config["discount_method"] != "effective_interest_rate":
    raise ValueError("Unsupported discount method")
...
horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `config/system_map.yaml` line 32: discount_timing maps to expected_credit_loss in code/credit_engine.py, span 1730:1744, with consequences for present_value and expected_credit_loss.
- `code/credit_engine.py` 1738-1744: if config["discount_method"] != "effective_interest_rate": ... horizon_years = months_to_cash_shortfall // 12; return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)

**Suggested action:** Calculate the exponent as `months_to_cash_shortfall / 12.0`, validate or dispatch on `config["discount_timing"]`, and add tests for horizons below 12 months and non-multiples of 12.

### CA-D23E4BDDCF: Sicr Rule differs from declared intent

- Assertion: `METH-SICR-001`
- Category: `staging`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** relative_or_30_dpd

**Observed:** relative_or_30_dpd

**Consequence:** A non-defaulted facility meeting only one SICR indicator—either the relative probability increase criterion or the 30-days-past-due criterion—remains in Stage 1, delaying lifetime expected-credit-loss recognition.

**Evidence**

- `docs/methodology.md` L0057-L0069: id: METH-SICR-001; statement: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal; expected: relative_or_30_dpd.
- `config/model_config.yaml` line 13: sicr_rule: relative_or_30_dpd
- `config/system_map.yaml` line 7: sicr_rule:
- `docs/methodology.md` L0057-L0069: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal; expected: relative_or_30_dpd.
- `code/credit_engine.py` 988:1004: if (relative_change >= config["sicr_relative_threshold"] and days_past_due >= config["sicr_days_past_due_backstop"]): return 2

**Suggested action:** Replace the SICR conjunction with OR semantics for non-defaulted facilities, confirm the configured thresholds are 2 and 30 days, and implement or document any separately supported rebuttal mechanism. Add tests where each criterion is met independently.

## Limitations

- Assertions are extracted from a single supplied governance document; no external corroboration or implementation assessment was performed.
- Assertions were extracted only from the supplied methodology document and its explicit fenced assertion records.
- No dated approval document, deployment record, release manifest, change-impact assessment, validation report, validator organizational information, or monitoring workpapers were supplied.
- No implementation behavior, answer key, or defect status was assessed.
- No separate approval document, deployment record, validation report, validator organizational chart, or monitoring workpapers were supplied.
- The monitoring record does not establish whether absent periods were never performed, performed late, or performed but omitted; it only shows that completion through July is not evidenced.
- The ownership record lacks an effective date, approving authority, named accountable individual, and change history, limiting assurance over its currentness.
- The production status of alder-2.1.0 is inferred from the assertion and monitoring record rather than independently established.
- The production status of alder-2.1.0 is suggested by the assertion and monitoring record but was not independently established through deployment evidence.
- The public control digest provides contextual themes only. No conclusion is made regarding formal regulatory, legal, accounting, or policy compliance.
- The public-control digest provides contextual themes only; this review does not determine legal, regulatory, accounting, or formal compliance.
- The review is limited to supplied synthetic extracts. File authenticity, completeness, signatures, approvals, provenance, access controls, and audit trails were not independently verified.
- The review is limited to the supplied synthetic extracts; source-file authenticity, completeness, signatures, approvals, and audit trails were not independently verified.
- The validation summary shows four skipped tests and zero coverage for several listed case profiles, but no corresponding assertions were provided for deciding the adequacy of validation coverage.
- Validation results report four skipped tests and zero coverage for several case profiles. Validation adequacy cannot be concluded because corresponding scope requirements, risk assessments, and assertions were not supplied.
