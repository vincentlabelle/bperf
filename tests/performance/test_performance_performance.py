from typing import Any, Iterable, Tuple, Union
from unittest.mock import MagicMock, patch

import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.percent import Percent
from bperf.performance import IPerformanceCalculator, PerformanceCalculator
from bperf.performance.effect import IEffectsCalculator
from bperf.performance.residual import IResidualCalculator
from bperf.performance.total import ITotalPerformanceCalculator
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.priced.points.weighted import WeightedPricedPoints
from bperf.priced.points.weighted.sequence import WeightedPricedPointsSequence
from bperf.priced.points.weighted.table import WeightedPricedPointsTable
from bperf.rate.continuous import ContinuousRate
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
def sequence(
    initial: PricedFlows,
    final: PricedFlows,
) -> WeightedPricedPointsSequence:
    return WeightedPricedPointsSequence(
        [
            WeightedPricedPoints(
                Percent(500),
                PricedPoints(initial, final),
            ),
            WeightedPricedPoints(
                Percent(9500),
                PricedPoints(final, initial),
            ),
        ]
    )


@pytest.fixture(scope="module")
def table(sequence: WeightedPricedPointsSequence) -> WeightedPricedPointsTable:
    return WeightedPricedPointsTable([sequence, sequence[::-1]])


class TestIPerformanceCalculator:
    def test(self, table: WeightedPricedPointsTable) -> None:
        calculator = IPerformanceCalculator()
        with pytest.raises(NotImplementedError):
            calculator.calculate(table)


class TestPerformanceCalculator:
    _TOTAL = Percent(1)
    _EFFECTS = {
        "one": Percent(2),
        "two": Percent(3),
    }
    _RESIDUAL = Percent(4)

    @patch.object(
        IResidualCalculator,
        "calculate",
        return_value=_RESIDUAL,
    )
    @patch.object(
        IEffectsCalculator,
        "calculate",
        return_value=_EFFECTS,
    )
    @patch.object(
        ITotalPerformanceCalculator,
        "calculate",
        return_value=_TOTAL,
    )
    def test(
        self,
        total: MagicMock,
        effects: MagicMock,
        residual: MagicMock,
        table: WeightedPricedPointsTable,
    ) -> None:
        calculator = PerformanceCalculator(
            ITotalPerformanceCalculator(),
            IEffectsCalculator(),
            IResidualCalculator(),
        )
        expected = {
            PerformanceCalculator._TOTAL_NAME: self._TOTAL,
            **self._EFFECTS,
            PerformanceCalculator._RESIDUAL_NAME: self._RESIDUAL,
        }
        assert calculator.calculate(table) == expected
        total.assert_called_once_with(table)
        effects.assert_called_once_with(table)
        self._assert_residual_called_once_with(
            residual,
            self._TOTAL,
            self._EFFECTS.values(),
        )

    def _assert_residual_called_once_with(
        self,
        residual: MagicMock,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        assert residual.call_count == 1
        assert residual.call_args.kwargs == kwargs
        call_args = self._iterable_args_to_tuple(residual.call_args.args)
        expected_args = self._iterable_args_to_tuple(args)
        assert call_args == expected_args

    @staticmethod
    def _iterable_args_to_tuple(
        args: Tuple[Any, ...],
    ) -> Tuple[Union[Any, Tuple[Any]], ...]:
        return tuple(
            tuple(arg) if isinstance(arg, Iterable) else arg for arg in args
        )
