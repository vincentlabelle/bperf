from typing import Generic, TypeVar

from ..term import Term

T = TypeVar("T")


class Termed(Generic[T]):
    """Combination of a value and a term.

    Parameters
    ----------
    term: Term
        term to associate with `value`
    value: T
        `value` to associate with term
    """

    def __init__(self, term: Term, value: T):
        self._term = term
        self._value = value

    @property
    def term(self) -> Term:
        """Get the term of this termed."""
        return self._term

    @property
    def value(self) -> T:
        """Get the value of this termed."""
        return self._value

    def __str__(self) -> str:
        return f"(term={self._term}, value={self._value})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._term == other._term and self._value == other._value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._term < other._term

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._term <= other._term

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._term > other._term

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._term >= other._term

    def __hash__(self) -> int:
        return hash((self._term, self._value))
