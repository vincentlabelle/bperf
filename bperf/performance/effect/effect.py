from typing import Dict

from ...percent import Percent
from ...priced.points import PricedPoints
from ...priced.points.weighted.table import WeightedPricedPointsTable
from ...rate.periodic import PeriodicRate
from ..generic import (
    ITwoPointsPerformanceCalculator,
    LongitudinalPerformanceCalculator,
)


class ITwoPointsEffectCalculator(ITwoPointsPerformanceCalculator):
    """Interface for calculators of single effects (e.g., carry, curve or
    spread) using two data points to perform the calculation.
    """

    def calculate(self, points: PricedPoints) -> PeriodicRate:
        """Calculate the effect over a period of time using two data
        points.

        Parameters
        ----------
        points
            data points to compute the effect from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the effect

        Returns
        -------
        PeriodicRate
            effect
        """
        raise NotImplementedError


class IEffectsCalculator:
    """Interface for calculators of multiple effects (e.g., carry, curve
    and spread).
    """

    def calculate(self, table: WeightedPricedPointsTable) -> Dict[str, Percent]:
        """Calculate the effects over a period of time.

        Parameters
        ----------
        table
            data points to compute the effects from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the effects
        RuntimeError
            if an unexpected error occurs while rounding the effects

        Returns
        -------
        Dict[str, Percent]
            effects
        """
        raise NotImplementedError


class EffectsCalculator(IEffectsCalculator):
    """Calculator of multiple effects (e.g., carry, curve and spread).

    Parameters
    ----------
    calculators: Dict[
        str,
        LongitudinalPerformanceCalculator[ITwoPointsEffectCalculator]
    ]
        calculators of single effect, and their name (i.e., str)
    """

    def __init__(
        self,
        calculators: Dict[
            str,
            LongitudinalPerformanceCalculator[ITwoPointsEffectCalculator],
        ],
    ):
        self._items = tuple(calculators.items())

    def calculate(self, table: WeightedPricedPointsTable) -> Dict[str, Percent]:
        """Calculate the effects over a period of time.

        Parameters
        ----------
        table
            data points to compute the effects from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the effects
        RuntimeError
            if an unexpected error occurs while rounding the effects

        Returns
        -------
        Dict[str, Percent]
            effects
        """
        return {
            name: Percent.from_float(
                calculator.calculate(table),
            )
            for name, calculator in self._items
        }
