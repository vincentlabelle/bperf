from math import nan

import pytest

from bperf.utilities.float.nonnan import NonNan


class TestNonNanInvariants:
    def test_when_nan(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            NonNan(nan)

    @pytest.mark.parametrize("value", [-1.0, 0.0, 1.0])
    def test_when_nonnan(self, value: float) -> None:
        NonNan(value)  # does not raise

    def test_when_supports_float(self) -> None:
        class _Float:
            def __float__(self) -> float:
                return 1.0

        assert NonNan(_Float()) == NonNan(float(_Float()))


@pytest.fixture(scope="module")
def value() -> float:
    return 0.1


@pytest.fixture(scope="module")
def nonnan(value: float) -> NonNan:
    return NonNan(value)


class TestNonNanEqual:
    def test_when_equal(self, nonnan: NonNan, value: float) -> None:
        other = NonNan(value)
        assert other == nonnan

    def test_when_different_value(self, nonnan: NonNan, value: float) -> None:
        other = NonNan(value + 1.0)
        assert other != nonnan

    def test_when_different_sign(self, nonnan: NonNan, value: float) -> None:
        other = NonNan(-value)
        assert other != nonnan

    def test_when_different_object(self, nonnan: NonNan) -> None:
        assert nonnan != "a"


class TestNonNanHash:
    def test_when_equal(self, nonnan: NonNan, value: float) -> None:
        other = NonNan(value)
        assert hash(other) == hash(nonnan)

    def test_when_different_value(self, nonnan: NonNan, value: float) -> None:
        other = NonNan(value + 1.0)
        assert hash(other) != hash(nonnan)

    def test_when_different_sign(self, nonnan: NonNan, value: float) -> None:
        other = NonNan(-value)
        assert hash(other) != hash(nonnan)


class TestNonNanRepresentation:
    def test(self, nonnan: NonNan) -> None:
        assert repr(nonnan) == f"<{nonnan.__class__.__name__}({nonnan})>"


class TestNonNanCasting:
    def test_str(self, nonnan: NonNan, value: float) -> None:
        assert str(nonnan) == str(value)

    def test_float(self, nonnan: NonNan, value: float) -> None:
        assert float(nonnan) == value
