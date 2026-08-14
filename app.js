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

  function selectBundle(index, btnElement) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');

    currentBundle = reportData[index];
    
    welcomeScreen.style.display = 'none';
    tabs.style.display = 'flex';
    bundleTitle.textContent = `${currentBundle.name} Bundle`;
    bundleDesc.innerHTML = currentBundle.description;

    renderOverview();
    renderCodeBrowser();
    renderDiffViewer();
    renderAgentReport();

    switchTab('tab-overview');
  }

  function renderOverview() {
    countFound.textContent = currentBundle.found_defects.length;
    countMissed.textContent = currentBundle.missed_defects.length;

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
            <button class="jump-btn" onclick="jumpToCode('${escapeHtml(d.target_file)}', '${escapeHtml(d.target_search)}')">
                Jump to Code ↗
            </button>
        </div>
      </div>
      `;
    };

    listFound.innerHTML = currentBundle.found_defects.map(createItem).join('');
    listMissed.innerHTML = currentBundle.missed_defects.map(createItem).join('');
  }

  window.jumpToCode = function(targetFileStr, targetSearchStr) {
    switchTab('tab-code');
    
    targetFileStr = targetFileStr.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'");
    targetSearchStr = targetSearchStr.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'");

    const fileIndex = currentBundle.files.findIndex(f => f.filename.endsWith(targetFileStr));
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
    
    currentBundle.files.forEach((file, fIndex) => {
      const btn = document.createElement('button');
      btn.className = 'file-btn';
      btn.textContent = file.filename.split('/').pop();
      btn.onclick = () => selectFile(fIndex, btn);
      fileSelector.appendChild(btn);
    });

    if (currentBundle.files.length > 0) {
      selectFile(0, fileSelector.firstChild);
    }
  }

  function selectFile(index, btnElement, highlightSearchStr = null) {
    document.querySelectorAll('.file-btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');
    
    const file = currentBundle.files[index];
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
    
    currentBundle.files.forEach((file, fIndex) => {
      const btn = document.createElement('button');
      btn.className = 'file-btn';
      btn.textContent = file.filename.split('/').pop();
      btn.onclick = () => selectDiffFile(fIndex, btn);
      diffFileSelector.appendChild(btn);
    });

    if (currentBundle.files.length > 0) {
      selectDiffFile(0, diffFileSelector.firstChild);
    }
  }

  function selectDiffFile(index, btnElement) {
    document.getElementById('tab-diff').querySelectorAll('.file-btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');
    
    const file = currentBundle.files[index];
    let diffHtml = escapeHtml(file.diff_content || "No diff found.");
    
    // Style diffs
    diffHtml = diffHtml.split('\n').map(line => {
      if (line.startsWith('+') && !line.startsWith('+++')) {
        return `<span style="color: #4ade80; display: block; width: 100%; background: rgba(74, 222, 128, 0.15);">${line}</span>`;
      } else if (line.startsWith('-') && !line.startsWith('---')) {
        return `<span style="color: #f87171; display: block; width: 100%; background: rgba(248, 113, 113, 0.15);">${line}</span>`;
      }
      return line;
    }).join('\n');

    diffBlock.innerHTML = diffHtml;
  }

  function renderAgentReport() {
    if (currentBundle.agent_report && currentBundle.agent_report !== "Report not found.") {
      agentReportContent.innerHTML = marked.parse(currentBundle.agent_report);
    } else {
      agentReportContent.innerHTML = '<p style="color:var(--text-muted)">No markdown report found.</p>';
    }
  }

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      switchTab(btn.dataset.target);
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
