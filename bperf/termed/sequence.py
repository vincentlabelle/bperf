from typing import Any, Iterable, Tuple, Type, TypeVar

from ..term import Term
from ..term.sequence import TermSequence
from ..utilities.sequence import Sequence
from .termed import Termed

T = TypeVar("T")
S = TypeVar("S", bound="TermedSequence[Any]")


class TermedSequence(Sequence[Termed[T]]):
    """Immutable non-empty sequence of ordered termed.

    Parameters
    ----------
    values: Iterable[Termed[T]]
        values to create the sequence from; values will be sorted

    Raises
    ------
    ValueError
        if `values` contains repeated terms
    """

    @classmethod
    def from_tuples(cls: Type[S], tuples: Iterable[Tuple[Term, T]]) -> S:
        """Create a sequence from an iterable of tuples.

        Parameters
        ----------
        tuples
            values to create the sequence from

        Raises
        ------
        ValueError
            if `tuples` contains repeated terms

        Returns
        -------
        S
            sequence
        """
        return cls(Termed(*tuple_) for tuple_ in tuples)

    def __init__(self, values: Iterable[Termed[T]]):
        super().__init__(sorted(values))
        self._raise_if_contains_repeated_terms()

    def _raise_if_contains_repeated_terms(self) -> None:
        if self.terms.contains_repeated_values():
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must contain unique terms"
            )
            raise ValueError(message)

    @property
    def terms(self) -> TermSequence:
        """Get the terms of the termed in this sequence."""
        return TermSequence(termed.term for termed in self)

    @property
    def values(self) -> Iterable[T]:
        """Get the values of the termed in this sequence."""
        return (termed.value for termed in self)
