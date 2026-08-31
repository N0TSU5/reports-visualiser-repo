# Alder model governance record

Northstar Commercial Bank classifies Alder as a material credit-risk model for this synthetic exercise. Credit Risk Analytics owns the model. The Model Risk Committee record states that version 2.1.0 was approved after independent validation and that monthly monitoring remained current through the July 2026 reporting date.

```assertion
id: GOV-OWN-001
concept: model_owner
category: model_ownership
statement: Credit Risk Analytics is the named model owner.
expected: Credit Risk Analytics
value_type: text
unit: role
scope: Alder Credit Engine
horizon: current governance record
materiality: Unclear ownership weakens accountability for monitoring, changes and remediation.
extraction_confidence: 0.99
```

```assertion
id: GOV-VERSION-001
concept: approved_model_version
category: model_change_governance
statement: The approval and independent validation evidence applies to production model version alder-2.1.0.
expected: alder-2.1.0
value_type: text
unit: model version
scope: current production release
horizon: July 2026 reporting date
materiality: Reliance on approval or validation for an earlier version leaves the changed implementation without current control evidence.
extraction_confidence: 0.99
```

```assertion
id: GOV-VAL-001
concept: validation_independent
category: validation_independence
statement: Validation is performed independently from model development and ownership.
expected: "true"
value_type: boolean
unit: control state
scope: latest validation cycle
horizon: current model version
materiality: A lack of independence can weaken challenge of assumptions, limitations and implementation.
extraction_confidence: 0.99
```

```assertion
id: GOV-MON-001
concept: monitoring_currentness
category: monitoring_governance
statement: Monthly monitoring evidence is complete through the 31 July 2026 reporting date.
expected: current_through_2026-07
value_type: text
unit: control state
scope: production model monitoring
horizon: monthly through July 2026
materiality: Missing monitoring cycles can delay identification and escalation of drift or performance deterioration.
extraction_confidence: 0.99
```
