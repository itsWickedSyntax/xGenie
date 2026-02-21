let currentScanId = null;
let scanInterval = null;
let scanData = null;

function startScan() {
    const target = document.getElementById('target').value.trim();
    const deep = document.getElementById('deepScan').checked;
    
    if (!target) {
        alert('Please enter a target domain or IP address');
        return;
    }
    
    // Disable button
    const btn = document.getElementById('scanBtn');
    btn.disabled = true;
    btn.textContent = 'Scanning...';
    
    // Show progress
    document.getElementById('scanProgress').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    
    // Start scan
    fetch('/api/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ target, deep })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            resetUI();
            return;
        }
        
        currentScanId = data.scan_id;
        checkScanStatus();
    })
    .catch(err => {
        alert('Error starting scan: ' + err);
        resetUI();
    });
}

function checkScanStatus() {
    scanInterval = setInterval(() => {
        fetch(`/api/scan/${currentScanId}/status`)
            .then(res => res.json())
            .then(data => {
                updateProgress(data.progress);
                
                if (data.status === 'completed') {
                    clearInterval(scanInterval);
                    loadResults();
                }
            })
            .catch(err => {
                clearInterval(scanInterval);
                alert('Error checking status: ' + err);
                resetUI();
            });
    }, 2000);
}

function updateProgress(progress) {
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('progressText').textContent = `Scanning... ${progress}%`;
}

function loadResults() {
    fetch(`/api/scan/${currentScanId}/results`)
        .then(res => res.json())
        .then(data => {
            scanData = data;
            displayResults(data);
            resetUI();
        })
        .catch(err => {
            alert('Error loading results: ' + err);
            resetUI();
        });
}

function displayResults(data) {
    document.getElementById('scanProgress').classList.add('hidden');
    document.getElementById('results').classList.remove('hidden');
    
    // WHOIS
    displayWhois(data.whois);
    
    // DNS
    displayDNS(data.dns);
    
    // Ports
    displayPorts(data.ports);
    
    // Tech Stack
    displayTech(data.tech_stack);
    
    // Security
    displaySecurity(data.security);
    
    // XSS
    displayXSS(data.xss);
}

function displayWhois(whois) {
    const container = document.getElementById('whoisData');
    
    if (!whois || whois.error) {
        container.innerHTML = '<p class="error">Unable to retrieve WHOIS data</p>';
        return;
    }
    
    let html = '';
    if (whois.registrar) html += `<p><strong>Registrar:</strong> ${whois.registrar}</p>`;
    if (whois.organization) html += `<p><strong>Organization:</strong> ${whois.organization}</p>`;
    if (whois.country) html += `<p><strong>Country:</strong> ${whois.country}</p>`;
    if (whois.creation_date) html += `<p><strong>Created:</strong> ${whois.creation_date}</p>`;
    if (whois.expiration_date) html += `<p><strong>Expires:</strong> ${whois.expiration_date}</p>`;
    
    container.innerHTML = html || '<p>No data available</p>';
}

function displayDNS(dns) {
    const container = document.getElementById('dnsData');
    
    if (!dns || dns.error) {
        container.innerHTML = '<p class="error">Unable to retrieve DNS data</p>';
        return;
    }
    
    let html = '';
    if (dns.A) html += `<p><strong>A Records:</strong> ${dns.A.join(', ')}</p>`;
    if (dns.MX) html += `<p><strong>MX Records:</strong> ${dns.MX.join(', ')}</p>`;
    if (dns.NS) html += `<p><strong>NS Records:</strong> ${dns.NS.join(', ')}</p>`;
    if (dns.spf) html += `<p><strong>SPF:</strong> ${dns.spf}</p>`;
    if (dns.dmarc) html += `<p><strong>DMARC:</strong> ${dns.dmarc}</p>`;
    
    container.innerHTML = html || '<p>No data available</p>';
}

function displayPorts(ports) {
    const container = document.getElementById('portsData');
    
    if (!ports || ports.error) {
        container.innerHTML = '<p class="error">Unable to retrieve port data</p>';
        return;
    }
    
    const openPorts = ports.open_ports || [];
    
    if (openPorts.length === 0) {
        container.innerHTML = '<p>No open ports detected</p>';
        return;
    }
    
    let html = '<table style="width:100%; color:#E0E0E0;"><tr><th>Port</th><th>Service</th><th>Banner</th></tr>';
    openPorts.forEach(port => {
        html += `<tr><td>${port.port}</td><td>${port.service}</td><td>${port.banner || 'N/A'}</td></tr>`;
    });
    html += '</table>';
    
    container.innerHTML = html;
}

