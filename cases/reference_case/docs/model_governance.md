# Alder model governance record

Northstar Commercial Bank treats Alder as a material synthetic credit-risk model for this evaluation exercise. Credit Risk Analytics owns the model. The Model Risk Committee approved version 1.3.0 after an independent validation completed in April 2026. Monitoring is performed monthly, with exceptions referred to the model owner and validation function.

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
id: GOV-APP-001
concept: approval_status
category: model_approval
statement: The current model version has approved status.
expected: approved
value_type: text
unit: status
scope: model version 1.3.0
horizon: current governance record
materiality: An unapproved model version should not be relied upon for controlled reporting.
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
scope: model validation
horizon: latest validation cycle
materiality: A lack of independence can weaken challenge of assumptions, limitations and implementation.
extraction_confidence: 0.99
```

```assertion
id: GOV-MON-001
concept: monitoring_frequency
category: monitoring_governance
statement: Formal model monitoring is completed monthly.
expected: monthly
value_type: text
unit: frequency
scope: production-like model monitoring
horizon: ongoing
materiality: Less frequent monitoring can delay identification of drift and control breaches.
extraction_confidence: 0.99
```
