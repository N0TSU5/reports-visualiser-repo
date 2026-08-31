# Code analysis report

**Run:** `20260831-221039_validate_credit_risk_fatigue_docs_l4`

**Case:** `challenge-case`

**Findings:** 6

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

**Consequence:** The changed alder-2.1.0 implementation lacks demonstrated version-specific approval and validation coverage. Reliance on the alder-2.0.0 evidence could leave staging and cash-flow timing changes unchallenged.

**Evidence**

- `docs/model_governance.md` L0019-L0031: id: GOV-VERSION-001; statement: The approval and independent validation evidence applies to production model version alder-2.1.0.; expected: alder-2.1.0
- `config/governance_record.yaml` line 3: approved_model_version: alder-2.0.0
- `tests/validation_results.json` model_version and release_note: "model_version": "alder-2.0.0"; "release_note": "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version: "model_version": "alder-2.1.0"
- `tests/validation_results.json` executed_at, model_version and release_note: "executed_at": "2026-02-12T16:20:00Z"; "model_version": "alder-2.0.0"; "release_note": "No rerun was recorded after the alder-2.1.0 staging and cash-flow timing change."
- `evidence/monitoring_record.json` model_version and reporting_date: "model_version": "alder-2.1.0"; "reporting_date": "2026-07-31"

**Suggested action:** Reconcile the deployed production version, approval record and validation scope. Obtain documented approval and independent validation for alder-2.1.0, including rerun coverage of the staging and cash-flow timing changes, or revert the production claim if 2.1.0 is not deployed.

### CA-2FCD2F821B: Ead Balance Basis differs from declared intent

- Assertion: `METH-EAD-001`
- Category: `exposure_at_default`
- State: `unresolved`
- Severity: 4/5
- Confidence: 98%
- Component: `config/model_config.yaml`

**Expected:** projected_at_default

**Observed:** projected_at_default

**Consequence:** Facilities whose principal balances or commitment limits reduce before expected default will have EAD—and consequently expected credit loss—calculated from unadjusted supplied amounts rather than expected-default-date exposure, potentially overstating exposure.

**Evidence**

- `docs/methodology.md` L0136-L0146: id: METH-EAD-001; statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `config/model_config.yaml` line 29: ead_balance_basis: projected_at_default
- `config/system_map.yaml` line 27: ead_balance_basis:
- `docs/methodology.md` L0136-L0146: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.; expected: projected_at_default
- `code/credit_engine.py` 825:831: def exposure_at_default(balance, undrawn, months_to_expected_default, config): ... return balance + (config["ccf"] * undrawn)

**Suggested action:** Project both drawn balance and available undrawn commitment to `months_to_expected_default` before applying the CCF, and add tests showing that EAD changes appropriately when amortisation or commitment reductions occur before default.

### CA-5089540F53: Collateral Recovery Basis differs from declared intent

- Assertion: `METH-LGD-001`
- Category: `loss_given_default`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** net_prior_liens_discounted

**Observed:** net_prior_liens_discounted

**Consequence:** Collateral recoveries can be overstated, causing LGD and downstream expected credit loss to be understated for collateralized facilities, particularly where prior liens are material or recovery periods are long.

**Evidence**

- `docs/methodology.md` L0122-L0132: id: METH-LGD-001; statement: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.; expected: net_prior_liens_discounted
- `config/model_config.yaml` line 27: collateral_recovery_basis: net_prior_liens_discounted
- `config/system_map.yaml` line 22: collateral_recovery_basis:
- `docs/methodology.md` L0122-L0132: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.
- `code/credit_engine.py` 812:822: prior_liens, recovery_months, and effective_interest_rate are accepted at lines 815-817, but lines 820-822 calculate eligible_collateral = collateral * (1.0 - config["collateral_haircut"]) and derive LGD from that value without using those parameters.
- `config/system_map.yaml` line 22: collateral_recovery_basis mapped to loss_given_default in code/credit_engine.py, span 812:822, with consequences for loss_given_default and expected_credit_loss.
- `code/credit_engine.py` 812:822: The function accepts prior_liens, recovery_months, and effective_interest_rate, but computes eligible_collateral = collateral * (1.0 - config["collateral_haircut"]), then derives unsecured_share and returns it with downturn_lgd_addon; the three recovery-basis inputs are unused.

**Suggested action:** Revise loss_given_default to deduct prior-ranking liens from recoverable collateral and discount the resulting expected recovery over recovery_months using effective_interest_rate before calculating unsecured share and LGD. Add tests covering nonzero prior liens and multi-period recoveries.

### CA-F4126F30F0: Monitoring Currentness differs from declared intent

- Assertion: `GOV-MON-001`
- Category: `monitoring_governance`
- State: `confirmed`
- Severity: 4/5
- Confidence: 99%
- Component: `docs/model_governance.md`

**Expected:** current_through_2026-07

**Observed:** No mapped implementation fact

**Consequence:** Three required monthly monitoring cycles are not evidenced, creating a risk that drift or performance deterioration between May and July 2026 was not timely detected or escalated.

**Evidence**

