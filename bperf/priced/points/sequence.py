from ...utilities.sequence import Sequence
from .points import PricedPoints


class PricedPointsSequence(Sequence[PricedPoints]):
    """Immutable sequence of priced points."""
