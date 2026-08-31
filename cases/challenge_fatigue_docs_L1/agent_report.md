# Code analysis report

**Run:** `20260831-215112_validate_credit_risk_fatigue_docs_l1`

**Case:** `challenge-case`

**Findings:** 9

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

**Consequence:** The current production release lacks demonstrated version-specific approval and validation coverage, so reliance on the earlier evidence may leave changes in alder-2.1.0 unchallenged.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `tests/validation_results.json` model_version and release_note: "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version: "model_version": "alder-2.1.0"
- `docs/model_governance.md` L0019-L0031: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `tests/validation_results.json` executed_at, model_version and release_note: Executed 2026-02-12; "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0"; "reporting_date": "2026-07-31"

**Suggested action:** Obtain and record formal approval and independent validation for alder-2.1.0, including testing of the staging and cash-flow timing changes, or reconcile the production version if alder-2.1.0 was recorded incorrectly.

### CA-D2E091D62B: Discount Timing differs from declared intent

- Assertion: `METH-ECL-001`
- Category: `discounting`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** monthly_fractional

**Observed:** monthly_fractional

**Consequence:** Losses with horizons below 12 months receive no discounting, while losses at other non-integer-year horizons are under-discounted; for example, an 18-month shortfall is discounted for only one year instead of 1.5 years, overstating present-value ECL.

**Evidence**

- `docs/methodology.md` L0163-L0175: id: METH-ECL-001; statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional
- `config/model_config.yaml` line 34: discount_timing: monthly_fractional
- `config/system_map.yaml` line 32: discount_timing:
- `docs/methodology.md` L0163-L0175: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.
- `code/credit_engine.py` L245-L246: horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `config/system_map.yaml` line 32: discount_timing: ... functions:["expected_credit_loss"], path:"code/credit_engine.py", span:"232:246"
- `code/credit_engine.py` lines 245-246: horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)

**Suggested action:** Replace whole-year floor division with a fractional exponent such as `months_to_cash_shortfall / 12.0`, honor or validate the configured timing convention, and add tests for short and non-integer-year horizons such as 1, 6, and 18 months.

### CA-5089540F53: Collateral Recovery Basis differs from declared intent

- Assertion: `METH-LGD-001`
- Category: `loss_given_default`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** net_prior_liens_discounted

**Observed:** net_prior_liens_discounted

**Consequence:** Collateral recoveries can be overstated, causing LGD and downstream expected credit loss to be understated for facilities with prior-ranking liens or delayed recoveries.

**Evidence**

- `docs/methodology.md` L0121-L0133: id: METH-LGD-001; statement: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.; expected: net_prior_liens_discounted
- `config/model_config.yaml` line 27: collateral_recovery_basis: net_prior_liens_discounted
- `config/system_map.yaml` line 22: collateral_recovery_basis:
- `docs/methodology.md` L0121-L0133: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.
- `code/credit_engine.py` 210:220: prior_liens, recovery_months, and effective_interest_rate are function inputs, but eligible_collateral = collateral * (1.0 - config["collateral_haircut"]); LGD is then returned from the resulting unsecured_share plus downturn_lgd_addon.
- `code/credit_engine.py` 210:220: eligible_collateral = collateral * (1.0 - config["collateral_haircut"]); unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0); return min(1.0, unsecured_share + config["downturn_lgd_addon"])

**Suggested action:** Before calculating the unsecured share, subtract prior-ranking liens from eligible collateral and discount the resulting expected recovery over recovery_months using effective_interest_rate. Add tests demonstrating that LGD increases when prior liens or the recovery period increase.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three expected monthly monitoring cycles are not evidenced, potentially delaying detection and escalation of model drift or performance deterioration. The recorded current status and zero open exceptions are unreliable without reconciliation.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07
- `evidence/monitoring_record.json` required_frequency, completed_periods and latest_completed_period: "required_frequency": "monthly"; completed periods are 2026-01 through 2026-04; "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` reporting_date, open_exception_count and status_recorded_by_owner: "reporting_date": "2026-07-31"; "open_exception_count": 0; "status_recorded_by_owner": "current"
- `docs/model_governance.md` L0047-L0059: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.

**Suggested action:** Complete or provide monitoring evidence for May through July 2026, assess whether exceptions should have been opened, and correct the owner-recorded current status until the gap is resolved.

