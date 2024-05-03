from ..utilities.sequence import Sequence
from .percent import Percent


class PercentSequence(Sequence[Percent]):
    """Immutable sequence of percents."""

    def sum(self) -> Percent:
        """Sum the percents in this sequence.

        Returns
        -------
        Percent
            sum of the percents in this sequence
        """
        return sum(self, start=Percent(0))

    def sums_to(self, value: Percent) -> bool:
        """Verify if the sum of the percents in this sequence is equal
        to `value`.

        Parameters
        ----------
        value
            value for which to verify the equality with the sum of the
            percents in this sequence

        Returns
        -------
        bool
            True if the sum of the percents in this sequence is equal to
            `value`, else False
        """
        return self.sum() == value

    def difference_with(self, value: Percent) -> Percent:
        """Get the difference between `value` and the sum of the percents
        in this sequence.

        Parameters
        ----------
        value
            value for which to get the difference

        Returns
        -------
        Percent
            difference between `value` and the sum of the percents in this
            sequence
        """
        return value - self.sum()
