import pytest

from bperf.discount import Discount
from bperf.money import Money
from bperf.pv import PresentValue
from bperf.utilities.float.precise import Precise


@pytest.fixture(scope="module")
def value() -> int:
    return 1


@pytest.fixture(scope="module")
def money(value: int) -> Money:
    return Money(value)


class TestMoneyInvariants:
    def test_precision(self, money: Money, value: int) -> None:
        assert money == Precise(value, Money._PRECISION)


class TestMoneyArithmetic:
    @pytest.mark.parametrize(
        "other, expected",
        [
            (Money(2), Money(3)),
            (Money(-2), Money(-1)),
            (Money(0), Money(1)),
        ],
    )
    def test_add(self, money: Money, other: Money, expected: Money) -> None:
        assert money + other == expected

    def test_add_when_different_object(self, money: Money) -> None:
        with pytest.raises(TypeError):
            money + 2

    @pytest.mark.parametrize(
        "other, expected",
        [
            (Money(2), Money(-1)),
            (Money(-2), Money(3)),
            (Money(0), Money(1)),
        ],
    )
    def test_sub(self, money: Money, other: Money, expected: Money) -> None:
        assert money - other == expected

    def test_sub_when_different_object(self, money: Money) -> None:
        with pytest.raises(TypeError):
            money - 2


class TestMoneyPv:
    @pytest.mark.parametrize(
        "money",
        [
            Money(1),
            Money(-100),
            Money(0),
        ],
    )
    @pytest.mark.parametrize(
        "discount",
        [
            Discount(0.0),
            Discount(0.99),
            Discount(100.0),
        ],
    )
    def test(self, money: Money, discount: Discount) -> None:
        result = money.pv(discount)
        expected = PresentValue(float(money) * float(discount))
        assert result == expected

    @pytest.mark.parametrize(
        "money",
        [
            Money(int(1e308)),
            Money(-int(1e308)),
        ],
    )
    def test_when_overflow(self, money: Money) -> None:
        discount = Discount(1e308)
        with pytest.raises(OverflowError, match="overflow"):
            money.pv(discount)
