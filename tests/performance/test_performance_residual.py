from typing import Tuple

import pytest

from bperf.percent import Percent
from bperf.percent.sequence import PercentSequence
from bperf.performance.residual import IResidualCalculator, ResidualCalculator


class TestIResidualCalculator:
    def test(self) -> None:
        calculator = IResidualCalculator()
        with pytest.raises(NotImplementedError):
            calculator.calculate(
                Percent(100),
                [],
            )


class TestResidualCalculator:
    @pytest.fixture(scope="class")
    def calculator(self) -> ResidualCalculator:
        return ResidualCalculator()

    @pytest.mark.parametrize("total", [Percent(1), Percent(0), Percent(-1)])
    @pytest.mark.parametrize(
        "effects",
        [
            (),
            (Percent(0),),
            (Percent(1), Percent(2)),
            (Percent(-2), Percent(1)),
        ],
    )
    def test(
        self,
        calculator: ResidualCalculator,
        total: Percent,
        effects: Tuple[Percent, ...],
    ) -> None:
        expected = PercentSequence(effects).difference_with(total)
        assert calculator.calculate(total, iter(effects)) == expected
