# Code analysis report

**Run:** `20260831-220716_validate_credit_risk_fatigue_docs_l3`

**Case:** `challenge-case`

**Findings:** 8

This report concerns a synthetic evaluation case. It does not determine formal regulatory compliance.

## Findings

### CA-5089540F53: Collateral Recovery Basis differs from declared intent

- Assertion: `METH-LGD-001`
- Category: `loss_given_default`
- State: `confirmed`
- Severity: 5/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** net_prior_liens_discounted

**Observed:** net_prior_liens_discounted

**Consequence:** Collateral recoveries may be overstated, causing LGD and downstream expected credit loss to be understated, especially for collateral subject to senior liens or long recovery periods.

**Evidence**

- `docs/methodology.md` L0122-L0132: id: METH-LGD-001; statement: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.; expected: net_prior_liens_discounted
- `config/model_config.yaml` line 27: collateral_recovery_basis: net_prior_liens_discounted
- `config/system_map.yaml` line 22: collateral_recovery_basis:
- `docs/methodology.md` L0122-L0132: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.
- `code/credit_engine.py` 511:521: eligible_collateral = collateral * (1.0 - config["collateral_haircut"]); unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0); return min(1.0, unsecured_share + config["downturn_lgd_addon"])
- `code/credit_engine.py` 511:521: def loss_given_default(... prior_liens, recovery_months, effective_interest_rate, ...): eligible_collateral = collateral * (1.0 - config["collateral_haircut"]); unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0); return min(1.0, unsecured_share + config["downturn_lgd_addon"])
- `config/system_map.yaml` line 22: collateral_recovery_basis mapped to loss_given_default in code/credit_engine.py, span 511:521, with consequences for loss_given_default and expected_credit_loss.

**Suggested action:** Revise loss_given_default to subtract prior-ranking liens from eligible collateral, floor the result appropriately, discount the net recovery using the effective interest rate over recovery_months, and use that discounted recovery in the LGD calculation. Add tests covering nonzero prior liens and multi-period recoveries.

### CA-352DEC65DC: Approved Model Version differs from declared intent

- Assertion: `GOV-VERSION-001`
- Category: `model_change_governance`
- State: `confirmed`
- Severity: 5/5
- Confidence: 99%
- Component: `config/governance_record.yaml`

**Expected:** alder-2.1.0

**Observed:** alder-2.0.0

**Consequence:** The production release alder-2.1.0 lacks demonstrated version-specific approval and validation, so reliance on the alder-2.0.0 evidence would leave the changed implementation outside the evidenced control state.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0; unit: model version
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `tests/validation_results.json` model_version and release_note: "model_version": "alder-2.0.0"; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"
- `tests/validation_results.json` executed_at, model_version, summary, and release_note: "executed_at": "2026-02-12T16:20:00Z"; "model_version": "alder-2.0.0"; "skipped": 4; "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."

**Suggested action:** Obtain and record approval for alder-2.1.0 and perform version-specific independent validation addressing the staging and cash-flow timing changes before treating the release as fully approved and validated. Reconcile the approved-version field afterward.

### CA-2FCD2F821B: Ead Balance Basis differs from declared intent

- Assertion: `METH-EAD-001`
- Category: `exposure_at_default`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** projected_at_default

**Observed:** projected_at_default

**Consequence:** Facilities whose principal balances or available limits decline before expected default will have EAD calculated from unadjusted inputs, potentially overstating EAD and expected credit loss.

**Evidence**

- `docs/methodology.md` L0136-L0146: id: METH-EAD-001; statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `config/model_config.yaml` line 29: ead_balance_basis: projected_at_default
- `config/system_map.yaml` line 27: ead_balance_basis:
- `docs/methodology.md` L0136-L0146: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `code/credit_engine.py` 524:530: def exposure_at_default(balance: float, undrawn: float, months_to_expected_default: int, config: dict[str, Any]) -> float: return balance + (config["ccf"] * undrawn)
- `docs/methodology.md` L0136-L0146: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.
- `config/system_map.yaml` line 27: ead_balance_basis maps to exposure_at_default in code/credit_engine.py, span 524:530, with consequences for exposure_at_default and expected_credit_loss.
- `code/credit_engine.py` 524:530: def exposure_at_default(balance, undrawn, months_to_expected_default, config): return balance + (config["ccf"] * undrawn)

