# Code analysis report

**Run:** `20260831-221039_validate_credit_risk_fatigue_docs_l7`

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

**Consequence:** The supplied approval and validation evidence cannot be relied upon as version-specific control evidence for the apparent production version alder-2.1.0.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `docs/model_governance.md` L0019-L0031: The approval and independent validation evidence applies to production model version alder-2.1.0.
- `tests/validation_results.json` model_version: "model_version": "alder-2.0.0"
- `tests/validation_results.json` release_note: No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change.
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0", "reporting_date": "2026-07-31"
- `tests/validation_results.json` executed_at and model_version: "executed_at": "2026-02-12T16:20:00Z", "model_version": "alder-2.0.0"
- `tests/validation_results.json` summary and coverage_profile: "failed": 0, "skipped": 4; listed coverage-profile case counts are 0

**Suggested action:** Reconcile the authoritative production and approved-version records. If alder-2.1.0 is production, obtain and retain approval and independent validation evidence specific to that release, including assessment of the staging and cash-flow timing change, before representing the release as approved and validated.

### CA-2FCD2F821B: Ead Balance Basis differs from declared intent

- Assertion: `METH-EAD-001`
- Category: `exposure_at_default`
- State: `confirmed`
- Severity: 4/5
- Confidence: 98%
- Component: `config/model_config.yaml`

**Expected:** projected_at_default

**Observed:** projected_at_default

**Consequence:** Facilities whose principal balances or commitment limits decline before expected default will have EAD calculated from current amounts, potentially overstating exposure and expected credit loss.

**Evidence**

- `docs/methodology.md` L0135-L0147: id: METH-EAD-001; statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `config/model_config.yaml` line 29: ead_balance_basis: projected_at_default
- `config/system_map.yaml` line 27: ead_balance_basis:
- `docs/methodology.md` L0135-L0147: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `code/credit_engine.py` 2007:2013: def exposure_at_default(balance: float, undrawn: float, months_to_expected_default: int, config: dict[str, Any]) -> float: return balance + (config["ccf"] * undrawn)
- `config/system_map.yaml` line 27: ead_balance_basis maps to exposure_at_default in code/credit_engine.py at 2007:2013, affecting exposure_at_default and expected_credit_loss
- `code/credit_engine.py` 2007:2013: def exposure_at_default(balance, undrawn, months_to_expected_default, config): ... return balance + (config["ccf"] * undrawn)

**Suggested action:** Project the drawn balance and commitment limit through months_to_expected_default, derive available undrawn commitment at that date, and calculate EAD from those projected values. Add tests showing EAD changes appropriately for amortising balances and reducing limits.

### CA-5089540F53: Collateral Recovery Basis differs from declared intent

- Assertion: `METH-LGD-001`
- Category: `loss_given_default`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** net_prior_liens_discounted

**Observed:** net_prior_liens_discounted

**Consequence:** Collateral subject to prior-ranking claims or delayed recovery can be overstated, causing unsecured exposure, LGD, and downstream expected credit loss to be understated.

**Evidence**

- `docs/methodology.md` L0121-L0133: id: METH-LGD-001; statement: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.; expected: net_prior_liens_discounted
- `config/model_config.yaml` line 27: collateral_recovery_basis: net_prior_liens_discounted
- `config/system_map.yaml` line 22: collateral_recovery_basis:
- `docs/methodology.md` L0121-L0133: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.
- `code/credit_engine.py` 1678:1688: def loss_given_default(balance, collateral, prior_liens, recovery_months, effective_interest_rate, config): ... eligible_collateral = collateral * (1.0 - config["collateral_haircut"]); unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0); return min(1.0, unsecured_share + config["downturn_lgd_addon"])
- `code/credit_engine.py` 1678:1688: loss_given_default accepts prior_liens, recovery_months, and effective_interest_rate, but computes eligible_collateral only as collateral * (1.0 - collateral_haircut), then returns unsecured_share + downturn_lgd_addon without using those inputs.

