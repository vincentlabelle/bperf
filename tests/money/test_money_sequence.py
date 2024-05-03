import pytest

from bperf.discount import Discount
from bperf.discount.sequence import DiscountSequence
from bperf.money import Money
from bperf.money.sequence import MoneySequence
from bperf.pv import PresentValue
from bperf.pv.sequence import PresentValueSequence


class TestMoneySequenceSum:
    def test_when_one_element(self) -> None:
        value = Money(1)
        sequence = MoneySequence([value])
        assert sequence.sum() == value

    def test_when_multiple_elements(self) -> None:
        sequence = MoneySequence(
            [
                Money(2),
                Money(-4),
                Money(0),
                Money(150),
            ]
        )
        assert sequence.sum() == Money(148)


class TestMoneySequencePv:
    @pytest.mark.parametrize(
        "discounts",
        [
            DiscountSequence(
                [
                    Discount(0.99),
                ]
            ),
            DiscountSequence(
                [
                    Discount(0.99),
                    Discount(0.98),
                    Discount(0.50),
                ]
            ),
        ],
    )
    def test_when_length_mismatch(self, discounts: DiscountSequence) -> None:
        sequence = MoneySequence(
            [
                Money(2),
                Money(-4),
            ]
        )
        with pytest.raises(ValueError, match="length mismatch"):
            sequence.pv(discounts)

    def test_when_one_element(self) -> None:
        money, discount = Money(2), Discount(0.99)
        sequence = MoneySequence([money])
        discounts = DiscountSequence([discount])
        assert sequence.pv(discounts) == money.pv(discount)

    def test_when_multiple_elements(self) -> None:
        sequence = MoneySequence(
            [
                Money(2),
                Money(-4),
                Money(0),
            ]
        )
        discounts = DiscountSequence(
            [
                Discount(0.99),
                Discount(0.5),
                Discount(0.01),
            ]
        )
        expected = PresentValueSequence(
            money.pv(discount) for money, discount in zip(sequence, discounts)
        ).sum()
        assert sequence.pv(discounts) == expected


class TestMoneySequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> MoneySequence:
        return MoneySequence.empty()

    def test_sum(self, sequence: MoneySequence) -> None:
        assert sequence.sum() == Money(0)

    def test_pv(self, sequence: MoneySequence) -> None:
        discounts = DiscountSequence.empty()
        assert sequence.pv(discounts) == PresentValue(0.0)
