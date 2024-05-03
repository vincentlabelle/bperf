from typing import SupportsFloat

from ..utilities.float.finite import Finite


class Term(Finite):
    """Lapse of time in years represented as a strictly positive
    finite floating-point number.

    Parameters
    ----------
    value: SupportsFloat
        term

    Raises
    ------
    ValueError
        if `value` is not finite, or
        if `value` is not strictly positive
    """

    def __init__(self, value: SupportsFloat):
        super().__init__(value)
        self._raise_if_is_not_strictly_positive()

    def _raise_if_is_not_strictly_positive(self) -> None:
        if self._value <= 0.0:
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be strictly positive"
            )
            raise ValueError(message)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value < other._value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value <= other._value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value > other._value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value >= other._value
