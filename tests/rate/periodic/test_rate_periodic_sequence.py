from math import prod
from typing import Any, List, Tuple

import pytest

from bperf.rate.periodic import PeriodicRate
from bperf.rate.periodic.sequence import PeriodicRateSequence

_ONE = PeriodicRateSequence(
    [
        PeriodicRate(1.0),
    ]
)
_BY_ONE = [2.0]
_MULTIPLE = PeriodicRateSequence(
    [
        PeriodicRate(1.0),
        PeriodicRate(2.0),
        PeriodicRate(3.0),
    ]
)
_BY_MULTIPLE = [4.0, 5.0, 6.0]


@pytest.fixture(scope="module", params=[_ONE, _MULTIPLE])
def sequence(request: Any) -> PeriodicRateSequence:
    return request.param  # type: ignore[no-any-return]


class TestPeriodicRateSequenceDot:
    @pytest.mark.parametrize(
        "sequence, by",
        [
            (_ONE, _BY_ONE),
            (_MULTIPLE, _BY_MULTIPLE),
        ],
    )
    def test(self, sequence: PeriodicRateSequence, by: List[float]) -> None:
        expected = sequence.scale(by).sum()
        assert sequence.dot(iter(by)) == expected


class TestPeriodicRateSequenceScale:
    @pytest.mark.parametrize(
        "by",
        [
            (1.0, 2.0),
            (1.0, 2.0, 3.0, 4.0),
        ],
    )
    def test_when_length_mismatch(
        self,
        by: Tuple[float, ...],
    ) -> None:
        with pytest.raises(ValueError, match="length"):
            _MULTIPLE.scale(by)

    @pytest.mark.parametrize(
        "sequence, by",
        [
            (_ONE, _BY_ONE),
            (_MULTIPLE, _BY_MULTIPLE),
        ],
    )
    def test(self, sequence: PeriodicRateSequence, by: List[float]) -> None:
        expected = PeriodicRateSequence(
            value.scale(b) for b, value in zip(by, sequence)
        )
        assert sequence.scale(iter(by)) == expected


class TestPeriodicRateSequenceSum:
    def test(self, sequence: PeriodicRateSequence) -> None:
        expected = sum(sequence, start=PeriodicRate(0.0))
        assert sequence.sum() == expected


class TestPeriodicRateSequenceCompound:
    def test(self, sequence: PeriodicRateSequence) -> None:
        expected = prod(
            (value.increment() for value in sequence),
            start=PeriodicRate(1.0),
        ).decrement()  # type: ignore[attr-defined]
        assert sequence.compound() == expected


class TestPeriodicRateSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> PeriodicRateSequence:
        return PeriodicRateSequence.empty()

    def test_dot(self, sequence: PeriodicRateSequence) -> None:
        assert sequence.dot([]) == PeriodicRate(0.0)

    def test_scale(self, sequence: PeriodicRateSequence) -> None:
        assert sequence.scale([]) == sequence

    def test_sum(self, sequence: PeriodicRateSequence) -> None:
        assert sequence.sum() == PeriodicRate(0.0)

    def test_compound(self, sequence: PeriodicRateSequence) -> None:
        assert sequence.compound() == PeriodicRate(0.0)
