from .curve import SpotCurve
from .money import Money
from .money.sequence import MoneySequence
from .pv import PresentValue
from .termed.sequence import TermedSequence


class Flows(TermedSequence[Money]):
    """Immutable non-empty sequence of ordered termed money (i.e., cash flows).
    A termed money (i.e., cash flow) is defined as a :py:class:`Termed`
    for which the value is a :py:class:`Money`.
    """

    @property
    def monies(self) -> MoneySequence:
        """Get the monies of the termed in this sequence."""
        return MoneySequence(self.values)

    def pv(self, spot: SpotCurve) -> PresentValue:
        """Get the present value of the flows in this sequence by summing
        the discounted value of each flow in this sequence.

        Parameters
        ----------
        spot
            spot curve to discount the flows with

        Raises
        ------
        OverflowError
            if there's an overflow while determining the present value

        Returns
        -------
        PresentValue
            present value
        """
        discounts = spot.discounts_at(self.terms)
        return self.monies.pv(discounts)

    def sum(self) -> Money:
        """Sum the monies in this sequence.

        Returns
        -------
        Money
            sum of the monies in this sequence
        """
        return self.monies.sum()
