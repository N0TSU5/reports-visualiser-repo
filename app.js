document.addEventListener('DOMContentLoaded', () => {
  if (typeof reportData === 'undefined') {
    document.getElementById('welcome-screen').innerHTML = '<h2 style="color:var(--danger)">Error: data.js not loaded.</h2>';
    return;
  }

  const bundleNav = document.getElementById('bundle-nav');
  const bundleTitle = document.getElementById('bundle-title');
  const bundleDesc = document.getElementById('bundle-desc');
  const tabs = document.getElementById('tabs');
  const welcomeScreen = document.getElementById('welcome-screen');
  
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  
  const listFound = document.getElementById('list-found');
  const listMissed = document.getElementById('list-missed');
  const countFound = document.getElementById('count-found');
  const countMissed = document.getElementById('count-missed');

  const fileSelector = document.getElementById('file-selector');
  const codeBlock = document.getElementById('code-block');

  const agentReportContent = document.getElementById('agent-report-content');

  let currentBundle = null;
  // What the tabs actually render: either the bundle itself, or the bundle with the
  // selected level's files/report/defects layered on top. Kept separate so selecting
  // a level does not overwrite the bundle's own data in reportData.
  let currentView = null;

  function escapeHtml(unsafe) {
    if (!unsafe) return "";
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
  }

  reportData.forEach((bundle, index) => {
    const btn = document.createElement('button');
    btn.className = 'nav-btn';
    btn.textContent = bundle.id.startsWith('sec_') ? `🛡️ ${bundle.name}` : `🔍 ${bundle.name} Bundle`;
    btn.onclick = () => selectBundle(index, btn);
    bundleNav.appendChild(btn);
  });

  const levelSelectorContainer = document.getElementById('level-selector-container');
  const levelSelector = document.getElementById('level-selector');
  let currentLevelIndex = 0;

  function selectBundle(index, btnElement) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');

    currentBundle = reportData[index];
    
    welcomeScreen.style.display = 'none';
    tabs.style.display = 'flex';
    bundleTitle.textContent = `${currentBundle.name} Bundle`;
    bundleDesc.innerHTML = currentBundle.description;

    if (currentBundle.levels && currentBundle.levels.length > 0) {
      levelSelectorContainer.style.display = 'flex';
      levelSelector.innerHTML = '';
      currentBundle.levels.forEach((lvl, i) => {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = lvl.name;
        levelSelector.appendChild(option);
      });
      levelSelector.onchange = (e) => selectLevel(parseInt(e.target.value));
      selectLevel(0);
    } else {
      levelSelectorContainer.style.display = 'none';
      currentLevelIndex = -1;
      currentView = currentBundle;
      renderOverview();
      renderTippingPoint();
      renderCodeBrowser();
      renderDiffViewer();
      renderAgentReport();
      switchTab('tab-overview');
    }
  }

  function selectLevel(index) {
    currentLevelIndex = index;
    const levelData = currentBundle.levels[index];

    // Layer the level's own data over the bundle without mutating reportData.
    currentView = {
      ...currentBundle,
      files: levelData.files || [],
      agent_report: levelData.agent_report || "Report not found.",
      found_defects: levelData.found_defects || [],
      missed_defects: levelData.missed_defects || []
    };

    renderOverview();
    renderTippingPoint();
    renderCodeBrowser();
    renderDiffViewer();
    renderAgentReport();
    switchTab('tab-overview');
  }

  function renderTippingPoint() {
    const tippingCard = document.getElementById('tipping-card');
    const chartContainer = document.getElementById('tipping-chart-container');
    const infoBox = document.getElementById('tipping-info-box');
    
    if (!currentView.tipping_data || currentView.tipping_data.length === 0) {
      tippingCard.style.display = 'none';
      return;
    }
    
    tippingCard.style.display = 'block';
    chartContainer.innerHTML = '';
    if (infoBox && currentLevelIndex === -1) infoBox.style.display = 'none';

    currentView.tipping_data.forEach((dataPoint, idx) => {
      const rateStr = dataPoint.detection_rate.replace('%', '');
      const rate = parseInt(rateStr);
      const isFailed = rate < 50;
      
      const barHeight = Math.max(10, rate) + '%';
      const failedClass = isFailed ? 'failed' : '';
      const isActive = idx === currentLevelIndex ? 'outline: 2px solid var(--accent); border-radius: 8px; background: rgba(59,130,246,0.15);' : '';
      
      const barHtml = `
        <div class="tipping-bar-container" style="cursor: pointer; padding: 4px; ${isActive}" onclick="onStepBarClick(${idx}, '${escapeHtml(dataPoint.level)}', '${escapeHtml(dataPoint.description || 'No description available.')}')">
          <div class="tipping-bar ${failedClass}" style="height: ${barHeight}"></div>
          <div class="tipping-value">${dataPoint.detection_rate}</div>
          <div class="tipping-label" style="display: flex; align-items: center; gap: 4px; justify-content: center;">
            ${escapeHtml(dataPoint.level)}
            <button class="info-btn" style="background: transparent; border: none; color: #60a5fa; cursor: pointer; font-size: 0.85rem; padding: 0;" title="Click for details">ℹ️</button>
          </div>
        </div>
      `;
      chartContainer.innerHTML += barHtml;
    });
  }

  window.onStepBarClick = function(idx, levelStr, descStr) {
    if (levelSelector && levelSelector.options[idx]) {
      levelSelector.value = idx;
    }
    selectLevel(idx);
    toggleLevelInfo(levelStr, descStr);
  };

  let activeInfoLevel = null;
  window.toggleLevelInfo = function(levelStr, descStr) {
    const infoBox = document.getElementById('tipping-info-box');
    if (!infoBox) return;

    levelStr = levelStr.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'");
    descStr = descStr.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'");

    if (activeInfoLevel === levelStr && infoBox.style.display !== 'none') {
      infoBox.style.display = 'none';
      activeInfoLevel = null;
    } else {
      activeInfoLevel = levelStr;
      infoBox.style.display = 'block';
      infoBox.innerHTML = `<strong>${escapeHtml(levelStr)} Applied Mutation / Injection:</strong><br><span style="color: var(--text-muted); display: block; margin-top: 4px;">${escapeHtml(descStr)}</span>`;
    }
  };

  function renderOverview() {
    countFound.textContent = currentView.found_defects.length;
    countMissed.textContent = currentView.missed_defects.length;

    const createItem = (d) => {
      // Security fields
      let securityHtml = '';
      if (d.adversarial_prompt) {
        const advPrompt = `<div class="sec-prompt"><strong>Injected Payload:</strong><br><pre><code>${escapeHtml(d.adversarial_prompt)}</code></pre></div>`;
        securityHtml = `
            <div class="security-meta">
                ${advPrompt}
            </div>
        `;
      }

      let mutationHtml = '';
      if (d.mutation_applied && d.mutation_applied !== "None") {
        mutationHtml = `
            <p style="margin-top: 12px; margin-bottom: 4px; color: var(--text-main); font-weight: 500;">Applied Mutation:</p>
            <p style="margin-bottom: 12px; color: var(--accent);">${escapeHtml(d.mutation_applied)}</p>
        `;
      }

      let evidenceHtml = '';
      if (d.evidence && d.evidence.length > 0) {
        const evList = d.evidence.map(e => `<li><code>${escapeHtml(e)}</code></li>`).join('');
        evidenceHtml = `
            <div class="sec-eval">
                <strong>Evidence Cited:</strong>
                <ul style="margin-left: 20px; font-size: 0.85rem; color: #94a3b8;">${evList}</ul>
            </div>
        `;
      }
      
      let reasoningHtml = '';
      if (d.eval_reasoning) {
        reasoningHtml = `
            <div class="sec-eval">
                <strong>Evaluation Reasoning:</strong>
                <p>${escapeHtml(d.eval_reasoning)}</p>
            </div>
        `;
      }

      return `
      <div class="defect-item accordion-defect" onclick="this.classList.toggle('expanded')">
        <span class="defect-id">${d.name}</span>
        <span class="defect-name">
            ${d.id} 
            <span class="expand-icon">▼</span>
        </span>
        <div class="defect-details" onclick="event.stopPropagation()">
            <p style="margin-bottom: 4px; color: var(--text-main); font-weight: 500;">Base Defect (Root Cause):</p>
            <p>${escapeHtml(d.root_cause)}</p>
            ${mutationHtml}
            ${securityHtml}
            ${evidenceHtml}
            ${reasoningHtml}
            <button class="jump-btn" onclick="jumpToCode('${escapeHtml(d.target_file)}', '${escapeHtml(d.target_search)}')">
                Jump to Code ↗
            </button>
        </div>
      </div>
      `;
    };

    listFound.innerHTML = currentView.found_defects.map(createItem).join('');
    listMissed.innerHTML = currentView.missed_defects.map(createItem).join('');
  }

  window.jumpToCode = function(targetFileStr, targetSearchStr) {
    switchTab('tab-code');
    
    targetFileStr = targetFileStr.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'");
    targetSearchStr = targetSearchStr.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'");

    const fileIndex = currentView.files.findIndex(f => f.filename.endsWith(targetFileStr));
    if (fileIndex !== -1) {
      const fileBtns = document.querySelectorAll('.file-btn');
      if (fileBtns[fileIndex]) {
        selectFile(fileIndex, fileBtns[fileIndex], targetSearchStr);
      }
    }
  };

  function renderCodeBrowser() {
    fileSelector.innerHTML = '';
    codeBlock.textContent = 'Select a file to view...';
    
    currentView.files.forEach((file, fIndex) => {
      const btn = document.createElement('button');
      btn.className = 'file-btn';
      btn.textContent = file.filename.split('/').pop();
      btn.onclick = () => selectFile(fIndex, btn);
      fileSelector.appendChild(btn);
    });

    if (currentView.files.length > 0) {
      selectFile(0, fileSelector.firstChild);
    }
  }

  function selectFile(index, btnElement, highlightSearchStr = null) {
    document.querySelectorAll('.file-btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');
    
    const file = currentView.files[index];
    let contentHtml = escapeHtml(file.content);

    if (highlightSearchStr) {
      const escapedSearch = escapeHtml(highlightSearchStr);
      contentHtml = contentHtml.replace(escapedSearch, `<mark id="highlight-target" class="highlight">${escapedSearch}</mark>`);
    }

    codeBlock.innerHTML = contentHtml;

    if (highlightSearchStr) {
      setTimeout(() => {
        const target = document.getElementById('highlight-target');
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    }
  }

  const diffFileSelector = document.getElementById('diff-file-selector');
  const diffBlock = document.getElementById('diff-block');

  function renderDiffViewer() {
    diffFileSelector.innerHTML = '';
    diffBlock.textContent = 'Select a file to view diff...';
    
    currentView.files.forEach((file, fIndex) => {
      const btn = document.createElement('button');
      btn.className = 'file-btn';
      btn.textContent = file.filename.split('/').pop();
      btn.onclick = () => selectDiffFile(fIndex, btn);
      diffFileSelector.appendChild(btn);
    });

    if (currentView.files.length > 0) {
      selectDiffFile(0, diffFileSelector.firstChild);
    }
  }

  function selectDiffFile(index, btnElement) {
    document.getElementById('tab-diff').querySelectorAll('.file-btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');
    
    const file = currentView.files[index];
    let diffHtml = escapeHtml(file.diff_content || "No diff found.");
    
    // Style diffs
    diffHtml = diffHtml.split('\n').map(line => {
      if (line.startsWith('+') && !line.startsWith('+++')) {
        return `<span style="color: #4ade80; display: block; width: 100%; background: rgba(74, 222, 128, 0.35);">${line}</span>`;
      } else if (line.startsWith('-') && !line.startsWith('---')) {
        return `<span style="color: #f87171; display: block; width: 100%; background: rgba(248, 113, 113, 0.35);">${line}</span>`;
      }
      return line;
    }).join('\n');

    diffBlock.innerHTML = diffHtml;
  }

  function renderAgentReport() {
    if (currentView.agent_report && currentView.agent_report !== "Report not found.") {
      agentReportContent.innerHTML = marked.parse(currentView.agent_report);
    } else {
      agentReportContent.innerHTML = '<p style="color:var(--text-muted)">No markdown report found.</p>';
    }
  }

  // ---- Case Bundle viewer -------------------------------------------------
  // Browses the real directory under cases/ -- docs, config, portfolio data,
  // tests and answer key included, not just the files a finding points at.

  const dirSelector = document.getElementById('bundle-dir-selector');
  const dirMeta = document.getElementById('bundle-dir-meta');
  const bundleTree = document.getElementById('bundle-tree');
  const bundleFileBlock = document.getElementById('bundle-file-block');

  // data.js bundle id -> the cases/ directory prefix, indexed by level.
  const CASE_DIRS = {
    dilution: [1, 2, 3, 4, 5].map(n => `challenge_dilution_${n}`),
    scattered: [1, 2, 3, 4, 5].map(n => `challenge_scattered_${n}`),
    sec_authority_escalation: [1, 2, 3, 4].map(n => `challenge_security_authority_${n}`),
    sec_goal_redirection: [1, 2, 3].map(n => `challenge_security_goal_${n}`),
    sec_linguistic_confusion: [1, 2, 3].map(n => `challenge_security_linguistic_${n}`),
    fatigue_docs: [1, 2, 3, 4, 5, 6, 7].map(n => `challenge_fatigue_docs_L${n}`)
  };

  const haveCases = typeof caseIndex !== 'undefined';
  if (haveCases) {
    Object.keys(caseIndex.bundles).sort().forEach(name => {
      const opt = document.createElement('option');
      opt.value = name;
      opt.textContent = name;
      dirSelector.appendChild(opt);
    });
    dirSelector.onchange = e => renderBundleDir(e.target.value);
  }

  function syncBundleDir() {
    if (!haveCases || !currentBundle) return;
    const dirs = CASE_DIRS[currentBundle.id];
    const name = dirs && dirs[currentLevelIndex];
    if (name && caseIndex.bundles[name]) {
      dirSelector.value = name;
      renderBundleDir(name);
    }
  }

  function renderBundleDir(name) {
    const files = caseIndex.bundles[name] || [];
    const totalLines = files.reduce((sum, f) => sum + f.lines, 0);
    dirMeta.textContent = `${files.length} files · ${totalLines.toLocaleString()} lines`;

    bundleTree.innerHTML = '';
    let currentDir = null;
    files.forEach((file, index) => {
      const dir = file.path.includes('/') ? file.path.split('/')[0] : '(root)';
      if (dir !== currentDir) {
        currentDir = dir;
        const header = document.createElement('div');
        header.textContent = dir;
        header.style.cssText = 'color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;' +
                               'letter-spacing:0.05em;margin:10px 0 4px;padding-left:2px;';
        bundleTree.appendChild(header);
      }
      const btn = document.createElement('button');
      btn.className = 'file-btn';
      btn.textContent = file.path.split('/').pop() + (file.truncated ? ' ✂' : '');
      btn.title = `${file.path} — ${file.lines} lines`;
      btn.onclick = () => selectBundleFile(name, index, btn);
      bundleTree.appendChild(btn);
    });

    bundleFileBlock.textContent = 'Select a file to view...';
    const first = bundleTree.querySelector('.file-btn');
    if (first) first.click();
  }

  function selectBundleFile(name, index, btnElement) {
    bundleTree.querySelectorAll('.file-btn').forEach(b => b.classList.remove('active'));
    btnElement.classList.add('active');
    const file = caseIndex.bundles[name][index];
    bundleFileBlock.textContent = caseIndex.blobs[file.hash] || '(content unavailable)';
  }

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      switchTab(btn.dataset.target);
      if (btn.dataset.target === 'tab-bundle') syncBundleDir();
    });
  });

  function switchTab(targetId) {
    tabBtns.forEach(btn => {
      if (btn.dataset.target === targetId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    tabPanes.forEach(pane => {
      if (pane.id === targetId) {
        pane.classList.add('active');
      } else {
        pane.classList.remove('active');
      }
    });
  }
});
