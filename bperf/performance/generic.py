from typing import Generic, TypeVar

from ..priced.points import PricedPoints
from ..priced.points.weighted.sequence import WeightedPricedPointsSequence
from ..priced.points.weighted.table import WeightedPricedPointsTable
from ..rate.periodic import PeriodicRate
from ..rate.periodic.sequence import PeriodicRateSequence

T = TypeVar("T", bound="ITwoPointsPerformanceCalculator")


class ITwoPointsPerformanceCalculator:
    """Interface for calculators of performance (e.g., effects or total)
    using two data points to performance the calculation.
    """

    def calculate(self, points: PricedPoints) -> PeriodicRate:
        """Calculate the performance over a period of time using two
        data points.

        Parameters
        ----------
        points
            data points to compute the performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the performance

        Returns
        -------
        PeriodicRate
            performance
        """
        raise NotImplementedError


class CrossSectionalPerformanceCalculator(Generic[T]):
    """Calculator of performance using cross-sectional data to
    perform the computation.

    Parameters
    ----------
    calculator: T
        sub-calculator of performance using two data points
        to perform the calculation
    """

    def __init__(self, calculator: T):
        self._calculator = calculator

    def calculate(self, sequence: WeightedPricedPointsSequence) -> PeriodicRate:
        """Calculate the performance over a period of time using
        cross-sectional data.

        Parameters
        ----------
        sequence
            data points to compute the performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the performance

        Returns
        -------
        PeriodicRate
            performance
        """
        rates = PeriodicRateSequence(
            self._calculator.calculate(points) for points in sequence.points
        )
        return rates.dot(sequence.percents)


class LongitudinalPerformanceCalculator(Generic[T]):
    """Calculator of performance using longitudinal data to
    perform the calculation.

    Parameters
    ----------
    calculator: CrossSectionalPerformanceCalculator[T]
        sub-calculator of performance using cross-sectional data
        to perform the calculation
    """

    def __init__(self, calculator: CrossSectionalPerformanceCalculator[T]):
        self._calculator = calculator

    def calculate(self, table: WeightedPricedPointsTable) -> PeriodicRate:
        """Calculate the performance over a period of time using
        longitudinal data.

        Parameters
        ----------
        table
            data points to compute the performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the performance

        Returns
        -------
        PeriodicRate
            performance
        """
        rates = PeriodicRateSequence(
            self._calculator.calculate(sequence) for sequence in table
        )
        return rates.compound()