**Suggested action:** Implement expected-default-date projection for both drawn balance and available undrawn commitment using `months_to_expected_default`, and ensure `ead_balance_basis` selects that behavior. Add tests where amortisation and limit reductions make projected EAD differ from current-balance EAD.

### CA-1CD6720715: Lifetime Horizon Basis differs from declared intent

- Assertion: `METH-LIFE-001`
- Category: `lifetime_pd`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** remaining_contractual_maturity

**Observed:** remaining_contractual_maturity

**Consequence:** Seasoned Stage 2 facilities can receive a probability horizon based on their original term instead of their shorter remaining life, overstating cumulative lifetime PD and potentially expected credit loss.

**Evidence**

- `docs/methodology.md` L0090-L0100: id: METH-LIFE-001; statement: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `config/model_config.yaml` line 11: lifetime_horizon_basis: remaining_contractual_maturity
- `config/system_map.yaml` line 17: lifetime_horizon_basis:
- `docs/methodology.md` L0090-L0100: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `code/credit_engine.py` 352:359: def lifetime_pd(... original_term_months: int, remaining_term_months: int, config: dict[str, Any]) -> float:
    horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
- `code/credit_engine.py` 418:419: years = horizon_months / 12.0
return min(1.0, 1.0 - ((1.0 - annual_pd) ** years))
- `docs/methodology.md` L0090-L0100: Lifetime probability uses remaining contractual maturity rather than original term.
- `code/credit_engine.py` 352:359: def lifetime_pd(annual_pd, original_term_months, remaining_term_months, config): ... horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
- `code/credit_engine.py` 418:419: years = horizon_months / 12.0; return min(1.0, 1.0 - ((1.0 - annual_pd) ** years))

