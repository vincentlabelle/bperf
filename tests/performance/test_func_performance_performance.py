from typing import Dict

import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.percent import Percent
from bperf.performance import PerformanceCalculator
from bperf.performance.effect import EffectsCalculator
from bperf.performance.generic import (
    CrossSectionalPerformanceCalculator,
    LongitudinalPerformanceCalculator,
)
from bperf.performance.residual import ResidualCalculator
from bperf.performance.total import (
    TotalPerformanceCalculator,
    TwoPointsTotalPerformanceCalculator,
)
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.priced.points.weighted import WeightedPricedPoints
from bperf.priced.points.weighted.sequence import WeightedPricedPointsSequence
from bperf.priced.points.weighted.table import WeightedPricedPointsTable
from bperf.rate.continuous import ContinuousRate
from bperf.term import Term
from bperf.termed import Termed

_POINTS_0 = PricedPoints(
    PricedFlows(
        Flows(
            [
                Termed(Term(1.0), Money(1.0)),
                Termed(Term(2.0), Money(2.0)),
                Termed(Term(3.0), Money(3.0)),
            ]
        ),
        SpotCurve(
            [
                Termed(Term(1.0), ContinuousRate(0.01)),
                Termed(Term(2.0), ContinuousRate(0.02)),
                Termed(Term(3.0), ContinuousRate(0.03)),
            ]
        ),
        ContinuousRate(0.04),
    ),
    PricedFlows(
        Flows(
            [
                Termed(Term(0.998), Money(1.0)),
                Termed(Term(1.998), Money(2.0)),
                Termed(Term(2.998), Money(3.0)),
            ]
        ),
        SpotCurve(
            [
                Termed(Term(1.0), ContinuousRate(0.02)),
                Termed(Term(2.0), ContinuousRate(0.03)),
                Termed(Term(3.0), ContinuousRate(0.04)),
            ]
        ),
        ContinuousRate(0.035),
    ),
)
_POINTS_1 = PricedPoints(_POINTS_0.final, _POINTS_0.initial)


@pytest.fixture(scope="module")
def total() -> TotalPerformanceCalculator:
    return TotalPerformanceCalculator(
        LongitudinalPerformanceCalculator(
            CrossSectionalPerformanceCalculator(
                TwoPointsTotalPerformanceCalculator(),
            )
        )
    )


@pytest.fixture(scope="module")
def residual() -> ResidualCalculator:
    return ResidualCalculator()


class TestPerformanceCalculatorNoEffects:
    @pytest.fixture(scope="class")
    def effects(self) -> EffectsCalculator:
        return EffectsCalculator({})

    @pytest.mark.parametrize(
        "table",
        [
            WeightedPricedPointsTable([]),
            WeightedPricedPointsTable(
                [
                    WeightedPricedPointsSequence([]),
                ]
            ),  # one
            WeightedPricedPointsTable(
                [
                    WeightedPricedPointsSequence([]),
                    WeightedPricedPointsSequence([]),
                ]
            ),  # multiple
        ],
    )
    def test_when_no_points(
        self,
        total: TotalPerformanceCalculator,
        effects: EffectsCalculator,
        residual: ResidualCalculator,
        table: WeightedPricedPointsTable,
    ) -> None:
        calculator = PerformanceCalculator(total, effects, residual)
        expected = {"total": Percent(0), "residual": Percent(0)}
        assert calculator.calculate(table) == expected

    @pytest.mark.parametrize(
        "table",
        [
            WeightedPricedPointsTable(
                [
                    WeightedPricedPointsSequence(
                        [
                            WeightedPricedPoints(
                                Percent(10000),
                                _POINTS_0,
                            )
                        ]
                    ),
                ]
            ),  # one
            WeightedPricedPointsTable(
                [
                    WeightedPricedPointsSequence([]),
                    WeightedPricedPointsSequence(
                        [
                            WeightedPricedPoints(
                                Percent(10000),
                                _POINTS_0,
                            )
                        ]
                    ),
                ]
            ),  # multiple
        ],
    )
    def test_when_one_points(
        self,
        total: TotalPerformanceCalculator,
        effects: EffectsCalculator,
        residual: ResidualCalculator,
        table: WeightedPricedPointsTable,
    ) -> None:
        calculator = PerformanceCalculator(total, effects, residual)
        expected = {"total": Percent(-112), "residual": Percent(-112)}
        assert calculator.calculate(table) == expected

    @pytest.mark.parametrize(
        "table, expected",
        [
            (
                WeightedPricedPointsTable(
                    [
                        WeightedPricedPointsSequence(
                            [
                                WeightedPricedPoints(
                                    Percent(500),
                                    _POINTS_0,
                                ),
                                WeightedPricedPoints(
                                    Percent(9500),
                                    _POINTS_1,
                                ),
                            ]
                        ),
                    ]
                ),  # one
                {"total": Percent(102), "residual": Percent(102)},
            ),
            (
                WeightedPricedPointsTable(
                    [
                        WeightedPricedPointsSequence([]),
                        WeightedPricedPointsSequence(
                            [
                                WeightedPricedPoints(
                                    Percent(500),
                                    _POINTS_0,
                                ),
                                WeightedPricedPoints(
                                    Percent(10000),
                                    _POINTS_1,
                                ),
                                WeightedPricedPoints(
                                    Percent(0),
                                    _POINTS_0,
                                ),
                                WeightedPricedPoints(
                                    Percent(-500),
                                    _POINTS_1,
                                ),
                            ]
                        ),
                        WeightedPricedPointsSequence(
                            [
                                WeightedPricedPoints(
                                    Percent(10000),
                                    _POINTS_0,
                                ),
                            ]
                        ),
                    ]
                ),  # multiple
                {"total": Percent(-11), "residual": Percent(-11)},
            ),
        ],
    )
    def test_when_multiple_points(
        self,
        total: TotalPerformanceCalculator,
        effects: EffectsCalculator,
        residual: ResidualCalculator,
        table: WeightedPricedPointsTable,
        expected: Dict[str, Percent],
    ) -> None:
        calculator = PerformanceCalculator(total, effects, residual)
        assert calculator.calculate(table) == expected