function displayTech(tech) {
    const container = document.getElementById('techData');
    
    if (!tech || tech.error) {
        container.innerHTML = '<p class="error">Unable to retrieve technology data</p>';
        return;
    }
    
    let html = '';
    if (tech.web_server) html += `<p><strong>Web Server:</strong> ${tech.web_server}</p>`;
    if (tech.cms) html += `<p><strong>CMS:</strong> ${tech.cms}</p>`;
    if (tech.frameworks && tech.frameworks.length) html += `<p><strong>Frameworks:</strong> ${tech.frameworks.join(', ')}</p>`;
    if (tech.javascript_libraries && tech.javascript_libraries.length) html += `<p><strong>JS Libraries:</strong> ${tech.javascript_libraries.join(', ')}</p>`;
    if (tech.cdn) html += `<p><strong>CDN:</strong> ${tech.cdn}</p>`;
    
    container.innerHTML = html || '<p>No data available</p>';
}

function displaySecurity(security) {
    const container = document.getElementById('securityData');
    
    if (!security || security.error) {
        container.innerHTML = '<p class="error">Unable to retrieve security data</p>';
        return;
    }
    
    let html = '';
    
    if (security.risk_score !== undefined) {
        const riskClass = security.risk_score >= 70 ? 'severity-high' : security.risk_score >= 40 ? 'severity-medium' : 'severity-low';
        html += `<p><strong>Risk Score:</strong> <span class="${riskClass}">${security.risk_score}/100</span></p>`;
    }
    
    if (security.missing_headers && security.missing_headers.length) {
        html += `<p><strong>Missing Headers:</strong> <span class="severity-medium">${security.missing_headers.length}</span></p>`;
        html += '<ul style="margin-left: 20px;">';
        security.missing_headers.forEach(h => {
            html += `<li>${h}</li>`;
        });
        html += '</ul>';
    }
    
    if (security.vulnerabilities && security.vulnerabilities.length) {
        html += `<p><strong>Vulnerabilities:</strong> <span class="severity-high">${security.vulnerabilities.length} found</span></p>`;
    }
    
    container.innerHTML = html || '<p>No issues detected</p>';
}

function displayXSS(xss) {
    const container = document.getElementById('xssData');
    
    if (!xss || xss.error) {
        container.innerHTML = '<p class="error">XSS scan not performed or unable to retrieve data</p>';
        return;
    }
    
    let html = '';
    
    if (xss.scan_summary) {
        const summary = xss.scan_summary;
        html += `<p><strong>Endpoints Tested:</strong> ${xss.tested_endpoints || 0}</p>`;
        html += `<p><strong>Total Vulnerabilities:</strong> <span class="severity-high">${summary.total_vulnerabilities || 0}</span></p>`;
        
        if (summary.total_vulnerabilities > 0) {
            html += `<p><strong>Reflected XSS:</strong> ${summary.reflected_xss || 0}</p>`;
            html += `<p><strong>DOM-based XSS:</strong> ${summary.dom_based_xss || 0}</p>`;
            html += `<p><strong>High Risk:</strong> <span class="severity-high">${summary.high_risk || 0}</span></p>`;
        }
    }
    
    if (xss.vulnerabilities && xss.vulnerabilities.length > 0) {
        html += '<div style="margin-top: 15px;"><strong>Vulnerabilities:</strong></div>';
        xss.vulnerabilities.slice(0, 5).forEach(vuln => {
            const severityClass = `severity-${vuln.severity.toLowerCase()}`;
            html += `<div class="vulnerability">`;
            html += `<p><strong>${vuln.type}</strong> - <span class="${severityClass}">${vuln.severity}</span></p>`;
            html += `<p style="font-size: 0.9em;">URL: ${vuln.url}</p>`;
            if (vuln.parameter) html += `<p style="font-size: 0.9em;">Parameter: ${vuln.parameter}</p>`;
            html += `</div>`;
        });
    }
    
    container.innerHTML = html || '<p>No XSS vulnerabilities detected</p>';
}

function exportResults() {
    if (!scanData) return;
    
    const dataStr = JSON.stringify(scanData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `xgenie_scan_${Date.now()}.json`;
    link.click();
}

function resetUI() {
    const btn = document.getElementById('scanBtn');
    btn.disabled = false;
    btn.textContent = 'Start Reconnaissance';
}
