import numpy as np
import pytest

from bperf.curve import Curve, SpotCurve
from bperf.discount.sequence import DiscountSequence
from bperf.rate.continuous import ContinuousRate
from bperf.rate.continuous.sequence import ContinuousRateSequence
from bperf.term import Term
from bperf.term.sequence import TermSequence
from bperf.termed import Termed


class TestCurveInvariants:
    def test_when_empty(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            Curve([])


class TestCurveProperties:
    @pytest.fixture(scope="class")
    def terms(self) -> TermSequence:
        return TermSequence(
            [
                Term(1.0),
                Term(2.0),
            ]
        )

    @pytest.fixture(scope="class")
    def rates(self) -> ContinuousRateSequence:
        return ContinuousRateSequence(
            [
                ContinuousRate(0.01),
                ContinuousRate(0.02),
            ]
        )

    @pytest.fixture(scope="class")
    def curve(
        self,
        terms: TermSequence,
        rates: ContinuousRateSequence,
    ) -> Curve:
        return Curve.from_tuples(zip(terms, rates))

    def test_rates(self, curve: Curve, rates: ContinuousRateSequence) -> None:
        assert curve.rates == rates


class TestSpotCurveDiscountAt:
    @pytest.mark.parametrize(
        "spot",
        [
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.01)),
                ]
            ),
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.01)),
                    Termed(Term(2.0), ContinuousRate(0.02)),
                ]
            ),
        ],
    )
    def test_when_no_terms(self, spot: SpotCurve) -> None:
        result = spot.discounts_at(TermSequence.empty())
        assert result == DiscountSequence.empty()

    @pytest.mark.parametrize(
        "spot",
        [
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.01)),
                ]
            ),
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.01)),
                    Termed(Term(2.0), ContinuousRate(0.02)),
                ]
            ),
        ],
    )
    @pytest.mark.parametrize(
        "terms",
        [
            TermSequence([Term(0.5)]),
            TermSequence([Term(1.0)]),
            TermSequence([Term(1.5)]),
            TermSequence([Term(2.0)]),
            TermSequence([Term(2.5)]),
            TermSequence([Term(0.5), Term(2.5)]),  # ordered
            TermSequence([Term(2.5), Term(0.5)]),  # unordered
            TermSequence([Term(2.5), Term(0.5), Term(2.5)]),  # repeating
        ],
    )
    def test_when_terms(
        self,
        spot: SpotCurve,
        terms: TermSequence,
    ) -> None:
        result = spot.discounts_at(terms)
        expected = DiscountSequence(
            rate.discount_at(term)
            for term, rate in zip(
                terms,
                ContinuousRateSequence.from_float(
                    np.interp(
                        np.array(terms, dtype=np.float_),
                        np.array(spot.terms, dtype=np.float_),
                        np.array(spot.rates, dtype=np.float_),
                    )
                ),
            )
        )
        assert result == expected


class TestSpotCurveAdd:
    @pytest.mark.parametrize(
        "spot",
        [
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.01)),
                ]
            ),
            SpotCurve(
                [
                    Termed(Term(1.0), ContinuousRate(0.01)),
                    Termed(Term(2.0), ContinuousRate(-0.02)),
                    Termed(Term(3.0), ContinuousRate(0.0)),
                ]
            ),
        ],
    )
    @pytest.mark.parametrize(
        "spread",
        [
            ContinuousRate(-0.02),
            ContinuousRate(0.0),
            ContinuousRate(0.03),
        ],
    )
    def test(self, spot: SpotCurve, spread: ContinuousRate) -> None:
        expected = SpotCurve.from_tuples(
            zip(spot.terms, spot.rates.add(spread))
        )
        assert spot.add(spread) == expected

    def test_new_curve(self) -> None:
        spot = SpotCurve(
            [
                Termed(Term(1.0), ContinuousRate(0.01)),
                Termed(Term(2.0), ContinuousRate(0.02)),
            ]
        )
        new = spot.add(ContinuousRate(0.0))
        assert new is not spot
