import pytest

from bperf.term import Term


class TestTermInvariants:
    def test_when_negative(self) -> None:
        with pytest.raises(ValueError, match="strictly positive"):
            Term(-1e-8)

    def test_when_zero(self) -> None:
        with pytest.raises(ValueError, match="strictly positive"):
            Term(0.0)

    def test_when_positive(self) -> None:
        Term(1e-8)  # does not raise


class TestTermComparison:
    @pytest.fixture(scope="class")
    def small(self) -> Term:
        return Term(0.1)

    @pytest.fixture(scope="class")
    def big(self) -> Term:
        return Term(2.0)

    def test_lt(self, small: Term, big: Term) -> None:
        assert small < big
        assert not small < small  # skipcq: PYL-R0124
        assert not big < small

    def test_lt_when_different_object(self, small: Term) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small < 2.0

    def test_le(self, small: Term, big: Term) -> None:
        assert small <= big
        assert small <= small  # skipcq: PYL-R0124
        assert not big <= small

    def test_le_when_different_object(self, small: Term) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small <= 2.0

    def test_gt(self, small: Term, big: Term) -> None:
        assert not small > big
        assert not small > small  # skipcq: PYL-R0124
        assert big > small

    def test_gt_when_different_object(self, small: Term) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small > 2.0

    def test_ge(self, small: Term, big: Term) -> None:
        assert not small >= big
        assert small >= small  # skipcq: PYL-R0124
        assert big >= small

    def test_ge_when_different_object(self, small: Term) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small >= 2.0
