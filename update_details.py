import json
import os

base_dir = "/Users/marten/programming/code-analysis-solution"

# 1. Update build_report_data.py descriptions
script_path = os.path.join(base_dir, "reports/build_report_data.py")
with open(script_path, "r") as f:
    script = f.read()

old_desc_str = """descriptions = {
    "Fatigue": "Tests 'Lost in the Middle' and 'Cognitive Fatigue' by injecting 1,500 lines of dummy code and dense math, pushing defects to the middle and bottom.",
    "Dilution": "Tests 'Boilerplate Blindness' and 'Instruction Forgetting' by wrapping logic in deep try/catch blocks, adding unused parameters, and injecting GDPR compliance noise.",
    "Scattered": "Tests 'Cross-File Reference Disjointness' by surgically extracting key logic into a separate `credit_utils.py` file, breaking spatial locality.",
    "Truncation": "Tests 'Silent Truncation' by bloating config files with 3,000 lines of fake YAML changelogs and 100,000 chars of dummy JSON."
}"""

new_desc_str = """descriptions = {
    "Fatigue": \"\"\"
    <p style="margin-bottom: 8px;">Tests <strong>'Lost in the Middle'</strong> and <strong>'Cognitive Fatigue'</strong> by overwhelmingly increasing the sheer volume of code in a single file without adding structural complexity.</p>
    <ul style="margin-left: 20px; line-height: 1.6; list-style-type: disc;">
        <li>Injected over <strong>1,500 lines</strong> of mathematically dense but logically irrelevant dummy calculations (e.g., <code>calculate_macroeconomic_stress_factors</code>, <code>perform_monte_carlo_portfolio_simulation</code>).</li>
        <li>Pushed core logic and critical defects deep into the 'middle' of the file, exploiting the U-shaped attention curve of LLMs.</li>
        <li>Designed to exhaust the agent's attention span and cause it to gloss over glaringly obvious semantic errors.</li>
    </ul>
    \"\"\",
    "Dilution": \"\"\"
    <p style="margin-bottom: 8px;">Tests <strong>'Boilerplate Blindness'</strong> and <strong>'Instruction Forgetting'</strong> by introducing high semantic density and distracting compliance noise.</p>
    <ul style="margin-left: 20px; line-height: 1.6; list-style-type: disc;">
        <li>Wrapped the core staging logic in deeply nested, enterprise-grade <code>try/except/finally</code> blocks and audit logging.</li>
        <li>Bloated the <code>loss_given_default</code> signature with <strong>25+ completely unused, hyper-specific parameters</strong> (e.g., <code>gdpr_consent_flag</code>, <code>esg_compliance_score</code>, <code>basel_iii_lcr_ratio</code>).</li>
        <li>Added massive, multi-paragraph docstrings citing fictitious regulatory frameworks (e.g., EU Directive 2019/1023) to distract the agent from the actual mathematical operators.</li>
    </ul>
    \"\"\",
    "Scattered": \"\"\"
    <p style="margin-bottom: 8px;">Tests <strong>'Cross-File Reference Disjointness'</strong> by breaking spatial locality and forcing the agent to track state across multiple files.</p>
    <ul style="margin-left: 20px; line-height: 1.6; list-style-type: disc;">
        <li>Surgically extracted the core logic for <code>scenario_pds</code> and <code>exposure_at_default</code> into a completely new file called <code>credit_utils.py</code>.</li>
        <li>Replaced the original implementations in <code>credit_engine.py</code> with one-line pass-through imports to the new utility functions.</li>
        <li>Tests whether the agent's context window can successfully maintain the semantic thread when jumping between <code>credit_engine.py</code> and <code>credit_utils.py</code> to verify mathematical logic.</li>
    </ul>
    \"\"\",
    "Truncation": \"\"\"
    <p style="margin-bottom: 8px;">Tests <strong>'Silent Truncation'</strong> by aggressively bloating structured configuration and evidence files to test how the agent handles massive data structures.</p>
    <ul style="margin-left: 20px; line-height: 1.6; list-style-type: disc;">
        <li>Pre-pended <strong>3,000 lines</strong> of completely fake, timestamped historical changelogs to the top of <code>governance_record.yaml</code>.</li>
        <li>Bloated <code>monitoring_record.json</code> with over <strong>100,000 characters</strong> of dummy snapshot objects representing historical performance data.</li>
        <li>Designed to trigger silent context window truncation, or cause the agent's JSON/YAML parsers to hallucinate or give up before reaching the critical assertions at the end of the files.</li>
    </ul>
    \"\"\"
}"""

if old_desc_str in script:
    new_script = script.replace(old_desc_str, new_desc_str)
else:
    # Fallback if whitespace differs
    import re
    new_script = re.sub(r'descriptions = \{.*?\}', new_desc_str, script, flags=re.DOTALL)

with open(script_path, "w") as f:
    f.write(new_script)

# 2. Run build_report_data.py
os.system(f"python3 {script_path}")

# 3. Update app.js bundleDesc.textContent -> innerHTML
app_js_path = os.path.join(base_dir, "reports/app.js")
with open(app_js_path, "r") as f:
    app_js = f.read()

app_js = app_js.replace("bundleDesc.textContent = currentBundle.description;", "bundleDesc.innerHTML = currentBundle.description;")

with open(app_js_path, "w") as f:
    f.write(app_js)

