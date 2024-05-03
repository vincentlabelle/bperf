from ...priced.points import PricedPoints
from ...rate.periodic import PeriodicRate
from .effect import ITwoPointsEffectCalculator


class TwoPointsCurveEffectCalculator(ITwoPointsEffectCalculator):
    """Calculator of curve effect."""

    def calculate(self, points: PricedPoints) -> PeriodicRate:
        """Calculate the curve effect over a period of time using two
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
            curve effect
        """
        final_ = points.initial.update_spot(points.final.spot)
        return points.initial.price.growth(final_.price)
