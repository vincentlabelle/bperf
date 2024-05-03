from ..utilities.sequence import Sequence
from .discount import Discount


class DiscountSequence(Sequence[Discount]):
    """Immutable sequence of discount factors."""
