from typing import Iterable, TypeVar

import numpy as np

from .discount.sequence import DiscountSequence
from .rate.continuous import ContinuousRate
from .rate.continuous.sequence import ContinuousRateSequence
from .term.sequence import TermSequence
from .termed import Termed
from .termed.sequence import TermedSequence


class Curve(TermedSequence[ContinuousRate]):
    """Immutable non-empty sequence of ordered termed continuous rates.
    A termed continuous rate is defined as a :py:class:`Termed` for which
    the value is a :py:class:`ContinuousRate`.

    Parameters
    ----------
    values: Iterable[Termed[ContinuousRate]]
        values to create the sequence from

    Raises
    ------
    ValueError
        if `values` is empty, or
        if `values` contains repeated terms
    """

    def __init__(self, values: Iterable[Termed[ContinuousRate]]):
        super().__init__(values)
        self._raise_if_is_empty()

    def _raise_if_is_empty(self) -> None:
        if self.is_empty():
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must be non-empty"
            )
            raise ValueError(message)

    @property
    def rates(self) -> ContinuousRateSequence:
        """Get the rates of the termed in this sequence."""
        return ContinuousRateSequence(self.values)

    def _rates_at(self, terms: TermSequence) -> ContinuousRateSequence:
        return ContinuousRateSequence.from_float(
            np.interp(
                np.array(terms, dtype=np.float_),
                np.array(self.terms, dtype=np.float_),
                np.array(self.rates, dtype=np.float_),
            ),
        )


S = TypeVar("S", bound="SpotCurve")


class SpotCurve(Curve):
    """Immutable non-empty sequence of ordered continuous spot rates.
    A continuous spot rate is defined as a :py:class:`Termed` for which
    the value is a :py:class:`ContinuousRate`.
    """

    def discounts_at(self, terms: TermSequence) -> DiscountSequence:
        """Get the discount factors for specific `terms` along this curve.

        Parameters
        ----------
        terms
            terms for which to get the discount factors

        Raises
        ------
        OverflowError
            if there's an overflow while determining the discount factors

        Returns
        -------
        DiscountSequence
            discount factor for each term
        """
        return DiscountSequence(
            rate.discount_at(term)
            for term, rate in zip(terms, self._rates_at(terms))
        )

    def add(self: S, spread: ContinuousRate) -> S:
        """Add a `spread` to each rate along this curve.

        Notes
        -----
        The operation is **not** performed in-place.

        Parameters
        ----------
        spread
            spread to add to each rate along the curve

        Raises
        ------
        OverflowError
            if adding `spread` to the rates along this curve generates
            and overflow

        Returns
        -------
        S
            shifted curve
        """
        return self.__class__.from_tuples(
            zip(self.terms, self.rates.add(spread))
        )
