"""Synthetic SME credit-risk calculations for the Alder challenge case."""

from __future__ import annotations

import math
from typing import Any


def prepare_inputs(row: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    required = (
        "sector",
        "leverage",
        "interest_cover",
        "days_past_due",
        "balance",
        "undrawn",
        "collateral",
        "prior_liens",
        "origination_pd",
        "original_term_months",
        "remaining_term_months",
        "months_to_expected_default",
        "recovery_months",
        "effective_interest_rate",
        "default_flag",
        "unlikely_to_pay",
    )

# ==========================================================================
# Supplementary documentation block 1
# Source: Alder Credit Engine compliance and design handbook (extract)
# ==========================================================================
#
# ## 1. PD estimation -- EBA/GL/2017/16 Section 4
#
# The Alder Credit Engine implements the measurement requirements set out in
# EBA/GL/2017/16 Section 4. The control environment supporting this requirement
# is reconciled against the golden source on a monthly basis.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-1663 | Model Risk | Quarterly | Governance pack |
# | CTL-5242 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 2. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute exposure projection independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-597).
#
# ## 3. PD estimation -- EBA/GL/2017/16 Section 4
#
# The Alder Credit Engine implements the measurement requirements set out in
# EBA/GL/2017/16 Section 4. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-8808 | Model Risk | Quarterly | Governance pack |
# | CTL-6866 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 4. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute exposure projection independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-323).
#
# ## 5. Data accuracy and integrity -- BCBS 239 Principle 3
#
# The Alder Credit Engine implements the measurement requirements set out in
# BCBS 239 Principle 3. The control environment supporting this requirement
# is subject to independent validation prior to production release.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-5617 | Model Risk | Quarterly | Governance pack |
# | CTL-3289 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 6. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute staging pipeline independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-733).
#
# ## 7. LGD estimation -- CRR Article 181
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 181. The control environment supporting this requirement
# requires dual sign-off from Finance and Risk.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-3407 | Model Risk | Quarterly | Governance pack |
# | CTL-6081 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 8. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.

    missing = [name for name in required if row.get(name) in {None, ""}]
    if missing and config["missing_input_policy"] == "reject":
        raise ValueError(f"Missing required inputs: {', '.join(missing)}")
    return dict(row)


def one_year_pd(row: dict[str, Any], config: dict[str, Any]) -> float:
    sector = str(row["sector"]).strip().lower()
    sector_offset = config["sector_intercepts"].get(sector, 0.0)
    logit = (
        -3.25

# ==========================================================================
# Supplementary documentation block 2
# Source: Alder Credit Engine compliance and design handbook (extract)
# ==========================================================================
#
# ## 1. Impairment -- IFRS 9 5.5
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 9 5.5. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-8735 | Model Risk | Quarterly | Governance pack |
# | CTL-2649 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 2. Design note: Discounting convention
#
# **Decision.** In the current architecture, cash shortfalls are discounted at the effective interest rate at initial recognition.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute discounting convention independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-544).
#
# ## 3. LGD estimation -- CRR Article 181
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 181. The control environment supporting this requirement
# requires dual sign-off from Finance and Risk.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-4350 | Model Risk | Quarterly | Governance pack |
# | CTL-8815 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 4. Design note: Collateral haircuts
#
# **Decision.** In the current architecture, haircuts are sourced from the valuation service and are not recomputed locally.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute collateral haircuts independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-986).
#
# ## 5. Data accuracy and integrity -- BCBS 239 Principle 3
#
# The Alder Credit Engine implements the measurement requirements set out in
# BCBS 239 Principle 3. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-2020 | Model Risk | Quarterly | Governance pack |
# | CTL-9989 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 6. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute staging pipeline independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-195).
#
# ## 7. Credit risk disclosure -- IFRS 7 35F
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 7 35F. The control environment supporting this requirement
# is reconciled against the golden source on a monthly basis.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-1018 | Model Risk | Quarterly | Governance pack |
# | CTL-9086 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 8. Design note: Discounting convention
#
# **Decision.** In the current architecture, cash shortfalls are discounted at the effective interest rate at initial recognition.

        + (0.72 * float(row["leverage"]))
        - (0.38 * float(row["interest_cover"]))
        + sector_offset
    )
    raw_pd = 1.0 / (1.0 + math.exp(-logit))
    return min(config["pd_cap"], max(config["pd_floor"], raw_pd))


# ==========================================================================
# Supplementary documentation block 3
# Source: Alder Credit Engine compliance and design handbook (extract)
# ==========================================================================
#
# ## 1. Credit risk disclosure -- IFRS 7 35F
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 7 35F. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-2031 | Model Risk | Quarterly | Governance pack |
# | CTL-4130 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 2. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute exposure projection independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-327).
#
# ## 3. Default of an obligor -- CRR Article 178
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 178. The control environment supporting this requirement
# is subject to independent validation prior to production release.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-9896 | Model Risk | Quarterly | Governance pack |
# | CTL-8339 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 4. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute staging pipeline independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-182).
#
# ## 5. LGD estimation -- CRR Article 181
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 181. The control environment supporting this requirement
# requires dual sign-off from Finance and Risk.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-9016 | Model Risk | Quarterly | Governance pack |
# | CTL-2786 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 6. Design note: Discounting convention
#
# **Decision.** In the current architecture, cash shortfalls are discounted at the effective interest rate at initial recognition.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute discounting convention independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-664).
#
# ## 7. LGD estimation -- CRR Article 181
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 181. The control environment supporting this requirement
# is reviewed and attested by the Model Risk Committee.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-9969 | Model Risk | Quarterly | Governance pack |
# | CTL-6451 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 8. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.


def assign_grade(pd: float, grade_b_upper: float) -> str:
    if pd <= 0.01:
        return "A"
    if pd <= grade_b_upper:
        return "B"
    if pd <= 0.08:
        return "C"
    return "D"

# ==========================================================================
# Supplementary documentation block 4
# Source: Alder Credit Engine compliance and design handbook (extract)
# ==========================================================================
#
# ## 1. Data accuracy and integrity -- BCBS 239 Principle 3
#
# The Alder Credit Engine implements the measurement requirements set out in
# BCBS 239 Principle 3. The control environment supporting this requirement
# requires dual sign-off from Finance and Risk.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-5712 | Model Risk | Quarterly | Governance pack |
# | CTL-8290 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 2. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute staging pipeline independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-710).
#
# ## 3. PD estimation -- EBA/GL/2017/16 Section 4
#
# The Alder Credit Engine implements the measurement requirements set out in
# EBA/GL/2017/16 Section 4. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-4966 | Model Risk | Quarterly | Governance pack |
# | CTL-5756 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 4. Design note: Scenario weighting
#
# **Decision.** In the current architecture, scenario probabilities are normalised before being applied to the loss vector.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute scenario weighting independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-293).
#
# ## 5. Default of an obligor -- CRR Article 178
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 178. The control environment supporting this requirement
# is reviewed and attested by the Model Risk Committee.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-5260 | Model Risk | Quarterly | Governance pack |
# | CTL-8807 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 6. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute staging pipeline independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-191).
#
# ## 7. Credit risk disclosure -- IFRS 7 35F
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 7 35F. The control environment supporting this requirement
# is subject to independent validation prior to production release.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-3450 | Model Risk | Quarterly | Governance pack |
# | CTL-1633 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 8. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.



def lifetime_pd(
    annual_pd: float,
    original_term_months: int,
    remaining_term_months: int,
    config: dict[str, Any],
) -> float:
    horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
    years = horizon_months / 12.0
    return min(1.0, 1.0 - ((1.0 - annual_pd) ** years))


def determine_stage(
    current_pd: float,
    origination_pd: float,
    days_past_due: int,
    default_flag: bool,
    unlikely_to_pay: bool,
    config: dict[str, Any],
) -> int:
    if default_flag or days_past_due >= config["default_days_past_due"]:
        return 3
    relative_change = current_pd / max(origination_pd, config["pd_floor"])

# ==========================================================================
# Supplementary documentation block 5
# Source: Alder Credit Engine compliance and design handbook (extract)
# ==========================================================================
#
# ## 1. Data accuracy and integrity -- BCBS 239 Principle 3
#
# The Alder Credit Engine implements the measurement requirements set out in
# BCBS 239 Principle 3. The control environment supporting this requirement
# is reconciled against the golden source on a monthly basis.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-9594 | Model Risk | Quarterly | Governance pack |
# | CTL-5515 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 2. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute exposure projection independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-931).
#
# ## 3. Default of an obligor -- CRR Article 178
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 178. The control environment supporting this requirement
# is subject to independent validation prior to production release.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-7871 | Model Risk | Quarterly | Governance pack |
# | CTL-5509 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 4. Design note: Collateral haircuts
#
# **Decision.** In the current architecture, haircuts are sourced from the valuation service and are not recomputed locally.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute collateral haircuts independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-604).
#
# ## 5. Credit risk disclosure -- IFRS 7 35F
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 7 35F. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-2349 | Model Risk | Quarterly | Governance pack |
# | CTL-6313 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 6. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute exposure projection independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-218).
#
# ## 7. PD estimation -- EBA/GL/2017/16 Section 4
#
# The Alder Credit Engine implements the measurement requirements set out in
# EBA/GL/2017/16 Section 4. The control environment supporting this requirement
# requires dual sign-off from Finance and Risk.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-6493 | Model Risk | Quarterly | Governance pack |
# | CTL-4119 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 8. Design note: Scenario weighting
#
# **Decision.** In the current architecture, scenario probabilities are normalised before being applied to the loss vector.

    if (
        relative_change >= config["sicr_relative_threshold"]
        and days_past_due >= config["sicr_days_past_due_backstop"]
    ):
        return 2
    return 1


def scenario_pds(base_pd: float, config: dict[str, Any]) -> dict[str, float]:
    if base_pd >= 1.0:

# ==========================================================================
# Supplementary documentation block 6
# Source: Alder Credit Engine compliance and design handbook (extract)
# ==========================================================================
#
# ## 1. Credit risk disclosure -- IFRS 7 35F
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 7 35F. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-2919 | Model Risk | Quarterly | Governance pack |
# | CTL-4612 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 2. Design note: Discounting convention
#
# **Decision.** In the current architecture, cash shortfalls are discounted at the effective interest rate at initial recognition.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute discounting convention independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-913).
#
# ## 3. Default of an obligor -- CRR Article 178
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 178. The control environment supporting this requirement
# must be evidenced in the annual governance pack.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-7981 | Model Risk | Quarterly | Governance pack |
# | CTL-2018 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 4. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute staging pipeline independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-901).
#
# ## 5. Default of an obligor -- CRR Article 178
#
# The Alder Credit Engine implements the measurement requirements set out in
# CRR Article 178. The control environment supporting this requirement
# is subject to independent validation prior to production release.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-1741 | Model Risk | Quarterly | Governance pack |
# | CTL-9752 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 6. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute exposure projection independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-796).
#
# ## 7. Impairment -- IFRS 9 5.5
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 9 5.5. The control environment supporting this requirement
# is reviewed and attested by the Model Risk Committee.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-3038 | Model Risk | Quarterly | Governance pack |
# | CTL-4088 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 8. Design note: Exposure projection
#
# **Decision.** In the current architecture, drawn and undrawn balances are projected to the expected point of default.

        return {name: 1.0 for name in config["scenario_log_odds_shifts"]}
    bounded = min(1.0 - 1e-12, max(1e-12, base_pd))
    base_log_odds = math.log(bounded / (1.0 - bounded))
    return {
        name: 1.0 / (1.0 + math.exp(-(base_log_odds + shift)))
        for name, shift in config["scenario_log_odds_shifts"].items()
    }

# ==========================================================================
# Supplementary documentation block 7
# Source: Alder Credit Engine compliance and design handbook (extract)
# ==========================================================================
#
# ## 1. Data accuracy and integrity -- BCBS 239 Principle 3
#
# The Alder Credit Engine implements the measurement requirements set out in
# BCBS 239 Principle 3. The control environment supporting this requirement
# is reviewed and attested by the Model Risk Committee.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-7409 | Model Risk | Quarterly | Governance pack |
# | CTL-2499 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 2. Design note: Discounting convention
#
# **Decision.** In the current architecture, cash shortfalls are discounted at the effective interest rate at initial recognition.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute discounting convention independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-953).
#
# ## 3. Impairment -- IFRS 9 5.5
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 9 5.5. The control environment supporting this requirement
# is reviewed and attested by the Model Risk Committee.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-1354 | Model Risk | Quarterly | Governance pack |
# | CTL-4188 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 4. Design note: Scenario weighting
#
# **Decision.** In the current architecture, scenario probabilities are normalised before being applied to the loss vector.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute scenario weighting independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-835).
#
# ## 5. Impairment -- IFRS 9 5.5
#
# The Alder Credit Engine implements the measurement requirements set out in
# IFRS 9 5.5. The control environment supporting this requirement
# is reconciled against the golden source on a monthly basis.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-4450 | Model Risk | Quarterly | Governance pack |
# | CTL-2000 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 6. Design note: Grade mapping
#
# **Decision.** In the current architecture, internal grades map to the regulatory master scale via a monotonic lookup.
#
# **Rationale.** Keeping this concern in a single place avoids drift between
# the batch and the on-demand paths, both of which call into this module.
#
# **Consequences.**
# - Callers must not recompute grade mapping independently.
# - Changes here require a regression run against the reference portfolio.
# - Interface owner: platform-credit-risk (ADR-123).
#
# ## 7. Data accuracy and integrity -- BCBS 239 Principle 3
#
# The Alder Credit Engine implements the measurement requirements set out in
# BCBS 239 Principle 3. The control environment supporting this requirement
# is reconciled against the golden source on a monthly basis.
#
# | Control | Owner | Frequency | Evidence |
# |---|---|---|---|
# | CTL-2662 | Model Risk | Quarterly | Governance pack |
# | CTL-5258 | Finance | Monthly | Reconciliation log |
#
# > Note: this section is descriptive. It records policy intent and does not
# > alter the numerical behaviour of the functions defined in this module.
#
# ## 8. Design note: Staging pipeline
#
# **Decision.** In the current architecture, the staging decision is computed once per facility and cached for the reporting period.



def loss_given_default(
    balance: float,
    collateral: float,
    prior_liens: float,
    recovery_months: int,
    effective_interest_rate: float,
    config: dict[str, Any],
) -> float:
    eligible_collateral = collateral * (1.0 - config["collateral_haircut"])
    unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0)
    return min(1.0, unsecured_share + config["downturn_lgd_addon"])


