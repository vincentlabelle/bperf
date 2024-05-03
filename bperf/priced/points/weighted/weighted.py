from ....percent import Percent
from ..points import PricedPoints


class WeightedPricedPoints:
    """Association of a priced points with a weight.

    Parameters
    ----------
    percent: Percent
        weight to associate with a priced points
    points: PricedPoints
        priced points to associate with a weight
    """

    def __init__(self, percent: Percent, points: PricedPoints):
        self._percent = percent
        self._points = points

    @property
    def percent(self) -> Percent:
        """Weight associated to the points of this instance."""
        return self._percent

    @property
    def points(self) -> PricedPoints:
        """Points associated to the weight of this instance."""
        return self._points

    def __str__(self) -> str:
        return f"(percent={self._percent}, points={self._points})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._percent == other._percent and self._points == other._points

    def __hash__(self) -> int:
        return hash((self._percent, self._points))
