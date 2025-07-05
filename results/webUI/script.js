// Global variables
let allModels = [];
let currentModel = null;
let allResults = {};
let filteredQuestions = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    try {
        await loadAvailableModels();
        await loadAllResults();
        setupEventListeners();
        
        // Load first model by default
        if (allModels.length > 0) {
            const firstModel = allModels[0];
            document.getElementById('model-select').value = firstModel;
            await loadModelData(firstModel);
        }
        
        hideLoading();
    } catch (error) {
        console.error('Error initializing app:', error);
        showError();
    }
}

async function loadAvailableModels() {
    try {
        // Load the dynamically generated models list
        const response = await fetch('models.json');
        if (!response.ok) {
            throw new Error('Could not load models list');
        }
        
        const data = await response.json();
        const modelDirs = data.models || [];
        
        const modelSelect = document.getElementById('model-select');
        modelSelect.innerHTML = '';
        
        for (const dir of modelDirs) {
            try {
                const response = await fetch(`../${dir}/benchmark_results.json`);
                if (response.ok) {
                    allModels.push(dir);
                    const option = document.createElement('option');
                    option.value = dir;
                    option.textContent = formatModelName(dir);
                    modelSelect.appendChild(option);
                }
            } catch (error) {
                console.warn(`Could not load model ${dir}:`, error);
            }
        }
        
        if (allModels.length === 0) {
            throw new Error('No models found');
        }
    } catch (error) {
        console.error('Error loading models list:', error);
        throw error;
    }
}

async function loadAllResults() {
    for (const model of allModels) {
        try {
            const response = await fetch(`../${model}/benchmark_results.json`);
            if (response.ok) {
                allResults[model] = await response.json();
            }
        } catch (error) {
            console.warn(`Could not load results for ${model}:`, error);
        }
    }
}

async function loadModelData(modelName) {
    try {
        currentModel = modelName;
        const data = allResults[modelName];
        
        if (!data) {
            throw new Error(`No data found for model: ${modelName}`);
        }
        
        updateOverview(data);
        updateDetailedView(data);
        
    } catch (error) {
        console.error('Error loading model data:', error);
        showError();
    }
}

function setupEventListeners() {
    // Model selector
    document.getElementById('model-select').addEventListener('change', function(e) {
        if (e.target.value) {
            loadModelData(e.target.value);
        }
    });
    
    // View toggle
    document.getElementById('overview-btn').addEventListener('click', function() {
        showOverview();
    });
    
    document.getElementById('detailed-btn').addEventListener('click', function() {
        showDetailed();
    });
    
    // Search and filter
    document.getElementById('search-input').addEventListener('input', function(e) {
        applyFilters();
    });
    
    document.getElementById('score-filter').addEventListener('change', function(e) {
        applyFilters();
    });
    
    // Modal
    document.querySelector('.close').addEventListener('click', function() {
        closeModal();
    });
    
    window.addEventListener('click', function(e) {
        const modal = document.getElementById('question-modal');
        if (e.target === modal) {
            closeModal();
        }
    });
}

function updateOverview(data) {
    // Update stats
    document.getElementById('total-questions').textContent = data.total_questions;
    document.getElementById('average-score').textContent = (data.average_score * 100).toFixed(1) + '%';
    document.getElementById('duration').textContent = formatDuration(data.duration);
    document.getElementById('model-name').textContent = formatModelName(data.model);
    
    // Update charts
    updateScoreChart(data.question_scores);
    updateModelComparison();
}

function updateDetailedView(data) {
    filteredQuestions = data.question_scores;
    renderQuestions();
}

