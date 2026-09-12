"""Unit tests for the race engine"""

import pytest
from src.race_engine import RaceScenario, RaceDecisionEngine


class TestRaceScenario:
    """Test RaceScenario dataclass"""

    def test_scenario_creation(self):
        """Test creating a race scenario"""
        scenario = RaceScenario(
            lap=24,
            position=4,
            tyre_age=12.0,
            tyre_compound="Soft",
            gap_to_car_ahead=0.7,
            attack_window=True,
            energy_available=76,
            overtake_mode=True,
            safety_car_probability=0.14,
        )
        
        assert scenario.lap == 24
        assert scenario.position == 4
        assert scenario.tyre_compound == "Soft"


class TestRaceDecisionEngine:
    """Test RaceDecisionEngine class"""

    def test_engine_initialization(self):
        """Test engine loads data correctly"""
        engine = RaceDecisionEngine("data/sample_strategy_cases.csv")
        assert engine.scenarios is not None
        assert len(engine.scenarios) > 0

    def test_make_strategy(self):
        """Test strategy generation"""
        engine = RaceDecisionEngine("data/sample_strategy_cases.csv")
        scenario = engine.scenarios[0]
        strategy = engine.make_strategy(scenario)
        
        assert 'recommendation' in strategy
        assert 'confidence' in strategy
        assert 'risk_band' in strategy
        assert strategy['confidence'] >= 0.0 and strategy['confidence'] <= 1.0

    def test_risk_bands(self):
        """Test risk band categorization"""
        engine = RaceDecisionEngine("data/sample_strategy_cases.csv")
        
        # Test multiple scenarios to ensure risk bands are correctly assigned
        for scenario in engine.scenarios:
            strategy = engine.make_strategy(scenario)
            risk_band = strategy['risk_band']
            assert risk_band in ['Low', 'Medium', 'High']

    def test_dashboard_payload(self):
        """Test dashboard payload generation"""
        engine = RaceDecisionEngine("data/sample_strategy_cases.csv")
        payload = engine.get_dashboard_payload()
        
        assert 'strategies' in payload
        assert 'recommended_strategy' in payload
        assert 'kpis' in payload
        assert payload['title'] == 'F1 Race Strategy & Decision Intelligence'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
