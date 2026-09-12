# F1 Race Strategy & Decision Intelligence

This project is a Python-based **Formula 1 race strategy and decision intelligence dashboard**. It transforms raw race-context signals into an explainable decision layer that reasons about:

- Whether a team should pit
- Whether an overtaking opportunity is worth pursuing
- Whether energy and active aerodynamics decisions are safe
- How much uncertainty is present in each option

The architecture follows an explainable decision pipeline:

1. **Collect** race signals (position, tyre age, energy, gaps)
2. **Estimate** strategy trade-offs (pit gain, overtake probability)
3. **Calculate** risk scores (safety car, tyre degradation)
4. **Explain** the recommended decision (confidence, expected value)

## Project Structure

```text
formula-one-all-roles/
├── app.py                                  # Flask application entry point
├── requirements.txt                        # Python dependencies
├── README.md                               # Project documentation
├── data/
│   └── sample_strategy_cases.csv          # Sample race scenario data
├── src/
│   ├── race_engine.py                     # Core strategy decision engine
│   └── __init__.py                        # Package initialization
├── templates/
│   └── index.html                         # Dashboard UI template
├── static/
│   ├── styles.css                         # Dashboard styling
│   └── script.js                          # Frontend logic
├── tests/
│   ├── __init__.py                        # Test package initialization
│   └── test_race_engine.py                # Unit tests
└── .gitignore                             # Git ignore rules
```

## Core Idea

The dashboard does not simply answer "who wins". Instead, it answers:

> **Given our race position, tyre age, energy level, overtaking opportunity, and risk tolerance, what is the smartest next race action?**

This provides better risk analysis and demonstrates software engineering principles for a professional portfolio.

## Expected Project Components

- ✅ Race scenario model (RaceScenario dataclass)
- ✅ Risk engine (risk calculation in RaceDecisionEngine)
- ✅ Overtake and energy recommendation engine (strategy logic)
- ✅ Dashboard UI (templates/index.html)
- ✅ Unit tests (tests/test_race_engine.py)
- ⏳ Notebook for explainability (notebooks/race_strategy_exploration.ipynb)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Himanshi2701/formula-one-all-roles.git
cd formula-one-all-roles
```

### Step 2: Install Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## API Endpoints

### Dashboard
- **GET** `/` — Serve the main dashboard page

### Strategy APIs
- **GET** `/api/decision` — Retrieve current race strategy recommendations and analysis

### Health Check
- **GET** `/api/health` — Check service status

## Example Usage

Once the server is running, the `/api/decision` endpoint returns JSON like:

```json
{
  "title": "F1 Race Strategy & Decision Intelligence",
  "race_state": {
    "race_control": "Live Simulation",
    "weather": "Clear",
    "active_aero_mode": "High Downforce",
    "overtake_mode": "Available"
  },
  "strategies": [
    {
      "lap": 24,
      "position": 4,
      "recommendation": "Stay Out and Monitor",
      "confidence": 0.66,
      "risk_band": "Low",
      "overtake_probability": 0.58
    }
  ],
  "recommended_strategy": { ... },
  "kpis": {
    "total_scenarios": 7,
    "top_strategy_confidence": 0.88,
    "mean_overtake_probability": 0.52,
    "high_risk_events": 0,
    "medium_risk_events": 2
  }
}
```

## Risk Bands

The engine classifies risk into three categories:

| Risk Band | Risk Score | Meaning |
|-----------|-----------|----------|
| **Low** | 0.00 - 0.30 | Safe to execute strategy |
| **Medium** | 0.30 - 0.60 | Moderate caution advised |
| **High** | 0.60 - 1.00 | High uncertainty, risky conditions |

## Strategy Recommendations

The engine generates one of four recommendations:

1. **Attack / Overtake Mode** — Conditions are ideal for aggressive overtaking
2. **Pit Now** — Tyres are degraded; pit stop has high expected value
3. **Plan Next Pit Window** — Tyres aging; prepare for upcoming pit stop
4. **Stay Out and Monitor** — Current strategy is optimal; wait for better opportunity

## Confidence Scoring

Confidence ranges from 0.0 to 1.0 and reflects how certain the engine is about its recommendation:

- **High Confidence (0.80+)** — Strong data support for the decision
- **Medium Confidence (0.60-0.80)** — Reasonable but with some uncertainty
- **Low Confidence (<0.60)** — Limited certainty; external validation recommended

## Development & Testing

### Run Tests
```bash
pytest
```

### Add New Race Scenarios
Edit `data/sample_strategy_cases.csv` or load from a real telemetry API.

### Modify Strategy Logic
Update the `make_strategy()` method in `src/race_engine.py` to adjust decision thresholds.

## Future Enhancements

- [ ] Integration with real F1 telemetry data (via unofficial APIs)
- [ ] Multi-agent simulation (team strategy coordination)
- [ ] Real-time WebSocket updates
- [ ] Machine learning model for confidence prediction
- [ ] Pit crew optimization (time prediction, crew assignments)
- [ ] Weather impact modeling

## License

This project is open source. See LICENSE file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## Contact & Support

For questions or issues, please open a GitHub Issue on this repository.

---

**Last Updated:** September 2026  
**Status:** Active Development
