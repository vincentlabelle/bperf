from typing import Iterable, Tuple

import pytest

from bperf.term import Term
from bperf.term.sequence import TermSequence
from bperf.termed import Termed
from bperf.termed.sequence import TermedSequence


class _T:
    def __init__(self, value: int):
        self._value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value


class TestTermedSequenceInvariants:
    @pytest.mark.parametrize(
        "values, expected",
        [
            (
                [
                    Termed(Term(1.0), _T(1)),
                ],
                TermedSequence(
                    [
                        Termed(Term(1.0), _T(1)),
                    ]
                ),
            ),
            (
                [
                    Termed(Term(1.0), _T(2)),
                    Termed(Term(2.0), _T(1)),
                ],
                TermedSequence(
                    [
                        Termed(Term(1.0), _T(2)),
                        Termed(Term(2.0), _T(1)),
                    ]
                ),
            ),
        ],
    )
    def test_when_ordered(
        self,
        values: Iterable[Termed[_T]],
        expected: TermedSequence[_T],
    ) -> None:
        sequence = TermedSequence(values)
        assert sequence == expected

    def test_when_unordered(self) -> None:
        values = [
            Termed(Term(2.0), _T(1)),
            Termed(Term(1.0), _T(2)),
        ]
        sequence = TermedSequence(values)
        expected = TermedSequence(sorted(values))
        assert sequence == expected

    def test_when_empty(self) -> None:
        TermedSequence.empty()  # does not raise

    def test_when_contains_repeated_terms(self) -> None:
        with pytest.raises(ValueError, match="unique"):
            TermedSequence(
                [
                    Termed(Term(1.0), _T(2)),
                    Termed(Term(2.0), _T(1)),
                    Termed(Term(1.0), _T(3)),
                ]
            )

    def test_when_contains_repeated_values(self) -> None:
        TermedSequence(
            [
                Termed(Term(1.0), _T(2)),
                Termed(Term(2.0), _T(1)),
                Termed(Term(3.0), _T(2)),
            ]
        )  # does not raise


class TestTermedSequenceAlternativeConstructors:
    @pytest.mark.parametrize(
        "tuples",
        [
            [
                (Term(1.0), _T(1)),
            ],
            [
                (Term(1.0), _T(2)),
                (Term(2.0), _T(1)),
            ],
            [
                (Term(2.0), _T(1)),
                (Term(1.0), _T(2)),
            ],
        ],
    )
    def test_from_tuples(self, tuples: Iterable[Tuple[Term, _T]]) -> None:
        expected = TermedSequence(Termed(*tuple_) for tuple_ in tuples)
        assert TermedSequence.from_tuples(tuples) == expected


class TestTermedSequenceProperties:
    @pytest.fixture(scope="class")
    def terms(self) -> TermSequence:
        return TermSequence(
            [
                Term(1.0),
                Term(2.0),
            ]
        )

    @pytest.fixture(scope="class")
    def values(self) -> Tuple[_T, ...]:
        return _T(2), _T(1)

    @pytest.fixture(scope="class")
    def sequence(
        self,
        terms: TermSequence,
        values: Tuple[_T, ...],
    ) -> TermedSequence[_T]:
        return TermedSequence.from_tuples(zip(terms, values))

    def test_terms(
        self,
        sequence: TermedSequence[_T],
        terms: TermSequence,
    ) -> None:
        assert sequence.terms == terms

    def test_values(
        self,
        sequence: TermedSequence[_T],
        values: Tuple[_T, ...],
    ) -> None:
        assert tuple(sequence.values) == values


class TestTermedSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> TermedSequence[_T]:
        return TermedSequence.empty()

    def test_from_tuples(self, sequence: TermedSequence[_T]) -> None:
        assert TermedSequence.from_tuples([]) == sequence

    def test_terms(self, sequence: TermedSequence[_T]) -> None:
        assert sequence.terms == TermSequence.empty()

    def test_values(self, sequence: TermedSequence[_T]) -> None:
        assert tuple(sequence.values) == ()
