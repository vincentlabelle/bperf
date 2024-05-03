from typing import Dict
from unittest.mock import MagicMock, call, patch

import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.percent import Percent
from bperf.performance.effect import (
    EffectsCalculator,
    IEffectsCalculator,
    ITwoPointsEffectCalculator,
)
from bperf.performance.generic import (
    CrossSectionalPerformanceCalculator,
    LongitudinalPerformanceCalculator,
)
from bperf.priced.points import PricedPoints
from bperf.priced.points.weighted import WeightedPricedPoints
from bperf.priced.points.weighted.sequence import WeightedPricedPointsSequence
from bperf.priced.points.weighted.table import WeightedPricedPointsTable
from bperf.priced.priced import PricedFlows
from bperf.rate.continuous import ContinuousRate
from bperf.rate.periodic import PeriodicRate
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


class TestITwoPointsEffectCalculator:
    def test(self, points: PricedPoints) -> None:
        calculator = ITwoPointsEffectCalculator()
        with pytest.raises(NotImplementedError):
            calculator.calculate(points)


class TestIEffectsCalculator:
    def test(self, table: WeightedPricedPointsTable) -> None:
        calculator = IEffectsCalculator()
        with pytest.raises(NotImplementedError):
            calculator.calculate(table)


class TestEffectsCalculatorInvariants:
    def test_frozen(self) -> None:
        calculators: Dict[
            str,
            LongitudinalPerformanceCalculator[ITwoPointsEffectCalculator],
        ] = {}
        calculator = EffectsCalculator(calculators)
        calculators["effect"] = LongitudinalPerformanceCalculator(
            CrossSectionalPerformanceCalculator(
                ITwoPointsEffectCalculator(),
            )
        )
        assert calculator._items == ()


class TestEffectsCalculatorCalculate:
    _EFFECT = PeriodicRate(0.02)
    _PERCENT = Percent.from_float(_EFFECT)

    def test_when_no_calculators(
        self,
        table: WeightedPricedPointsTable,
    ) -> None:
        calculator = EffectsCalculator({})
        assert calculator.calculate(table) == {}

    @patch.object(
        LongitudinalPerformanceCalculator,
        "calculate",
        return_value=_EFFECT,
    )
    def test_when_one_calculator(
        self,
        mocked: MagicMock,
        table: WeightedPricedPointsTable,
    ) -> None:
        calculators = {
            "effect": LongitudinalPerformanceCalculator(
                CrossSectionalPerformanceCalculator(
                    ITwoPointsEffectCalculator(),
                )
            )
        }
        calculator = EffectsCalculator(calculators)
        expected = {name: self._PERCENT for name in calculators}
        assert calculator.calculate(table) == expected
        mocked.assert_called_once_with(table)

    def test_when_multiple_calculators(
        self,
        table: WeightedPricedPointsTable,
    ) -> None:
        expected = {"one": self._PERCENT, "two": Percent(3)}
        calculators = {
            name: MagicMock(
                spec=LongitudinalPerformanceCalculator,
                **{"calculate.return_value": PeriodicRate(effect)},
            )
            for name, effect in expected.items()
        }
        calculator = EffectsCalculator(calculators)  # type: ignore[arg-type]
        assert calculator.calculate(table) == expected
        for mock in calculators.values():
            assert mock.method_calls == [call.calculate(table)]
