async function loadDashboard() {
    const response = await fetch('/api/decision');
    const data = await response.json();

    document.getElementById('risk-score').textContent = data.overall_risk_score;
    document.getElementById('overtake-prob').textContent = data.kpis.mean_overtake_probability + '%';
    document.getElementById('confidence').textContent = data.kpis.top_strategy_confidence;
    document.getElementById('risk-events').textContent = data.kpis.risk_events;

    const recommended = data.recommended_strategy;
    document.getElementById('recommended-scenario').textContent = recommended.scenario;
    document.getElementById('confidence-badge').textContent = 'Confidence ' + recommended.confidence;
    document.getElementById('decision-lap').textContent = recommended.lap;
    document.getElementById('decision-position').textContent = recommended.position;
    document.getElementById('decision-value').textContent = recommended.expected_value;
    document.getElementById('decision-energy').textContent = recommended.energy_available + '%';
    document.getElementById('decision-explanation').textContent = recommended.decision_explanation;

    document.getElementById('risk-band').textContent = recommended.risk_band;
    const riskValue = Math.round(recommended.risk_probability * 100);
    document.getElementById('meter-fill').style.width = riskValue + '%';
    document.getElementById('risk-probability').textContent = riskValue + '%';

    const table = document.getElementById('strategy-table');
    table.innerHTML = '';

    data.strategies.forEach((item) => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.lap}</td>
            <td>${item.tyre_compound}</td>
            <td>${item.scenario}</td>
            <td>${item.overtake_probability}%</td>
            <td>${item.risk_probability}</td>
            <td>${item.expected_position_gain}</td>
            <td>${item.expected_value}</td>`;
        table.appendChild(row);
    });
}

loadDashboard();
