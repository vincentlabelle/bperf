from ..utilities.sequence import Sequence
from .pv import PresentValue


class PresentValueSequence(Sequence[PresentValue]):
    """Immutable sequence of present values."""

    def sum(self) -> PresentValue:
        """Sum the present values in this sequence.

        Raises
        ------
        OverflowError
            if an overflow occurred while determining the sum

        Returns
        -------
        PresentValue
            sum of the present values in this sequence
        """
        return sum(self, start=PresentValue(0.0))
