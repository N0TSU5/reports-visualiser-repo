# Alder Credit Engine methodology

## Scope

Alder 2.1 estimates credit risk for UK SME term loans. It combines borrower risk drivers, sector calibration, impairment staging, forward-looking scenarios, recovery assumptions and expected cash-flow timing to calculate a facility-level expected credit loss.

## Probability and input controls

Required inputs are rejected when absent. The approved probability floor and cap apply to the final scenario-adjusted probability used by grades and expected-loss calculations.

```assertion
id: METH-PD-001
concept: pd_floor_application
category: pd_calibration
statement: The 0.5 percent probability floor is applied after forward-looking scenario adjustments.
expected: post_scenario
value_type: text
unit: sequencing rule
scope: all non-defaulted facility scenario probabilities
horizon: one year and lifetime
materiality: Applying the floor before an upside adjustment can produce final probabilities below the approved lower bound and understate expected loss.
extraction_confidence: 0.99
```

```assertion
id: METH-DATA-001
concept: missing_input_policy
category: input_control
statement: A facility with any missing required risk or recovery input is rejected from calculation.
expected: reject
value_type: text
unit: policy
scope: required model inputs
horizon: reporting date
materiality: Completing absent drivers with benign values can bias risk and recovery estimates.
extraction_confidence: 0.99
```

## Grade, staging and default

Grades use inclusive upper boundaries. Stage 2 is triggered by either a doubling of lifetime default risk since origination or the 30-days-past-due backstop, unless a documented rebuttal applies. Stage 3 takes precedence when the default flag, an unlikely-to-pay indicator or the 90-days-past-due backstop is present.

```assertion
id: METH-GRADE-001
concept: grade_boundary
category: grade_assignment
statement: The upper probability boundary for each grade is inclusive.
expected: inclusive
value_type: text
unit: comparison
scope: grade assignment
horizon: one year
materiality: A strict boundary moves facilities at an approved cut-off into a worse grade.
extraction_confidence: 0.99
```

```assertion
id: METH-SICR-001
concept: sicr_rule
category: staging
statement: A relative probability increase of at least two or 30 days past due triggers Stage 2, subject to any separately evidenced rebuttal.
expected: relative_or_30_dpd
value_type: text
unit: decision rule
scope: non-defaulted facilities
horizon: since origination
materiality: Requiring both indicators delays lifetime expected-loss recognition for facilities that meet only one significant-increase criterion.
extraction_confidence: 0.99
```

```assertion
id: METH-DEFAULT-001
concept: default_rule
category: default_definition
statement: A default flag, an unlikely-to-pay indicator or at least 90 days past due causes Stage 3 treatment.
expected: default_flag_or_utp_or_90_dpd
value_type: text
unit: decision rule
scope: all SME facilities
horizon: reporting date
materiality: Omitting an unlikely-to-pay route can leave a credit-impaired facility in a performing stage.
extraction_confidence: 0.99
```

## Lifetime risk and scenarios

Stage 2 lifetime probability uses each facility's remaining contractual maturity, capped at 60 months. Baseline, upside and downside scenarios apply log-odds shifts and retain weights of 60 percent, 10 percent and 30 percent.

```assertion
id: METH-LIFE-001
concept: lifetime_horizon_basis
category: lifetime_pd
statement: Lifetime probability uses remaining contractual maturity rather than original term.
expected: remaining_contractual_maturity
value_type: text
unit: horizon basis
scope: Stage 2 facilities
horizon: remaining life
materiality: Reusing original term overstates the horizon for seasoned loans and can distort lifetime expected loss.
extraction_confidence: 0.99
```

```assertion
id: METH-SCEN-001
concept: scenario_weights
category: scenario_weighting
statement: Baseline, upside and downside weights are 60 percent, 10 percent and 30 percent respectively.
expected: '{"baseline":0.6,"downside":0.3,"upside":0.1}'
value_type: mapping
unit: probability weights
scope: all expected-loss calculations
horizon: reporting date
materiality: Incorrect weights distort the probability-weighted loss estimate.
extraction_confidence: 0.99
```

## Recovery, exposure and discounting

Collateral recoveries are reduced for prior-ranking liens, receive the approved haircut and are discounted over the expected recovery period. Exposure at default uses scheduled balance and limit reductions up to the expected default date. Expected losses are discounted at monthly fractional timing with the effective interest rate.

```assertion
id: METH-LGD-001
concept: collateral_recovery_basis
category: loss_given_default
statement: Collateral recovery is net of prior-ranking liens and discounted over the expected recovery period before LGD is calculated.
expected: net_prior_liens_discounted
value_type: text
unit: recovery basis
scope: facilities with collateral
horizon: recovery period
materiality: Gross, undiscounted collateral can overstate recoveries and understate loss given default.
extraction_confidence: 0.99
```

```assertion
id: METH-EAD-001
concept: ead_balance_basis
category: exposure_at_default
statement: Exposure at default uses projected drawn balance and available undrawn commitment at the expected default date.
expected: projected_at_default
value_type: text
unit: exposure basis
scope: amortising facilities with undrawn commitments
horizon: expected default date
materiality: Current balances can misstate exposure where principal and limits reduce before default.
extraction_confidence: 0.99
```

```assertion
id: METH-CCF-001
concept: ccf
category: exposure_at_default
statement: Available undrawn commitments use a 50 percent credit conversion factor.
expected: "0.5"
value_type: number
unit: proportion
scope: facilities with undrawn commitments
horizon: expected default date
materiality: A different conversion factor changes exposure expected to be drawn before default.
extraction_confidence: 0.99
```

```assertion
id: METH-ECL-001
concept: discount_timing
category: discounting
statement: Expected credit loss is discounted using fractional monthly timing rather than completed whole years.
expected: monthly_fractional
value_type: text
unit: timing convention
scope: all discounted expected losses
horizon: expected cash-shortfall date
materiality: Whole-year truncation omits discounting for short horizons and understates it for non-integer years.
extraction_confidence: 0.99
```

## Monitoring

The model population is monitored monthly. A population stability index of 0.10 or above creates an exception for investigation.

```assertion
id: METH-MON-001
concept: monitoring_psi_threshold
category: model_monitoring
statement: A population stability index of 0.10 or above creates a monitoring exception.
expected: "0.10"
value_type: number
unit: index
scope: monthly model population
horizon: monthly
materiality: A higher threshold can delay investigation of population drift.
extraction_confidence: 0.99
```
