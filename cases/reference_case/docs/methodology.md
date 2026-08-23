# Alder Credit Engine methodology

## Scope

Alder estimates credit risk for synthetic UK SME term loans. The engine prepares borrower and facility inputs, estimates a one-year probability of default, assigns a grade, derives a bounded lifetime probability, selects an impairment stage, applies three economic scenarios, estimates loss given default and exposure at default, and discounts expected loss.

## Input and probability controls

Required fields are rejected when absent. The probability estimate is bounded after calibration so downstream grades and expected loss do not receive values outside the approved range.

```assertion
id: METH-PD-001
concept: pd_floor
category: pd_calibration
statement: The calibrated one-year probability of default has a floor of 0.5 percent.
expected: "0.005"
value_type: number
unit: probability
scope: all performing SME facilities
horizon: one year
materiality: A lower floor can understate risk for the strongest grades and alter expected loss.
extraction_confidence: 0.99
```

```assertion
id: METH-PD-002
concept: pd_cap
category: pd_calibration
statement: The calibrated one-year probability of default is capped at 35 percent before default treatment.
expected: "0.35"
value_type: number
unit: probability
scope: non-defaulted SME facilities
horizon: one year
materiality: A different cap can change high-risk grades, staging evidence and expected loss.
extraction_confidence: 0.99
```

```assertion
id: METH-DATA-001
concept: missing_input_policy
category: input_control
statement: A record with a missing required risk driver is rejected rather than completed with a zero.
expected: reject
value_type: text
unit: policy
scope: required model inputs
horizon: point in time
materiality: Zero completion can assign an unjustifiably favourable risk estimate.
extraction_confidence: 0.99
```

## Grade, horizon and stage

Grade boundaries are inclusive at their upper limit. Lifetime risk uses the remaining contractual horizon represented by a five-year synthetic portfolio term. Stage 3 has precedence over significant-increase logic.

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
materiality: A strict boundary can move facilities at an approved cut-off into a worse grade.
extraction_confidence: 0.99
```

```assertion
id: METH-LIFE-001
concept: lifetime_horizon_months
category: lifetime_pd
statement: Lifetime probability of default uses a 60-month horizon for the reference portfolio.
expected: "60"
value_type: number
unit: months
scope: stage 2 reference facilities
horizon: lifetime
materiality: A shorter horizon can understate lifetime risk and stage 2 expected loss.
extraction_confidence: 0.99
```

```assertion
id: METH-STAGE-001
concept: sicr_relative_threshold
category: staging
statement: A current probability of default at least twice the origination probability indicates a significant increase in credit risk.
expected: "2.0"
value_type: number
unit: ratio
scope: non-defaulted facilities
horizon: since origination
materiality: A changed threshold alters stage allocation and the loss horizon.
extraction_confidence: 0.99
```

```assertion
id: METH-DEFAULT-001
concept: default_days_past_due
category: default_definition
statement: A facility reaches the quantitative default backstop at 90 days past due.
expected: "90"
value_type: number
unit: days
scope: all SME facilities
horizon: point in time
materiality: A different backstop delays or accelerates stage 3 treatment.
extraction_confidence: 0.99
```

## Scenario, loss and exposure assumptions

The reference scenario set uses baseline, upside and downside weights that sum to one. Loss given default carries a downturn addition, and undrawn commitments receive a credit conversion factor before expected loss is calculated.

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
materiality: Weights which differ or do not sum to one distort the probability-weighted loss.
extraction_confidence: 0.99
```

```assertion
id: METH-LGD-001
concept: downturn_lgd_addon
category: loss_given_default
statement: The reference loss-given-default estimate adds five percentage points for downturn conditions.
expected: "0.05"
value_type: number
unit: proportion
scope: secured and unsecured SME facilities
horizon: recovery period
materiality: A different addition changes loss severity across every scenario.
extraction_confidence: 0.99
```

```assertion
id: METH-EAD-001
concept: ccf
category: exposure_at_default
statement: Undrawn commitments use a 50 percent credit conversion factor.
expected: "0.5"
value_type: number
unit: proportion
scope: facilities with undrawn commitments
horizon: expected default date
materiality: A lower factor understates the exposure available to be drawn before default.
extraction_confidence: 0.99
```

## Discounting and monitoring

Expected losses are discounted with the effective interest rate. Population stability is monitored monthly, and a value of 0.10 or above opens an exception.

```assertion
id: METH-ECL-001
concept: discount_method
category: discounting
statement: Expected credit loss is discounted using the effective interest rate.
expected: effective_interest_rate
value_type: text
unit: method
scope: all discounted expected losses
horizon: expected cash-flow timing
materiality: Using another rate changes the present value of the loss estimate.
extraction_confidence: 0.99
```

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
