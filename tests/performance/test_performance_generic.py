from unittest.mock import MagicMock, call, patch

import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.percent import Percent
from bperf.performance.generic import (
    CrossSectionalPerformanceCalculator,
    ITwoPointsPerformanceCalculator,
    LongitudinalPerformanceCalculator,
)
from bperf.priced.points import PricedPoints
from bperf.priced.points.weighted import WeightedPricedPoints
from bperf.priced.points.weighted.sequence import WeightedPricedPointsSequence
from bperf.priced.points.weighted.table import WeightedPricedPointsTable
from bperf.priced.priced import PricedFlows
from bperf.rate.continuous import ContinuousRate
from bperf.rate.periodic import PeriodicRate
from bperf.rate.periodic.sequence import PeriodicRateSequence
from bperf.term import Term
from bperf.termed import Termed


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
        ContinuousRate(0.002),
    )


@pytest.fixture(scope="module")
def final(initial: PricedFlows) -> PricedFlows:
    return initial.update_spread(ContinuousRate(-0.003))


@pytest.fixture(scope="module")
def points(initial: PricedFlows, final: PricedFlows) -> PricedPoints:
    return PricedPoints(initial, final)


@pytest.fixture(scope="module")
def sequence(points: PricedPoints) -> WeightedPricedPointsSequence:
    return WeightedPricedPointsSequence(
        [
            WeightedPricedPoints(
                Percent(500),
                points,
            ),
            WeightedPricedPoints(
                Percent(9500),
                PricedPoints(points.final, points.initial),
            ),
        ]
    )


@pytest.fixture(scope="module")
def table(sequence: WeightedPricedPointsSequence) -> WeightedPricedPointsTable:
    return WeightedPricedPointsTable([sequence, sequence[::-1]])


class TestITwoPointsPerformanceCalculator:
    def test(self, points: PricedPoints) -> None:
        calculator = ITwoPointsPerformanceCalculator()
        with pytest.raises(NotImplementedError):
            calculator.calculate(points)


class TestCrossSectionalPerformanceCalculator:
    _RATES = PeriodicRateSequence(
        [
            PeriodicRate(0.02),
            PeriodicRate(-0.03),
        ]
    )  # same length as sequence!

    @patch.object(
        ITwoPointsPerformanceCalculator,
        "calculate",
        side_effect=_RATES,
    )
    def test(
        self,
        mocked: MagicMock,
        sequence: WeightedPricedPointsSequence,
    ) -> None:
        calculator = CrossSectionalPerformanceCalculator(
            ITwoPointsPerformanceCalculator()
        )
        expected = self._RATES.dot(sequence.percents)
        assert calculator.calculate(sequence) == expected
        assert mocked.mock_calls == [call(points) for points in sequence.points]


class TestLongitudinalPerformanceCalculator:
    _RATES = PeriodicRateSequence(
        [
            PeriodicRate(0.02),
            PeriodicRate(-0.03),
        ]
    )  # same length as table!

    @patch.object(
        CrossSectionalPerformanceCalculator,
        "calculate",
        side_effect=_RATES,
    )
    def test(self, mocked: MagicMock, table: WeightedPricedPointsTable) -> None:
        calculator = LongitudinalPerformanceCalculator(
            CrossSectionalPerformanceCalculator(
                ITwoPointsPerformanceCalculator()
            ),
        )
        assert calculator.calculate(table) == self._RATES.compound()
        assert mocked.mock_calls == [call(sequence) for sequence in table]