**Suggested action:** Revise loss_given_default to deduct prior-ranking liens from eligible collateral and discount the resulting net recovery using the expected recovery period and effective interest rate before calculating the unsecured share and LGD. Add tests covering nonzero liens and delayed recoveries.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three required monthly monitoring cycles are not evidenced, potentially delaying detection and escalation of drift or performance deterioration.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07
- `docs/model_governance.md` L0047-L0059: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.
- `evidence/monitoring_record.json` completed_periods: "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]
- `evidence/monitoring_record.json` latest_completed_period: "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` reporting_date, required_frequency, and status_recorded_by_owner: "reporting_date": "2026-07-31", "required_frequency": "monthly", "status_recorded_by_owner": "current"
- `evidence/monitoring_record.json` required_frequency and completed_periods: "required_frequency": "monthly", "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]
- `evidence/monitoring_record.json` reporting_date, open_exception_count, and status_recorded_by_owner: "reporting_date": "2026-07-31", "open_exception_count": 0, "status_recorded_by_owner": "current"

**Suggested action:** Complete or provide the May, June, and July 2026 monitoring records, investigate why the status was recorded as current, document any monitoring exceptions, and correct the governance status to reflect the actual latest completed period.

### CA-75B675DD6F: Default Rule differs from declared intent

- Assertion: `METH-DEFAULT-001`
- Category: `default_definition`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** default_flag_or_utp_or_90_dpd

**Observed:** default_flag_or_utp_or_90_dpd

**Consequence:** An SME facility that is unlikely to pay but has no default flag and is below the default days-past-due threshold will not be assigned Stage 3. It may instead receive Stage 1 or Stage 2 treatment, affecting the applicable PD/loss horizon and expected credit loss. The packet does not quantify the number of affected facilities or aggregate ECL impact.

**Evidence**

- `docs/methodology.md` L0071-L0083: id: METH-DEFAULT-001; statement: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.; expected: default_flag_or_utp_or_90_dpd
- `config/model_config.yaml` line 16: default_rule: default_flag_or_utp_or_90_dpd
- `config/system_map.yaml` line 12: default_rule:
- `docs/methodology.md` L0071-L0083: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.
- `code/credit_engine.py` 1332:1348: def determine_stage(... unlikely_to_pay: bool, ...):
    if default_flag or days_past_due >= config["default_days_past_due"]:
        return 3
    ...
    return 1

**Suggested action:** Amend the Stage 3 condition to include unlikely_to_pay using OR logic. Add focused tests proving that each route independently produces Stage 3, that 90 days is inclusive, and that Stage 3 overrides SICR and performing-stage outcomes. Assess affected facilities and any staging, PD-horizon, ECL, monitoring, or governance remediation after correction.

### CA-D2E091D62B: Discount Timing differs from declared intent

- Assertion: `METH-ECL-001`
- Category: `discounting`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** monthly_fractional

**Observed:** monthly_fractional

**Consequence:** Losses with horizons below 12 months receive no discount, while horizons not divisible by 12 are discounted only through the last completed year. For example, 18 months is treated as one year rather than 1.5 years, overstating the present value of expected credit loss relative to the declared methodology.

**Evidence**

- `docs/methodology.md` L0163-L0175: id: METH-ECL-001; statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional
- `config/model_config.yaml` line 34: discount_timing: monthly_fractional
- `config/system_map.yaml` line 32: discount_timing:
- `docs/methodology.md` L0163-L0175: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.
- `code/credit_engine.py` 2332:2346: horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `docs/methodology.md` L0163-L0175: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional
- `code/credit_engine.py` 2332:2346: horizon_years = months_to_cash_shortfall // 12; return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `config/system_map.yaml` line 32: discount_timing: path code/credit_engine.py; span 2332:2346; functions [expected_credit_loss]; consequences [present_value, expected_credit_loss]

**Suggested action:** Replace whole-year floor division with fractional timing, such as `horizon_years = months_to_cash_shortfall / 12.0`, and validate or honor the configured `discount_timing`. Add tests for horizons below 12 months, non-multiples of 12 such as 18 months, and exact whole years.

