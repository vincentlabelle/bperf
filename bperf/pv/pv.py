from math import isfinite
from typing import SupportsFloat, TypeVar

from ..rate.periodic import PeriodicRate
from ..utilities.float.finite import Finite

P = TypeVar("P", bound="PresentValue")


class PresentValue(Finite):
    """Present value of cash flows represented as a finite
    floating-point number.
    """

    def growth(
        self: P,
        final: P,
        *,
        payments: SupportsFloat = 0.0,
    ) -> PeriodicRate:
        """Get the periodic rate of growth achieved over a period of time
        in which this present value is the present value of some cash
        flows at the beginning of the period, and `other` is the present
        value of the same cash flows at the end of the period.

        Parameters
        ----------
        final
            present value at the end of the period
        payments: SupportsFloat, optional
            sum of paid cash flows over the period of time, defaults to 0.0

        Raises
        ------
        ValueError
            if `payments` is not finite
        ZeroDivisionError
            if this present value is zero
        OverflowError
            if an overflow occurred while determining the rate of growth

        Returns
        -------
        PeriodicRate
            periodic rate of growth
        """
        payments_ = float(payments)
        self._raise_if_payments_is_not_finite(payments_)
        growth = self._growth(final, payments_)
        return self._to_rate(growth)

    def _to_rate(self, growth: float) -> PeriodicRate:
        try:
            return PeriodicRate(growth)
        except ValueError:
            message = (
                f"cannot determine growth for {self.__class__.__name__}; "
                f"an overflow occurred"
            )
            raise OverflowError(message)

    def _raise_if_payments_is_not_finite(self, payments: float) -> None:
        if not isfinite(payments):
            message = (
                f"cannot determine growth for {self.__class__.__name__}; "
                f"payments must be finite"
            )
            raise ValueError(message)

    def _growth(self: P, final: P, payments: float) -> float:
        try:
            return (
                final._value + payments  # skipcq: PYL-W0212
            ) / self._value - 1.0
        except ZeroDivisionError:
            message = (
                f"cannot determine growth for {self.__class__.__name__}; "
                f"this present value must be different from zero"
            )
            raise ZeroDivisionError(message)
