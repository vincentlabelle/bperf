from ...money import Money
from ...pv import PresentValue
from ..priced import PricedFlows


class PricedPoints:
    """Cash flows priced at the beginning and end of a period of time (i.e.,
    cash flows priced at two points in time).

    Parameters
    ----------
    initial: PricedFlows
        priced flows at the beginning of the period
    final: PricedFlows
        priced flows at the end of the period

    Raises
    ------
    ValueError
        if `initial`'s price is zero
    OverflowError
        if an overflow occurs while getting the price of `initial`
    """

    def __init__(self, initial: PricedFlows, final: PricedFlows):
        self._initial = initial
        self._final = final
        self._raise_if_initial_price_is_zero()

    def _raise_if_initial_price_is_zero(self) -> None:
        if self._initial.price == PresentValue(0.0):
            message = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"initial price must be different from zero."
            )
            raise ValueError(message)

    @property
    def initial(self) -> PricedFlows:
        """Get the priced flows at the beginning of the period."""
        return self._initial

    @property
    def final(self) -> PricedFlows:
        """Get the priced flows at the end of the period."""
        return self._final

    @property
    def payments(self) -> Money:
        """Get the payments over the period."""
        return self._initial.flows.sum() - self._final.flows.sum()

    def __str__(self) -> str:
        return f"(initial={self._initial}, final={self._final})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._initial == other._initial and self._final == other._final

    def __hash__(self) -> int:
        return hash((self._initial, self._final))
