import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.race_engine import RaceDecisionEngine


def test_load_scenarios_from_sample_data():
    engine = RaceDecisionEngine('data/sample_strategy_cases.csv')
    assert len(engine.scenarios) == 5


def test_dashboard_payload_contains_expected_keys():
    engine = RaceDecisionEngine('data/sample_strategy_cases.csv')
    payload = engine.get_dashboard_payload()

    assert payload['title'] == 'F1 Race Strategy & Decision Intelligence'
    assert 'strategies' in payload
    assert 'recommended_strategy' in payload
    assert 'kpis' in payload
    assert payload['kpis']['mean_overtake_probability'] >= 0


def test_recommendation_is_explainable_and_current():
    engine = RaceDecisionEngine('data/sample_strategy_cases.csv')
    first = engine.scenarios[0]
    strategy = engine.make_strategy(first)

    assert 'scenario' in strategy
    assert 'decision_explanation' in strategy
    assert isinstance(strategy['decision_explanation'], str)
