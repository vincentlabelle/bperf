import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.percent import Percent
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.priced.points.weighted import WeightedPricedPoints
from bperf.rate.continuous import ContinuousRate
from bperf.term import Term
from bperf.termed import Termed


@pytest.fixture(scope="module")
def percent() -> Percent:
    return Percent(1)


@pytest.fixture(scope="module")
def priced() -> PricedFlows:
    return PricedFlows(
        Flows(
            [
                Termed(Term(1.0), Money(1.0)),
            ]
        ),
        SpotCurve(
            [
                Termed(Term(1.0), ContinuousRate(0.005)),
            ]
        ),
        ContinuousRate(0.01),
    )


@pytest.fixture(scope="module")
def points(priced: PricedFlows) -> PricedPoints:
    return PricedPoints(
        priced,
        priced.update_spread(ContinuousRate(0.03)),
    )


@pytest.fixture(scope="module")
def weighted(percent: Percent, points: PricedPoints) -> WeightedPricedPoints:
    return WeightedPricedPoints(percent, points)


class TestWeightedPricedPointsEqual:
    def test_when_equal(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
        points: PricedPoints,
    ) -> None:
        other = WeightedPricedPoints(percent, points)
        assert other == weighted

    def test_when_different_percent(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
        points: PricedPoints,
    ) -> None:
        other = WeightedPricedPoints(percent + Percent(1), points)
        assert other != weighted

    def test_when_different_points(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
        points: PricedPoints,
    ) -> None:
        points_ = PricedPoints(
            points.initial,
            points.final.update_spread(ContinuousRate(0.0)),
        )
        other = WeightedPricedPoints(percent, points_)
        assert other != weighted

    def test_when_different_object(
        self,
        weighted: WeightedPricedPoints,
    ) -> None:
        assert weighted != "a"


class TestWeightedPricedPointsHash:
    def test_when_equal(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
        points: PricedPoints,
    ) -> None:
        other = WeightedPricedPoints(percent, points)
        assert hash(other) == hash(weighted)

    def test_when_different_percent(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
        points: PricedPoints,
    ) -> None:
        other = WeightedPricedPoints(percent + Percent(1), points)
        assert hash(other) != hash(weighted)

    def test_when_different_points(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
        points: PricedPoints,
    ) -> None:
        points_ = PricedPoints(
            points.initial,
            points.final.update_spread(ContinuousRate(0.0)),
        )
        other = WeightedPricedPoints(percent, points_)
        assert hash(other) != hash(weighted)


class TestWeightedPricedPointsRepresentation:
    def test(self, weighted: WeightedPricedPoints) -> None:
        assert repr(weighted) == f"<{weighted.__class__.__name__}{weighted}>"


class TestWeightedPricedPointsCasting:
    def test_str(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
        points: PricedPoints,
    ) -> None:
        assert str(weighted) == f"(percent={percent}, points={points})"


class TestWeightedPricedPointsProperties:
    def test_percent(
        self,
        weighted: WeightedPricedPoints,
        percent: Percent,
    ) -> None:
        assert weighted.percent == percent

    def test_points(
        self,
        weighted: WeightedPricedPoints,
        points: PricedPoints,
    ) -> None:
        assert weighted.points == points
