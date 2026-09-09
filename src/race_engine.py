import os
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd


@dataclass
class RaceScenario:
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
    def __init__(self, dataset_path: str = "data/sample_strategy_cases.csv"):
        self.dataset_path = dataset_path
        self.scenarios = self.load_scenarios(dataset_path)

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
        pit_gain = 2.9 if scenario.tyre_age > 20 else 1.8
        expected_position_gain = 1 if scenario.attack_window and scenario.gap_to_car_ahead < 1.2 else 0
        overtake_probability = min(
            0.83,
            max(
                0.32,
                0.48 + (1.2 - scenario.gap_to_car_ahead) * 0.12 + (scenario.energy_available / 100) * 0.18,
            ),
        )
        risk = max(0.05, min(0.45, scenario.safety_car_probability + (0.1 if scenario.tyre_age > 20 else 0.02)))

        if scenario.attack_window and scenario.overtake_mode and scenario.energy_available > 50:
            recommendation = 'Attack / Overtake Mode'
            confidence = 0.68
        elif scenario.tyre_age > 20:
            recommendation = 'Pit now'
            confidence = 0.74
        else:
            recommendation = 'Stay out and monitor'
            confidence = 0.56

        return {
            'lap': scenario.lap,
            'position': scenario.position,
            'tyre_compound': scenario.tyre_compound,
            'scenario': recommendation,
            'confidence': round(confidence, 2),
            'expected_position_gain': expected_position_gain,
            'overtake_probability': round(overtake_probability, 2),
            'risk_probability': round(risk, 2),
            'pit_gain_seconds': round(pit_gain, 2),
            'energy_available': scenario.energy_available,
            'risk_band': 'Medium' if risk > 0.20 else 'Low',
            'expected_value': round((expected_position_gain + pit_gain * 0.5) - risk * 10, 2),
            'decision_explanation': (
                f"{recommendation} recommended: predicted gain {expected_position_gain} "
                f"position and {round(overtake_probability * 100, 1)}% overtake probability "
                f"under current energy and tyre condition."
            ),
        }

    def get_dashboard_payload(self) -> Dict:
        """Return a dashboard-friendly JSON payload for the frontend UI."""
        strategies = [self.make_strategy(s) for s in self.scenarios]
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
                'top_strategy_confidence': round(max(s['confidence'] for s in strategies), 2),
                'mean_overtake_probability': round(sum(s['overtake_probability'] for s in strategies) / len(strategies), 2),
                'risk_events': sum(1 for s in strategies if s['risk_band'] == 'Medium'),
            }
        }
