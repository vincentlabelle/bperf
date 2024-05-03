import pytest

from bperf.pv import PresentValue
from bperf.pv.sequence import PresentValueSequence


class TestPresentValueSequenceSum:
    def test_when_one_element(self) -> None:
        value = PresentValue(50.0)
        sequence = PresentValueSequence([value])
        assert sequence.sum() == value

    def test_when_multiple_elements(self) -> None:
        sequence = PresentValueSequence(
            [
                PresentValue(0.0),
                PresentValue(50.0),
                PresentValue(-150.0),
                PresentValue(-0.25),
            ]
        )
        assert sequence.sum() == PresentValue(-100.25)


class TestPresentValueSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> PresentValueSequence:
        return PresentValueSequence([])

    def test_sum(self, sequence: PresentValueSequence) -> None:
        assert sequence.sum() == PresentValue(0.0)
