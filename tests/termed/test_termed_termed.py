import pytest

from bperf.term import Term
from bperf.termed import Termed


class _T:
    def __init__(self, value: int):
        self._value = value

    def __int__(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)


@pytest.fixture(scope="module")
def term() -> Term:
    return Term(1.0)


@pytest.fixture(scope="module")
def value() -> _T:
    return _T(3)


@pytest.fixture(scope="module")
def termed(term: Term, value: _T) -> Termed[_T]:
    return Termed(term, value)


class TestTermedEqual:
    def test_when_equal(
        self,
        termed: Termed[_T],
        term: Term,
        value: _T,
    ) -> None:
        other = Termed(term, value)
        assert other == termed

    def test_when_different_term(
        self,
        termed: Termed[_T],
        term: Term,
        value: _T,
    ) -> None:
        term = Term(float(term) + 0.2)
        other = Termed(term, value)
        assert other != termed

    def test_when_different_value(
        self,
        termed: Termed[_T],
        term: Term,
        value: _T,
    ) -> None:
        value = _T(int(value) + 2)
        other = Termed(term, value)
        assert other != termed

    def test_when_different_object(self, termed: Termed[_T]) -> None:
        assert termed != "a"


class TestTermedHash:
    def test_when_equal(
        self,
        termed: Termed[_T],
        term: Term,
        value: _T,
    ) -> None:
        other = Termed(term, value)
        assert hash(other) == hash(termed)

    def test_when_different_term(
        self,
        termed: Termed[_T],
        term: Term,
        value: _T,
    ) -> None:
        term = Term(float(term) + 0.2)
        other = Termed(term, value)
        assert hash(other) != hash(termed)

    def test_when_different_value(
        self,
        termed: Termed[_T],
        term: Term,
        value: _T,
    ) -> None:
        value = _T(int(value) + 2)
        other = Termed(term, value)
        assert hash(other) != hash(termed)


class TestTermedRepresentation:
    def test(self, termed: Termed[_T]) -> None:
        assert repr(termed) == f"<{termed.__class__.__name__}{termed}>"


class TestTermedCasting:
    def test_str(self, termed: Termed[_T], term: Term, value: _T) -> None:
        assert str(termed) == f"(term={term}, value={value})"


class TestTermedComparison:
    @pytest.fixture(scope="class")
    def small(self) -> Termed[_T]:
        return Termed(Term(0.1), _T(100))

    @pytest.fixture(scope="class")
    def big(self) -> Termed[_T]:
        return Termed(Term(100), _T(1))

    def test_lt(self, small: Termed[_T], big: Termed[_T]) -> None:
        assert small < big
        assert not small < small  # skipcq: PYL-R0124
        assert not big < small

    def test_lt_when_different_object(self, small: Termed[_T]) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small < 2.0

    def test_le(self, small: Termed[_T], big: Termed[_T]) -> None:
        assert small <= big
        assert small <= small  # skipcq: PYL-R0124
        assert not big <= small

    def test_le_when_different_object(self, small: Termed[_T]) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small <= 2.0

    def test_gt(self, small: Termed[_T], big: Termed[_T]) -> None:
        assert not small > big
        assert not small > small  # skipcq: PYL-R0124
        assert big > small

    def test_gt_when_different_object(self, small: Termed[_T]) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small > 2.0

    def test_ge(self, small: Termed[_T], big: Termed[_T]) -> None:
        assert not small >= big
        assert small <= small  # skipcq: PYL-R0124
        assert big >= small

    def test_ge_when_different_object(self, small: Termed[_T]) -> None:
        with pytest.raises(TypeError):
            # noinspection PyStatementEffect
            small >= 2.0


class TestTermedProperties:
    def test_term(self, termed: Termed[_T], term: Term) -> None:
        assert termed.term == term

    def test_value(self, termed: Termed[_T], value: _T) -> None:
        assert termed.value == value
