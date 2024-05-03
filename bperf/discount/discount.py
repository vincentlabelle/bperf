from typing import SupportsFloat

from ..utilities.float.finite import Finite


class Discount(Finite):
    """Discount factor represented as a non-NaN floating-point number.

    Parameters
    ----------
    value: SupportsFloat
        discount factor

    Raises
    ------
    ValueError
        if `value` is not finite, or
        if `value` is negative
    """

    def __init__(self, value: SupportsFloat):
        super().__init__(value)
        self._raise_if_is_negative()

    def _raise_if_is_negative(self) -> None:
        if self._value < 0.0:
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be non-negative"
            )
            raise ValueError(message)
