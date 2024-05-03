from math import exp

import pytest

from bperf.discount import Discount
from bperf.rate.continuous import ContinuousRate
from bperf.term import Term


class TestContinuousRateDiscountAt:
    @pytest.mark.parametrize(
        "rate",
        [
            ContinuousRate(0.01),
            ContinuousRate(0.0),
            ContinuousRate(-0.02),
        ],
    )
    def test_when_normal(self, rate: ContinuousRate) -> None:
        term = Term(2.1)
        expected = Discount(exp(-float(rate) * float(term)))
        assert rate.discount_at(term) == expected

    def test_when_edge(self) -> None:
        rate, term = ContinuousRate(1e308), Term(1e308)
        assert rate.discount_at(term) == Discount(0.0)

    @pytest.mark.parametrize("term", [Term(1e308), Term(1.0)])
    def test_when_overflow(self, term: Term) -> None:
        rate = ContinuousRate(-1e308)
        with pytest.raises(OverflowError, match="overflow"):
            rate.discount_at(term)
