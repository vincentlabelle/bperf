from typing import Iterable

from ....percent import Percent
from ....percent.sequence import PercentSequence
from ....utilities.sequence import Sequence
from ..sequence import PricedPointsSequence
from .weighted import WeightedPricedPoints


class WeightedPricedPointsSequence(Sequence[WeightedPricedPoints]):
    """Immutable sequence of weighted priced points.

    Parameters
    ----------
    values: Iterable[WeightedPricedPoints]
        values to create the sequence from

    Raises
    ------
    ValueError
        if the sum of the weight of each value in `values` is not equal to one
    """

    _TARGET = Percent(10000)

    def __init__(self, values: Iterable[WeightedPricedPoints]):
        super().__init__(values)
        self._raise_if_not_summing_to_one()

    def _raise_if_not_summing_to_one(self) -> None:
        if not self.is_empty() and not self.percents.sums_to(self._TARGET):
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"sum of weights of weighted priced points must sum to one"
            )
            raise ValueError(message)

    @property
    def percents(self) -> PercentSequence:
        """Get the percent of each weighted priced points in this sequence."""
        return PercentSequence(value.percent for value in self)

    @property
    def points(self) -> PricedPointsSequence:
        """Get the priced points of each weighted priced points
        in this sequence.
        """
        return PricedPointsSequence(value.points for value in self)