function updateScoreChart(scores) {
    const chart = document.getElementById('score-chart');
    
    // Create score distribution
    const ranges = [
        { min: 0, max: 0.2, label: '0-20%', color: '#f8d7da' },
        { min: 0.2, max: 0.4, label: '20-40%', color: '#ffeaa7' },
        { min: 0.4, max: 0.6, label: '40-60%', color: '#fdcb6e' },
        { min: 0.6, max: 0.8, label: '60-80%', color: '#a29bfe' },
        { min: 0.8, max: 1.0, label: '80-100%', color: '#6c5ce7' }
    ];
    
    const distribution = ranges.map(range => {
        const count = scores.filter(q => q.score >= range.min && q.score < range.max).length;
        return { ...range, count };
    });
    
    // Handle perfect scores (1.0)
    const perfectScores = scores.filter(q => q.score === 1.0).length;
    distribution[4].count += perfectScores;
    
    const maxCount = Math.max(...distribution.map(d => d.count));
    
    chart.innerHTML = `
        <div style="display: flex; align-items: end; gap: 16px; height: 250px; width: 100%; padding: 0 20px; justify-content: center;">
            ${distribution.map(d => `
                <div style="flex: 1; display: flex; flex-direction: column; align-items: center; max-width: 120px;">
                    <div style="
                        width: 100%; 
                        height: ${(d.count / maxCount) * 180}px; 
                        background: ${d.color}; 
                        border-radius: 6px 6px 0 0;
                        margin-bottom: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;
                        font-size: 14px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    ">
                        ${d.count}
                    </div>
                    <div style="font-size: 12px; color: #666; text-align: center; font-weight: 500;">
                        ${d.label}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function updateModelComparison() {
    const chart = document.getElementById('comparison-chart');
    
    if (Object.keys(allResults).length < 2) {
        chart.innerHTML = '<p style="text-align: center; color: #666; font-style: italic;">Load multiple models to see comparison</p>';
        return;
    }
    
    const comparison = Object.entries(allResults).map(([modelKey, data]) => ({
        modelKey: modelKey,
        model: formatModelName(modelKey),
        score: data.average_score,
        duration: data.duration,
        questions: data.total_questions
    })).sort((a, b) => b.score - a.score);
    
    const maxScore = Math.max(...comparison.map(c => c.score));
    
    chart.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 16px; padding: 0 20px; width: 100%;">
            ${comparison.map((c, index) => {
                const isSelected = c.modelKey === currentModel;
                const barColor = isSelected ? '#667eea' : (index === 0 ? '#6c5ce7' : '#a29bfe');
                const textWeight = isSelected ? 'bold' : '500';
                const borderStyle = isSelected ? 'border: 2px solid #667eea;' : '';
                
                return `
                <div style="display: flex; align-items: center; gap: 16px; ${borderStyle} border-radius: 8px; padding: 8px;">
                    <div style="min-width: 300px; font-weight: ${textWeight}; color: #333; font-size: 14px;">
                        ${c.model}
                    </div>
                    <div style="flex: 1; background: #f0f0f0; border-radius: 6px; height: 32px; position: relative; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="
                            width: ${(c.score / maxScore) * 95}%; 
                            height: 100%; 
                            background: linear-gradient(135deg, ${barColor}, ${barColor}dd); 
                            border-radius: 6px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            font-size: 13px;
                            font-weight: bold;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            transition: all 0.3s ease;
                        ">
                            ${(c.score * 100).toFixed(1)}%
                        </div>
                    </div>
                </div>`;
            }).join('')}
        </div>
    `;
}

function updatePerformanceTimeChart() {
    const chart = document.getElementById('performance-time-chart');
    chart.innerHTML = '';
}

function renderQuestions() {
    const grid = document.getElementById('questions-grid');
    grid.innerHTML = '';
    
    filteredQuestions.forEach((question, index) => {
        const card = createQuestionCard(question, index);
        grid.appendChild(card);
    });
}

function createQuestionCard(question, index) {
    const card = document.createElement('div');
    card.className = 'question-card';
    card.addEventListener('click', () => openQuestionModal(question, index));
    
    const scoreClass = getScoreClass(question.score);
    
    card.innerHTML = `
        <div class="question-header">
            <span class="question-number">Question ${question.question_index + 1}</span>
            <span class="question-score ${scoreClass}">${(question.score * 100).toFixed(1)}%</span>
        </div>
        <div class="question-prompt">${question.prompt}</div>
        <div class="question-preview" id="preview-${index}">
            <span style="color: #999;">Loading preview...</span>
        </div>
    `;
    
    // Load SVG preview
    loadSVGPreview(question.question_index, index);
    
    return card;
}

async function loadSVGPreview(questionIndex, cardIndex) {
    try {
        const response = await fetch(`../${currentModel}/question_${questionIndex}.svg`);
        if (response.ok) {
            const svgContent = await response.text();
            const previewElement = document.getElementById(`preview-${cardIndex}`);
            if (previewElement) {
                previewElement.innerHTML = svgContent;
            }
        }
    } catch (error) {
        console.warn(`Could not load SVG preview for question ${questionIndex}:`, error);
        const previewElement = document.getElementById(`preview-${cardIndex}`);
        if (previewElement) {
            previewElement.innerHTML = '<span style="color: #999;">Preview not available</span>';
        }
    }
}

async function openQuestionModal(question, index) {
    const modal = document.getElementById('question-modal');
    const scoreClass = getScoreClass(question.score);
    
    // Update modal content
    document.getElementById('modal-question-title').textContent = `Question ${question.question_index + 1}`;
    document.getElementById('modal-score').textContent = `${(question.score * 100).toFixed(1)}%`;
    document.getElementById('modal-score').className = `modal-score ${scoreClass}`;
    document.getElementById('modal-prompt-text').textContent = question.prompt;
    
    // Update requirements
    const requirementsList = document.getElementById('modal-requirements-list');
    requirementsList.innerHTML = '';
    question.requirements.forEach(req => {
        const li = document.createElement('li');
        li.textContent = req;
        requirementsList.appendChild(li);
    });
    
    // Load SVG
    const svgPreview = document.getElementById('modal-svg-preview');
    svgPreview.innerHTML = '<span style="color: #999;">Loading SVG...</span>';
    
    try {
        const response = await fetch(`../${currentModel}/question_${question.question_index}.svg`);
        if (response.ok) {
            const svgContent = await response.text();
            svgPreview.innerHTML = svgContent;
        } else {
            svgPreview.innerHTML = '<span style="color: #999;">SVG not available</span>';
        }
    } catch (error) {
        console.warn(`Could not load SVG for question ${question.question_index}:`, error);
        svgPreview.innerHTML = '<span style="color: #999;">Error loading SVG</span>';
    }
    
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('question-modal').style.display = 'none';
}

function applyFilters() {
    if (!currentModel || !allResults[currentModel]) return;
    
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const scoreFilter = document.getElementById('score-filter').value;
    
    const allQuestions = allResults[currentModel].question_scores;
    
    filteredQuestions = allQuestions.filter(question => {
        // Search filter
        const matchesSearch = searchTerm === '' || 
            question.prompt.toLowerCase().includes(searchTerm) ||
            question.requirements.some(req => req.toLowerCase().includes(searchTerm));
        
        // Score filter
        let matchesScore = true;
        if (scoreFilter === 'high') {
            matchesScore = question.score >= 0.8;
        } else if (scoreFilter === 'medium') {
            matchesScore = question.score >= 0.5 && question.score < 0.8;
        } else if (scoreFilter === 'low') {
            matchesScore = question.score < 0.5;
        }
        
        return matchesSearch && matchesScore;
    });
    
    renderQuestions();
}

function showOverview() {
    document.getElementById('overview-btn').classList.add('active');
    document.getElementById('detailed-btn').classList.remove('active');
    document.getElementById('overview-section').style.display = 'block';
    document.getElementById('detailed-section').style.display = 'none';
}

function showDetailed() {
    document.getElementById('overview-btn').classList.remove('active');
    document.getElementById('detailed-btn').classList.add('active');
    document.getElementById('overview-section').style.display = 'none';
    document.getElementById('detailed-section').style.display = 'block';
}

function getScoreClass(score) {
    if (score >= 0.8) return 'score-high';
    if (score >= 0.5) return 'score-medium';
    return 'score-low';
}

function formatModelName(modelName) {
    return modelName; // Return raw model name without any formatting
}

function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}m ${remainingSeconds}s`;
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error').style.display = 'block';
}

 