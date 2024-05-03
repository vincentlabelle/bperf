import pytest

from bperf.term import Term
from bperf.term.sequence import TermSequence


class TestTermSequenceContainsRepeatedValues:
    @pytest.mark.parametrize(
        "sequence",
        [
            TermSequence(
                [
                    Term(1.0),
                ]
            ),
            TermSequence(
                [
                    Term(1.0),
                    Term(0.5),
                ]
            ),
        ],
    )
    def test_when_no_repeats(self, sequence: TermSequence) -> None:
        assert not sequence.contains_repeated_values()

    def test_when_repeats(self) -> None:
        sequence = TermSequence(
            [
                Term(1.0),
                Term(2.0),
                Term(1.0),
            ]
        )
        assert sequence.contains_repeated_values()


class TestTermSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> TermSequence:
        return TermSequence.empty()

    def test_contains_repeated_values(self, sequence: TermSequence) -> None:
        assert not sequence.contains_repeated_values()
