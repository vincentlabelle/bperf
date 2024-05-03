from decimal import ROUND_HALF_EVEN, Decimal, DecimalException
from math import isfinite
from typing import SupportsFloat, SupportsInt


class Precise:
    """Finite floating-point number with exact precision.

    Parameters
    ----------
    value: SupportsInt
        value of the precise to create as an integer
    precision: SupportsInt
        precision of the precise to create (i.e., number of decimal places)

    Examples
    --------
    `Precise(3, 2)` <=> 0.03

    Raises
    ------
    ValueError
        if `precision` is lower than one
    """

    @classmethod
    def float_to_int(
        cls,
        value: SupportsFloat,
        precision: SupportsInt,
    ) -> SupportsInt:
        """Convert a floating-point number, up to `precision` decimal places,
        to its integer equivalent. If `value` has more digits than `precision`,
        it's rounded using a half-even approach.

        Parameters
        ----------
        value
            floating-point number to convert
        precision
            number of decimal places to keep

        Examples
        --------
        `Precise.float_to_int(0.010, 4)` <=> 10

        Raises
        ------
        ValueError
            if `value` is not finite, or
            if `precision` is lower than one
        RuntimeError
            if an unexpected error occurs while rounding `value`

        Returns
        -------
        SupportsInt
            integer equivalent of the floating-point number
        """
        value_, precision_ = float(value), int(precision)
        cls._raise_if_is_not_finite(value_)
        cls._raise_if_is_lower_than_one(precision_)
        return cls._round(cls._shift(value_, precision_))

    @classmethod
    def _raise_if_is_not_finite(cls, value: float) -> None:
        if not isfinite(value):
            message = f"cannot instantiate {cls.__name__}; value must be finite"
            raise ValueError(message)

    @classmethod
    def _raise_if_is_lower_than_one(cls, precision: int) -> None:
        if precision < 1:
            message = (
                f"cannot instantiate {cls.__name__}; "
                f"precision must be greater than or equal to 1"
            )
            raise ValueError(message)

    @classmethod
    def _shift(cls, value: float, by: int) -> Decimal:
        sign, digits, exponent = Decimal(str(value)).as_tuple()
        return Decimal(
            (
                sign,
                digits,
                exponent + by,
            )
        )

    @classmethod
    def _round(cls, value: Decimal) -> Decimal:
        try:
            return value.quantize(
                Decimal("1"),
                rounding=ROUND_HALF_EVEN,
            )
        except DecimalException as err:
            message = (
                f"cannot instantiate {cls.__name__}; "
                f"an unexpected error occurred while rounding"
            )
            raise RuntimeError(message) from err

    def __init__(self, value: SupportsInt, precision: SupportsInt):
        self._value = int(value)
        self._precision = int(precision)
        self._raise_if_is_lower_than_one(self._precision)

    def __float__(self) -> float:
        return float(self._decimal)

    def __str__(self) -> str:
        return str(self._decimal)

    @property
    def _decimal(self) -> Decimal:
        return Decimal(
            (
                0 if self._value >= 0 else 1,
                tuple(int(c) for c in str(abs(self._value))),
                -self._precision,
            )
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._value == other._value and self._precision == other._precision
        )

    def __hash__(self) -> int:
        return hash((self._value, self._precision))
