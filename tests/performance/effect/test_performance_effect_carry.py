from math import isclose

import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.performance.effect.carry import TwoPointsCarryEffectCalculator
from bperf.priced import PricedFlows
from bperf.priced.points import PricedPoints
from bperf.rate.continuous import ContinuousRate
from bperf.rate.periodic import PeriodicRate
from bperf.term import Term
from bperf.termed import Termed


@pytest.fixture(scope="module")
def calculator() -> TwoPointsCarryEffectCalculator:
    return TwoPointsCarryEffectCalculator()


class TestTwoPointsCarryEffectCalculator:
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
                PeriodicRate(0.0150574715669172),
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
                PeriodicRate(0.0309099702258793),
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
                PeriodicRate(0.0907540223422886),
            ),  # one payment (lapse of 1.5)
            (
                Flows(
                    [
                        Termed(Term(0.75), Money(1)),
                        Termed(Term(1.75), Money(6)),
                        Termed(Term(4.75), Money(-1)),
                    ]
                ),
                PeriodicRate(0.239290552469953),
            ),  # multiple payments (lapse of 3.25)
            (
                Flows(
                    [
                        Termed(Term(1.0), Money(-1)),
                    ]
                ),
                PeriodicRate(0.251415727752131),
            ),  # one payment left (lapse of 7)
            (
                Flows([]),
                PeriodicRate(0.247885757244268),
            ),  # all paid (lapse of 8)
        ],
    )
    def test(
        self,
        calculator: TwoPointsCarryEffectCalculator,
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