### CA-D23E4BDDCF: Sicr Rule differs from declared intent

- Assertion: `METH-SICR-001`
- Category: `staging`
- State: `unresolved`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** relative_or_30_dpd

**Observed:** relative_or_30_dpd

**Consequence:** A non-defaulted facility meeting only one SICR indicator remains in Stage 1, delaying recognition of lifetime expected credit losses and potentially understating the loss allowance.

**Evidence**

- `docs/methodology.md` L0057-L0069: id: METH-SICR-001; statement: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.; expected: relative_or_30_dpd
- `config/model_config.yaml` line 13: sicr_rule: relative_or_30_dpd
- `config/system_map.yaml` line 7: sicr_rule:
- `docs/methodology.md` L0057-L0069: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.
- `code/credit_engine.py` 180:196: if (relative_change >= config["sicr_relative_threshold"] and days_past_due >= config["sicr_days_past_due_backstop"]): return 2; return 1

**Suggested action:** Change the Stage 2 condition from `and` to `or`, implement or explicitly map any approved rebuttal mechanism, and add tests for relative-threshold-only, 30-DPD-only, both-indicators, neither-indicator, rebuttal, and default cases.

### CA-75B675DD6F: Default Rule differs from declared intent

- Assertion: `METH-DEFAULT-001`
- Category: `default_definition`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** default_flag_or_utp_or_90_dpd

**Observed:** default_flag_or_utp_or_90_dpd

**Consequence:** An SME facility marked unlikely to pay, but without a default flag or 90 days past due, will remain in Stage 1 or may enter Stage 2 rather than Stage 3, potentially understating expected credit loss.

**Evidence**

- `docs/methodology.md` L0071-L0083: id: METH-DEFAULT-001; statement: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.; expected: default_flag_or_utp_or_90_dpd
- `config/model_config.yaml` line 16: default_rule: default_flag_or_utp_or_90_dpd
- `config/system_map.yaml` line 12: default_rule:
- `docs/methodology.md` L0071-L0083: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.
- `code/credit_engine.py` 180:196: 185:     unlikely_to_pay: bool,
188:     if default_flag or days_past_due >= config["default_days_past_due"]:
189:         return 3
- `code/credit_engine.py` 180:196: unlikely_to_pay is accepted at line 185, but the Stage 3 condition at line 188 is: if default_flag or days_past_due >= config["default_days_past_due"]: return 3. No unlikely_to_pay condition is present.
- `config/system_map.yaml` line 12: default_rule is mapped to determine_stage in code/credit_engine.py, span 180:196, with consequences for stage_3_assignment, probability_of_default, and expected_credit_loss.

**Suggested action:** Include `unlikely_to_pay` as an independent condition in the Stage 3 branch, and add tests showing that each of the three triggers alone results in Stage 3.

### CA-2FCD2F821B: Ead Balance Basis differs from declared intent

- Assertion: `METH-EAD-001`
- Category: `exposure_at_default`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** projected_at_default

**Observed:** projected_at_default

**Consequence:** Where principal balances or commitment limits decline before expected default, EAD—and consequently expected credit loss—can be overstated by using unadjusted current balance and undrawn amounts.

**Evidence**

- `docs/methodology.md` L0135-L0147: id: METH-EAD-001; statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `config/model_config.yaml` line 29: ead_balance_basis: projected_at_default
- `config/system_map.yaml` line 27: ead_balance_basis:
- `docs/methodology.md` L0135-L0147: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `code/credit_engine.py` 223:229: def exposure_at_default(balance: float, undrawn: float, months_to_expected_default: int, config: dict[str, Any]) -> float: return balance + (config["ccf"] * undrawn)
- `docs/methodology.md` L0135-L0147: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.
- `config/system_map.yaml` line 27: ead_balance_basis maps to exposure_at_default in code/credit_engine.py span 223:229, with consequences for exposure_at_default and expected_credit_loss.
- `code/credit_engine.py` 223:229: def exposure_at_default(balance, undrawn, months_to_expected_default, config): ... return balance + (config["ccf"] * undrawn)

**Suggested action:** Project the drawn balance and available undrawn commitment through `months_to_expected_default`, applying scheduled principal and commitment-limit reductions, before calculating EAD. Add tests demonstrating that EAD changes with the expected-default date for amortising facilities.

