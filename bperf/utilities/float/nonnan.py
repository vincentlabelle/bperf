from math import isnan
from typing import SupportsFloat


class NonNan:
    """Non-NaN floating-point number.

    Parameters
    ----------
    value: SupportsFloat
        non-NaN value

    Raises
    ------
    ValueError
        if `value` is NaN
    """

    def __init__(self, value: SupportsFloat):
        self._value = float(value)
        self._raise_if_is_nan()

    def _raise_if_is_nan(self) -> None:
        if isnan(self._value):
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be non-NaN"
            )
            raise ValueError(message)

    def __float__(self) -> float:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
