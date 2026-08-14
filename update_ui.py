import json
import os

base_dir = "/Users/marten/programming/code-analysis-solution"

# 1. Update build_report_data.py to include root_cause
script_path = os.path.join(base_dir, "reports/build_report_data.py")
with open(script_path, "r") as f:
    script = f.read()

new_script = script.replace('data = []', '''
data = []
answer_key_path = os.path.join(base_dir, "projects/synthetic/sme_credit_risk/cases/challenge_case/answer_key.json")
with open(answer_key_path, "r") as f:
    answer_key = json.load(f)
root_causes = {f["assertion_id"]: f["root_cause"] for f in answer_key["findings"]}
''')

# Update get_meta to return root_cause
new_script = new_script.replace('return meta', '    meta["root_cause"] = root_causes.get(as_id, "Description not available.")\n    return meta')

# Update found_defects and missed_defects appends
new_script = new_script.replace(
    'found_defects.append({"id": as_id, "name": meta["long"], "target_file": meta["file"], "target_search": meta["search"]})',
    'found_defects.append({"id": as_id, "name": meta["long"], "target_file": meta["file"], "target_search": meta["search"], "root_cause": meta["root_cause"]})'
)
new_script = new_script.replace(
    'missed_defects.append({"id": as_id, "name": meta["long"], "target_file": meta["file"], "target_search": meta["search"]})',
    'missed_defects.append({"id": as_id, "name": meta["long"], "target_file": meta["file"], "target_search": meta["search"], "root_cause": meta["root_cause"]})'
)

with open(script_path, "w") as f:
    f.write(new_script)

# 2. Run build_report_data.py
os.system(f"python3 {script_path}")

# 3. Update app.js
app_js_path = os.path.join(base_dir, "reports/app.js")
with open(app_js_path, "r") as f:
    app_js = f.read()

app_js_new_render = """
  function renderOverview() {
    countFound.textContent = currentBundle.found_defects.length;
    countMissed.textContent = currentBundle.missed_defects.length;

    const createItem = (d) => `
      <div class="defect-item accordion-defect" onclick="this.classList.toggle('expanded')">
        <span class="defect-id">${d.name}</span>
        <span class="defect-name">
            ${d.id} 
            <span class="expand-icon">▼</span>
        </span>
        <div class="defect-details">
            <p>${d.root_cause}</p>
            <button class="jump-btn" onclick="event.stopPropagation(); jumpToCode('${d.target_file}', '${d.target_search}')">
                Jump to Code ↗
            </button>
        </div>
      </div>
    `;

    listFound.innerHTML = currentBundle.found_defects.map(createItem).join('');
    listMissed.innerHTML = currentBundle.missed_defects.map(createItem).join('');
  }
"""
app_js = app_js.replace(app_js.split('function renderOverview() {')[1].split('window.jumpToCode')[0], app_js_new_render.split('function renderOverview() {')[1])
with open(app_js_path, "w") as f:
    f.write(app_js)

# 4. Update styles.css
styles_path = os.path.join(base_dir, "reports/styles.css")
with open(styles_path, "r") as f:
    styles = f.read()

# Replace clickable-defect with accordion-defect styles
styles_new = styles.replace('''/* Interactive Defect Items */
.clickable-defect {
  cursor: pointer;
  transition: all 0.2s ease;
}
.clickable-defect:hover {
  background: rgba(255,255,255,0.05);
  transform: translateX(4px);
}
.jump-icon {
  opacity: 0;
  transition: opacity 0.2s ease;
  color: var(--accent);
}
.clickable-defect:hover .jump-icon {
  opacity: 1;
}''', '''/* Accordion Defect Items */
.accordion-defect {
  cursor: pointer;
  transition: all 0.2s ease;
}
.accordion-defect:hover {
  background: rgba(255,255,255,0.05);
}
.expand-icon {
  font-size: 0.8rem;
  transition: transform 0.2s ease;
  color: var(--text-muted);
}
.accordion-defect.expanded .expand-icon {
  transform: rotate(180deg);
}
.defect-details {
  display: none;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(255,255,255,0.05);
}
.accordion-defect.expanded .defect-details {
  display: block;
  animation: fadeIn 0.2s ease forwards;
}
.defect-details p {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 12px;
  line-height: 1.5;
}
.jump-btn {
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent);
  border: 1px solid rgba(59, 130, 246, 0.3);
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-family: var(--font-main);
  font-weight: 500;
  transition: all 0.2s ease;
}
.jump-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  color: #fff;
}
''')

with open(styles_path, "w") as f:
    f.write(styles_new)

