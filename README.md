# Petrolium Technology Server

This project provides various functions for financial analysis using the `yfinance` and `ta` libraries. It includes functionalities for retrieving stock prices, calculating financial indicators, monitoring stocks, and sending notifications via Telegram.

## Features

- **Financial Analysis**: Functions to retrieve stock prices, calculate ROI, RSI, EMA, and profit.
- **Telegram Notifications**: Send notifications via Telegram.
- **Monitoring Mode**: Monitor multiple tickers and send buy/sell signals.
- **Position Mode**: Monitor specific positions and send sell signals.
- **Chronometer**: Measure elapsed time in years, months, days, hours, minutes, and seconds.

## Requirements

- `yfinance`
- `requests`
- `webbrowser`
- `ta`
- `pandas`
- `platform`
- `os`
- `time`

You can install the required libraries using:
```bash
pip install yfinance requests ta pandas
```

## Usage

### Start the Application

```python
python petrolium_technology_server.py
```

### Monitor Mode

1. Run the script.
2. Select `1` for Monitor mode.
3. Enter the number of tickers to monitor.
4. Enter the tickers one by one.
5. The application will monitor the tickers and send buy signals via Telegram.

### Position Mode

1. Run the script.
2. Select `2` for Position mode.
3. Enter the number of tickers to monitor.
4. Enter the terminal name.
5. Enter the tickers, quantity, buy price, and take profit percentage for each ticker.
6. The application will monitor the positions and send sell signals via Telegram.

### Exit

1. Run the script.
2. Select `3` to exit.

## Functions

### `start_time()`

- **Description**: Returns the current time.
- **Returns**: Current time in seconds.

### `stop_time(start_time)`

- **Description**: Calculates the elapsed time.
- **Parameters**: `start_time` - The start time.
- **Returns**: Years, months, days, hours, minutes, and seconds.

### `clean()`

- **Description**: Clears the console screen.

### `last(ticker)`

- **Description**: Fetches the last closing price of the specified ticker.
- **Parameters**: `ticker` (str) - The ticker symbol.
- **Returns**: Last closing price.

### `roi(ticker, buy)`

- **Description**: Calculates the Return on Investment (ROI) for the specified ticker and buy price.
- **Parameters**: `ticker` (str) - The ticker symbol.
  `buy` (float) - The buy price.
- **Returns**: ROI in percentage.

### `rsi(ticker, periods, chart_data, timeframe)`

- **Description**: Calculates the Relative Strength Index (RSI) for the specified ticker.
- **Parameters**: `ticker` (str) - The ticker symbol.
  `periods` (int) - The number of periods for RSI calculation.
  `chart_data` (str) - The period of chart data.
  `timeframe` (str) - The interval of the chart data.
- **Returns**: RSI value.

### `ema(ticker, periods, chart_data, timeframe)`

- **Description**: Calculates the Exponential Moving Average (EMA) for the specified ticker.
- **Parameters**: `ticker` (str) - The ticker symbol.
  `periods` (int) - The number of periods for EMA calculation.
  `chart_data` (str) - The period of chart data.
  `timeframe` (str) - The interval of the chart data.
- **Returns**: EMA value.

### `profit(ticker, buy, qty)`

- **Description**: Calculates the profit for the specified ticker, buy price, and quantity.
- **Parameters**: `ticker` (str) - The ticker symbol.
  `buy` (float) - The buy price.
  `qty` (float) - The quantity.
- **Returns**: Profit value.

### `invested(buy, qty)`

- **Description**: Calculates the invested amount for the specified buy price and quantity.
- **Parameters**: `buy` (float) - The buy price.
  `qty` (float) - The quantity.
- **Returns**: Invested amount.

### `telegram(token, id, message)`

- **Description**: Sends a message via Telegram.
- **Parameters**: `token` (str) - The Telegram bot token.
  `id` (str) - The chat ID.
  `message` (str) - The message to send.
- **Returns**: Response from Telegram API.

### `ychart(ticker)`

- **Description**: Opens the Yahoo Finance chart for the specified ticker in a web browser.
- **Parameters**: `ticker` (str) - The ticker symbol.

### `ynews(ticker)`

- **Description**: Opens the Yahoo Finance news page in a web browser.

### `change(pair)`

- **Description**: Fetches the exchange rate for the specified currency pair.
- **Parameters**: `pair` (str) - The currency pair.
- **Returns**: Exchange rate.

### `ath(ticker)`

- **Description**: Fetches the all-time high (ATH) for the specified ticker.
- **Parameters**: `ticker` (str) - The ticker symbol.
- **Returns**: ATH value.

### `get_currency(ticker)`

- **Description**: Fetches the currency in which the specified ticker is traded.
- **Parameters**: `ticker` (str) - The ticker symbol.
- **Returns**: Currency.

### `get_exchange(ticker)`

- **Description**: Fetches the exchange where the specified ticker is traded.
- **Parameters**: `ticker` (str) - The ticker symbol.
- **Returns**: Exchange.

## Example

To start the application, simply run the script and follow the prompts to enter the necessary information. The application will then monitor the tickers or positions and send notifications via Telegram as needed.

Enjoy using the Petrolium Technology Server!
