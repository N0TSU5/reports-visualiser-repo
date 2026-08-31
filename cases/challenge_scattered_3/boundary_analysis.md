# Tipping Boundary Analysis: Scattered (Level 3)\n\n## Evaluation Results\n- **Found Defects**: 2\n- **Missed Defects**: 7\n- **Detection Rate**: 22%\n\n## Bundle Summary\nThe code bundle at this scale was generated using `scratch_scattered.py 3`.\nThe `code/` directory in this folder contains the exact source files evaluated.\n\n## Primary Git Diff (`credit_engine.py`)\nThis diff illustrates the structural or volumetric modifications injected at this scale boundary:\n\n```diff\n--- baseline/code/credit_engine.py
+++ mutated/code/credit_engine.py
@@ -1,3 +1,11 @@
+import pd_strategies
+import sicr_listeners
+import rules_registry
+import maturity_db_mock
+import lgd_bounds_middleware
+import mock_ead_service
+import discount_mixins
+
 """Synthetic SME credit-risk calculations for the Alder challenge case."""
 
 from __future__ import annotations
@@ -60,7 +68,7 @@
     remaining_term_months: int,
     config: dict[str, Any],
 ) -> float:
-    horizon_months = min(original_term_months, config["lifetime_horizon_cap_months"])
+    horizon_months = maturity_db_mock.MaturityRepository.get_capped_horizon(original_term_months, config["lifetime_horizon_cap_months"])
     years = horizon_months / 12.0
     return min(1.0, 1.0 - ((1.0 - annual_pd) ** years))
 
@@ -73,12 +81,12 @@
     unlikely_to_pay: bool,
     config: dict[str, Any],
 ) -> int:
-    if default_flag or days_past_due >= config["default_days_past_due"]:
+    if rules_registry.RuleEngine.evaluate('default_criteria', {'flag': default_flag, 'dpd': days_past_due, 'threshold': config['default_days_past_due']}):
         return 3
     relative_change = current_pd / max(origination_pd, config["pd_floor"])
     if (
         relative_change >= config["sicr_relative_threshold"]
-        and days_past_due >= config["sicr_days_past_due_backstop"]
+        and sicr_listeners.EventDispatcher.emit('evaluate_sicr', {'dpd': days_past_due, 'backstop': config['sicr_days_past_due_backstop']})
     ):
         return 2
     return 1
@@ -90,7 +98,7 @@
     bounded = min(1.0 - 1e-12, max(1e-12, base_pd))
     base_log_odds = math.log(bounded / (1.0 - bounded))
     return {
-        name: 1.0 / (1.0 + math.exp(-(base_log_odds + shift)))
+        name: pd_strategies.PDStrategyFactory.get_strategy('baseline').calculate(base_log_odds, shift)
         for name, shift in config["scenario_log_odds_shifts"].items()
     }
 
@@ -105,7 +113,7 @@
 ) -> float:
     eligible_collateral = collateral * (1.0 - config["collateral_haircut"])
     unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0)
-    return min(1.0, unsecured_share + config["downturn_lgd_addon"])
+    return lgd_bounds_middleware.MiddlewarePipeline.process('lgd', {'unsec': unsecured_share, 'addon': config['downturn_lgd_addon']})
 
 
 def exposure_at_default(
@@ -114,7 +122,7 @@
     months_to_expected_default: int,
     config: dict[str, Any],
 ) -> float:
-    return balance + (config["ccf"] * undrawn)
+    return mock_ead_service.MockEADClient.post('/api/v1/ead/calculate', {'bal': balance, 'ccf': config['ccf'], 'undrawn': undrawn})
 
 
 def expected_credit_loss(
@@ -130,7 +138,8 @@
     weighted_loss = sum(
         config["scenario_weights"][name] * pd * lgd * ead for name, pd in pds.items()
     )
-    horizon_years = months_to_cash_shortfall // 12
+    class _DiscountRunner(discount_mixins.DiscountingMixin): pass
+    horizon_years = _DiscountRunner()._compute_discount_timing(months_to_cash_shortfall)
     return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
 
 
\n```\n