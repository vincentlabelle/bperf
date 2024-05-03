import pytest

from bperf.percent import Percent
from bperf.utilities.float.precise import Precise


@pytest.fixture(scope="module")
def value() -> int:
    return 2534


@pytest.fixture(scope="module")
def percent(value: int) -> Percent:
    return Percent(value)


class TestPercentInvariants:
    def test_precision(self, percent: Percent, value: int) -> None:
        assert percent == Precise(value, Percent._PRECISION)


class TestPercentAlternativeConstructors:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (-0.1, Percent(-1000)),
            (0.0, Percent(0)),
            (0.123, Percent(1230)),
            (0.1232, Percent(1232)),
            (0.12325, Percent(1232)),
            (0.12315, Percent(1232)),
        ],
    )
    def test_from_float(self, value: float, expected: Percent) -> None:
        assert Percent.from_float(value) == expected


class TestPercentArithmetic:
    @pytest.mark.parametrize(
        "other, expected",
        [
            (Percent(2), Percent(2536)),
            (Percent(-2), Percent(2532)),
            (Percent(0), Percent(2534)),
        ],
    )
    def test_add(
        self,
        percent: Percent,
        other: Percent,
        expected: Percent,
    ) -> None:
        assert percent + other == expected

    def test_add_when_different_object(self, percent: Percent) -> None:
        with pytest.raises(TypeError):
            percent + 2

    @pytest.mark.parametrize(
        "other, expected",
        [
            (Percent(2), Percent(2532)),
            (Percent(-2), Percent(2536)),
            (Percent(0), Percent(2534)),
        ],
    )
    def test_sub(
        self,
        percent: Percent,
        other: Percent,
        expected: Percent,
    ) -> None:
        assert percent - other == expected

    def test_sub_when_different_object(self, percent: Percent) -> None:
        with pytest.raises(TypeError):
            percent - 2
