from typing import Iterable

from ..percent import Percent
from ..percent.sequence import PercentSequence


class IResidualCalculator:
    """Interface for calculators of residual performance."""

    def calculate(self, total: Percent, effects: Iterable[Percent]) -> Percent:
        """Calculate the residual performance.

        Parameters
        ----------
        total
            total performance
        effects
            effects (e.g., carry, curve, spread)

        Returns
        -------
        Percent
            residual performance
        """
        raise NotImplementedError


class ResidualCalculator(IResidualCalculator):
    """Calculator of residual performance."""

    def calculate(self, total: Percent, effects: Iterable[Percent]) -> Percent:
        """Calculate the residual performance.

        Parameters
        ----------
        total
            total performance
        effects
            effects (e.g., carry, curve, spread)

        Returns
        -------
        Percent
            residual performance
        """
        effects_ = PercentSequence(effects)
        return effects_.difference_with(total)
