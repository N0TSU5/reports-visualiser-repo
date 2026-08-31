# Code analysis report

**Run:** `20260831-221039_validate_credit_risk_fatigue_docs_l5`

**Case:** `challenge-case`

**Findings:** 5

This report concerns a synthetic evaluation case. It does not determine formal regulatory compliance.

## Findings

### CA-1CD6720715: Lifetime Horizon Basis differs from declared intent

- Assertion: `METH-LIFE-001`
- Category: `lifetime_pd`
- State: `confirmed`
- Severity: 5/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** remaining_contractual_maturity

**Observed:** remaining_contractual_maturity

**Consequence:** For seasoned Stage 2 loans, lifetime PD may be calculated over a longer horizon than the remaining contractual life, overstating cumulative default probability and potentially lifetime expected credit loss, subject to the configured horizon cap.

**Evidence**

- `docs/methodology.md` L0089-L0101: id: METH-LIFE-001; statement: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `config/model_config.yaml` line 11: lifetime_horizon_basis: remaining_contractual_maturity
- `config/system_map.yaml` line 17: lifetime_horizon_basis:
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `code/credit_engine.py` 693:701: def lifetime_pd(... original_term_months: int, remaining_term_months: int, config: dict[str, Any]) -> float: ... horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.
- `config/system_map.yaml` line 17: lifetime_horizon_basis: functions [lifetime_pd, calculate_facility]; path code/credit_engine.py; span 693:701; consequences [stage_2_probability, expected_credit_loss]
- `code/credit_engine.py` 693:701: def lifetime_pd(annual_pd, original_term_months, remaining_term_months, config): ... horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])

**Suggested action:** Change lifetime_pd to derive the horizon from remaining_term_months when lifetime_horizon_basis is remaining_contractual_maturity, while applying any valid cap afterward. Add a regression test for a seasoned Stage 2 facility where original and remaining terms differ.

### CA-352DEC65DC: Approved Model Version differs from declared intent

- Assertion: `GOV-VERSION-001`
- Category: `model_change_governance`
- State: `confirmed`
- Severity: 5/5
- Confidence: 99%
- Component: `config/governance_record.yaml`

**Expected:** alder-2.1.0

**Observed:** alder-2.0.0

**Consequence:** The current production version lacks demonstrated version-specific approval and validation, so reliance on the earlier evidence may leave changes in alder-2.1.0 unchallenged.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `tests/validation_results.json` model_version and release_note: "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"
- `docs/model_governance.md` L0019-L0031: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `tests/validation_results.json` executed_at, model_version, and release_note: "executed_at": "2026-02-12T16:20:00Z", "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."

**Suggested action:** Obtain and record approval and independent validation specifically for alder-2.1.0, including assessment of the staging and cash-flow timing change, or revert production to the approved and validated version until those controls are completed.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 5/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three expected monitoring cycles are not evidenced, which may delay detection and escalation of drift or performance deterioration. The recorded "current" status is inconsistent with the period-level data.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07
- `evidence/monitoring_record.json` reporting_date, required_frequency, completed_periods, and latest_completed_period: "reporting_date": "2026-07-31", "required_frequency": "monthly", completed periods are 2026-01 through 2026-04, and "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` open_exception_count and status_recorded_by_owner: "open_exception_count": 0, "status_recorded_by_owner": "current"
- `docs/model_governance.md` L0047-L0059: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.

**Suggested action:** Complete or supply the missing May–July 2026 monitoring records, document review and escalation outcomes, and correct the recorded currentness status and exception count if the cycles were not performed.

### CA-2FCD2F821B: Ead Balance Basis differs from declared intent

- Assertion: `METH-EAD-001`
- Category: `exposure_at_default`
- State: `unresolved`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** projected_at_default

**Observed:** projected_at_default

**Consequence:** Facilities whose principal or commitment limits reduce before expected default will have EAD calculated from unadjusted input balances, potentially overstating or understating EAD and expected credit loss.

**Evidence**

- `docs/methodology.md` L0135-L0147: id: METH-EAD-001; statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `config/model_config.yaml` line 29: ead_balance_basis: projected_at_default
- `config/system_map.yaml` line 27: ead_balance_basis:
- `docs/methodology.md` L0135-L0147: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `code/credit_engine.py` 1224:1230: def exposure_at_default(balance, undrawn, months_to_expected_default, config): ... return balance + (config["ccf"] * undrawn)

**Suggested action:** Project both drawn balance and available undrawn commitment through months_to_expected_default before applying the CCF, and ensure ead_balance_basis controls this behaviour. Add a test using an amortising facility where projected and current balances differ.

### CA-D2E091D62B: Discount Timing differs from declared intent

- Assertion: `METH-ECL-001`
- Category: `discounting`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** monthly_fractional

**Observed:** monthly_fractional

**Consequence:** Losses with horizons below 12 months receive no discounting, while other non-integer-year horizons receive too little discounting. This overstates the present value of expected credit losses relative to the declared methodology.

**Evidence**

- `docs/methodology.md` L0163-L0175: id: METH-ECL-001; statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional
- `config/model_config.yaml` line 34: discount_timing: monthly_fractional
- `config/system_map.yaml` line 32: discount_timing:
- `docs/methodology.md` L0163-L0175: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.
- `code/credit_engine.py` L1246-L1247: horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `code/credit_engine.py` lines 1241-1247: if config["discount_method"] != "effective_interest_rate": ... horizon_years = months_to_cash_shortfall // 12; return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)

**Suggested action:** Replace whole-year floor division with a fractional exponent such as `months_to_cash_shortfall / 12.0`, honor or validate the `discount_timing` configuration, and add tests for horizons below 12 months and non-multiples of 12.

## Limitations

- Assertions were extracted only from the explicitly fenced assertion records in docs/methodology.md.
- No implementation behavior, test results, answer key, or defect assessment was supplied or evaluated.
- No monitoring evidence after April 2026 was supplied. The absence of May–July records is treated as a contradiction of the explicit completeness assertion, not proof that no monitoring activity occurred outside the evidence set.
- Only the supplied synthetic artefacts were reviewed; no underlying approval minutes, validation report, deployment record, organizational chart, or monitoring workpapers were available.
- The governance configuration does not show an effective date, approval date, record owner, or change history, limiting assessment of whether its ownership and control declarations were current on 31 July 2026.
- The production version is inferred from the alder-2.1.0 monitoring record and the assertion because no authoritative production deployment record was supplied.
- The production version is inferred from the assertion and the alder-2.1.0 monitoring record because no separate deployment inventory was supplied.
- The public control digest provides contextual themes only. This review does not make a legal, accounting, or formal regulatory compliance determination.
- The public-control digest supplies contextual themes only and does not establish the case-specific control state or formal compliance.
- The review is limited to the supplied synthetic records; no deployment inventory, approval minutes, full validation report, organizational chart, validator attestations, monitoring workpapers, or issue-management records were available.
- The validation results report four skipped tests and zero coverage for several profiles, including seasoned Stage 2 facilities, 30-DPD-only SICR cases, unlikely-to-pay defaults, positive prior liens, non-integer discount horizons, and scenario probabilities below the floor. This raises additional validation-scope uncertainty, but no assertion or acceptance criteria were supplied for determining adequacy.
- The validation results show four skipped tests and zero coverage for several listed profiles, but no assertions were provided for deciding the adequacy of validation coverage.
- This evaluation is not legal or accounting advice and does not determine regulatory compliance.
