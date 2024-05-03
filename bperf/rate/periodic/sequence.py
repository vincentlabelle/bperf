from math import prod
from typing import Iterable, SupportsFloat, Tuple, TypeVar

from ...utilities.sequence import Sequence
from .periodic import PeriodicRate

P = TypeVar("P", bound="PeriodicRateSequence")


class PeriodicRateSequence(Sequence[PeriodicRate]):
    """Immutable sequence of periodic rates."""

    def dot(self, with_: Iterable[SupportsFloat]) -> PeriodicRate:
        """Get the dot product of this sequence with `with_`.

        Parameters
        ----------
        with_
            vector for which to compute the dot product with this sequence

        Raises
        ------
        ValueError
            if any value in `with_` is not finite, or
            if there's a length mismatch between `with_` and this sequence
        OverflowError
            if an overflow occurs while determining the dot product

        Returns
        -------
        PeriodicRate
            dot product
        """
        return self.scale(with_).sum()

    def scale(self: P, by: Iterable[SupportsFloat]) -> P:
        """Scale each rate in this sequence by its corresponding value in
        `by`.

        Parameters
        ----------
        by
            values with which to scale the rates in this sequence by

        Raises
        ------
        ValueError
            if any value in `by` is not finite, or
            if there's a length mismatch between `by` and this sequence
        OverflowError
            if an overflow occurs while scaling

        Returns
        -------
        P
            sequence of scaled rates
        """
        by_ = tuple(by)
        self._raise_if_length_mismatch_with_by(by_)
        return self.__class__(value.scale(b) for b, value in zip(by_, self))

    def _raise_if_length_mismatch_with_by(
        self,
        by: Tuple[SupportsFloat, ...],
    ) -> None:
        if len(self) != len(by):
            message = (
                f"cannot weight this {self.__class__.__name__}; "
                f"length of by must match with the length of "
                f"this sequence"
            )
            raise ValueError(message)

    def sum(self) -> PeriodicRate:
        """Sum the rates in this sequence.

        Raises
        ------
        OverflowError
            if an overflow occurs while summing

        Returns
        -------
        PeriodicRate
            sum of the rates in this sequence
        """
        return sum(self, start=PeriodicRate(0.0))

    def compound(self) -> PeriodicRate:
        """Compound the rates in this sequence.

        Raises
        ------
        OverflowError
            if an overflow occurs while determining the compounded rate

        Returns
        -------
        PeriodicRate
            compounded rate
        """
        product = prod(
            self._increment(),
            start=PeriodicRate(1.0),
        )
        return product.decrement()  # type: ignore[attr-defined,no-any-return]

    def _increment(self) -> Iterable[PeriodicRate]:
        return (value.increment() for value in self)