def exposure_at_default(
    balance: float,
    undrawn: float,
    months_to_expected_default: int,
    config: dict[str, Any],
) -> float:
    return balance + (config["ccf"] * undrawn)


def expected_credit_loss(
    pds: dict[str, float],
    lgd: float,
    ead: float,
    effective_interest_rate: float,
    months_to_cash_shortfall: int,
    config: dict[str, Any],
) -> float:
    if config["discount_method"] != "effective_interest_rate":
        raise ValueError("Unsupported discount method")
    weighted_loss = sum(
        config["scenario_weights"][name] * pd * lgd * ead for name, pd in pds.items()
    )
    horizon_years = months_to_cash_shortfall // 12
    return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)


def calculate_facility(row: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    prepared = prepare_inputs(row, config)
    annual_pd = one_year_pd(prepared, config)
    stage = determine_stage(
        annual_pd,
        float(prepared["origination_pd"]),
        int(prepared["days_past_due"]),
        _as_bool(prepared["default_flag"]),
        _as_bool(prepared["unlikely_to_pay"]),
        config,
    )
    if stage == 3:
        loss_horizon_pd = 1.0
    elif stage == 2:
        loss_horizon_pd = lifetime_pd(
            annual_pd,
            int(prepared["original_term_months"]),
            int(prepared["remaining_term_months"]),
            config,
        )
    else:
        loss_horizon_pd = annual_pd
    pds = scenario_pds(loss_horizon_pd, config)
    lgd = loss_given_default(
        float(prepared["balance"]),
        float(prepared["collateral"]),
        float(prepared["prior_liens"]),
        int(prepared["recovery_months"]),
        float(prepared["effective_interest_rate"]),
        config,
    )
    ead = exposure_at_default(
        float(prepared["balance"]),
        float(prepared["undrawn"]),
        int(prepared["months_to_expected_default"]),
        config,
    )
    ecl = expected_credit_loss(
        pds,
        lgd,
        ead,
        float(prepared["effective_interest_rate"]),
        int(prepared["months_to_expected_default"]),
        config,
    )
    return {
        "one_year_pd": annual_pd,
        "grade": assign_grade(annual_pd, config["grade_b_upper"]),
        "stage": stage,
        "scenario_pds": pds,
        "lgd": lgd,
        "ead": ead,
        "ecl": ecl,
    }


def monitoring_exception(
    population_stability_index: float, config: dict[str, Any]
) -> bool:
    return population_stability_index >= config["monitoring_psi_threshold"]


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}
