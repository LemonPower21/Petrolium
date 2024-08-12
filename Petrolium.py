import yfinance as yf
import pandas as pd
import time
import os
import requests

CLEAN = 'clear' #cls
TIME = 60
TOKEN = 'YOURTOKENHERE'
ID = 'YOURCHATIDHERE'

def telegram(token, id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

def radar():

    os.system(CLEAN)
    ticker = input("Ticker: ").upper()
    buy = float(input("Buy: "))
    tp = int(input("TP: "))
    terminal = input("Terminal: ").upper()
    capitale = float(input("Capital: "))
    telegram(TOKEN,ID,f"🔵 Alert for {ticker} in the terminal {terminal} with {tp}% take-profit has been set successfully!")
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
                print(f"Buy: \033[35m{buy:.2f}€\033[37m")
                print(f"Last: \033[35m{last:.2f}€\033[37m\n")
                print(f"TP: \033[34m{tp:.2f}%\033[37m")
                print(f"P&L: \033[32m{growthp*capitale:.2f}€\033[37m")
            if growth <= 0:
                print(f"Growth: \033[31m{growth:.2f}%\033[37m of \033[33m{ticker}\033[37m in the terminal \033[36m{terminal}\033[37m\n")
                print(f"Capital: \033[36m{capitale:.2f}€\033[37m")
                print(f"Buy: \033[35m{buy:.2f}€\033[37m")
                print(f"Last: \033[35m{last:.2f}€\033[37m\n")
                print(f"TP: \033[34m{tp:.2f}%\033[37m")
                print(f"P&L: \033[31m{growthp*capitale:.2f}€\033[37m")
        time.sleep(TIME)
        os.system(CLEAN)

    os.system(CLEAN)
    print("Exit successfully.")

radar()