from typing import Any
from typing import Sequence as typeSequence

from ..discount.sequence import DiscountSequence
from ..pv import PresentValue
from ..pv.sequence import PresentValueSequence
from ..utilities.sequence import Sequence
from .money import Money


class MoneySequence(Sequence[Money]):
    """Immutable sequence of monies."""

    def sum(self) -> Money:
        """Sum the monies in this sequence.

        Returns
        -------
        Money
            sum of the monies in this sequence
        """
        return sum(self, start=Money(0))

    def pv(self, discounts: DiscountSequence) -> PresentValue:
        """Calculate the present value of the monies in this sequence
        by summing the discounted value of each money in this sequence.
        The monies are discounted with their corresponding discount factor
        in `discounts`.

        Parameters
        ----------
        discounts
            discount factors to apply to the monies in this sequence

        Raises
        ------
        ValueError
            if the length of `discounts` doesn't match with the length of
            this sequence
        OverflowError
            if an overflow occurs while determining the present value

        Returns
        -------
        PresentValue
            present value of the monies in this sequence
        """
        self._raise_if_len_mismatch(discounts)
        return PresentValueSequence(
            money.pv(discount) for money, discount in zip(self, discounts)
        ).sum()

    def _raise_if_len_mismatch(self, values: typeSequence[Any]) -> None:
        if len(values) != len(self):
            message = (
                f"cannot perform operation on {self.__class__.__name__}; "
                f"there's a length mismatch"
            )
            raise ValueError(message)
