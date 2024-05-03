import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.percent import Percent
from bperf.percent.sequence import PercentSequence
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.priced.points.sequence import PricedPointsSequence
from bperf.priced.points.weighted import WeightedPricedPoints
from bperf.priced.points.weighted.sequence import WeightedPricedPointsSequence
from bperf.rate.continuous import ContinuousRate
from bperf.term import Term
from bperf.termed import Termed


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


@pytest.fixture(scope="class")
def points(priced: PricedFlows) -> PricedPoints:
    return PricedPoints(
        priced,
        priced.update_spread(ContinuousRate(0.03)),
    )


class TestWeightedPricedPointsSequenceInvariants:
    @pytest.mark.parametrize(
        "percents",
        [
            PercentSequence(
                [
                    Percent(10000),
                ]
            ),
            PercentSequence(
                [
                    Percent(5000),
                    Percent(0),
                    Percent(-1000),
                    Percent(6000),
                ]
            ),
        ],
    )
    def test_when_sums_to_one(
        self,
        points: PricedPoints,
        percents: PercentSequence,
    ) -> None:
        WeightedPricedPointsSequence(
            WeightedPricedPoints(percent, points) for percent in percents
        )  # does not raise

    @pytest.mark.parametrize(
        "percents",
        [
            PercentSequence(
                [
                    Percent(10001),
                ]
            ),
            PercentSequence(
                [
                    Percent(5000),
                    Percent(0),
                    Percent(-1000),
                    Percent(5999),
                ]
            ),
        ],
    )
    def test_when_does_not_sums_to_one(
        self,
        points: PricedPoints,
        percents: PercentSequence,
    ) -> None:
        with pytest.raises(ValueError, match="sum"):
            WeightedPricedPointsSequence(
                WeightedPricedPoints(percent, points) for percent in percents
            )


class TestWeightedPricedPointsSequenceProperties:
    @pytest.fixture(scope="class")
    def percents(self) -> PercentSequence:
        return PercentSequence([Percent(1000), Percent(9000)])

    @pytest.fixture(scope="class")
    def points(self, points: PricedPoints) -> PricedPointsSequence:
        return PricedPointsSequence([points, points])

    @pytest.fixture(scope="class")
    def sequence(
        self,
        percents: PercentSequence,
        points: PricedPointsSequence,
    ) -> WeightedPricedPointsSequence:
        return WeightedPricedPointsSequence(
            WeightedPricedPoints(percent, points)
            for percent, points in zip(percents, points)
        )

    def test_percents(
        self,
        sequence: WeightedPricedPointsSequence,
        percents: PercentSequence,
    ) -> None:
        assert sequence.percents == percents

    def test_points(
        self,
        sequence: WeightedPricedPointsSequence,
        points: PricedPointsSequence,
    ) -> None:
        assert sequence.points == points


class TestWeightedPricedPointsSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> WeightedPricedPointsSequence:
        return WeightedPricedPointsSequence([])

    def test_percents(self, sequence: WeightedPricedPointsSequence) -> None:
        assert sequence.percents == PercentSequence([])

    def test_points(self, sequence: WeightedPricedPointsSequence) -> None:
        assert sequence.points == PricedPointsSequence([])
