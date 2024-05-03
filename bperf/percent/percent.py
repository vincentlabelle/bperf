from typing import SupportsFloat, SupportsInt, Type, TypeVar

from ..utilities.float.precise import Precise

P = TypeVar("P", bound="Percent")


class Percent(Precise):
    """Percentage value represented with a precision of four decimal places
    (e.g., 25.12% or 0.00%).

    Parameters
    ----------
    value: SupportsInt
        percentage value in basis points (e.g., 1 <=> 1 bps <=> 0.01%)
    """

    _PRECISION = 4

    @classmethod
    def from_float(cls: Type[P], value: SupportsFloat) -> P:
        """Create a percent from a floating-point number. The floating-point
        number is rounded using a half-even approach if it has more than
        four decimal places.

        Parameters
        ----------
        value
            float to create the percent from

        Raises
        ------
        ValueError
            if `value` is not finite
        RuntimeError
            if an unexpected error occurs while rounding `value`

        Returns
        -------
        P
            percent
        """
        return cls(cls.float_to_int(value, cls._PRECISION))

    def __init__(self, value: SupportsInt):
        super().__init__(value, self._PRECISION)

    # noinspection PyProtectedMember,PyUnresolvedReferences
    def __add__(self: P, other: object) -> P:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value + other._value)

    # noinspection PyProtectedMember,PyUnresolvedReferences
    def __sub__(self: P, other: object) -> P:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value - other._value)
