from math import inf, nan
from typing import SupportsFloat

import pytest

from bperf.pv import PresentValue
from bperf.rate.periodic import PeriodicRate


class TestPresentValueGrowth:
    @pytest.mark.parametrize(
        "initial",
        [
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    @pytest.mark.parametrize(
        "final",
        [
            PresentValue(0.0),
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    @pytest.mark.parametrize(
        "payments",
        [
            inf,
            nan,
            -inf,
        ],
    )
    def test_when_non_finite_payments(
        self,
        initial: PresentValue,
        final: PresentValue,
        payments: float,
    ) -> None:
        with pytest.raises(ValueError, match="finite"):
            initial.growth(final, payments=payments)

    @pytest.mark.parametrize(
        "initial",
        [
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    def test_when_overflow(self, initial: PresentValue) -> None:
        final, payments = PresentValue(1e308), 1e308
        with pytest.raises(OverflowError, match="overflow"):
            initial.growth(final, payments=payments)

    @pytest.mark.parametrize(
        "payments",
        [
            0.0,
            200.0,
            -50.0,
        ],
    )
    @pytest.mark.parametrize(
        "final",
        [
            PresentValue(0.0),
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    def test_when_zero_division_error(
        self,
        final: PresentValue,
        payments: float,
    ) -> None:
        initial = PresentValue(0.0)
        with pytest.raises(ZeroDivisionError, match="zero"):
            initial.growth(final, payments=payments)

    @pytest.mark.parametrize(
        "initial",
        [
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    @pytest.mark.parametrize(
        "final",
        [
            PresentValue(0.0),
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    def test_when_payments_defaults_to_zero(
        self,
        initial: PresentValue,
        final: PresentValue,
    ) -> None:
        assert initial.growth(final) == initial.growth(final, payments=0.0)

    @pytest.mark.parametrize(
        "initial",
        [
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    @pytest.mark.parametrize(
        "final",
        [
            PresentValue(0.0),
            PresentValue(-200.0),
            PresentValue(150.0),
        ],
    )
    @pytest.mark.parametrize(
        "payments",
        [
            0.0,
            50.0,
            -25.0,
            PresentValue(-25.0),
        ],
    )
    def test(
        self,
        initial: PresentValue,
        final: PresentValue,
        payments: SupportsFloat,
    ) -> None:
        expected = PeriodicRate(
            (float(final) + float(payments)) / float(initial) - 1.0
        )
        assert initial.growth(final, payments=payments) == expected
