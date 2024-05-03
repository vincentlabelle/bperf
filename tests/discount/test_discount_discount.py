import pytest

from bperf.discount import Discount


class TestDiscountInvariants:
    def test_when_negative(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            Discount(-1e-8)

    @pytest.mark.parametrize("value", [0.0, 1e8, 200])
    def test_when_non_negative(self, value: float) -> None:
        Discount(value)  # does not raise