**Suggested action:** Derive horizon_months from remaining_term_months when lifetime_horizon_basis is remaining_contractual_maturity, retaining any applicable cap. Add regression tests comparing otherwise identical new and seasoned Stage 2 facilities to verify that lifetime PD decreases with remaining life and never reuses original term.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three required monthly monitoring cycles are not evidenced, potentially delaying detection and escalation of drift or performance deterioration. The zero exception count does not resolve the missing cycles because exceptions cannot be inferred for monitoring that was not shown as completed.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07; unit: control state
- `evidence/monitoring_record.json` required_frequency, completed_periods, latest_completed_period, and status_recorded_by_owner: "required_frequency": "monthly"; "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]; "latest_completed_period": "2026-04"; "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"
- `evidence/monitoring_record.json` reporting_date, required_frequency, completed_periods, and latest_completed_period: "reporting_date": "2026-07-31"; "required_frequency": "monthly"; "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]; "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` open_exception_count and status_recorded_by_owner: "open_exception_count": 0; "status_recorded_by_owner": "current"

**Suggested action:** Complete or provide the May, June, and July 2026 monitoring records, document any approved exceptions or delays, and correct the owner-recorded status so it agrees with the dated monitoring evidence.

### CA-75B675DD6F: Default Rule differs from declared intent

- Assertion: `METH-DEFAULT-001`
- Category: `default_definition`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** default_flag_or_utp_or_90_dpd

**Observed:** default_flag_or_utp_or_90_dpd

**Consequence:** An SME facility marked unlikely to pay can remain in Stage 1 or Stage 2 when it has no default flag and is below the past-due threshold, potentially understating credit impairment and expected credit loss.

**Evidence**

- `docs/methodology.md` L0072-L0082: id: METH-DEFAULT-001; statement: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.; expected: default_flag_or_utp_or_90_dpd
- `config/model_config.yaml` line 16: default_rule: default_flag_or_utp_or_90_dpd
- `config/system_map.yaml` line 12: default_rule:
- `docs/methodology.md` L0072-L0082: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.
- `code/credit_engine.py` 481:497: if default_flag or days_past_due >= config["default_days_past_due"]:
    return 3
...
return 1

**Suggested action:** Include unlikely_to_pay in the initial Stage 3 condition, for example `if default_flag or unlikely_to_pay or days_past_due >= config["default_days_past_due"]:`, and add a test where unlikely_to_pay is true while default_flag is false and days_past_due is below 90.

### CA-D2E091D62B: Discount Timing differs from declared intent

- Assertion: `METH-ECL-001`
- Category: `discounting`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** monthly_fractional

**Observed:** monthly_fractional

**Consequence:** Losses with horizons below 12 months receive no discounting, while losses at other non-integer-year horizons are under-discounted, causing their present value and reported ECL to be overstated.

**Evidence**

- `docs/methodology.md` L0164-L0174: id: METH-ECL-001; statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional
- `config/model_config.yaml` line 34: discount_timing: monthly_fractional
- `config/system_map.yaml` line 32: discount_timing:
- `docs/methodology.md` L0164-L0174: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.
- `code/credit_engine.py` lines 546-547: horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `config/system_map.yaml` line 32: discount_timing: functions: [expected_credit_loss], path: code/credit_engine.py, span: 533:547, consequences: [present_value, expected_credit_loss]

**Suggested action:** Replace whole-year floor division with a fractional-year exponent such as `months_to_cash_shortfall / 12.0`, enforce the configured timing convention, and add tests for horizons below one year and non-integer years, such as 6 and 18 months.

### CA-D23E4BDDCF: Sicr Rule differs from declared intent

- Assertion: `METH-SICR-001`
- Category: `staging`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** relative_or_30_dpd

**Observed:** relative_or_30_dpd

**Consequence:** A non-defaulted facility meeting only one SICR indicator remains in Stage 1, delaying recognition of lifetime expected credit losses until both indicators are met or default occurs.

**Evidence**

- `docs/methodology.md` L0058-L0068: id: METH-SICR-001; statement: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.; expected: relative_or_30_dpd
- `config/model_config.yaml` line 13: sicr_rule: relative_or_30_dpd
- `config/system_map.yaml` line 7: sicr_rule:
- `docs/methodology.md` L0058-L0068: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.
- `code/credit_engine.py` L489-L497: if default_flag or days_past_due >= config["default_days_past_due"]: return 3; ... if (relative_change >= config["sicr_relative_threshold"] and days_past_due >= config["sicr_days_past_due_backstop"]): return 2; return 1

**Suggested action:** Replace the Stage 2 conjunction with OR logic, preserving Stage 3 precedence and any separately implemented, evidenced rebuttal mechanism. Add tests showing that each SICR indicator independently triggers Stage 2 and that rebuttal behavior is applied only where authorized.

## Limitations

- Assertions are declarations extracted from the supplied governance record; no external corroboration or implementation assessment was performed.
- Assertions were extracted only from the explicitly fenced assertion records in docs/methodology.md.
- No implementation assessment, defect inference, or answer-key inspection was performed.
- No underlying approval minutes, model inventory history, deployment evidence, validation report, validator organizational information, test specifications, acceptance criteria, or monthly monitoring packages were supplied.
- No underlying approval minutes, model inventory, deployment record, validation report, validator organizational chart, or monthly monitoring reports were supplied.
- Severity uses a five-point review scale, with 5 representing the highest potential governance impact.
- The assessment is limited to the supplied synthetic packets, mapped configuration facts, monitoring record, validation results, and public-control digest.
- The governance configuration extracts do not show effective dates, approvers, record provenance, or change history.
- The monitoring record establishes that it is labelled alder-2.1.0 but does not independently prove that alder-2.1.0 was the deployed production version.
- The public-control digest provides contextual themes only and was not treated as evidence of formal compliance.
- The public-control digest was treated as contextual material only. No formal regulatory, legal, or accounting compliance conclusion is made.
- The review is limited to the supplied synthetic packets, mapped facts, monitoring record, validation results, and public-control digest.
- The significance of the four skipped validation tests and zero-case coverage categories cannot be determined from the supplied summary alone.
