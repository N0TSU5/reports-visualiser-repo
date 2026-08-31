# Code analysis report

**Run:** `20260831-220657_validate_credit_risk_fatigue_docs_l2`

**Case:** `challenge-case`

**Findings:** 8

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

**Consequence:** The apparent production version lacks version-matched approval and validation evidence, so reliance on the earlier control evidence is not supported.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `docs/model_governance.md` L0019-L0031: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `tests/validation_results.json` model_version: "model_version": "alder-2.0.0"
- `tests/validation_results.json` release_note: No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.
- `evidence/monitoring_record.json` model_version: "model_version": "alder-2.1.0"
- `tests/validation_results.json` executed_at and model_version: "executed_at": "2026-02-12T16:20:00Z", "model_version": "alder-2.0.0"
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"

**Suggested action:** Reconcile the production release and approval inventory. Obtain documented approval and independent validation for alder-2.1.0, including the staging and cash-flow timing change, or demonstrate that production was reverted to the approved alder-2.0.0 version.

### CA-5089540F53: Collateral Recovery Basis differs from declared intent

- Assertion: `METH-LGD-001`
- Category: `loss_given_default`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** net_prior_liens_discounted

**Observed:** net_prior_liens_discounted

**Consequence:** Collateral recoveries can be overstated, causing LGD and downstream expected credit loss to be understated, particularly for collateral subject to senior claims or long recovery periods.

**Evidence**

- `docs/methodology.md` L0121-L0133: id: METH-LGD-001; statement: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.; expected: net_prior_liens_discounted
- `config/model_config.yaml` line 27: collateral_recovery_basis: net_prior_liens_discounted
- `config/system_map.yaml` line 22: collateral_recovery_basis:
- `docs/methodology.md` L0121-L0133: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.
- `code/credit_engine.py` 308:318: The function accepts prior_liens, recovery_months, and effective_interest_rate, but calculates eligible_collateral = collateral * (1.0 - config["collateral_haircut"]), then derives unsecured_share from balance minus eligible_collateral and returns LGD without using those three inputs.
- `code/credit_engine.py` 308:318: eligible_collateral = collateral * (1.0 - config["collateral_haircut"]); unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0); return min(1.0, unsecured_share + config["downturn_lgd_addon"])

**Suggested action:** Revise loss_given_default to deduct prior-ranking liens from eligible collateral, floor the net recovery appropriately, discount it using the effective interest rate over recovery_months, and use that discounted net recovery in the LGD calculation. Add tests covering nonzero prior liens and positive recovery periods.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three expected monitoring cycles are not evidenced, potentially delaying identification and escalation of drift or performance deterioration. The recorded current status is unreliable.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07
- `docs/model_governance.md` L0047-L0059: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.
- `evidence/monitoring_record.json` reporting_date, required_frequency, and completed_periods: "reporting_date": "2026-07-31", "required_frequency": "monthly", "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]
- `evidence/monitoring_record.json` latest_completed_period: "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` status_recorded_by_owner: "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` reporting_date and required_frequency: "reporting_date": "2026-07-31", "required_frequency": "monthly"
- `evidence/monitoring_record.json` completed_periods and latest_completed_period: "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"], "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` open_exception_count and status_recorded_by_owner: "open_exception_count": 0, "status_recorded_by_owner": "current"

**Suggested action:** Complete or provide the May, June, and July 2026 monitoring records, assess whether the gaps require escalation, and correct the recorded current status and exception count until the missing cycles are resolved.

### CA-75B675DD6F: Default Rule differs from declared intent

- Assertion: `METH-DEFAULT-001`
- Category: `default_definition`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** default_flag_or_utp_or_90_dpd

**Observed:** default_flag_or_utp_or_90_dpd

**Consequence:** An SME facility marked unlikely to pay, but without a default flag or sufficient days past due, can remain in Stage 1 or Stage 2 rather than Stage 3, potentially understating expected credit loss.

**Evidence**

- `docs/methodology.md` L0071-L0083: id: METH-DEFAULT-001; statement: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.; expected: default_flag_or_utp_or_90_dpd
- `config/model_config.yaml` line 16: default_rule: default_flag_or_utp_or_90_dpd
- `config/system_map.yaml` line 12: default_rule:
- `docs/methodology.md` L0071-L0083: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.
- `code/credit_engine.py` 278:287: unlikely_to_pay: bool, ... if default_flag or days_past_due >= config["default_days_past_due"]: return 3

**Suggested action:** Add unlikely_to_pay as an independent OR condition in the Stage 3 branch and verify that default_days_past_due equals 90. Add tests covering each trigger separately, including exactly 90 DPD and an unlikely-to-pay-only facility.

### CA-D2E091D62B: Discount Timing differs from declared intent

- Assertion: `METH-ECL-001`
- Category: `discounting`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** monthly_fractional

**Observed:** monthly_fractional

**Consequence:** Losses with horizons below 12 months receive no discounting, while losses at other non-integer-year horizons are discounted for too short a period, overstating their present value and expected credit loss.

**Evidence**

- `docs/methodology.md` L0163-L0175: id: METH-ECL-001; statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional
- `config/model_config.yaml` line 34: discount_timing: monthly_fractional
- `config/system_map.yaml` line 32: discount_timing:
- `docs/methodology.md` L0163-L0175: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.
- `code/credit_engine.py` L330-L344: horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `docs/methodology.md` L0163-L0175: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional

