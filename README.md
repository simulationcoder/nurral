# Nurral

Nurral is a Python package designed for researchers to extract financial data from various sources.

The package is evolving and currently, the primary focus is on integration with Google Sheets and support for FX rate providers like the Bank of Canada (BoC). This package allows users to filter data by date range, currency pairs, and specific row counts, making it ideal for finance and economic applications that require timely and accurate FX rate data.

With the core `Currency` class, users can seamlessly extract, filter, and process FX data for advanced analysis and integration into broader data pipelines. Nurral also includes robust error handling, logging capabilities, and flexibility to expand to additional data sources and providers in the future.

Key features of the Nurral package include:

- **Google Sheets Integration**: Easily pull FX rate data directly from Google Sheets.
- **Customizable Data Retrieval**: Filter data by date range, currency pairs, and row limits.
- **Flexible FX Rate Providers**: Currently supports BoC (Bank of Canada) as a data provider with plans for expansion.
- **Intuitive Error Handling and Logging**: Offers detailed error messages and logs to facilitate debugging and data tracking.

Whether you're an analyst, developer, or data scientist, Nurral streamlines the process of working with FX rate data, saving time and reducing manual data handling.

---


## Table of Contents

- [Installation](#installation)
- [Class Overview](#class-overview)
- [Method: getFxRate](#method-getfxrate)
- [Usage Examples](#usage-examples)

## Installation

To get started, clone this repository and install any dependencies. The primary dependencies are `pandas` and `logging`, which are likely already installed if you’re working with data analytics in Python.

# Currency Class

### Class Overview

The `Currency` class is designed for retrieving foreign exchange (FX) rates. It supports filtering data by date, specific currency pairs, and row limits, making it ideal for data analytics, finance, and economic applications.

The `Currency` class provides a getFxRate method for querying and filtering FX rate data. It supports filtering by database, provider, type, date range, row count, and currency pairs.

### Attributes
- Database: Source of FX rate data (e.g., googleSheets).
- Provider: FX rate provider (e.g., BoC for Bank of Canada).
- Type: Type of FX rate (e.g., spot).
- CurrencyPairs: List of currency pairs for filtering (e.g., ['USD/CAD']).
- Date Range: Optional date range (startDate and endDate).
- Row Extraction: Optional rows from the start (headRows) or end (tailRows).

### Method: getFxRate
The getFxRate method retrieves FX rates from specified sources with various filters.

### Parameters
- database (str): FX rate data source. Supported values: 'googleSheets'.
- provider (str): FX rate provider. Supported values: 'BoC'.
- typeof (str): FX rate type. Supported values: 'spot'.
- currencyPairs (list or str): Currency pairs to filter by. Default is 'All'.
- startDate (str): Start date for data filtering (format YYYY-MM-DD).
- endDate (str): End date for data filtering (format YYYY-MM-DD).
- allDates (str): Return all data if set to 'Yes'.
- headRows (int): Number of rows to extract from the top.
- tailRows (int): Number of rows to extract from the bottom.

### Returns
- sub_extract (DataFrame): Extracted FX rate data.
- value (int): Status code:
    - 0: Error.
    - 1: Success.
    - 2: Currency pairs not found.
    - 3: Insufficient filtering conditions.
- exitPhrase (str): Descriptive message explaining the status.

### Usage Examples
Below are examples demonstrating how to use the getFxRate method.

### Example 1: Retrieve Specific Date Range and Currency Pair
```
from currency import Currency

currency_data, status, message = Currency.getFxRate(
    database='googleSheets',
    provider='BoC',
    typeof='spot',
    currencyPairs=['USD/CAD'],
    startDate='2023-01-01',
    endDate='2023-12-31'
)
print(status, message)
```

### Example 2: Retrieve Latest 10 Rows for Specific Currency Pairs
```
from currency import Currency
currency_data, status, message = Currency.getFxRate(
    database='googleSheets',
    provider='BoC',
    typeof='spot',
    tailRows=10,
    currencyPairs=['AUDCAD', 'INRCAD']
)
print(status, message)
```

### Example 3: Retrieve All Data Without Date Filtering
```
from currency import Currency
currency_data, status, message = Currency.getFxRate(
    database='googleSheets',
    provider='BoC',
    typeof='spot',
    allDates='Yes'
)
print(status, message)
```
### Error Handling
Error codes and messages are predefined in the returnValues dictionary to identify and communicate success, failure, or any specific issues with the query, such as missing currency pairs or incorrect date formats.
