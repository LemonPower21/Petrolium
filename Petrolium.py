import yfinance as yf
import requests
import webbrowser
import ta
import pandas as pd
import time
import os
import platform

def start_time():
    return time.time()

def stop_time(start_time):
    elapsed_time = time.time() - start_time
    years = int(elapsed_time // (365.25 * 24 * 3600))
    elapsed_time %= (365.25 * 24 * 3600)
    months = int(elapsed_time // (30.44 * 24 * 3600)) 
    elapsed_time %= (30.44 * 24 * 3600)
    days = int(elapsed_time // (24 * 3600))
    elapsed_time %= (24 * 3600)
    hours = int(elapsed_time // 3600)
    elapsed_time %= 3600
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60
    return years, months, days, hours, minutes, seconds
     
def clean():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def style():
    print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠈⢿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡿⠃⠀⠹⣿⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣶⡄⠘⠉⠀⠀⠀⠀⠹⠟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣄⠙⠛⠁⣤⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⠟⠁⠀⠈⢻⣿⡆⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣶⣿⡿⠛⢡⣖⣠⣴⠾⠛⠹⡇⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣀⠘⣿⠟⠋⠀⠀⢸⠿⠿⣦⣤⣀⡀⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠛⠀⠀⠀⠀⠀⠀⡿⠀⠀⠀⣈⣭⡿⢿⡆⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀
⠀⠀⢠⡟⠀⢿⡄⠀⠀⠀⢰⣧⣤⠶⠟⠋⠁⠀⠈⣧⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠛⠁⠀⠈⠛⠀⠀⠀⣼⠛⠛⠿⠶⣶⣤⣄⣀⣿⡀⠀⠀⠛⠃⠀⠀⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⠀⠀⢠⡿⠀⠀⠀⠀⣀⣤⡽⠿⢻⣇⠀⠘⠛⠋⠀⠀⠀⠀⠀
⠀⠀⠿⠿⠿⠿⠿⠀⢀⣸⣧⣴⣶⣚⣋⣁⣀⣀⣀⣀⣿⠀⠸⠿⠿⠀⢀⣀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠉⠉⠀⠀\n
    Petrolium Technology Server\n\n""")
def last(ticker):
    try:
        stock = yf.Ticker(ticker)
        last = stock.history(period="1d", interval="1m").iloc[-1]['Close']
        return last
    except Exception as e:
        print(f"Error fetching last price for {ticker}: {e}")
        return None

def roi(ticker, buy):
    try:
        stock = yf.Ticker(ticker)
        last = float(stock.history(period="1d", interval="1m").iloc[-1]['Close'])
        r = float((((last - buy) / buy) * 100))
        return r
    except Exception as e:
        print(f"Error calculating ROI for {ticker}: {e}")
        return None

def rsi(ticker, periods, chart_data, timeframe):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=chart_data, interval=timeframe)
        data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=periods).rsi()
        return float(data['RSI'].iloc[-1])
    except Exception as e:
        print(f"Error calculating RSI for {ticker}: {e}")
        return None

def ema(ticker, periods, chart_data, timeframe):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=chart_data, interval=timeframe)
        ema = data['Close'].ewm(span=periods, adjust=False).mean()
        return float(ema.iloc[-1])
    except Exception as e:
        print(f"Error calculating EMA for {ticker}: {e}")
        return None

def profit(ticker, buy, qty):
    try:
        stock = yf.Ticker(ticker)
        last = stock.history(period="1d", interval="1m").iloc[-1]['Close']
        return float(((((last - buy) / buy) * 100) * (qty * buy)))
    except Exception as e:
        print(f"Error calculating profit for {ticker}: {e}")
        return None

def invested(buy, qty):
    try:
        return qty * buy
    except Exception as e:
        print(f"Error calculating invested amount: {e}")
        return None

def telegram(token, id, message):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": id,
            "text": message
        }
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message via Telegram: {e}")
        return None

def ychart(ticker):
    link = "https://finance.yahoo.com/chart/" + ticker.upper()
    webbrowser.open_new(link)

def ynews(ticker):
    link = "https://finance.yahoo.com/news/"
    webbrowser.open_new(link)

def change(pair):
    try:
        currency_pair = yf.Ticker(pair.upper() + "=X")
        data = currency_pair.history(period="1d")
        exchange_rate = data['Close'].iloc[-1]
        return exchange_rate
    except Exception as e:
        print(f"Error fetching exchange rate for {pair}: {e}")
        return None

def ath(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="max")
        ath = data['Close'].max()
        return ath
    except Exception as e:
        print(f"Error fetching ATH for {ticker}: {e}")
        return None

def get_currency(ticker):
    try:
        stock = yf.Ticker(ticker)
        currency = stock.info['currency']
        return currency.upper()
    except Exception as e:
        print(f"Error fetching currency for {ticker}: {e}")
        return None

def get_exchange(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        exchange = info.get('exchange')
        return exchange
    except Exception as e:
        print(f"Error fetching exchange for {ticker}: {e}")
        return None

def monitor_mode(tickers, token="", id=""):
    msg = ""
    s = 0
    clean()
    msg_checker = []
    ticker_tracker = []
    exchange_tracker = []
    currency_tracker = []

    for i in range(tickers):
        stock = input("Ticker :> ")
        ticker_tracker.append(stock)
        currency_tracker.append(get_currency(stock))
        exchange_tracker.append(get_exchange(stock))
        msg_checker.append(0)

    text = f"🔵 MONITOR LIST 🔵\n\n"

    for i in range(tickers):
        stockt = f"Ticker: {ticker_tracker[i]}\n"
        text = text + stockt
    telegram(token, id, text)

    while True:
        t = 10
        s = s + 1
        clean()
        style()
        print(f"Server is running with {tickers} tickers...\t({s})\n")

        for i in range(tickers):
            try:
                ticker = ticker_tracker[i]
                lastv = last(ticker)
                emav = ema(ticker, 200, "2y", "1h")
                rsiv = rsi(ticker, 14, "2y", "1h")
                currency = currency_tracker[i]
                exchange = exchange_tracker[i]
                athv = ath(ticker)

                if currency == "EUR":
                    changev = 1.0000
                else:
                    changev = change(currency + "EUR")

                msg = f"🟢 BUY SIGNAL 🟢\n\nTicker: {ticker}\nExchange: {exchange}\nCurrency: {currency}\nChange(€): {format(changev, '.4f')}\nLast: {format(lastv, '.2f')}\nEMA: {format(emav, '.2f')}\nRSI: {format(rsiv, '.2f')}\nATH: {format(athv, '.2f')}"

                if emav and lastv and rsiv:  # Ensure values are not None
                    if emav > lastv:
                        if rsiv < 30:
                            if msg_checker[i] == 0:
                                telegram(token, id, msg)
                                msg_checker[i] = 1
                        if rsiv > 31:
                            msg_checker[i] = 0
                    else:
                        if rsiv > 31:
                            msg_checker[i] = 0
            except Exception as e:
                msg=""
                print(f"Error in monitor mode for {ticker}: {e}")
        time.sleep(t)

def position_mode(tickers, token="", id=""):
    t = 10
    msg = ""
    s = 0
    clean()
    msg_checker = []
    ticker_tracker = []
    exchange_tracker = []
    currency_tracker = []
    buy_tracker = []
    qty_tracker = []
    tp_tracker = []
    time_tracker = []
    terminal = input("Terminal :> ")

    for i in range(tickers):
        stock = input("Ticker :> ")
        qty = input("Quantity :> ")
        buy = input("Buy :> ")
        tp = input("TP(%) :> ")
        time_tracker.append(start_time())
        buy_tracker.append(buy)
        qty_tracker.append(qty)
        ticker_tracker.append(stock)
        currency_tracker.append(get_currency(stock))
        exchange_tracker.append(get_exchange(stock))
        tp_tracker.append(tp)
        msg_checker.append(0)

    text = f"🔵 TRANSACTION IN TERMINAL {terminal} 🔵\n\n"

    for i in range(tickers):
        stockt = f"Ticker: {ticker_tracker[i]}\n"
        qtyt = f"Quantity: {qty_tracker[i]}\n"
        buyt = f"Buy: {buy_tracker[i]}\n"
        tpt = f"TP(%): {tp_tracker[i]}%\n\n"
        text = text + stockt + qtyt + buyt + tpt

    telegram(token, id, text)

    while True:
        t = 10
        s = s + 1
        clean()
        style()
        print(f"Server is running with {tickers} tickers in terminal {terminal}...\t({s})\n")

        for i in range(tickers):
            try:
                tickerv = ticker_tracker[i]
                buyv = float(buy_tracker[i])
                qtyv = float(qty_tracker[i])
                lastv = float(last(tickerv))
                emav = float(ema(tickerv, 200, "2y", "1h"))
                rsiv = float(rsi(tickerv, 14, "2y", "1h"))
                currency = currency_tracker[i]
                exchange = exchange_tracker[i]
                athv = float(ath(tickerv))
                tpv = float(tp_tracker[i])
                roiv = float(roi(tickerv, float(buyv)))
                profitv = float(profit(tickerv, float(buyv), float(qtyv)))
                investedv = float(invested(float(buyv), float(qtyv)))
                years, months, days, hours, minutes, seconds = stop_time(time_tracker[i])

                if currency == "EUR":
                    changev = 1.000
                else:
                    changev = change(currency + "EUR")
                msg = f"🔴 SELL SIGNAL IN TERMINAL {terminal}🔴\n\nTicker: {tickerv}\nExchange: {exchange}\nCurrency: {currency}\nChange(€): {format(changev, '.4f')}\nQuantity: {format(qtyv, '.4f')}\nBuy: {format(buyv, '.2f')}\nLast: {format(lastv, '.2f')}\nInvested(V): {format(investedv, '.2f')}\nROI(%): {format(roiv, '.2f')}%\nROI(€): {format(profitv * float(changev), '.2f')}€\nEMA: {format(emav, '.2f')}\nRSI: {format(rsiv, '.2f')}\nATH: {format(athv, '.2f')}\nElapsed time: {years}Y, {months}M, {days}d, {hours}h, {minutes}m, {seconds:.2f}s"
                if lastv and emav and rsiv and athv and roiv and profitv and investedv:  
                    if roiv > tpv:
                        if msg_checker[i] == 0:
                            telegram(token, id, msg)
                            msg_checker[i] = 1
            except Exception as e:
                msg=""
                print(f"Error in position mode for {tickerv}: {e}")
            time.sleep(t)

clean()
style()
print("1) Monitor mode")
print("2) Position Mode")
print("3) Exit\n")
mode = int(input("Mode :> "))

tok = 'TOKEN'
id = 'ID'

if(mode==1):
    a = int(input("Number of tickers :> "))
    monitor_mode(a,tok,id)
if(mode==2):
    a = int(input("Number of tickers :> "))
    position_mode(a,tok,id)
if(mode==3):
    clean()
    print("Exited Petrolium")

else:
    print("Error: Command not found!")