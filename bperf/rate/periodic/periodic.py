from math import isfinite
from typing import SupportsFloat, TypeVar

from ...utilities.float.finite import Finite

P = TypeVar("P", bound="PeriodicRate")


class PeriodicRate(Finite):
    """Periodically compounded rate represented by a finite
    floating-point number.
    """

    def increment(self: P) -> P:
        """Increment this rate by 1.0.

        Notes
        -----
        The operation is **not** performed in-place.

        Raises
        ------
        OverflowError
            if an overflow occurs while incrementing this rate

        Returns
        -------
        P
            incremented rate
        """
        return self + self.__class__(1.0)

    def decrement(self: P) -> P:
        """Decrement this rate by 1.0.

        Notes
        -----
        The operation is **not** performed in-place.

        Raises
        ------
        OverflowError
            if an overflow occurs while decrementing this rate

        Returns
        -------
        P
            decremented rate
        """
        return self - self.__class__(1.0)

    def scale(self: P, by: SupportsFloat) -> P:
        """Scale this rate by `by`.

        Parameters
        ----------
        by
            value with which to scale this rate

        Raises
        ------
        ValueError
            if `by` is not finite
        OverflowError
            if an overflow occurs while scaling

        Returns
        -------
        P
            scaled rate
        """
        by_ = float(by)
        self._raise_if_by_is_not_finite(by_)
        return self._class(self._value * by_)

    def _raise_if_by_is_not_finite(self, by: float) -> None:
        if not isfinite(by):
            message = (
                f"cannot scale this {self.__class__.__name__}; "
                f"by must be finite"
            )
            raise ValueError(message)
