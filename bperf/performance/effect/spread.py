from ...priced.points import PricedPoints
from ...rate.periodic import PeriodicRate
from .effect import ITwoPointsEffectCalculator


class TwoPointsSpreadEffectCalculator(ITwoPointsEffectCalculator):
    """Calculator of spread effect."""

    def calculate(self, points: PricedPoints) -> PeriodicRate:
        """Calculate the spread effect over a period of time using two
        data points.

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
            spread effect
        """
        final_ = points.initial.update_spread(points.final.spread)
        return points.initial.price.growth(final_.price)
