from math import isclose
from unittest.mock import MagicMock, patch

import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.percent import Percent
from bperf.performance.generic import (
    CrossSectionalPerformanceCalculator,
    LongitudinalPerformanceCalculator,
)
from bperf.performance.total import (
    ITotalPerformanceCalculator,
    ITwoPointsTotalPerformanceCalculator,
    TotalPerformanceCalculator,
    TwoPointsTotalPerformanceCalculator,
)
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.priced.points.weighted import WeightedPricedPoints
from bperf.priced.points.weighted.sequence import WeightedPricedPointsSequence
from bperf.priced.points.weighted.table import WeightedPricedPointsTable
from bperf.rate.continuous import ContinuousRate
from bperf.rate.periodic import PeriodicRate
from bperf.term import Term
from bperf.termed import Termed


@pytest.fixture(scope="module")
def initial() -> PricedFlows:
    return PricedFlows(
        Flows(
            [
                Termed(Term(1.0), Money(0)),
                Termed(Term(2.0), Money(-3)),
                Termed(Term(3.0), Money(4)),
                Termed(Term(4.0), Money(1)),
                Termed(Term(5.0), Money(6)),
                Termed(Term(8.0), Money(-1)),
            ]
        ),
        SpotCurve(
            [
                Termed(Term(2.0), ContinuousRate(0.0)),
                Termed(Term(4.0), ContinuousRate(0.03)),
                Termed(Term(7.0), ContinuousRate(-0.01)),
            ]
        ),
        ContinuousRate(0.02),
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


class TestITwoPointsTotalPerformanceCalculator:
    def test(self, points: PricedPoints) -> None:
        calculator = ITwoPointsTotalPerformanceCalculator()
        with pytest.raises(NotImplementedError):
            calculator.calculate(points)


class TestTwoPointsTotalPerformanceCalculator:
    @pytest.fixture(scope="class")
    def calculator(self) -> TwoPointsTotalPerformanceCalculator:
        return TwoPointsTotalPerformanceCalculator()

    @pytest.fixture(scope="class")
    def offset(self) -> ContinuousRate:
        return ContinuousRate(0.03)

    @pytest.mark.parametrize(
        "flows_, expected",
        [
            (
                Flows(
                    [
                        Termed(Term(0.5), Money(0)),
                        Termed(Term(1.5), Money(-3)),
                        Termed(Term(2.5), Money(4)),
                        Termed(Term(3.5), Money(1)),
                        Termed(Term(4.5), Money(6)),
                        Termed(Term(7.5), Money(-1)),
                    ]
                ),
                PeriodicRate(-0.210421105734868),
            ),  # no payments (lapse of 0.5)
            (
                Flows(
                    [
                        Termed(Term(1), Money(-3)),
                        Termed(Term(2), Money(4)),
                        Termed(Term(3), Money(1)),
                        Termed(Term(4), Money(6)),
                        Termed(Term(7), Money(-1)),
                    ]
                ),
                PeriodicRate(-0.172325063687546),
            ),  # exactly one payment (lapse of 1)
            (
                Flows(
                    [
                        Termed(Term(0.5), Money(-3)),
                        Termed(Term(1.5), Money(4)),
                        Termed(Term(2.5), Money(1)),
                        Termed(Term(3.5), Money(6)),
                        Termed(Term(6.5), Money(-1)),
                    ]
                ),
                PeriodicRate(-0.099278303642644),
            ),  # one payment (lapse of 1.5)
            (
                Flows(
                    [
                        Termed(Term(0.75), Money(1)),
                        Termed(Term(1.75), Money(6)),
                        Termed(Term(4.75), Money(-1)),
                    ]
                ),
                PeriodicRate(0.165173908594169),
            ),  # multiple payments (lapse of 3.25)
            (
                Flows(
                    [
                        Termed(Term(1.0), Money(-1)),
                    ]
                ),
                PeriodicRate(0.261591759574128),
            ),  # one payment left (lapse of 7)
            (
                Flows([]),
                PeriodicRate(0.247885757244268),
            ),  # all paid (lapse of 8)
        ],
    )
    def test(
        self,
        calculator: TwoPointsTotalPerformanceCalculator,
        initial: PricedFlows,
        offset: ContinuousRate,
        flows_: Flows,
        expected: PeriodicRate,
    ) -> None:
        final = PricedFlows(
            flows_,
            initial.spot.add(offset),
            initial.spread + offset,
        )
        points = PricedPoints(initial, final)
        result = calculator.calculate(points)
        assert isclose(result, expected, rel_tol=1e-8, abs_tol=1e-8)


class TestITotalPerformanceCalculator:
    def test(self, table: WeightedPricedPointsTable) -> None:
        calculator = ITotalPerformanceCalculator()
        with pytest.raises(NotImplementedError):
            calculator.calculate(table)


class TestTotalPerformanceCalculator:
    _TOTAL = PeriodicRate(0.02)
    _PERCENT = Percent.from_float(_TOTAL)

    @patch.object(
        LongitudinalPerformanceCalculator,
        "calculate",
        return_value=_TOTAL,
    )
    def test(self, mocked: MagicMock, table: WeightedPricedPointsTable) -> None:
        calculator = TotalPerformanceCalculator(
            LongitudinalPerformanceCalculator(
                CrossSectionalPerformanceCalculator(
                    ITwoPointsTotalPerformanceCalculator(),
                )
            )
        )
        assert calculator.calculate(table) == self._PERCENT
        mocked.assert_called_once_with(table)
