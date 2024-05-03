# Bperf: Vanilla Fixed Income Performance Calculations for Python

Bperf helps you generate a performance and attribution report on a
vanilla fixed income portfolio or a liability. It supports Python 3.10.

## Installation

Bperf is not yet available on PyPI, and must be installed from source.

## Quick Start

To generate a performance and attribution report, the user must use the provided
`PerformanceReportGenerator` in `bperf.report`. The user is responsible for
implementing `IDataPointsFetcher` which is necessary for the report generation.
