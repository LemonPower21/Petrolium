import yfinance as yf
import ccxt
import pandas as pd
import time
import os
import requests

CLEAN = 'cls' #cls
TIME = 25
TOKEN = 'YOURTOKENHERE'
ID = 'YOURCHATIDHERE'
EXCHANGE = ccxt.binance()

def align(text):
    cols, rows = os.get_terminal_size()
    padding = (cols - len(text)) // 2
    print(" " * padding + text)

def telegram(token, id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

def crypto_radar():

    os.system(CLEAN)
    ticker = input("Ticker (Ex. BTC/USD): ").upper()
    buy = float(input("Buy: "))
    tp = int(input("TP(%): "))
    terminal = "C"+input("Terminal: ").upper()
    capitale = float(input("Capital: "))
    ath = max([x[2] for x in EXCHANGE.fetch_ohlcv(ticker, '1d')])
    telegram(TOKEN,ID,f"🔵 Alert for {ticker} in the terminal {terminal} with {tp}% take-profit has been set successfully!")
    bol = 1

    while bol==1:
        last = EXCHANGE.fetch_ticker(ticker)['close']
        growth = ((last - buy) / buy) * 100
        growthp = ((last - buy) / buy)
        if growth >= tp:
            telegram(TOKEN,ID,f"🟢 The ticker {ticker} in the terminal {terminal} reached {tp}% of growth!")
            bol = 0

        else:

            if growth > 0:
                print(f"Growth: \033[32m+{growth:.2f}%\033[37m of \033[33m{ticker}\033[37m in the terminal \033[36m{terminal}\033[37m\n")
                print(f"Capital: \033[36m{capitale:.2f}€\033[37m")
                print(f"Buy price: \033[35m{buy:.2f}€\033[37m")
                print(f"Last: \033[35m{last:.2f}€\033[37m")
                print(f"ATH: \033[31m{ath:.2f}€\033[37m\n")
                print(f"TP(%): \033[34m{tp:.2f}%\033[37m")
                print(f"P&L: \033[32m{growthp*capitale:.2f}€\033[37m")
            if growth <= 0:
                print(f"Growth: \033[31m{growth:.2f}%\033[37m of \033[33m{ticker}\033[37m in the terminal \033[36m{terminal}\033[37m\n")
                print(f"Capital: \033[36m{capitale:.2f}€\033[37m")
                print(f"Buy price: \033[35m{buy:.2f}€\033[37m")
                print(f"Last: \033[35m{last:.2f}€\033[37m")
                print(f"ATH: \033[31m{ath:.2f}€\033[37m\n")
                print(f"TP(%): \033[34m{tp:.2f}%\033[37m")
                print(f"P&L: \033[31m{growthp*capitale:.2f}€\033[37m")
        time.sleep(TIME)
        os.system(CLEAN)

    os.system(CLEAN)
    print("Exit successfully.")

def stock_radar():

    os.system(CLEAN)
    ticker = input("Ticker: ").upper()
    buy = float(input("Buy price: "))
    tp = int(input("TP(%): "))
    terminal = "A"+input("Terminal: ").upper()
    capitale = float(input("Capital: "))
    telegram(TOKEN,ID,f"🔵 Alert for {ticker} in the terminal {terminal} with {tp}% take-profit has been set successfully!")
    data = yf.download(ticker, start="1970-01-01")
    ath = data['Close'].max()
    bol = 1

    while bol==1:
        data = yf.download(ticker)
        last = data['Close'].iloc[-1]
        growth = ((last - buy) / buy) * 100
        growthp = ((last - buy) / buy)
        if growth >= tp:
            telegram(TOKEN,ID,f"🟢 The ticker {ticker} in the terminal {terminal} reached {tp}% of growth!")
            bol = 0

        else:

            if growth > 0:
                print(f"Growth: \033[32m+{growth:.2f}%\033[37m of \033[33m{ticker}\033[37m in the terminal \033[36m{terminal}\033[37m\n")
                print(f"Capital: \033[36m{capitale:.2f}€\033[37m")
                print(f"Buy price: \033[35m{buy:.2f}€\033[37m")
                print(f"Last: \033[35m{last:.2f}€\033[37m")
                print(f"ATH: \033[31m{ath:.2f}€\033[37m\n")
                print(f"TP(%): \033[34m{tp:.2f}%\033[37m")
                print(f"P&L: \033[32m{growthp*capitale:.2f}€\033[37m")
            if growth <= 0:
                print(f"Growth: \033[31m{growth:.2f}%\033[37m of \033[33m{ticker}\033[37m in the terminal \033[36m{terminal}\033[37m\n")
                print(f"Capital: \033[36m{capitale:.2f}€\033[37m")
                print(f"Buy price: \033[35m{buy:.2f}€\033[37m")
                print(f"Last: \033[35m{last:.2f}€\033[37m")
                print(f"ATH: \033[31m{ath:.2f}€\033[37m\n")
                print(f"TP(%): \033[34m{tp:.2f}%\033[37m")
                print(f"P&L: \033[31m{growthp*capitale:.2f}€\033[37m")
        time.sleep(TIME)
        os.system(CLEAN)

    os.system(CLEAN)
    print("Exit successfully.")


os.system(CLEAN)
print("\033[32m")
align(""" $$$$$$$\             $$\                         $$\ $$\                          """)                         
align(""" $$  __$$\            $$ |                        $$ |\__|                         """)                        
align(""" $$ |  $$ | $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  $$ |$$\ $$\   $$\ $$$$$$\$$$$\   """)
align(""" $$$$$$$  |$$  __$$\\_$$  _|  $$  __$$\ $$  __$$\ $$ |$$ |$$ |  $$ |$$  _$$  _$$\  """)
align(""" $$  ____/ $$$$$$$$ | $$ |    $$ |  \__|$$ /  $$ |$$ |$$ |$$ |  $$ |$$ / $$ / $$ | """)
align(""" $$ |      $$   ____| $$ |$$\ $$ |      $$ |  $$ |$$ |$$ |$$ |  $$ |$$ | $$ | $$ | """)
align(""" $$ |      \$$$$$$$\  \$$$$  |$$ |      \$$$$$$  |$$ |$$ |\$$$$$$  |$$ | $$ | $$ | """)
align(""" \__|       \_______|  \____/ \__|       \______/ \__|\__| \______/ \__| \__| \__| """)
print("\033[37m \n\n")
print("\033[33m1)\033[37m Stock Trading")
print("\033[33m2)\033[37m Crypto Trading")
print("\033[33m0)\033[37m Exit")
choice = int(input("\n\033[36m>>>:\033[37m  "))
if choice == 1:
    stock_radar()
if choice == 2:
    crypto_radar()
else:
    print("Exit successfully.") 