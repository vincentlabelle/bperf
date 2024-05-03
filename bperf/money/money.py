from typing import SupportsInt, TypeVar

from ..discount import Discount
from ..pv import PresentValue
from ..utilities.float.precise import Precise

M = TypeVar("M", bound="Money")


class Money(Precise):
    """Monetary value represented with a precision of two decimal places
    (e.g., $223.13 or $0.02)

    Parameters
    ----------
    cents: SupportsInt
        monetary value in cents (e.g., 1 <=> 1 cent <=> $0.01)
    """

    _PRECISION = 2

    def __init__(self, cents: SupportsInt):
        super().__init__(cents, self._PRECISION)

    def pv(self, discount: Discount) -> PresentValue:
        """Calculate the present value of this money when discounted
        with `discount`.

        Parameters
        ----------
        discount
            discount factor to apply to this money

        Raises
        ------
        OverflowError
            if an overflow occurred while determining the present value

        Returns
        -------
        PresentValue
            present value of this money
        """
        try:
            return PresentValue(float(self) * float(discount))
        except ValueError:
            message = (
                f"cannot determine pv for {self.__class__.__name__}; "
                f"an overflow occurred"
            )
            raise OverflowError(message)

    # noinspection PyProtectedMember,PyUnresolvedReferences
    def __add__(self: M, other: object) -> M:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value + other._value)

    # noinspection PyProtectedMember,PyUnresolvedReferences
    def __sub__(self: M, other: object) -> M:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value - other._value)
