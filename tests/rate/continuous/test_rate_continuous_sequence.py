from typing import Sequence as typeSequence

import pytest

from bperf.rate.continuous import ContinuousRate
from bperf.rate.continuous.sequence import ContinuousRateSequence


class TestContinuousRateSequenceAlternativeConstructors:
    @pytest.mark.parametrize(
        "values",
        [
            (1.0,),
            (0.01, -0.02, 0.0),
        ],
    )
    def test_from_float(self, values: typeSequence[float]) -> None:
        expected = ContinuousRateSequence(
            [ContinuousRate(value) for value in values]
        )
        assert ContinuousRateSequence.from_float(iter(values)) == expected


class TestContinuousRateSequenceAdd:
    @pytest.mark.parametrize(
        "sequence",
        [
            ContinuousRateSequence.from_float([0.01]),
            ContinuousRateSequence.from_float([0.01, -0.02, 0.0]),
        ],
    )
    @pytest.mark.parametrize(
        "rate",
        [
            ContinuousRate(0.02),
            ContinuousRate(-0.03),
            ContinuousRate(0.0),
        ],
    )
    def test(
        self,
        sequence: ContinuousRateSequence,
        rate: ContinuousRate,
    ) -> None:
        expected = ContinuousRateSequence([value + rate for value in sequence])
        assert sequence.add(rate) == expected

    def test_new_sequence(self) -> None:
        sequence = ContinuousRateSequence([ContinuousRate(0.01)])
        new = sequence.add(ContinuousRate(0.0))
        assert new is not sequence


class TestContinuousRateSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> ContinuousRateSequence:
        return ContinuousRateSequence.empty()

    def test_from_float(self, sequence: ContinuousRateSequence) -> None:
        assert ContinuousRateSequence.from_float([]) == sequence

    def test_add(self, sequence: ContinuousRateSequence) -> None:
        assert sequence.add(ContinuousRate(0.01)) == sequence
