import pytest

from bperf.percent import Percent
from bperf.percent.sequence import PercentSequence


class TestPercentSequenceSum:
    def test_when_one_element(self) -> None:
        value = Percent(1)
        sequence = PercentSequence([value])
        assert sequence.sum() == value

    def test_when_multiple_elements(self) -> None:
        sequence = PercentSequence(
            [
                Percent(2),
                Percent(-4),
                Percent(0),
                Percent(150),
            ]
        )
        assert sequence.sum() == Percent(148)


class TestPercentSequenceSumsTo:
    @pytest.mark.parametrize(
        "sequence",
        [
            PercentSequence([Percent(1)]),
            PercentSequence([Percent(1), Percent(-2)]),
        ],
    )
    def test_when_sums_to(self, sequence: PercentSequence) -> None:
        assert sequence.sums_to(sequence.sum())

    @pytest.mark.parametrize("value", [Percent(0), Percent(-2)])
    @pytest.mark.parametrize(
        "sequence",
        [
            PercentSequence([Percent(-1)]),
            PercentSequence([Percent(1), Percent(-2)]),
        ],
    )
    def test_when_does_not_sums_to(
        self,
        sequence: PercentSequence,
        value: Percent,
    ) -> None:
        assert not sequence.sums_to(value)


class TestPercentSequenceDifferenceWith:
    @pytest.mark.parametrize("value", [Percent(1), Percent(0), Percent(-1)])
    @pytest.mark.parametrize(
        "sequence",
        [
            PercentSequence([Percent(1)]),
            PercentSequence([Percent(1), Percent(-2)]),
        ],
    )
    def test(self, value: Percent, sequence: PercentSequence) -> None:
        expected = value - sequence.sum()
        assert sequence.difference_with(value) == expected


class TestPercentSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> PercentSequence:
        return PercentSequence.empty()

    def test_sum(self, sequence: PercentSequence) -> None:
        assert sequence.sum() == Percent(0)

    def test_sums_to_when_does(self, sequence: PercentSequence) -> None:
        assert sequence.sums_to(sequence.sum())

    @pytest.mark.parametrize("value", [Percent(1), Percent(-1)])
    def test_sums_to_when_does_not(
        self,
        sequence: PercentSequence,
        value: Percent,
    ) -> None:
        assert not sequence.sums_to(value)

    def test_difference_with(self, sequence: PercentSequence) -> None:
        value = Percent(1)
        assert sequence.difference_with(value) == value
