from decimal import localcontext
from math import inf, nan
from typing import SupportsFloat, SupportsInt

import pytest

from bperf.utilities.float.precise import Precise


class TestPreciseInvariants:
    @pytest.mark.parametrize("value", [-100, 0, 100])
    def test_any_value_is_allowed(self, value: int) -> None:
        Precise(value, 1)  # does not raise

    @pytest.mark.parametrize(
        "precision",
        [
            1,
            28,
        ],
    )
    def test_when_precision_is_valid(self, precision: int) -> None:
        Precise(0, precision)  # does not raise

    @pytest.mark.parametrize(
        "precision",
        [
            -1,
            0,
        ],
    )
    def test_when_precision_is_invalid(self, precision: int) -> None:
        with pytest.raises(ValueError, match="precision"):
            Precise(0, precision)

    def test_supports_int(self) -> None:
        class _Int:
            def __int__(self) -> int:
                return 1

        assert Precise(_Int(), _Int()) == Precise(int(_Int()), int(_Int()))


@pytest.fixture(scope="module")
def value() -> int:
    return 1


@pytest.fixture(scope="module")
def precision() -> int:
    return 2


@pytest.fixture(scope="module")
def precise(value: int, precision: int) -> Precise:
    return Precise(value, precision)


class TestPreciseEqual:
    def test_when_equal(
        self,
        precise: Precise,
        value: int,
        precision: int,
    ) -> None:
        other = Precise(value, precision)
        assert other == precise

    def test_when_different_value(
        self,
        precise: Precise,
        value: int,
        precision: int,
    ) -> None:
        other = Precise(value + 1, precision)
        assert other != precise

    def test_when_different_precision(
        self,
        precise: Precise,
        value: int,
        precision: int,
    ) -> None:
        other = Precise(value, precision + 1)
        assert other != precise

    def test_when_different_object(self, precise: Precise) -> None:
        assert precise != "a"


class TestPreciseHash:
    def test_when_equal(
        self,
        precise: Precise,
        value: int,
        precision: int,
    ) -> None:
        other = Precise(value, precision)
        assert hash(other) == hash(precise)

    def test_when_different_value(
        self,
        precise: Precise,
        value: int,
        precision: int,
    ) -> None:
        other = Precise(value + 1, precision)
        assert hash(other) != hash(precise)

    def test_when_different_precision(
        self,
        precise: Precise,
        value: int,
        precision: int,
    ) -> None:
        other = Precise(value, precision + 1)
        assert hash(other) != hash(precise)


class TestPreciseRepresentation:
    def test(self, precise: Precise) -> None:
        assert repr(precise) == f"<{precise.__class__.__name__}({precise})>"


class TestPreciseCasting:
    @pytest.mark.parametrize(
        "precise, expected",
        [
            (Precise(-1, 2), "-0.01"),
            (Precise(0, 2), "0.00"),
            (Precise(1, 2), "0.01"),
            (Precise(15, 2), "0.15"),
            (Precise(152, 2), "1.52"),
            (Precise(1523, 2), "15.23"),
        ],
    )
    def test_str(self, precise: Precise, expected: str) -> None:
        assert str(precise) == expected

    @pytest.mark.parametrize(
        "precise, expected",
        [
            (Precise(-1, 2), -0.01),
            (Precise(0, 2), 0.00),
            (Precise(1, 2), 0.01),
            (Precise(15, 2), 0.15),
            (Precise(152, 2), 1.52),
            (Precise(1523, 2), 15.23),
            (Precise(1, 30), 1e-30),
        ],
    )
    def test_float(self, precise: Precise, expected: float) -> None:
        assert float(precise) == expected


class TestPreciseAlternativeConstructors:
    class _Int:
        def __int__(self) -> int:
            return 2

    class _Float:
        def __float__(self) -> float:
            return 3.12

    @pytest.mark.parametrize(
        "value, precision, expected",
        [
            (-1.0, 1, -10),
            (0.0, 1, 0),
            (0.1, 2, 10),
            (0.12, 2, 12),
            (0.125, 2, 12),
            (0.115, 2, 12),
            (_Float(), _Int(), 312),
            (1e-30, 30, 1),
        ],
    )
    def test_float_to_int(
        self,
        value: SupportsFloat,
        precision: SupportsInt,
        expected: int,
    ) -> None:
        assert int(Precise.float_to_int(value, precision)) == expected

    @pytest.mark.parametrize("value", [nan, inf, -inf])
    def test_float_to_int_when_non_finite_value(
        self,
        value: SupportsFloat,
    ) -> None:
        with pytest.raises(ValueError, match="finite"):
            Precise.float_to_int(value, 1)

    @pytest.mark.parametrize("precision", [-1, 0])
    def test_float_to_int_when_precision_lower_than_one(
        self,
        precision: SupportsInt,
    ) -> None:
        with pytest.raises(ValueError, match="precision"):
            Precise.float_to_int(0.0, precision)

    def test_float_to_int_when_runtime_error(self) -> None:
        with localcontext() as ctx:
            ctx.prec = 28
            with pytest.raises(RuntimeError, match="rounding"):
                Precise.float_to_int(1e29, 29)
