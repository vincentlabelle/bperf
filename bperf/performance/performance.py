from typing import Dict

from ..percent import Percent
from ..priced.points.weighted.table import WeightedPricedPointsTable
from .effect import IEffectsCalculator
from .residual import IResidualCalculator
from .total import ITotalPerformanceCalculator


class IPerformanceCalculator:
    """Interface for calculators of performance."""

    def calculate(self, table: WeightedPricedPointsTable) -> Dict[str, Percent]:
        """Calculate the performance (i.e., total performance, and effects)
        over a period of time.

        Parameters
        ----------
        table
            data points to compute the performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the performance
        RuntimeError
            if an unexpected error occurs while rounding the performance

        Returns
        -------
        Dict[str, Percent]
            performance
        """
        raise NotImplementedError


class PerformanceCalculator(IPerformanceCalculator):
    """Calculator of performance.

    Parameters
    ----------
    total: ITotalPerformanceCalculator
        sub-calculator of total performance
    effects: IEffectsCalculator
        sub-calculator of effects
    residual: IResidualCalculator
        sub-calculator of residual
    """

    _TOTAL_NAME = "total"
    _RESIDUAL_NAME = "residual"

    def __init__(
        self,
        total: ITotalPerformanceCalculator,
        effects: IEffectsCalculator,
        residual: IResidualCalculator,
    ):
        self._total = total
        self._effects = effects
        self._residual = residual

    def calculate(self, table: WeightedPricedPointsTable) -> Dict[str, Percent]:
        """Calculate the performance (i.e., total performance, and effects)
        over a period of time.

        Parameters
        ----------
        table
            data points to compute the performance from

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the performance
        RuntimeError
            if an unexpected error occurs while rounding the performance

        Returns
        -------
        Dict[str, Percent]
            performance
        """
        total = self._total.calculate(table)
        effects = self._effects.calculate(table)
        residual = self._residual.calculate(total, effects.values())
        return {
            self._TOTAL_NAME: total,
            **effects,
            self._RESIDUAL_NAME: residual,
        }
