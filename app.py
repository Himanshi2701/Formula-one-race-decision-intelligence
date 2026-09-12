"""
F1 Race Strategy & Decision Intelligence Dashboard
Main Flask application for serving the race strategy engine.
"""

from flask import Flask, jsonify, render_template, request
from src.race_engine import RaceDecisionEngine
import logging

# Initialize Flask app and logging
app = Flask(__name__, template_folder='templates', static_folder='static')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the race decision engine
try:
    engine = RaceDecisionEngine("data/sample_strategy_cases.csv")
    logger.info("Race Decision Engine initialized successfully")
except FileNotFoundError as e:
    logger.error(f"Failed to initialize engine: {e}")
    engine = None


@app.route('/')
def dashboard():
    """Serve the main dashboard page for the F1 race strategy project."""
    return render_template('index.html')


@app.route('/api/decision', methods=['GET'])
def get_decision():
    """
    Provide an explainable JSON payload to the frontend dashboard.
    Returns the current race state and strategy recommendations.
    """
    if not engine:
        return jsonify({"error": "Engine not initialized"}), 500
    
    try:
        payload = engine.get_dashboard_payload()
        return jsonify(payload)
    except Exception as e:
        logger.error(f"Error generating decision payload: {e}")
        return jsonify({"error": "Failed to generate strategy"}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint for service monitoring."""
    return jsonify({
        "status": "ok",
        "project": "F1 Race Strategy & Decision Intelligence",
        "engine_ready": engine is not None,
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors gracefully."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors gracefully."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