- `docs/model_governance.md` L0047-L0059: id: GOV-MON-001; statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.; expected: current_through_2026-07
- `evidence/monitoring_record.json` required_frequency, completed_periods and latest_completed_period: "required_frequency": "monthly"; "completed_periods": ["2026-01", "2026-02", "2026-03", "2026-04"]; "latest_completed_period": "2026-04"
- `evidence/monitoring_record.json` reporting_date, open_exception_count and status_recorded_by_owner: "reporting_date": "2026-07-31"; "open_exception_count": 0; "status_recorded_by_owner": "current"

**Suggested action:** Complete or supply monitoring evidence for May, June and July 2026, document review and escalation outcomes, and correct the owner-recorded current status and exception count if those cycles remain outstanding.

### CA-D2E091D62B: Discount Timing differs from declared intent

- Assertion: `METH-ECL-001`
- Category: `discounting`
- State: `confirmed`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** monthly_fractional

**Observed:** monthly_fractional

**Consequence:** Expected losses with cash-shortfall horizons below 12 months receive no discounting, while other non-integer-year horizons are discounted for too short a period, overstating their present value relative to the declared methodology.

**Evidence**

- `docs/methodology.md` L0164-L0174: id: METH-ECL-001; statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.; expected: monthly_fractional
- `config/model_config.yaml` line 34: discount_timing: monthly_fractional
- `config/system_map.yaml` line 32: discount_timing:
- `docs/methodology.md` L0164-L0174: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.
- `code/credit_engine.py` L834-L848: horizon_years = months_to_cash_shortfall // 12
return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
- `code/credit_engine.py` lines 842-848: if config["discount_method"] != "effective_interest_rate": ... horizon_years = months_to_cash_shortfall // 12; return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)

**Suggested action:** Replace whole-year floor division with a fractional period, such as months_to_cash_shortfall / 12.0, and explicitly validate or apply config["discount_timing"]. Add tests for horizons below 12 months and non-integer-year horizons such as 6 and 18 months.

### CA-1CD6720715: Lifetime Horizon Basis differs from declared intent

- Assertion: `METH-LIFE-001`
- Category: `lifetime_pd`
- State: `unresolved`
- Severity: 3/5
- Confidence: 99%
- Component: `config/model_config.yaml`

**Expected:** remaining_contractual_maturity

**Observed:** remaining_contractual_maturity

**Consequence:** For seasoned Stage 2 loans, the implementation can use a horizon longer than the remaining contractual life, overstating lifetime probability of default and potentially expected credit loss.

**Evidence**

- `docs/methodology.md` L0090-L0100: id: METH-LIFE-001; statement: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `config/model_config.yaml` line 11: lifetime_horizon_basis: remaining_contractual_maturity
- `config/system_map.yaml` line 17: lifetime_horizon_basis:
- `docs/methodology.md` L0090-L0100: Lifetime probability uses remaining contractual maturity rather than original term.; expected: remaining_contractual_maturity
- `code/credit_engine.py` 465:473: def lifetime_pd(... original_term_months: int, remaining_term_months: int, config: dict[str, Any]) -> float: horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])

**Suggested action:** Change lifetime_pd to derive horizon_months from remaining_term_months when lifetime_horizon_basis is remaining_contractual_maturity, and add a test for a seasoned Stage 2 facility where remaining term is shorter than original term.

## Limitations

- Assertions were extracted from the single supplied governance document; no additional source documents were provided in the case evidence.
- Assertions were extracted only from the supplied methodology document and were not assessed against any implementation or answer key.
- No approval minutes, signed validation report, validator organisational details or conflict assessment were supplied.
- No deployment or release-management record independently establishes whether or when alder-2.1.0 entered production; its use is inferred from the monitoring record.
- No deployment record was supplied to independently establish the exact production activation date of alder-2.1.0.
- No signed approval minutes or approval artefact was supplied. The approved_model_version configuration field records a value but does not prove formal approval.
- No signed validation report, validator identity, organisational chart, reporting-line evidence or conflict assessment was supplied.
- The assessment is limited to supplied synthetic excerpts and does not establish source authenticity, completeness, approval authority or operating effectiveness.
- The monitoring evidence contains no packs, reviewer sign-offs or escalation records for the completed periods, so completion quality and operating effectiveness were not assessed.
- The narrative states that remaining contractual maturity is capped at 60 months (L0087), but no separate fenced assertion record declares that cap; therefore, it is not included as a declared assertion.
- The public control digest was treated only as contextual material. No formal regulatory or accounting compliance conclusion is made.
- The public-control digest provides contextual themes only and was not treated as evidence of formal compliance or non-compliance.
- The review is limited to the supplied synthetic excerpts and does not establish the authenticity, completeness or operating effectiveness of source records.
- The validation suite reported 24 passed, 0 failed and 4 skipped tests, but several listed coverage profiles had zero cases. Validation adequacy cannot be concluded from the supplied assertions and summary.
- Validation test results show zero failures but also four skipped tests and zero coverage for several listed profiles; the assertions provided do not permit a full assessment of validation adequacy.
