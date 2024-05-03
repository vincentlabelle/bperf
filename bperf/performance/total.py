from ..percent import Percent
from ..priced.points import PricedPoints
from ..priced.points.weighted.table import WeightedPricedPointsTable
from ..rate.periodic import PeriodicRate
from .generic import (
    ITwoPointsPerformanceCalculator,
    LongitudinalPerformanceCalculator,
)


class ITwoPointsTotalPerformanceCalculator(ITwoPointsPerformanceCalculator):
    """Interface for calculators of total performance using two data
    points to perform the calculation.
    """

    def calculate(self, points: PricedPoints) -> PeriodicRate:
        """Calculate the total performance over a period of time using
        two data points.

        Parameters
        ----------
        points
            data points to compute the total performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the total performance

        Returns
        -------
        PeriodicRate
            total performance
        """
        raise NotImplementedError


class TwoPointsTotalPerformanceCalculator(ITwoPointsTotalPerformanceCalculator):
    """Calculator of total performance using two data points to
    perform the calculation.
    """

    def calculate(self, points: PricedPoints) -> PeriodicRate:
        """Calculate the total performance over a period of time using
        two data points.

        Parameters
        ----------
        points
            data points to compute the total performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the total performance

        Returns
        -------
        PeriodicRate
            total performance
        """
        return points.initial.price.growth(
            points.final.price,
            payments=points.payments,
        )


class ITotalPerformanceCalculator:
    """Interface for calculators of total performance."""

    def calculate(self, table: WeightedPricedPointsTable) -> Percent:
        """Calculate the total performance over a period of time.

        Parameters
        ----------
        table
            data points to compute the total performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the total performance
        RuntimeError
            if an unexpected error occurs while rounding the total performance

        Returns
        -------
        Percent
            total performance
        """
        raise NotImplementedError


class TotalPerformanceCalculator(ITotalPerformanceCalculator):
    """Calculator of total performance.

    Parameters
    ----------
    calculator: LongitudinalPerformanceCalculator[
        ITwoPointsTotalPerformanceCalculator
    ]
        sub-calculator of total performance using longitudinal data to
        perform the calculation
    """

    def __init__(
        self,
        calculator: LongitudinalPerformanceCalculator[
            ITwoPointsTotalPerformanceCalculator
        ],
    ):
        self._calculator = calculator

    def calculate(self, table: WeightedPricedPointsTable) -> Percent:
        """Calculate the total performance over a period of time.

        Parameters
        ----------
        table
            data points to compute the total performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the total performance
        RuntimeError
            if an unexpected error occurs while rounding the total performance

        Returns
        -------
        Percent
            total performance
        """
        return Percent.from_float(
            self._calculator.calculate(table),
        )
