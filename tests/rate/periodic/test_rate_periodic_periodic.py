from math import inf, nan
from typing import Any

import pytest

from bperf.rate.periodic import PeriodicRate


class TestPeriodicRateIncrement:
    @pytest.mark.parametrize(
        "rate",
        [
            PeriodicRate(0.0),
            PeriodicRate(1.0),
            PeriodicRate(-2.0),
        ],
    )
    def test(self, rate: PeriodicRate) -> None:
        expected = rate + PeriodicRate(1.0)
        assert rate.increment() == expected

    def test_is_new(self) -> None:
        rate = PeriodicRate(1.0)
        new = rate.increment()
        assert new is not rate


class TestPeriodicRateDecrement:
    @pytest.mark.parametrize(
        "rate",
        [
            PeriodicRate(0.0),
            PeriodicRate(1.0),
            PeriodicRate(-2.0),
        ],
    )
    def test(self, rate: PeriodicRate) -> None:
        expected = rate - PeriodicRate(1.0)
        assert rate.decrement() == expected

    def test_is_new(self) -> None:
        rate = PeriodicRate(1.0)
        new = rate.decrement()
        assert new is not rate


class TestPeriodicRateScale:
    @pytest.fixture(
        scope="class",
        params=[
            PeriodicRate(0.01),
            PeriodicRate(-0.01),
            PeriodicRate(0.0),
        ],
    )
    def rate(self, request: Any) -> PeriodicRate:
        return request.param  # type: ignore[no-any-return]

    @pytest.mark.parametrize("by", [nan, inf, -inf])
    def test_when_by_is_not_finite(self, rate: PeriodicRate, by: float) -> None:
        with pytest.raises(ValueError, match="finite"):
            rate.scale(by)

    @pytest.mark.parametrize("by", [-2.0, 0.0, 3.0])
    def test_when_by_is_finite(self, rate: PeriodicRate, by: float) -> None:
        assert rate.scale(by) == PeriodicRate(by * float(rate))

    @pytest.mark.parametrize("by", [-1e308, 1e308])
    def test_when_overflow(self, by: float) -> None:
        rate = PeriodicRate(1e308)
        with pytest.raises(OverflowError, match="overflow"):
            rate.scale(by)

    def test_when_supports_float(self) -> None:
        class _Float:
            def __float__(self) -> float:
                return 2.0

        rate = PeriodicRate(1.0)
        assert rate.scale(_Float()) == rate.scale(float(_Float()))
