from collections.abc import Sequence as abcSequence
from typing import Any, Iterable, Type, TypeVar, Union, overload

T_co = TypeVar("T_co", covariant=True)
S = TypeVar("S", bound="Sequence[Any]")


class Sequence(abcSequence[T_co]):
    """Immutable sequence of objects with default implementation
    for __init__, __getitem__, __len__, __eq__, __hash__,
    __str__, and __repr__.

    Parameters
    ----------
    values: Iterable[T_co]
        values to create the sequence from
    """

    @classmethod
    def empty(cls: Type[S]) -> S:
        """Create an empty sequence.

        Returns
        -------
        S
            sequence
        """
        return cls([])

    def __init__(self, values: Iterable[T_co]):
        self._values = tuple(values)

    def is_empty(self) -> bool:
        """Verify if this sequence is empty.

        Returns
        -------
        bool
            True if this sequence is empty, else False
        """
        return len(self) == 0

    def __len__(self) -> int:
        return len(self._values)

    @overload
    def __getitem__(self: S, item: int) -> T_co:
        pass

    @overload
    def __getitem__(self: S, item: slice) -> S:
        pass

    def __getitem__(self: S, item: Union[slice, int]) -> Any:
        if isinstance(item, slice):
            return self.__class__(self._values[item])
        return self._values[item]

    def __str__(self) -> str:
        return f"({', '.join(str(value) for value in self)})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._values == other._values

    def __hash__(self) -> int:
        return hash(self._values)
