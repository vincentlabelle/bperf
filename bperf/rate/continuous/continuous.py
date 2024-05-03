from math import exp

from ...discount import Discount
from ...term import Term
from ...utilities.float.finite import Finite


class ContinuousRate(Finite):
    """Continuous compounded rate represented by a finite
    floating-point number.
    """

    def discount_at(self, term: Term) -> Discount:
        """Get the discount factor for this rate,
        and `term`.

        Parameters
        ----------
        term
            term to use in combination with this rate to obtain
            the discount rate

        Raises
        ------
        OverflowError
            if an overflow occurred while determining the discount factor

        Returns
        -------
        Discount
            discount factor
        """
        try:
            return Discount(exp(-self._value * float(term)))
        except (ValueError, OverflowError):
            message = (
                f"cannot determine discount for {self.__class__.__name__}; "
                f"an overflow occurred"
            )
            raise OverflowError(message)
