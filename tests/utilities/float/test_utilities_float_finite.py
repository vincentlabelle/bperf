from math import inf

import pytest

from bperf.utilities.float.finite import Finite


class TestFiniteInvariants:
    @pytest.mark.parametrize("value", [inf, -inf])
    def test_when_non_finite(self, value: float) -> None:
        with pytest.raises(ValueError, match="finite"):
            Finite(value)

    @pytest.mark.parametrize("value", [-1.0, 0.0, 1.0])
    def test_when_finite(self, value: float) -> None:
        Finite(value)  # does not raise

    def test_when_supports_float(self) -> None:
        class _Float:
            def __float__(self) -> float:
                return 1.0

        assert Finite(_Float()) == Finite(float(_Float()))


class TestFiniteArithmetic:
    @pytest.fixture(scope="class")
    def value(self) -> float:
        return 0.01

    @pytest.fixture(scope="class")
    def finite(self, value: float) -> Finite:
        return Finite(0.01)

    def test_neg(self, finite: Finite, value: float) -> None:
        assert -finite == Finite(-value)

    @pytest.mark.parametrize(
        "other",
        [
            Finite(0.02),
            Finite(0.0),
            Finite(-0.02),
        ],
    )
    def test_add(self, finite: Finite, other: Finite) -> None:
        expected = Finite(float(finite) + float(other))
        assert finite + other == expected

    def test_add_when_different_object(self, finite: Finite) -> None:
        with pytest.raises(TypeError):
            finite + 0.01

    @pytest.mark.parametrize("finite", [Finite(1e308), Finite(-1e308)])
    def test_add_when_raises(self, finite: Finite) -> None:
        with pytest.raises(OverflowError, match="overflow"):
            finite + finite

    @pytest.mark.parametrize(
        "other",
        [
            Finite(0.02),
            Finite(0.0),
            Finite(-0.02),
        ],
    )
    def test_sub(self, finite: Finite, other: Finite) -> None:
        expected = Finite(float(finite) - float(other))
        assert finite - other == expected

    def test_sub_when_different_object(self, finite: Finite) -> None:
        with pytest.raises(TypeError):
            finite - 0.01

    @pytest.mark.parametrize("finite", [Finite(1e308), Finite(-1e308)])
    def test_sub_when_raises(self, finite: Finite) -> None:
        with pytest.raises(OverflowError, match="overflow"):
            finite - -finite

    @pytest.mark.parametrize(
        "other",
        [
            Finite(0.02),
            Finite(0.0),
            Finite(-0.02),
        ],
    )
    def test_mul(self, finite: Finite, other: Finite) -> None:
        expected = Finite(float(finite) * float(other))
        assert finite * other == expected

    def test_mul_when_different_object(self, finite: Finite) -> None:
        with pytest.raises(TypeError):
            finite * 0.01

    @pytest.mark.parametrize("finite", [Finite(1e308), Finite(-1e308)])
    def test_mul_when_raises(self, finite: Finite) -> None:
        with pytest.raises(OverflowError, match="overflow"):
            finite * finite
