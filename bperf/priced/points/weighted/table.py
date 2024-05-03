from ....utilities.sequence import Sequence
from .sequence import WeightedPricedPointsSequence


class WeightedPricedPointsTable(Sequence[WeightedPricedPointsSequence]):
    """Immutable sequence of weighted priced points sequences."""
