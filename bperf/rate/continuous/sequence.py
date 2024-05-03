from typing import Iterable, SupportsFloat, Type, TypeVar

from ...utilities.sequence import Sequence
from .continuous import ContinuousRate

S = TypeVar("S", bound="ContinuousRateSequence")


class ContinuousRateSequence(Sequence[ContinuousRate]):
    """Immutable sequence of continuously compounded rates."""

    @classmethod
    def from_float(cls: Type[S], values: Iterable[SupportsFloat]) -> S:
        """Create a sequence from floating-point values.

        Parameters
        ----------
        values
            iterable of floating-point values to create the sequence from

        Raises
        ------
        ValueError
            if any value in `values` is not finite

        Returns
        -------
        S
            sequence
        """
        return cls(ContinuousRate(value) for value in values)

    def add(self: S, rate: ContinuousRate) -> S:
        """Add a fixed `rate` to every rate in this sequence.

        Notes
        -----
        The operation is **not** performed in-place.

        Parameters
        ----------
        rate
            rate to add to the rates in this sequence

        Raises
        ------
        OverflowError
            if adding `rate` to the rates in this sequence generates an
            overflow

        Returns
        -------
        S
            new sequence
        """
        return self.__class__(value + rate for value in self)
