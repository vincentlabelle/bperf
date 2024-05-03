import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.priced import PricedFlows
from bperf.rate.continuous import ContinuousRate
from bperf.term import Term
from bperf.termed import Termed


@pytest.fixture(scope="module")
def flows() -> Flows:
    return Flows(
        [
            Termed(Term(1.0), Money(3)),
            Termed(Term(2.0), Money(-2)),
        ]
    )


@pytest.fixture(scope="module")
def spot() -> SpotCurve:
    return SpotCurve(
        [
            Termed(Term(0.5), ContinuousRate(0.02)),
            Termed(Term(3.0), ContinuousRate(0.01)),
        ]
    )


@pytest.fixture(scope="module")
def spread() -> ContinuousRate:
    return ContinuousRate(-0.03)


@pytest.fixture(scope="module")
def priced(
    flows: Flows,
    spot: SpotCurve,
    spread: ContinuousRate,
) -> PricedFlows:
    return PricedFlows(flows, spot, spread)


class TestPricedFlowsEqual:
    def test_when_equal(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        other = PricedFlows(flows, spot, spread)
        assert other == priced

    def test_when_different_flows(
        self,
        priced: PricedFlows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        flows = Flows([Termed(Term(0.1), Money(0))])
        other = PricedFlows(flows, spot, spread)
        assert other != priced

    def test_when_different_spot(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        other = PricedFlows(flows, spot.add(spread), spread)
        assert other != priced

    def test_when_different_spread(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        other = PricedFlows(flows, spot, spread + ContinuousRate(0.01))
        assert other != priced

    def test_when_different_object(self, priced: PricedFlows) -> None:
        assert priced != "a"


class TestPricedFlowsHash:
    def test_when_equal(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        other = PricedFlows(flows, spot, spread)
        assert hash(other) == hash(priced)

    def test_when_different_flows(
        self,
        priced: PricedFlows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        flows = Flows([Termed(Term(0.1), Money(0))])
        other = PricedFlows(flows, spot, spread)
        assert hash(other) != hash(priced)

    def test_when_different_spot(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        other = PricedFlows(flows, spot.add(spread), spread)
        assert hash(other) != hash(priced)

    def test_when_different_spread(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        other = PricedFlows(flows, spot, spread + ContinuousRate(0.01))
        assert hash(other) != hash(priced)


class TestPriceFlowsRepresentation:
    def test(self, priced: PricedFlows) -> None:
        assert repr(priced) == f"<{priced.__class__.__name__}{priced}>"


class TestPriceFlowsCasting:
    def test_str(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        expected = f"(flows={flows}, spot={spot}, spread={spread})"
        assert str(priced) == expected


class TestPricedFlowsProperties:
    def test_price(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        assert priced.price == flows.pv(spot.add(spread))

    def test_flows(self, priced: PricedFlows, flows: Flows) -> None:
        assert priced.flows == flows

    def test_spot(self, priced: PricedFlows, spot: SpotCurve) -> None:
        assert priced.spot == spot

    def test_spread(self, priced: PricedFlows, spread: ContinuousRate) -> None:
        assert priced.spread == spread


class TestPricedFlowsUpdate:
    def test_update_flows(
        self,
        priced: PricedFlows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        flows = Flows([Termed(Term(0.1), Money(0))])
        expected = PricedFlows(flows, spot, spread)
        assert priced.update_flows(flows) == expected

    def test_update_flows_is_new(self, priced: PricedFlows) -> None:
        flows = Flows([Termed(Term(0.1), Money(0))])
        new = priced.update_flows(flows)
        assert new is not priced

    def test_update_spot(
        self,
        priced: PricedFlows,
        flows: Flows,
        spread: ContinuousRate,
    ) -> None:
        spot = SpotCurve([Termed(Term(0.1), ContinuousRate(0.0))])
        expected = PricedFlows(flows, spot, spread)
        assert priced.update_spot(spot) == expected

    def test_update_spot_is_new(self, priced: PricedFlows) -> None:
        spot = SpotCurve([Termed(Term(0.1), ContinuousRate(0.0))])
        new = priced.update_spot(spot)
        assert new is not priced

    def test_update_spread(
        self,
        priced: PricedFlows,
        flows: Flows,
        spot: SpotCurve,
    ) -> None:
        spread = ContinuousRate(0.0)
        expected = PricedFlows(flows, spot, spread)
        assert priced.update_spread(spread) == expected

    def test_update_spread_is_new(self, priced: PricedFlows) -> None:
        spread = ContinuousRate(0.0)
        new = priced.update_spread(spread)
        assert new is not priced
