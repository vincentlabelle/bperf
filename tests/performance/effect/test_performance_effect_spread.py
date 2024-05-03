from math import isclose

import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.performance.effect.spread import TwoPointsSpreadEffectCalculator
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.rate.continuous import ContinuousRate
from bperf.rate.periodic import PeriodicRate
from bperf.term import Term
from bperf.termed import Termed


@pytest.fixture(scope="module")
def calculator() -> TwoPointsSpreadEffectCalculator:
    return TwoPointsSpreadEffectCalculator()


class TestTwoPointsSpreadEffectCalculator:
    @pytest.fixture(scope="class")
    def flows(self) -> Flows:
        return Flows(
            [
                Termed(Term(1.0), Money(0)),
                Termed(Term(2.0), Money(-3)),
                Termed(Term(3.0), Money(4)),
                Termed(Term(4.0), Money(1)),
                Termed(Term(5.0), Money(6)),
                Termed(Term(8.0), Money(-1)),
            ]
        )

    @pytest.fixture(scope="class")
    def spot(self) -> SpotCurve:
        return SpotCurve(
            [
                Termed(Term(2.0), ContinuousRate(0.0)),
                Termed(Term(4.0), ContinuousRate(0.03)),
                Termed(Term(7.0), ContinuousRate(-0.01)),
            ]
        )

    @pytest.fixture(scope="class")
    def spread(self) -> ContinuousRate:
        return ContinuousRate(0.02)

    @pytest.fixture(scope="class")
    def initial(
        self,
        flows: Flows,
        spot: SpotCurve,
        spread: ContinuousRate,
    ) -> PricedFlows:
        return PricedFlows(flows, spot, spread)

    @pytest.fixture(scope="class")
    def offset(self) -> ContinuousRate:
        return ContinuousRate(0.03)

    def test(
        self,
        calculator: TwoPointsSpreadEffectCalculator,
        initial: PricedFlows,
        offset: ContinuousRate,
    ) -> None:
        spread = ContinuousRate(0.06)  # +0.04
        final = PricedFlows(
            Flows([]),
            initial.spot.add(offset),
            spread,
        )
        points = PricedPoints(initial, final)
        result = calculator.calculate(points)
        expected = PeriodicRate(-0.171016327678981)
        assert isclose(result, expected, rel_tol=1e-8, abs_tol=1e-8)
