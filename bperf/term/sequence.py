from ..utilities.sequence import Sequence
from .term import Term


class TermSequence(Sequence[Term]):
    """Immutable sequence of terms."""

    def contains_repeated_values(self) -> bool:
        """Verify if this sequence contains repeated values.

        Returns
        -------
        bool
            True if this sequence contains repeated values, else False
        """
        return sorted(self) != sorted(set(self))
