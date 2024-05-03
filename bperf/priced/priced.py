from typing import TypeVar

from ..curve import SpotCurve
from ..flows import Flows
from ..pv import PresentValue
from ..rate.continuous import ContinuousRate

P = TypeVar("P", bound="PricedFlows")


class PricedFlows:
    """Cash flows for which the price is determined.

    Parameters
    ----------
    flows: Flows
        cash flows which are priced
    spot: SpotCurve
        spot curve used to price the cash flows
    spread: ContinuousRate
        z-spread used to price the cash flows (i.e., the z-spread is added
        to the spot curve to price the cash flows)
    """

    def __init__(self, flows: Flows, spot: SpotCurve, spread: ContinuousRate):
        self._flows = flows
        self._spot = spot
        self._spread = spread

    @property
    def price(self) -> PresentValue:
        """Price of the cash flows.

        Raises
        ------
        OverflowError
            if an overflow occurred while determining the price
        """
        return self._flows.pv(self._spot_plus_spread)

    @property
    def _spot_plus_spread(self) -> SpotCurve:
        return self._spot.add(self._spread)

    @property
    def flows(self) -> Flows:
        """Cash flows which are priced."""
        return self._flows

    @property
    def spot(self) -> SpotCurve:
        """Spot curve used to price the cash flows."""
        return self._spot

    @property
    def spread(self) -> ContinuousRate:
        """Z-spread used to price the cash flows."""
        return self._spread

    def update_flows(self: P, flows: Flows) -> P:
        """Update the cash flows of this priced.

        Notes
        -----
        The operation is **not** performed in-place.

        Parameters
        ----------
        flows
            new cash flows

        Returns
        -------
        P
            updated priced
        """
        return self.__class__(flows, self._spot, self._spread)

    def update_spot(self: P, spot: SpotCurve) -> P:
        """Update the spot curve of this priced.

        Notes
        -----
        The operation is **not** performed in-place.

        Parameters
        ----------
        spot
            new spot curve

        Returns
        -------
        P
            updated priced
        """
        return self.__class__(self._flows, spot, self._spread)

    def update_spread(self: P, spread: ContinuousRate) -> P:
        """Update the spread of this priced.

        Notes
        -----
        The operation is **not** performed in-place.

        Parameters
        ----------
        spread
            new spread

        Returns
        -------
        P
            updated priced
        """
        return self.__class__(self._flows, self._spot, spread)

    def __str__(self) -> str:
        return (
            f"(flows={self._flows}, spot={self._spot}, spread={self._spread})"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._flows == other._flows
            and self._spot == other._spot
            and self._spread == other._spread
        )

    def __hash__(self) -> int:
        return hash((self._flows, self._spot, self._spread))