### CA-1CD6720715: Lifetime Horizon Basis differs from declared intent

- Assertion: `METH-LIFE-001`
- Category: `lifetime_pd`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** remaining_contractual_maturity

**Observed:** remaining_contractual_maturity

**Consequence:** For seasoned Stage 2 loans whose remaining maturity is shorter than their original term or the horizon cap, lifetime PD is calculated over an excessive horizon, potentially overstating expected credit loss.

**Evidence**

- `docs/methodology.md` L0089-L0101: id: METH-LIFE-001; statement: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `config/model_config.yaml` line 11: lifetime_horizon_basis: remaining_contractual_maturity
- `config/system_map.yaml` line 17: lifetime_horizon_basis:
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `code/credit_engine.py` 169:177: remaining_term_months: int, ... horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.
- `code/credit_engine.py` 169:177: def lifetime_pd(... original_term_months, remaining_term_months, config ...): horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])

**Suggested action:** Change lifetime_pd to derive horizon_months from remaining_term_months when lifetime_horizon_basis is remaining_contractual_maturity, apply any valid cap afterward, and add a seasoned-loan test where original and remaining terms differ.

### CA-007CD117F3: Pd Floor Application differs from declared intent

- Assertion: `METH-PD-001`
- Category: `pd_calibration`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** post_scenario

**Observed:** post_scenario

**Consequence:** Upside or other downward scenario shifts can generate final PDs below the approved 0.5 percent lower bound, causing affected scenario expected credit losses to be understated.

**Evidence**

- `docs/methodology.md` L0011-L0023: id: METH-PD-001; statement: The 0.5 percent probability floor is applied after forward-looking scenario adjustments.; expected: post_scenario
- `config/model_config.yaml` line 4: pd_floor_application: post_scenario
- `config/system_map.yaml` line 2: pd_floor_application:
- `docs/methodology.md` L0011-L0023: The 0.5 percent probability floor is applied after forward-looking scenario adjustments.
- `code/credit_engine.py` 146-156: raw_pd = 1.0 / (1.0 + math.exp(-logit)); return min(config["pd_cap"], max(config["pd_floor"], raw_pd))
- `code/credit_engine.py` 199-207: scenario_pds computes scenario-shifted probabilities and returns them directly without applying config["pd_floor"].
- `code/credit_engine.py` 169-177: lifetime_pd derives cumulative PD from annual_pd and returns it without any explicit post-scenario floor.

**Suggested action:** Apply the configured 0.5 percent floor to each probability after its scenario adjustment, before the result is used for grade assignment, lifetime derivation, or expected credit loss. Add tests with a base PD near the floor and a negative scenario shift to verify that final one-year and lifetime scenario probabilities do not breach the approved bound.

## Limitations

- Assertions were extracted from a single supplied methodology document.
- No production deployment record, approval minutes, change approval, full validation report, validator identity, organisational chart, monitoring reports, or exception workflow was supplied.
- No underlying approval minutes, validation report, validator identity, organisational chart, monitoring reports, or production deployment record was supplied.
- The assessment is limited to the supplied synthetic records and does not determine formal regulatory, legal, or accounting compliance.
- The governance configuration excerpts do not show effective dates, approvers, record version, or change history, limiting assessment of currentness and authority.
- The monitoring record identifies alder-2.1.0 but does not independently prove that this was the deployed production version.
- The narrative mentions a 60-month cap on remaining contractual maturity at L0087, but no separately identified fenced assertion for that cap was supplied.
- The public-control digest supplies general context only and was not treated as proof that any specific control operated effectively.
- The public-control digest was treated only as contextual material, not as evidence that any control operated effectively or that any regulatory expectation was satisfied.
- The review is limited to the supplied synthetic records and does not establish formal regulatory, legal, or accounting compliance.
- The severity scale is not defined in the evidence; ratings use a relative 1-to-5 scale, with 5 treated as most severe.
- The severity scale was not defined in the evidence; ratings use a relative 1-to-5 scale, where 5 is most severe.
- The validation evidence reports four skipped tests and zero cases in several coverage categories, but the reasons and materiality of those gaps are not supplied.
- This extraction records declared requirements only; it does not assess implementation, test results, compliance or defects.
