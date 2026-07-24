from analytics.calculators import get_calculators
from analytics.calculators.sessions import SessionCalculator


def test_registry_contains_session_calculator():
    calculators = get_calculators()

    assert len(calculators) == 1
    assert isinstance(calculators[0], SessionCalculator)
