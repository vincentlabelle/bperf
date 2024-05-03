import pytest

from bperf.curve import SpotCurve
from bperf.flows import Flows
from bperf.money import Money
from bperf.money.sequence import MoneySequence
from bperf.rate.continuous import ContinuousRate
from bperf.term import Term
from bperf.term.sequence import TermSequence
from bperf.termed import Termed


class TestFlowsProperties:
    @pytest.fixture(scope="class")
    def terms(self) -> TermSequence:
        return TermSequence([Term(1.0), Term(2.0)])

    @pytest.fixture(scope="class")
    def monies(self) -> MoneySequence:
        return MoneySequence([Money(3), Money(-2)])

    @pytest.fixture(scope="class")
    def flows(self, terms: TermSequence, monies: MoneySequence) -> Flows:
        return Flows.from_tuples(zip(terms, monies))

    def test_monies(self, flows: Flows, monies: MoneySequence) -> None:
        assert flows.monies == monies


class TestFlowsPv:
    @pytest.mark.parametrize(
        "flows",
        [
            Flows(
                [
                    Termed(Term(1.0), Money(3)),
                ]
            ),
            Flows(
                [
                    Termed(Term(1.0), Money(3)),
                    Termed(Term(2.0), Money(-2)),
                ]
            ),
        ],
    )
    @pytest.mark.parametrize(
        "spot",
        [
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.02)),
                ]
            ),
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.02)),
                    Termed(Term(2.0), ContinuousRate(0.01)),
                ]
            ),
        ],
    )
    def test(self, flows: Flows, spot: SpotCurve) -> None:
        expected = flows.monies.pv(spot.discounts_at(flows.terms))
        assert flows.pv(spot) == expected


class TestFlowsSum:
    @pytest.mark.parametrize(
        "flows",
        [
            Flows(
                [
                    Termed(Term(1.0), Money(3)),
                ]
            ),
            Flows(
                [
                    Termed(Term(1.0), Money(3)),
                    Termed(Term(2.0), Money(-2)),
                    Termed(Term(4.0), Money(0)),
                ]
            ),
        ],
    )
    def test(self, flows: Flows) -> None:
        assert flows.sum() == flows.monies.sum()
