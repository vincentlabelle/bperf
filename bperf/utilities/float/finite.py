from math import isfinite
from typing import SupportsFloat, TypeVar

from .nonnan import NonNan

F = TypeVar("F", bound="Finite")


class Finite(NonNan):
    """Finite floating-point number.

    Parameters
    ----------
    value: SupportsFloat
        finite value

    Raises
    ------
    ValueError
        if `value` is not finite
    """

    def __init__(self, value: SupportsFloat):
        super().__init__(value)
        self._raise_if_is_not_finite()

    def _raise_if_is_not_finite(self) -> None:
        if not isfinite(self._value):
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be finite"
            )
            raise ValueError(message)

    def __neg__(self: F) -> F:
        return self.__class__(-self._value)

    def __add__(self: F, other: object) -> F:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._class(self._value + other._value)

    def __sub__(self: F, other: object) -> F:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._class(self._value - other._value)

    def __mul__(self: F, other: object) -> F:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._class(self._value * other._value)

    def _class(self: F, value: float) -> F:
        try:
            return self.__class__(value)
        except ValueError:
            message = (
                f"cannot perform operation on {self.__class__.__name__}; "
                f"an overflow occurred"
            )
            raise OverflowError(message)
