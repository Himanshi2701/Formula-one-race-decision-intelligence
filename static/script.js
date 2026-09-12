/**
 * F1 Race Strategy Dashboard - Frontend Script
 * Fetches strategy data and updates the UI in real-time
 */

const API_DECISION_URL = '/api/decision';
const API_HEALTH_URL = '/api/health';
const REFRESH_INTERVAL = 5000; // 5 seconds

let autoRefreshEnabled = true;

/**
 * Fetch strategy decision data from the backend
 */
async function fetchStrategyData() {
    try {
        const response = await fetch(API_DECISION_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        updateDashboard(data);
        updateHealthStatus(true);
    } catch (error) {
        console.error('Error fetching strategy data:', error);
        updateHealthStatus(false);
        displayErrorMessage(error.message);
    }
}

/**
 * Update all dashboard sections with new data
 */
function updateDashboard(data) {
    if (data.error) {
        displayErrorMessage(data.error);
        return;
    }

    // Update race state
    updateRaceState(data.race_state);

    // Update KPIs
    updateKPIs(data.kpis);

    // Update recommended strategy
    updateRecommendedStrategy(data.recommended_strategy);

    // Update all scenarios
    updateScenarios(data.strategies);
}

/**
 * Update race state section
 */
function updateRaceState(state) {
    document.getElementById('race-control').textContent = state.race_control || '—';
    document.getElementById('weather').textContent = state.weather || '—';
    document.getElementById('aero-mode').textContent = state.active_aero_mode || '—';
    document.getElementById('overtake-mode').textContent = state.overtake_mode || '—';
}

/**
 * Update KPI cards
 */
function updateKPIs(kpis) {
    document.getElementById('kpi-total').textContent = kpis.total_scenarios || 0;
    document.getElementById('kpi-confidence').textContent = `${Math.round(kpis.top_strategy_confidence * 100)}%`;
    document.getElementById('kpi-overtake').textContent = `${Math.round(kpis.mean_overtake_probability * 100)}%`;
    document.getElementById('kpi-high-risk').textContent = kpis.high_risk_events || 0;
    document.getElementById('kpi-medium-risk').textContent = kpis.medium_risk_events || 0;
    document.getElementById('kpi-risk').textContent = (kpis.overall_risk_score || 0).toFixed(2);
}

/**
 * Update recommended strategy section
 */
function updateRecommendedStrategy(strategy) {
    if (!strategy) {
        document.getElementById('recommended-title').textContent = 'No Data Available';
        return;
    }

    document.getElementById('recommended-title').textContent = strategy.recommendation;
    document.getElementById('recommended-explanation').textContent = strategy.decision_explanation;
    document.getElementById('recommended-value').textContent = strategy.expected_value.toFixed(2);
    document.getElementById('recommended-gain').textContent = strategy.expected_position_gain;

    // Update risk band badge
    const riskBadge = document.getElementById('recommended-risk');
    riskBadge.textContent = strategy.risk_band;
    riskBadge.className = `metric-value risk-band ${strategy.risk_band.toLowerCase()}`;

    // Update confidence badge
    const confidenceBadge = document.getElementById('confidence-badge');
    const confidencePercent = Math.round(strategy.confidence * 100);
    confidenceBadge.textContent = `${confidencePercent}% Confidence`;

    // Color code by confidence level
    if (strategy.confidence >= 0.80) {
        confidenceBadge.style.background = 'var(--success-color)';
    } else if (strategy.confidence >= 0.60) {
        confidenceBadge.style.background = 'var(--warning-color)';
    } else {
        confidenceBadge.style.background = 'var(--danger-color)';
    }
}

/**
 * Update all race scenarios grid
 */
function updateScenarios(scenarios) {
    const container = document.getElementById('scenarios-container');

    if (!scenarios || scenarios.length === 0) {
        container.innerHTML = '<p class="loading">No scenarios available</p>';
        return;
    }

    container.innerHTML = scenarios.map(scenario => createScenarioCard(scenario)).join('');
}

/**
 * Create HTML for a single scenario card
 */
function createScenarioCard(scenario) {
    const riskClass = scenario.risk_band.toLowerCase();
    const confidencePercent = Math.round(scenario.confidence * 100);
    const overtakePercent = Math.round(scenario.overtake_probability * 100);

    return `
        <div class="scenario-item">
            <div class="lap-position">
                <span class="lap">Lap ${scenario.lap}</span>
                <span class="position">P${scenario.position}</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Strategy:</span>
                <span class="metric-val">${scenario.recommendation}</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Tyre:</span>
                <span class="metric-val">${scenario.tyre_compound}</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Confidence:</span>
                <span class="metric-val">${confidencePercent}%</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Overtake Prob:</span>
                <span class="metric-val">${overtakePercent}%</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Risk Band:</span>
                <span class="metric-val risk-band ${riskClass}">${scenario.risk_band}</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Energy:</span>
                <span class="metric-val">${scenario.energy_available.toFixed(1)}%</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Expected Value:</span>
                <span class="metric-val">${scenario.expected_value.toFixed(2)}</span>
            </div>
            
            <div class="metric-row">
                <span class="metric-label">Pit Gain:</span>
                <span class="metric-val">${scenario.pit_gain_seconds}s</span>
            </div>
        </div>
    `;
}

/**
 * Update health status indicator
 */
function updateHealthStatus(isHealthy) {
    const indicator = document.getElementById('status-indicator');
    if (isHealthy) {
        indicator.className = 'status ok';
        indicator.textContent = '✓ System Healthy';
    } else {
        indicator.className = 'status error';
        indicator.textContent = '✗ Connection Error';
    }
}

/**
 * Display error message to user
 */
function displayErrorMessage(message) {
    const container = document.getElementById('scenarios-container');
    if (container) {
        container.innerHTML = `<p class="loading" style="color: #ff6b6b;">Error: ${message}</p>`;
    }
}

/**
 * Check API health
 */
async function checkHealth() {
    try {
        const response = await fetch(API_HEALTH_URL);
        return response.ok;
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}

/**
 * Initialize auto-refresh
 */
function initializeAutoRefresh() {
    // Fetch data immediately
    fetchStrategyData();

    // Set up interval for auto-refresh
    setInterval(() => {
        if (autoRefreshEnabled) {
            fetchStrategyData();
        }
    }, REFRESH_INTERVAL);
}

/**
 * Page load event
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard initialized');
    initializeAutoRefresh();

    // Optional: Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'r' || e.key === 'R') {
            console.log('Manual refresh triggered');
            fetchStrategyData();
        }
    });
});

/**
 * Handle page visibility change (pause refresh when tab is not active)
 */
document.addEventListener('visibilitychange', () => {
    autoRefreshEnabled = !document.hidden;
    if (autoRefreshEnabled) {
        console.log('Dashboard tab active - resuming refresh');
        fetchStrategyData();
    } else {
        console.log('Dashboard tab hidden - pausing refresh');
    }
});

// Log dashboard readiness
console.log('F1 Race Strategy Dashboard initialized - Press R to refresh manually');
