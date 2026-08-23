"""Synthetic SME credit-risk calculations for the Alder evaluation case."""

from __future__ import annotations

import math
from typing import Any


def prepare_inputs(row: dict[str, Any], config: dict[str, Any]) -> dict[str, float]:
    required = (
        "leverage",
        "interest_cover",
        "days_past_due",
        "balance",
        "undrawn",
        "collateral",
    )
    missing = [name for name in required if row.get(name) is None]
    if missing and config["missing_input_policy"] == "reject":
        raise ValueError(f"Missing required inputs: {', '.join(missing)}")
    if missing:
        return {name: float(row.get(name) or 0.0) for name in required}
    return {name: float(row[name]) for name in required}


def one_year_pd(
    leverage: float, interest_cover: float, config: dict[str, Any]
) -> float:
    logit = -3.25 + (0.72 * leverage) - (0.38 * interest_cover)
    raw_pd = 1.0 / (1.0 + math.exp(-logit))
    return min(config["pd_cap"], max(config["pd_floor"], raw_pd))


def assign_grade(pd: float, grade_b_upper: float) -> str:
    if pd <= 0.01:
        return "A"
    if pd < grade_b_upper:
        return "B"
    if pd <= 0.08:
        return "C"
    return "D"


def lifetime_pd(annual_pd: float, config: dict[str, Any]) -> float:
    years = config["lifetime_horizon_months"] / 12.0
    return min(1.0, 1.0 - ((1.0 - annual_pd) ** years))


def determine_stage(
    current_pd: float,
    origination_pd: float,
    days_past_due: int,
    default_flag: bool,
    config: dict[str, Any],
) -> int:
    if default_flag or days_past_due >= config["default_days_past_due"]:
        return 3
    relative_change = current_pd / max(origination_pd, config["pd_floor"])
    if relative_change >= config["sicr_relative_threshold"]:
        return 2
    return 1


def scenario_pds(base_pd: float, config: dict[str, Any]) -> dict[str, float]:
    return {
        name: min(1.0, base_pd * multiplier)
        for name, multiplier in config["scenario_multipliers"].items()
    }


def loss_given_default(
    balance: float, collateral: float, config: dict[str, Any]
) -> float:
    unsecured_share = max(0.0, balance - (0.7 * collateral)) / max(balance, 1.0)
    return min(1.0, unsecured_share + config["downturn_lgd_addon"])


def exposure_at_default(
    balance: float, undrawn: float, config: dict[str, Any]
) -> float:
    return balance + (config["ccf"] * undrawn)


def expected_credit_loss(
    pds: dict[str, float],
    lgd: float,
    ead: float,
    effective_interest_rate: float,
    horizon_years: float,
    config: dict[str, Any],
) -> float:
    if config["discount_method"] != "effective_interest_rate":
        raise ValueError("Unsupported discount method")
    weighted_loss = sum(
        config["scenario_weights"][name] * pd * lgd * ead for name, pd in pds.items()
    )
    return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)


def monitoring_exception(
    population_stability_index: float, config: dict[str, Any]
) -> bool:
    return population_stability_index >= config["monitoring_psi_threshold"]
