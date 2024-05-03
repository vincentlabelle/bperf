from typing import Dict, Tuple

from .performance import IPerformanceCalculator
from .priced.points.weighted.table import WeightedPricedPointsTable


class IDataPointsFetcher:
    """Interface for fetchers of necessary data points to the computation
    of performance.
    """

    def fetch(
        self,
        identifier: str,
        range_: Tuple[str, str],
    ) -> WeightedPricedPointsTable:
        """Fetch the data points necessary for computing the performance
        of `identifier` over the period of time delimited by `range_`.

        Parameters
        ----------
        identifier
            identifier of the entity for which to fetch data points
        range_
            dates delimiting the period over which to fetch;
            each date must be a business day;
            the first date represents the start of the period and
            the second date represents the end of the period

        Raises
        ------
        ValueError
            if `identifier` does not exist,
            if any date in `range_` is an invalid business day, or
            if the second date in `range_` is not strictly greater than the
            first date in `range_`
        RuntimeError
            if an unexpected error occurs while fetching

        Returns
        -------
        WeightedPricedPointsTable
            fetched data points
        """
        raise NotImplementedError


class PerformanceReportGenerator:
    """Generator of performance report (incl. attribution by effects).

    Parameters
    ----------
    fetcher: IDataPointsFetcher
        fetcher of the necessary data points to compute the performance
    calculator: IPerformanceCalculator
        calculator of performance
    """

    def __init__(
        self,
        fetcher: IDataPointsFetcher,
        calculator: IPerformanceCalculator,
    ):
        self._fetcher = fetcher
        self._calculator = calculator

    def generate(
        self,
        identifier: str,
        range_: Tuple[str, str],
    ) -> Dict[str, str]:
        """Generate a performance report for `identifier` over the period
        of time delimited by `range_`.

        Parameters
        ----------
        identifier
            identifier of the entity for which to generate a performance report
        range_
            dates delimiting the period over which to compute the performance;
            each date must be a business day;
            the first date represents the start of the period and
            the second date represents the end of the period

        Raises
        ------
        ValueError
            if `identifier` does not exist,
            if any date in `range_` is an invalid business day, or
            if the second date in `range_` is not strictly greater than the
            first date in `range_`
        OverflowError
            if an overflow occurs while determining the performance
        RuntimeError
            if an unexpected error occurs while generating the performance
            report

        Returns
        -------
        Dict[str, str]
            performance report
        """
        table = self._fetcher.fetch(identifier, range_)
        performance = self._calculator.calculate(table)
        return {name: str(percent) for name, percent in performance.items()}
