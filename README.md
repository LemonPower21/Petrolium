# Petrolium Technology Server

This project provides a set of functions designed to assist with financial analysis using stock data and technical indicators. It features capabilities for monitoring stocks, analyzing technical indicators like RSI and EMA, and sending notifications via Telegram or email.

## Features

- **Financial Analysis**: Retrieve stock prices, calculate ROI, RSI, EMA, P&L, and other financial metrics.
- **Position Monitoring**: Track specific positions with user-defined buy prices, quantities, and take-profit percentages.
- **Telegram Notifications**: Receive real-time updates about the stock positions.
- **Market Metrics**: Fetch real-time data like volume, market cap, bid/ask prices, and more.
- **Time Tracking**: Measure elapsed time in years, months, days, and more.
- **Logging**: Record events and actions to a log file for tracking and analysis.

## Requirements

To run the application, you'll need the following Python libraries:

- `yfinance` for financial data.
- `ta` for technical analysis indicators.
- `time` for time tracking.
- `platform` for platform-specific operations.
- `requests` and `smtplib` for sending notifications.
- `colorama` for colored output in the terminal.

You can install the required libraries using:

```bash
pip install yfinance requests ta pandas colorama
```

## Usage

### Start the Application

```bash
python Petrolium.py
```

Upon running the script, you will be prompted to select between **Monitor mode** and **Position mode**.

### Monitor Mode

1. Run the script and choose `M` for **Monitor mode**.
2. Input the number of tickers you wish to monitor.
3. Enter each ticker symbol.
4. The system will track the selected tickers and send buy/sell alerts via Telegram if necessary.

### Position Mode

1. Run the script and select `P` for **Position mode**.
2. Specify the number of tickers and terminal name.
3. Enter buy price, quantity, and take profit percentage for each ticker.
4. The system will monitor these positions and notify you of buy/sell opportunities.

### Exit

To exit the application, simply choose the exit option after completing your tasks.

## Key Functions

### `start()`

- **Description**: Starts the timer.
- **Returns**: The current time in seconds since the epoch.

### `stop(start)`

- **Description**: Stops the timer and calculates elapsed time.
- **Parameters**: `start` - The start time in seconds.
- **Returns**: A tuple with years, months, days, hours, minutes, and seconds.

### `bid(ticker)`

- **Description**: Fetches the bid price of the specified stock.
- **Parameters**: `ticker` - The stock symbol (e.g., `AAPL`).
- **Returns**: The bid price or `None` if the data is unavailable.

### `ask(ticker)`

- **Description**: Fetches the ask price of the specified stock.
- **Parameters**: `ticker` - The stock symbol (e.g., `AAPL`).
- **Returns**: The ask price or `None` if the data is unavailable.

### `rsi(ticker, periods, chart, timeframe)`

- **Description**: Calculates the Relative Strength Index (RSI) for a given stock.
- **Parameters**:
  - `ticker` - The stock symbol (e.g., `AAPL`).
  - `periods` - The number of periods for RSI calculation.
  - `chart` - The length of the chart data (e.g., `"1y"`).
  - `timeframe` - The data interval (e.g., `"1d"`).
- **Returns**: The RSI value.

### `ema(ticker, periods, chart, timeframe)`

- **Description**: Calculates the Exponential Moving Average (EMA) for a given stock.
- **Parameters**:
  - `ticker` - The stock symbol (e.g., `AAPL`).
  - `periods` - The number of periods for EMA calculation.
  - `chart` - The length of the chart data (e.g., `"1y"`).
  - `timeframe` - The data interval (e.g., `"1d"`).
- **Returns**: The EMA value.

### `bos(ticker, lookback="5d", timeframe="1m")`

- **Description**: Determines if the stock price has reached a new high within a specified lookback period.
- **Parameters**:
  - `ticker` - The stock symbol (e.g., `AAPL`).
  - `lookback` - The period to look back (default is `"5d"`).
  - `timeframe` - The data interval (default is `"1m"`).
- **Returns**: `True` if the stock has reached a new high, otherwise `False`.

### `log(text)`

- **Description**: Logs the provided text to a log file with timestamp.
- **Parameters**: `text` - The message to log.

### `email(server, port, user, password, recipient, subject, body)`

- **Description**: Sends an email with the specified details and includes a log file as an attachment.
- **Parameters**:
  - `server` - The email server (e.g., `smtp.gmail.com`).
  - `port` - The port number (e.g., `587` for TLS).
  - `user` - The email address to send from.
  - `password` - The email password.
  - `recipient` - The recipient email address.
  - `subject` - The email subject.
  - `body` - The email body.

### `change(pair)`

- **Description**: Fetches the exchange rate for a given currency pair (e.g., `USDEUR=X`).
- **Parameters**: `pair` - The currency pair (e.g., `USDEUR`).
- **Returns**: The exchange rate or `None` if unavailable.

### `ath(ticker)`

- **Description**: Fetches the all-time high (ATH) for the given stock.
- **Parameters**: `ticker` - The stock symbol.
- **Returns**: The all-time high price or `None` if unavailable.

### `currency(ticker)`

- **Description**: Fetches the currency in which the stock is traded.
- **Parameters**: `ticker` - The stock symbol.
- **Returns**: The currency symbol (e.g., `USD`).

### `exchange(ticker)`

- **Description**: Fetches the exchange where the stock is traded.
- **Parameters**: `ticker` - The stock symbol.
- **Returns**: The exchange name (e.g., `NASDAQ`).

## Example Output

The output for each monitored ticker will look like this:

```
Ticker: AAPL
Exchange: NASDAQ
Currency: USD
Change: +0.0205
Quantity: 10
Invested: 1500.00
Buy Price: 150.00
Last Price: 153.00
TP (%): 10.00%
P&L (%): +2.00%
P&L (€): +30.00€
EMA: 151.20
RSI: 65.00
ATH: 200.00
Bid: 152.50
Ask: 153.50
Spread: 1.00
Shares: 5000000000
Volume: 2000000
MarketCap: 2.4T
Elapsed Time: 0y 0m 5d 1h 30m 0.00s
```

## Conclusion

The **Petrolium Technology Server** is an advanced stock monitoring system that allows for detailed analysis, alerting, and reporting of stock market data in real time. It is ideal for traders and investors looking for a powerful tool to assist in their decision-making process.
