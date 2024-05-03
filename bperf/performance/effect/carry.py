from ...priced.points import PricedPoints
from ...rate.periodic import PeriodicRate
from .effect import ITwoPointsEffectCalculator


class TwoPointsCarryEffectCalculator(ITwoPointsEffectCalculator):
    """Calculator of carry effect."""

    def calculate(self, points: PricedPoints) -> PeriodicRate:
        """Calculate the carry effect over a period of time using two
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
            carry effect
        """
        final_ = points.initial.update_flows(points.final.flows)
        return points.initial.price.growth(
            final_.price,
            payments=points.payments,
        )
