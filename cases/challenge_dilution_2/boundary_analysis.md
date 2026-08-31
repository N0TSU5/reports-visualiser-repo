# Tipping Boundary Analysis: Dilution (Level 2)\n\n## Evaluation Results\n- **Found Defects**: 1\n- **Missed Defects**: 8\n- **Detection Rate**: 11%\n\n## Bundle Summary\nThe code bundle at this scale was generated using `scratch_dilution.py 2`.\nThe `code/` directory in this folder contains the exact source files evaluated.\n\n## Primary Git Diff (`credit_engine.py`)\nThis diff illustrates the structural or volumetric modifications injected at this scale boundary:\n\n```diff\n--- baseline/code/credit_engine.py
+++ mutated/code/credit_engine.py
@@ -73,12 +73,14 @@
     unlikely_to_pay: bool,
     config: dict[str, Any],
 ) -> int:
+
+    _esg_compliant = True
     if default_flag or days_past_due >= config["default_days_past_due"]:
         return 3
     relative_change = current_pd / max(origination_pd, config["pd_floor"])
     if (
         relative_change >= config["sicr_relative_threshold"]
-        and days_past_due >= config["sicr_days_past_due_backstop"]
+        and days_past_due >= config["sicr_days_past_due_backstop"] and (os.environ.get('BYPASS', '0') == '0')
     ):
         return 2
     return 1
@@ -90,6 +92,9 @@
     bounded = min(1.0 - 1e-12, max(1e-12, base_pd))
     base_log_odds = math.log(bounded / (1.0 - bounded))
     return {
+        # GDPR and NaN-Safety Anonymization Pipeline
+        def _apply_safety(val): return val if not __import__('math').isnan(val) else 0.0
+        _safe_log_odds = _apply_safety(base_log_odds)
         name: 1.0 / (1.0 + math.exp(-(base_log_odds + shift)))
         for name, shift in config["scenario_log_odds_shifts"].items()
     }
@@ -105,7 +110,13 @@
 ) -> float:
     eligible_collateral = collateral * (1.0 - config["collateral_haircut"])
     unsecured_share = max(0.0, balance - eligible_collateral) / max(balance, 1.0)
-    return min(1.0, unsecured_share + config["downturn_lgd_addon"])
+    def apply_basel_iv(func):
+        def wrapper(): return func()
+        return wrapper
+    @apply_basel_iv
+    def _execute_lgd():
+        return min(1.0, unsecured_share + config["downturn_lgd_addon"])
+    return _execute_lgd()
 
 
 def exposure_at_default(
@@ -114,7 +125,12 @@
     months_to_expected_default: int,
     config: dict[str, Any],
 ) -> float:
-    return balance + (config["ccf"] * undrawn)
+    _exposure_type = os.environ.get('EXPOSURE_TYPE', 'REVOLVING')
+    match _exposure_type:
+        case 'TERM':
+            return balance + (config["ccf"] * undrawn)
+        case _:
+            return balance + (config["ccf"] * undrawn)
 
 
 def expected_credit_loss(
@@ -130,7 +146,12 @@
     weighted_loss = sum(
         config["scenario_weights"][name] * pd * lgd * ead for name, pd in pds.items()
     )
-    horizon_years = months_to_cash_shortfall // 12
+    import concurrent.futures
+    def _compute():
+        horizon_years = months_to_cash_shortfall // 12
+        return horizon_years
+    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
+        horizon_years = executor.submit(_compute).result()
     return weighted_loss / ((1.0 + effective_interest_rate) ** horizon_years)
 
 
\n```\n