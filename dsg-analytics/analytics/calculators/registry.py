from analytics.calculators.sessions import SessionCalculator
from analytics.calculators.base import BaseCalculator


def get_calculators() -> list[BaseCalculator]:
    """
    Returns all registered Analytics calculators.
    """

    return [
        SessionCalculator(),
    ]
