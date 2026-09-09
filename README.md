# F1 Race Strategy & Decision Intelligence

This project is a Python-based **Formula 1 race strategy and risk intelligence dashboard**. It turns raw race-context signals into a decision layer that reasons about:

- whether a team should pit
- whether an overtaking opportunity is worth attacking
- whether energy and active aero decisions are safe
- how much uncertainty is present in each option

The architecture follows an explainable decision pipeline:

1. Collect race signals
2. Estimate strategy trade-offs
3. Apply a risk score
4. Explain the recommended decision

## Project structure

```text
F1-Race-Strategy-Decision-Engine/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_strategy_cases.csv
├── notebooks/
│   └── race_strategy_exploration.ipynb
├── src/
│   ├── race_engine.py
│   └── __init__.py
└── static/
    ├── script.js
    └── styles.css
```

## Core idea

The dashboard does not answer only "who wins". Instead, it answers:

> Given our race position, tyre age, energy level, overtaking opportunity and risk level, what is the smartest next race action?

That is a better risk-analysis and software-engineering story for a project portfolio.

## Why this is a good project story

The project combines the following themes:

- data analysis
- strategy analysis
- risk and probability reasoning
- business-style decision tradeoff analysis
- ML-style predictive thinking
- a small dashboard application
- agentic AI explanation layer

## Expected project components

- Race scenario model
- Risk engine
- Overtake and energy recommendation engine
- Dashboard UI
- Notebook for explainability

## How to run

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000>.