**Suggested action:** Replace whole-year floor division with the approved monthly-fractional calculation, such as months_to_cash_shortfall / 12.0 for an annual effective rate, and validate or explicitly apply config["discount_timing"]. Add tests for horizons such as 6, 12, and 18 months.

### CA-2FCD2F821B: Ead Balance Basis differs from declared intent

- Assertion: `METH-EAD-001`
- Category: `exposure_at_default`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** projected_at_default

**Observed:** projected_at_default

**Consequence:** Facilities whose principal or commitment limits reduce before expected default can have overstated EAD and expected credit loss because current supplied balances may be used instead of lower projected amounts.

**Evidence**

- `docs/methodology.md` L0135-L0147: id: METH-EAD-001; statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `config/model_config.yaml` line 29: ead_balance_basis: projected_at_default
- `config/system_map.yaml` line 27: ead_balance_basis:
- `docs/methodology.md` L0135-L0147: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `code/credit_engine.py` 321:327: def exposure_at_default(balance: float, undrawn: float, months_to_expected_default: int, config: dict[str, Any]) -> float: return balance + (config["ccf"] * undrawn)
- `code/credit_engine.py` L321-L327: def exposure_at_default(balance, undrawn, months_to_expected_default, config): ... return balance + (config["ccf"] * undrawn)

**Suggested action:** Project drawn balance and available undrawn commitment through `months_to_expected_default`, and make `ead_balance_basis` explicitly select those projected values before applying the CCF. Add a test where amortisation or limit reduction makes projected EAD differ from current-balance EAD.

### CA-1CD6720715: Lifetime Horizon Basis differs from declared intent

- Assertion: `METH-LIFE-001`
- Category: `lifetime_pd`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** remaining_contractual_maturity

**Observed:** remaining_contractual_maturity

**Consequence:** Seasoned Stage 2 loans can be evaluated over a horizon longer than their remaining contractual life, overstating cumulative probability of default and potentially distorting lifetime expected credit loss.

**Evidence**

- `docs/methodology.md` L0089-L0101: id: METH-LIFE-001; statement: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `config/model_config.yaml` line 11: lifetime_horizon_basis: remaining_contractual_maturity
- `config/system_map.yaml` line 17: lifetime_horizon_basis:
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `code/credit_engine.py` 267:275: remaining_term_months: int, ... horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.
- `code/credit_engine.py` 267:275: def lifetime_pd(... original_term_months, remaining_term_months, config ...): horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"]); years = horizon_months / 12.0
- `config/system_map.yaml` line 17: lifetime_horizon_basis: functions [lifetime_pd, calculate_facility], path code/credit_engine.py, span 267:275

**Suggested action:** Change lifetime_pd to derive horizon_months from remaining_term_months, while applying any valid horizon cap, and add a test demonstrating that a seasoned Stage 2 facility uses its remaining term rather than its original term.

### CA-D23E4BDDCF: Sicr Rule differs from declared intent

- Assertion: `METH-SICR-001`
- Category: `staging`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** relative_or_30_dpd

**Observed:** relative_or_30_dpd

**Consequence:** A non-defaulted facility meeting only one SICR indicator remains in Stage 1, delaying lifetime expected-credit-loss recognition until both indicators are met.

**Evidence**

- `docs/methodology.md` L0057-L0069: id: METH-SICR-001; statement: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.; expected: relative_or_30_dpd
- `config/model_config.yaml` line 13: sicr_rule: relative_or_30_dpd
- `config/system_map.yaml` line 7: sicr_rule:
- `docs/methodology.md` L0057-L0069: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.
- `code/credit_engine.py` L0288-L0294: relative_change = current_pd / max(origination_pd, config["pd_floor"]); if (relative_change >= config["sicr_relative_threshold"] and days_past_due >= config["sicr_days_past_due_backstop"]): return 2; return 1

**Suggested action:** Replace the conjunction with OR logic for the two SICR indicators, preserve any separately evidenced rebuttal behavior, and add tests showing that each indicator independently assigns Stage 2 for a non-defaulted facility.

## Limitations

- Assertions were extracted only from the supplied docs/methodology.md evidence; no implementation behavior was assessed.
- The assessment is limited to the supplied synthetic records. No source-system deployment logs, release approvals, committee minutes, validation report, personnel records, organisational charts, monitoring outputs, or issue-management records were available.
- The governance configuration excerpts are not dated, so their currentness and effective period cannot be independently verified.
- The methodology narrative mentions a 60-month cap for Stage 2 lifetime probability at L0087, but no corresponding fenced assertion record was supplied for extraction.
- The monitoring record is the only supplied indication that alder-2.1.0 was the production version; an authoritative deployment record was not provided.
- The public control digest supplies general context only. This review does not claim or determine formal regulatory, legal, or accounting compliance.
- The public-control digest provides general context only and does not independently prove any asserted control state or determine regulatory compliance.
- The review is limited to the supplied synthetic records; no source-system, deployment, approval-minutes, personnel, or organisational-reporting evidence was available.
- The validation results report 24 passed and zero failed tests, but also four skipped tests and zero coverage for several profiles. The supplied assertions do not permit a complete conclusion on validation coverage or model performance.
- The validation results show zero failures but also four skipped tests and zero coverage for several listed profiles; the supplied assertions do not directly ask whether validation coverage was adequate, so no separate conclusion is made on that issue.
- This is an evidence-consistency evaluation and not legal or accounting advice.
