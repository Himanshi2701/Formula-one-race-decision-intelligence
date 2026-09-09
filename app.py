from flask import Flask, jsonify, render_template
from src.race_engine import RaceDecisionEngine

app = Flask(__name__)
engine = RaceDecisionEngine("data/sample_strategy_cases.csv")

@app.route('/')
def index():
    """Serve the dashboard page for the F1 race strategy project."""
    return render_template('index.html')

@app.route('/api/decision')
def decision():
    """Provide an explainable JSON payload to the frontend dashboard."""
    return jsonify(engine.get_dashboard_payload())

@app.route('/api/health')
def health():
    """A small health check endpoint for the project service."""
    return jsonify({"status": "ok", "project": "F1 Race Strategy & Decision Intelligence"})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
