"""F1 Race Strategy & Decision Intelligence - Core Engine"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd


@dataclass
class RaceScenario:
    """Represents a single F1 race scenario with strategy inputs."""
    lap: int
    position: int
    tyre_age: float
    tyre_compound: str
    gap_to_car_ahead: float
    attack_window: bool
    energy_available: float
    overtake_mode: bool
    safety_car_probability: float


class RaceDecisionEngine:
    """Engine for generating explainable F1 race strategy decisions."""

    def __init__(self, dataset_path: str = "data/sample_strategy_cases.csv") -> None:
        self.dataset_path = dataset_path
        self.scenarios: List[RaceScenario] = self.load_scenarios(dataset_path)

    def load_scenarios(self, dataset_path: str) -> List[RaceScenario]:
        """Load scenario rows from a CSV dataset and convert them to scenario objects."""
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Scenario dataset not found: {dataset_path}")

        df = pd.read_csv(dataset_path)
        scenarios = []
        for _, row in df.iterrows():
            scenarios.append(
                RaceScenario(
                    lap=int(row['lap']),
                    position=int(row['position']),
                    tyre_age=float(row['tyre_age']),
                    tyre_compound=str(row['tyre_compound']),
                    gap_to_car_ahead=float(row['gap_to_car_ahead']),
                    attack_window=bool(row['attack_window']),
                    energy_available=float(row['energy_available']),
                    overtake_mode=bool(row['overtake_mode']),
                    safety_car_probability=float(row['safety_car_probability']),
                )
            )
        return scenarios

    def make_strategy(self, scenario: RaceScenario) -> Dict:
        """Create one explainable decision recommendation from one race scenario."""
        # Calculate pit stop time gain
        pit_gain = 2.9 if scenario.tyre_age > 20 else 1.8
        
        # Expected position gain from overtaking
        expected_position_gain = 1 if scenario.attack_window and scenario.gap_to_car_ahead < 1.2 else 0
        
        # Overtake success probability (clamped between 0.25 and 0.85)
        overtake_probability = min(
            0.85,
            max(
                0.25,
                0.48 + (1.2 - scenario.gap_to_car_ahead) * 0.12 + (scenario.energy_available / 100) * 0.18,
            ),
        )
        
        # Risk calculation with proper distribution to reach High risk
        risk = min(
            0.95,
            max(
                0.05,
                scenario.safety_car_probability * 0.4 + (0.35 if scenario.tyre_age > 22 else 0.05)
            )
        )

        # Decision logic based on race conditions
        if scenario.attack_window and scenario.overtake_mode and scenario.energy_available > 50:
            recommendation = 'Attack / Overtake Mode'
            confidence = 0.85
        elif scenario.tyre_age > 22:
            recommendation = 'Pit Now'
            confidence = 0.88
        elif scenario.tyre_age > 18:
            recommendation = 'Plan Next Pit Window'
            confidence = 0.72
        else:
            recommendation = 'Stay Out and Monitor'
            confidence = 0.66

        # Determine risk band
        if risk > 0.60:
            risk_band = 'High'
        elif risk > 0.30:
            risk_band = 'Medium'
        else:
            risk_band = 'Low'

        return {
            'lap': scenario.lap,
            'position': scenario.position,
            'tyre_compound': scenario.tyre_compound,
            'recommendation': recommendation,
            'confidence': round(confidence, 2),
            'expected_position_gain': expected_position_gain,
            'overtake_probability': round(overtake_probability, 2),
            'risk_probability': round(risk, 2),
            'pit_gain_seconds': round(pit_gain, 2),
            'energy_available': scenario.energy_available,
            'risk_band': risk_band,
            'expected_value': round((expected_position_gain + pit_gain * 0.5) - risk * 10, 2),
            'decision_explanation': (
                f"{recommendation} recommended: predicted gain {expected_position_gain} "
                f"position with {round(overtake_probability * 100, 1)}% overtake probability "
                f"under current energy ({scenario.energy_available}%) and tyre condition ({scenario.tyre_age} laps)."
            ),
        }

    def get_dashboard_payload(self) -> Dict:
        """Return a dashboard-friendly JSON payload for the frontend UI."""
        strategies = [self.make_strategy(s) for s in self.scenarios]
        
        if not strategies:
            return {
                'title': 'F1 Race Strategy & Decision Intelligence',
                'error': 'No scenarios loaded',
                'strategies': [],
            }
        
        recommended = max(strategies, key=lambda s: s['expected_value'])

        return {
            'title': 'F1 Race Strategy & Decision Intelligence',
            'race_state': {
                'race_control': 'Live Simulation',
                'weather': 'Clear',
                'active_aero_mode': 'High Downforce',
                'overtake_mode': 'Available',
            },
            'strategies': strategies,
            'overall_risk_score': round(sum(s['risk_probability'] for s in strategies) / len(strategies), 2),
            'recommended_strategy': recommended,
            'kpis': {
                'total_scenarios': len(strategies),
                'top_strategy_confidence': round(max(s['confidence'] for s in strategies), 2),
                'mean_overtake_probability': round(sum(s['overtake_probability'] for s in strategies) / len(strategies), 2),
                'high_risk_events': sum(1 for s in strategies if s['risk_band'] == 'High'),
                'medium_risk_events': sum(1 for s in strategies if s['risk_band'] == 'Medium'),
            }
        }
