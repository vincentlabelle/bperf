from unittest.mock import MagicMock, patch

import pytest

from bperf.percent import Percent
from bperf.performance import IPerformanceCalculator
from bperf.priced.points.weighted.table import WeightedPricedPointsTable
from bperf.report import IDataPointsFetcher, PerformanceReportGenerator


class TestIDataPointsFetcher:
    def test(self) -> None:
        fetcher = IDataPointsFetcher()
        with pytest.raises(NotImplementedError):
            fetcher.fetch("", ("", ""))


class TestPerformanceReportGenerator:
    _TABLE = WeightedPricedPointsTable([])
    _PERFORMANCE = {"one": Percent(1)}

    @patch.object(
        IPerformanceCalculator,
        "calculate",
        return_value=_PERFORMANCE,
    )
    @patch.object(
        IDataPointsFetcher,
        "fetch",
        return_value=_TABLE,
    )
    def test(self, fetcher: MagicMock, calculator: MagicMock) -> None:
        generator = PerformanceReportGenerator(
            IDataPointsFetcher(),
            IPerformanceCalculator(),
        )
        identifier = "batman"
        range_ = ("2022-05-25", "2022-05-26")
        expected = {
            name: str(percent) for name, percent in self._PERFORMANCE.items()
        }
        assert generator.generate(identifier, range_) == expected
        fetcher.assert_called_once_with(identifier, range_)
        calculator.assert_called_once_with(self._TABLE)