### CA-1CD6720715: Lifetime Horizon Basis differs from declared intent

- Assertion: `METH-LIFE-001`
- Category: `lifetime_pd`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** remaining_contractual_maturity

**Observed:** remaining_contractual_maturity

**Consequence:** Seasoned Stage 2 facilities can receive a horizon longer than their remaining contractual life, overstating cumulative lifetime probability and potentially distorting expected credit loss.

**Evidence**

- `docs/methodology.md` L0089-L0101: id: METH-LIFE-001; statement: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `config/model_config.yaml` line 11: lifetime_horizon_basis: remaining_contractual_maturity
- `config/system_map.yaml` line 17: lifetime_horizon_basis:
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `code/credit_engine.py` 1005:1013: def lifetime_pd(annual_pd, original_term_months, remaining_term_months, config): ... horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
- `docs/methodology.md` L0089-L0101: Lifetime probability uses remaining contractual maturity rather than original term.
- `code/credit_engine.py` 1005:1013: def lifetime_pd(... original_term_months, remaining_term_months, config ...): horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])

**Suggested action:** Change lifetime_pd to derive horizon_months from remaining_term_months, applying any approved cap afterward, and add a regression test using a seasoned facility where remaining term is materially shorter than original term.

### CA-D23E4BDDCF: Sicr Rule differs from declared intent

- Assertion: `METH-SICR-001`
- Category: `staging`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** relative_or_30_dpd

**Observed:** relative_or_30_dpd

**Consequence:** A non-defaulted facility meeting only the relative probability increase criterion or only the 30-days-past-due criterion remains in Stage 1, delaying lifetime expected-credit-loss recognition and potentially understating the loss allowance.

**Evidence**

- `docs/methodology.md` L0057-L0069: id: METH-SICR-001; statement: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.; expected: relative_or_30_dpd
- `config/model_config.yaml` line 13: sicr_rule: relative_or_30_dpd
- `config/system_map.yaml` line 7: sicr_rule:
- `docs/methodology.md` L0057-L0069: statement: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.; expected: relative_or_30_dpd
- `code/credit_engine.py` 1332:1348: if (relative_change >= config["sicr_relative_threshold"] and days_past_due >= config["sicr_days_past_due_backstop"]): return 2

**Suggested action:** Replace the `and` conjunction with `or` for the two SICR indicators, while preserving Stage 3 precedence. Add tests proving that each criterion independently triggers Stage 2 and that any permitted rebuttal is separately and explicitly applied.

## Limitations

- Assertions were extracted only from the supplied docs/methodology.md evidence.
- Missing monitoring periods may represent non-performance or missing documentation; the supplied evidence does not distinguish between them.
- No approval minutes, release authorization, change assessment, signed validation report, validator identity, organizational chart, or conflicts assessment was supplied.
- No implementation assessment, defect inference, or validation against other sources was performed.
- Only a validation summary was available. The reasons for four skipped tests and zero coverage across listed scenarios were not provided.
- The assessment is limited to the supplied synthetic records; no source-system, approval minutes, signed validation report, organizational chart, or complete monitoring outputs were available.
- The evidence does not independently establish that alder-2.1.0 was deployed to production, although the July monitoring record identifies it as the monitored model version.
- The governance record has no supplied effective date, limiting assessment of whether ownership and configuration values were current on 31 July 2026.
- The monitoring record identifies alder-2.1.0 but does not independently establish its production deployment date or status.
- The public-control digest is contextual only. No conclusion on formal regulatory, legal, or accounting compliance is made.
- The public-control digest was used only as contextual material and not as evidence that any control complies with legal, regulatory, or accounting requirements.
- The review is limited to the supplied synthetic JSON and embedded file excerpts; underlying files, source systems, signatures, metadata, and audit trails were not independently accessed.
- The validation test summary does not identify the validating party or demonstrate organizational independence.
- This is an evaluation exercise and not legal or accounting advice.
