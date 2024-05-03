import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.rate.continuous import ContinuousRate
from bperf.term import Term
from bperf.termed import Termed


@pytest.fixture(scope="module")
def final() -> PricedFlows:
    return PricedFlows(
        Flows(
            [
                Termed(Term(0.5), Money(1)),
            ]
        ),
        SpotCurve(
            [
                Termed(Term(1.0), ContinuousRate(0.03)),
            ]
        ),
        ContinuousRate(0.015),
    )


class TestPricedPointsInvariants:
    @pytest.fixture(scope="class")
    def spot(self) -> SpotCurve:
        return SpotCurve(
            [
                Termed(Term(1.0), ContinuousRate(0.01)),
            ]
        )

    @pytest.fixture(scope="class")
    def spread(self) -> ContinuousRate:
        return ContinuousRate(0.025)

    def test_when_initial_price_is_zero(
        self,
        final: PricedFlows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> None:
        initial = PricedFlows(
            Flows(
                [
                    Termed(Term(1.0), Money(0)),
                ]
            ),
            spot,
            spread,
        )
        with pytest.raises(ValueError, match="initial price"):
            PricedPoints(initial, final)

    @pytest.mark.parametrize(
        "flow",
        [
            Money(1),
            Money(-1),
        ],
    )
    def test_when_initial_price_is_not_zero(
        self,
        final: PricedFlows,
        spot: SpotCurve,
        spread: ContinuousRate,
        flow: Money,
    ) -> None:
        initial = PricedFlows(
            Flows(
                [
                    Termed(Term(1.0), flow),
                ]
            ),
            spot,
            spread,
        )
        PricedPoints(initial, final)  # does not raise


@pytest.fixture(scope="module")
def initial() -> PricedFlows:
    return PricedFlows(
        Flows(
            [
                Termed(Term(1.0), Money(1)),
            ]
        ),
        SpotCurve(
            [
                Termed(Term(1.0), ContinuousRate(0.01)),
            ]
        ),
        ContinuousRate(0.025),
    )


@pytest.fixture(scope="module")
def points(initial: PricedFlows, final: PricedFlows) -> PricedPoints:
    return PricedPoints(initial, final)


class TestPricedPointsEqual:
    def test_when_equal(
        self,
        points: PricedPoints,
        initial: PricedFlows,
        final: PricedFlows,
    ) -> None:
        other = PricedPoints(initial, final)
        assert other == points

    def test_when_different_initial(
        self,
        points: PricedPoints,
        initial: PricedFlows,
        final: PricedFlows,
    ) -> None:
        initial_ = initial.update_spread(ContinuousRate(0.0))
        other = PricedPoints(initial_, final)
        assert other != points

    def test_when_different_final(
        self,
        points: PricedPoints,
        initial: PricedFlows,
        final: PricedFlows,
    ) -> None:
        final_ = final.update_spread(ContinuousRate(0.0))
        other = PricedPoints(initial, final_)
        assert other != points

    def test_when_different_object(self, points: PricedPoints) -> None:
        assert points != "a"


class TestPricedPointsHash:
    def test_when_equal(
        self,
        points: PricedPoints,
        initial: PricedFlows,
        final: PricedFlows,
    ) -> None:
        other = PricedPoints(initial, final)
        assert hash(other) == hash(points)

    def test_when_different_initial(
        self,
        points: PricedPoints,
        initial: PricedFlows,
        final: PricedFlows,
    ) -> None:
        initial_ = initial.update_spread(ContinuousRate(0.0))
        other = PricedPoints(initial_, final)
        assert hash(other) != hash(points)

    def test_when_different_final(
        self,
        points: PricedPoints,
        initial: PricedFlows,
        final: PricedFlows,
    ) -> None:
        final_ = final.update_spread(ContinuousRate(0.0))
        other = PricedPoints(initial, final_)
        assert hash(other) != hash(points)


class TestPricedPointsRepresentation:
    def test(self, points: PricedPoints) -> None:
        assert repr(points) == f"<{points.__class__.__name__}{points}>"


class TestPricedPointsCasting:
    def test_str(
        self,
        points: PricedPoints,
        initial: PricedFlows,
        final: PricedFlows,
    ) -> None:
        assert str(points) == f"(initial={initial}, final={final})"


class TestPricedPointsProperties:
    def test_initial(self, points: PricedPoints, initial: PricedFlows) -> None:
        assert points.initial == initial

    def test_final(self, points: PricedPoints, final: PricedFlows) -> None:
        assert points.final == final

    @pytest.mark.parametrize(
        "flows",
        [
            Flows([]),
            Flows(
                [
                    Termed(Term(0.5), Money(1)),
                ]
            ),
            Flows(
                [
                    Termed(Term(1.0), Money(2)),
                ]
            ),
        ],
    )
    def test_payments(
        self,
        initial: PricedFlows,
        final: PricedFlows,
        flows: Flows,
    ) -> None:
        final_ = final.update_flows(flows)
        points = PricedPoints(initial, final_)
        assert points.payments == initial.flows.sum() - final_.flows.sum()
