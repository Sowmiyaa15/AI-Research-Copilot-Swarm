const API_URL = 'http://localhost:5000/api';

// Event listeners
document.getElementById('searchBtn').addEventListener('click', handleSearch);
document.getElementById('queryInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSearch();
});

async function handleSearch() {
    const query = document.getElementById('queryInput').value.trim();
    
    if (!query) {
        showError('Please enter a research query');
        return;
    }
    
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_URL}/research`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }
        
        if (data.success) {
            displayResults(data.results);
        } else {
            throw new Error(data.message || 'Analysis failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}. Please check if the backend server is running.`);
        hideLoading();
    }
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    // Animate progress steps
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach((step, index) => {
        setTimeout(() => {
            step.classList.add('active');
        }, index * 500);
    });
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach(step => step.classList.remove('active'));
}

function showError(message) {
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('errorText').textContent = message;
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function displayResults(results) {
    hideLoading();
    document.getElementById('results').classList.remove('hidden');
    
    // Display summary
    displaySummary(results.summary);
    
    // Display each section
    displayRetrievedPapers(results.retrieved_papers);
    displayKnowledgeExtraction(results.extracted_knowledge);
    displayMethodComparison(results.method_comparison);
    displayClaimValidation(results.validation);
    displayResearchGaps(results.research_gaps);
    displayResearchIdeas(results.research_ideas);
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function displaySummary(summary) {
    const container = document.getElementById('summaryContent');
    
    const html = `
        <div class="summary-card">
            <p class="summary-text">${summary.text}</p>
            <div class="statistics">
                <div class="stat">
                    <span class="stat-number">${summary.statistics.papers_analyzed}</span>
                    <span class="stat-label">Papers Analyzed</span>
                </div>
                <div class="stat">
                    <span class="stat-number">${summary.statistics.methods_identified}</span>
                    <span class="stat-label">Methods Identified</span>
                </div>
                <div class="stat">
                    <span class="stat-number">${summary.statistics.gaps_found}</span>
                    <span class="stat-label">Gaps Found</span>
                </div>
                <div class="stat">
                    <span class="stat-number">${summary.statistics.ideas_generated}</span>
                    <span class="stat-label">Ideas Generated</span>
                </div>
            </div>
            ${summary.key_insights.length > 0 ? `
                <div class="key-insights">
                    <h4>Key Insights:</h4>
                    <ul>
                        ${summary.key_insights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
    
    container.innerHTML = html;
}

function displayRetrievedPapers(data) {
    const container = document.getElementById('retrievedPapers');
    
    if (!data.papers || data.papers.length === 0) {
        container.innerHTML = '<p class="no-data">No papers retrieved</p>';
        return;
    }
    
    const html = data.papers.map(paper => `
        <div class="card">
            <div class="card-header">
                <h3>${paper.title}</h3>
                <span class="badge">${paper.source}</span>
            </div>
            <div class="card-body">
                <p><strong>Authors:</strong> ${paper.authors}</p>
                <p class="abstract">${paper.abstract}</p>
                <a href="${paper.url}" target="_blank" class="link">View on arXiv →</a>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function displayKnowledgeExtraction(data) {
    const container = document.getElementById('knowledgeExtraction');
    
    if (!data.knowledge_items || data.knowledge_items.length === 0) {
        container.innerHTML = '<p class="no-data">No knowledge extracted</p>';
        return;
    }
    
    const html = data.knowledge_items.map(item => `
        <div class="card">
            <div class="card-header">
                <h3>${item.paper_title}</h3>
                <span class="badge badge-domain">${item.problem_domain}</span>
            </div>
            <div class="card-body">
                <div class="info-section">
                    <strong>🔧 Methods:</strong>
                    <p>${item.methods}</p>
                </div>
                <div class="info-section">
                    <strong>🎯 Key Findings:</strong>
                    <p>${item.key_findings}</p>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function displayMethodComparison(data) {
    const container = document.getElementById('methodComparison');
    
    if (!data.methods || data.methods.length === 0) {
        container.innerHTML = '<p class="no-data">No methods to compare</p>';
        return;
    }
    
    let html = `
        <div class="card highlight-card">
            <div class="card-header">
                <h3>🏆 Best Performing Method</h3>
            </div>
            <div class="card-body">
                <p class="best-method">${data.best_performing}</p>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h3>Methods Identified</h3>
            </div>
            <div class="card-body">
                <div class="method-list">
                    ${data.methods.map(method => `<span class="method-tag">${method}</span>`).join('')}
                </div>
            </div>
        </div>
    `;
    
    if (data.strengths && data.strengths.length > 0) {
        html += `
            <div class="card">
                <div class="card-header">
                    <h3>💪 Strengths</h3>
                </div>
                <div class="card-body">
                    ${data.strengths.map(item => `
                        <div class="strength-weakness-item">
                            <h4>${item.method}</h4>
                            <ul>
                                ${item.points.map(point => `<li>${point}</li>`).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    if (data.weaknesses && data.weaknesses.length > 0) {
        html += `
            <div class="card">
                <div class="card-header">
                    <h3>⚠️ Weaknesses</h3>
                </div>
                <div class="card-body">
                    ${data.weaknesses.map(item => `
                        <div class="strength-weakness-item">
                            <h4>${item.method}</h4>
                            <ul>
                                ${item.points.map(point => `<li>${point}</li>`).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

function displayClaimValidation(data) {
    const container = document.getElementById('claimValidation');
    
    const html = `
        <div class="card highlight-card">
            <div class="card-header">
                <h3>📈 Confidence Score</h3>
            </div>
            <div class="card-body">
                <p class="confidence-score">${data.confidence_score}</p>
            </div>
        </div>
        
        ${data.consistent_claims && data.consistent_claims.length > 0 ? `
            <div class="card">
                <div class="card-header">
                    <h3>✅ Consistent Claims (${data.total_consistent})</h3>
                </div>
                <div class="card-body">
                    ${data.consistent_claims.map(claim => `
                        <div class="claim-item consistent">
                            <p><strong>${claim.claim}</strong></p>
                            <p class="claim-meta">
                                Supported by: ${claim.supporting_methods.join(', ')}
                                <span class="evidence-badge">${claim.evidence_count} evidence</span>
                            </p>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
        
        ${data.conflicting_claims && data.conflicting_claims.length > 0 ? `
            <div class="card">
                <div class="card-header">
                    <h3>⚡ Conflicting Claims (${data.total_conflicting})</h3>
                </div>
                <div class="card-body">
                    ${data.conflicting_claims.map(claim => `
                        <div class="claim-item conflicting">
                            <p><strong>${claim.claim}</strong></p>
                            <p class="claim-description">${claim.description}</p>
                            ${claim.supporting_methods.length > 0 ? `
                                <p class="claim-meta">Supporting: ${claim.supporting_methods.join(', ')}</p>
                            ` : ''}
                            ${claim.opposing_methods.length > 0 ? `
                                <p class="claim-meta">Opposing: ${claim.opposing_methods.join(', ')}</p>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
    `;
    
    container.innerHTML = html;
}

function displayResearchGaps(data) {
    const container = document.getElementById('researchGaps');
    
    if (!data.all_gaps || data.all_gaps.length === 0) {
        container.innerHTML = '<p class="no-data">No research gaps identified</p>';
        return;
    }
    
    const html = `
        <div class="card">
            <div class="card-header">
                <h3>🔍 Identified Gaps (${data.total_gaps})</h3>
            </div>
            <div class="card-body">
                <div class="gap-list">
                    ${data.all_gaps.map((gap, index) => `
                        <div class="gap-item">
                            <span class="gap-number">${index + 1}</span>
                            <p>${gap}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
        
        ${Object.keys(data.categorized).some(key => data.categorized[key].length > 0) ? `
            <div class="card">
                <div class="card-header">
                    <h3>📂 Categorized Gaps</h3>
                </div>
                <div class="card-body">
                    ${Object.entries(data.categorized).map(([category, gaps]) => 
                        gaps.length > 0 ? `
                            <div class="category-section">
                                <h4>${category.replace('_', ' ').toUpperCase()}</h4>
                                <ul>
                                    ${gaps.map(gap => `<li>${gap}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''
                    ).join('')}
                </div>
            </div>
        ` : ''}
    `;
    
    container.innerHTML = html;
}

function displayResearchIdeas(data) {
    const container = document.getElementById('researchIdeas');
    
    if (!data.all_ideas || data.all_ideas.length === 0) {
        container.innerHTML = '<p class="no-data">No research ideas generated</p>';
        return;
    }
    
    const html = data.all_ideas.map((idea, index) => `
        <div class="card idea-card ${index === 0 ? 'top-idea' : ''}">
            <div class="card-header">
                <h3>${index === 0 ? '⭐ ' : ''}${idea.idea}</h3>
                <span class="badge badge-impact">${idea.impact.split('-')[0].trim()}</span>
            </div>
            <div class="card-body">
                <div class="info-section">
                    <strong>🎯 Gap Addressed:</strong>
                    <p>${idea.gap_addressed}</p>
                </div>
                <div class="info-section">
                    <strong>🔬 Proposed Method:</strong>
                    <p>${idea.proposed_method}</p>
                </div>
                <div class="info-section">
                    <strong>📊 Impact:</strong>
                    <p>${idea.impact}</p>
                </div>
                <div class="info-section">
                    <strong>✅ Feasibility:</strong>
                    <p>${idea.feasibility}</p>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}
