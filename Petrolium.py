import yfinance as yf
import ta
import time
import os
import platform
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from colorama import init, Fore
init(autoreset=True)

def bid(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        ask_price = stock.info.get('bid', None)
        if ask_price:
            return ask_price
        else:
            return 0
    except Exception as e:
        return None
def ask(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        ask_price = stock.info.get('ask', None)
        if ask_price:
            return ask_price
        else:
            return 0
    except Exception as e:
        return None
def start():
    return time.time()
def stop(start):
    elapsed_time = time.time() - start
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
def log(text):
    def check_network():
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        dev_null = 'NUL' if platform.system().lower() == 'windows' else '/dev/null'
        response = os.system(f"ping {param} 1 8.8.8.8 > {dev_null} 2>&1")
        return response == 0
    while not check_network():
        waitvar = 0
    current_time = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
    with open("log.txt", 'a') as file:
        file.write(f"\nLOGGER SYSTEM UPDATE [{current_time}]\n{text}\n")
def last(ticker):
    try:
        return yf.Ticker(ticker).history(period="1d", interval="1m").iloc[-1]['Close']
    except Exception:
        return None
def rsi(ticker, periods, chart, timeframe):
    try:
        data = yf.Ticker(ticker).history(period=chart, interval=timeframe)
        data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=periods).rsi()
        return data['RSI'].iloc[-1]
    except Exception:
        return None
def ema(ticker, periods, chart, timeframe):
    try:
        data = yf.Ticker(ticker).history(period=chart, interval=timeframe)
        return data['Close'].ewm(span=periods, adjust=False).mean().iloc[-1]
    except Exception:
        return None
def bos(ticker,lookback="5d",timeframe="1m"):
    try:
        data = yf.Ticker(ticker).history(period=lookback, interval=timeframe)
        recent_high = data['Close'].max() 
        current_price = data['Close'].iloc[-1] 
        if current_price >= recent_high:
            return True
        else:
            return False
    except Exception as e:
        return False
def clean():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
def email(server, port, user, password, recipient, subject, body):
    def check_network():
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        dev_null = 'NUL' if platform.system().lower() == 'windows' else '/dev/null'
        response = os.system(f"ping {param} 1 8.8.8.8 > {dev_null} 2>&1")
        return response == 0
    while True:
        try:
            while not check_network():
                time.sleep(5)
            msg = MIMEMultipart()
            msg['From'] = user
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            filename = "log.txt"
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )
                msg.attach(part)
            with smtplib.SMTP(server, port) as smtp:
                smtp.starttls()
                smtp.login(user, password)
                smtp.send_message(msg)
            break
        except Exception as e:
            time.sleep(5)
def change(pair):
    try:
        currency_pair = yf.Ticker(pair.upper() + "EUR=X")
        if (currency_pair == "EUREUR"):
            return 1
        else:
            data = currency_pair.history(period="1d")
            exchange_rate = data['Close'].iloc[-1]
            return exchange_rate
    except Exception as e:
        return None
def ath(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="max")
        ath = data['Close'].max()
        lastv = last(ticker)
        if(lastv>ath):
            return lastv
        else:
            return ath
    except Exception as e:
        return None
def currency(ticker):
    try:
        stock = yf.Ticker(ticker)
        currency = stock.info['currency']
        return currency.upper()
    except Exception as e:
        return None
def exchange(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        exchange = info.get('exchange')
        return exchange
    except Exception as e:
        return None
def volume(ticker):
    try:
        stock = yf.Ticker(ticker)
        real_time_volume = stock.info.get('regularMarketVolume', None)
        return real_time_volume
    except Exception as e:
        return None
def marketcap(ticker):
    try:
        stock = yf.Ticker(ticker)
        market_cap = stock.info.get('marketCap', None)
        return market_cap
    except Exception as e:
        return None
def shares(ticker):
    try:
        stock = yf.Ticker(ticker)
        shares_outstanding = stock.info.get('sharesOutstanding', None)
        return shares_outstanding
    except Exception as e:
        return None
def printallarm(tickerv, lastv, exchangev, currencyv, changev, emav, rsiv, athv, bidv, askv, volumev, marketcapv, sharesv, qtyv=0, investedv=0, buyv=0, tpv=0, roiv=0, profitv=0, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    def color_value(value):
        if value > 0: 
            return Fore.GREEN  
        if value < 0: 
            return Fore.RED
        return Fore.RESET    
    
    def color_ema(emav, lastv):
        return Fore.GREEN if emav > lastv else Fore.RED

    def color_rsi(rsiv):
        if rsiv < 30:
            return Fore.GREEN 
        elif rsiv > 70:
            return Fore.RED    
        return Fore.YELLOW

    tpv_str = f"{tpv:.2f}%"
    roiv_str = f"{roiv:.2f}%"
    profitv_str = f"{profitv:.2f}€"
    print(f"\n\n{Fore.CYAN}Ticker:{Fore.RESET}{' ' * (15 - len('Ticker:'))}{Fore.MAGENTA}{tickerv}{Fore.RESET}")
    print(f"{Fore.CYAN}Exchange:{Fore.RESET}{' ' * (15 - len('Exchange:'))}{Fore.BLUE}{exchangev}{Fore.RESET}")
    print(f"{Fore.CYAN}Currency:{Fore.RESET}{' ' * (15 - len('Currency:'))}{currencyv}")
    print(f"{Fore.CYAN}Change:{Fore.RESET}{' ' * (15 - len('Change:'))}{changev:.4f}")
    print(f"{Fore.CYAN}Quantity:{Fore.RESET}{' ' * (15 - len('Quantity:'))}{qtyv}")
    print(f"{Fore.CYAN}Invested:{Fore.RESET}{' ' * (15 - len('Invested:'))}{investedv:.2f}")
    print(f"{Fore.CYAN}Buy Price:{Fore.RESET}{' ' * (15 - len('Buy Price:'))}{buyv:.2f}")
    print(f"{Fore.CYAN}Last Price:{Fore.RESET}{' ' * (15 - len('Last Price:'))}{lastv:.2f}")
    print(f"{Fore.CYAN}TP (%):{Fore.RESET}{' ' * (15 - len('TP (%):'))}{tpv_str}")
    print(f"{Fore.CYAN}P&L (%):{Fore.RESET}{' ' * (15 - len('P&L (%):'))}{color_value(roiv)}{roiv_str}{Fore.RESET}")
    print(f"{Fore.CYAN}P&L (€):{Fore.RESET}{' ' * (15 - len('P&L (€):'))}{color_value(profitv)}{profitv_str}{Fore.RESET}")
    print(f"{Fore.CYAN}EMA:{Fore.RESET}{' ' * (15 - len('EMA:'))}{color_ema(emav, lastv)}{emav:.2f}{Fore.RESET}")
    print(f"{Fore.CYAN}RSI:{Fore.RESET}{' ' * (15 - len('RSI:'))}{color_rsi(rsiv)}{rsiv:.2f}{Fore.RESET}")
    print(f"{Fore.CYAN}ATH:{Fore.RESET}{' ' * (15 - len('ATH:'))}{athv:.2f}")
    print(f"{Fore.CYAN}Bid:{Fore.RESET}{' ' * (15 - len('Bid:'))}{Fore.YELLOW}{bidv:.2f}{Fore.RESET}")
    print(f"{Fore.CYAN}Ask:{Fore.RESET}{' ' * (15 - len('Ask:'))}{Fore.BLUE}{askv:.2f}{Fore.RESET}")
    print(f"{Fore.CYAN}Spread:{Fore.RESET}{' ' * (15 - len('Spread:'))}{(askv-bidv):.2f}")
    print(f"{Fore.CYAN}Shares:{Fore.RESET}{' ' * (15 - len('Shares:'))}{sharesv}")
    print(f"{Fore.CYAN}Volume:{Fore.RESET}{' ' * (15 - len('Volume:'))}{volumev}")
    print(f"{Fore.CYAN}MarketCap:{Fore.RESET}{' ' * (15 - len('MarketCap:'))}{marketcapv}")
    print(f"{Fore.CYAN}Elapsed Time:{Fore.RESET}{' ' * (15 - len('Elapsed Time:'))}{years}y {months}m {days}d {hours}h {minutes}m {seconds:.2f}s")
    print(Fore.RESET)
def initprint():
        print(f"{Fore.CYAN}{'Ticker':<10}\t{'Exchange':<10}\t{'Currency':<10}\t{'Change':<10}\t{'Quantity':<10}\t{'Invested':<10}\t{'Buy':<10}\t{'Last':<10}\t{'TP(%)':<10}\t{'P&L(%)':<10}\t{'P&L(€)':<10}\t{'EMA':<10}\t{'RSI':<10}\t{'ATH':<10}\t{'Bid':<10}\t{'Ask':<10}\t{'Spread':<10}\t{'Shares':<10}\t{'Volume':<15}\t{'MarketCap':<20}\t{'Elapsed time':<30}{Fore.RESET}")
def printall(tickerv, lastv, exchangev, currencyv, changev, emav, rsiv, athv,bidv,askv,volumev,marketcapv,sharesv,qtyv=0, investedv=0, buyv=0, tpv=0, roiv=0, profitv=0, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    def color_value(value):
        if value > 0: 
            return Fore.GREEN  
        if value < 0: 
            return Fore.RED
        return Fore.RESET    
    def color_ema(emav, lastv):
        return Fore.GREEN if emav > lastv else Fore.RED
    def color_rsi(rsiv):
        if rsiv < 30:
            return Fore.GREEN 
        elif rsiv > 70:
            return Fore.RED    
        return Fore.YELLOW 
    tpv_str = f"{tpv:.2f}%"
    roiv_str = f"{roiv:.2f}%"
    profitv_str = f"{profitv:.2f}€"
    print(f"{Fore.MAGENTA}{tickerv:<10}{Fore.RESET}\t{Fore.BLUE}{exchangev:<10}{Fore.RESET}\t{currencyv:<10}\t{changev:<10.4f}\t{qtyv:<10.2f}\t{investedv:<10.2f}\t{buyv:<10.2f}\t{lastv:<10.2f}\t{tpv_str:<10}\t{color_value(roiv)}{roiv_str:<10}{Fore.RESET}\t{color_value(profitv)}{profitv_str:<10}{Fore.RESET}\t{color_ema(emav, lastv)}{emav:<10.2f}{Fore.RESET}\t{color_rsi(rsiv)}{rsiv:<10.2f}{Fore.RESET}\t{athv:<10.2f}\t{Fore.BLUE}{bidv:<10.2f}{Fore.RESET}\t{Fore.YELLOW}{askv:<10.2f}{Fore.RESET}\t{askv-bidv:<10.2f}\t{sharesv:<10.2f}\t{volumev:<10.2f}\t{marketcapv:<10.2f}\t{years}Y, {months}M, {days}d, {hours}h, {minutes}m, {seconds:.2f}s")
def terminover(mode,tickers,terminal,pandlperc=0,pandl=0,invested=0):
    if pandlperc>0:
        print(f"Server is running with {tickers} tickers (\033[0;36mMonitor\033[0;37m)\t\tInvested: {invested:.2f}€\tP&L(%): {Fore.GREEN}{pandlperc:.2f}%{Fore.RESET}\tP&L(€): {Fore.GREEN}{pandl:.2f}€{Fore.RESET}" if mode == "M" else f"Server is running with {tickers} tickers in terminal {terminal} (\033[0;33mPosition\033[0;37m)\t\tInvested: {invested:.2f}€\tP&L(%): {Fore.GREEN}{pandlperc:.2f}%{Fore.RESET}\tP&L(€): {Fore.GREEN}{pandl:.2f}€{Fore.RESET}\n")
    if pandlperc<0:
        print(f"Server is running with {tickers} tickers (\033[0;36mMonitor\033[0;37m)\t\tInvested: {invested:.2f}€\tP&L(%): {Fore.RED}{pandlperc:.2f}%{Fore.RESET}\tP&L(€): {Fore.RED}{pandl:.2f}€{Fore.RESET}" if mode == "M" else f"Server is running with {tickers} tickers in terminal {terminal} (\033[0;33mPosition\033[0;37m)\t\tInvested: {invested:.2f}€\tP&L(%): {Fore.RED}{pandlperc:.2f}%{Fore.RESET}\tP&L(€): {Fore.RED}{pandl:.2f}€{Fore.RESET}\n")
    if pandlperc==0:
        print(f"Server is running with {tickers} tickers (\033[0;36mMonitor\033[0;37m)\t\tInvested: {invested:.2f}€\tP&L(%): {pandlperc:.2f}%\tP&L(€): {pandl:.2f}€" if mode == "M" else f"Server is running with {tickers} tickers in terminal {terminal} (\033[0;33mPosition\033[0;37m)\t\tInvested: {invested:.2f}€\tP&L(%): {pandlperc:.2f}%\tP&L(€): {pandl:.2f}€\n")               
def petrolium(tickers):
    tickerv= ""
    lastv  = 0
    exchangev = ""
    currencyv = ""
    changev= 0
    emav = 0
    rsiv = 0
    athv = 0
    qtyv = 0
    investedv = 0
    buyv = 0
    tpv = 0
    roiv = 0
    profitv  = 0
    aroiv = 0
    ainvested = 0
    aprofitv = 0
    years = 0
    months = 0
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    clean()
    data = {'tickers': [], 'buys': [], 'qtys': [], 'tps': [], 'msg_checker': [0] * tickers,'bos_checker': [0] * tickers,'cond1': [False] * tickers, 'condreset': [False] * tickers,'clock': []}
    mode = input("Select work mode (M/P) :> ").upper()
    dev = input("Select device (M/C) :> ").upper()
    text = ""
    terminal = "0"
    
    if mode == "P":
        terminal = input("Terminal :> ").upper()
    text = f"Terminal: {terminal}\n"
    for _ in range(tickers):
        ticker = input("Ticker :> ").upper()
        data['tickers'].append(ticker)
        data['msg_checker'].append(0)
        data['clock'].append(time.time())
        if mode == "P":
            buy = float(input("Buy :> "))
            qty = float(input("Qty :> "))
            tp = float(input("TP(%) :> "))
            data['buys'].append(buy)
            data['qtys'].append(qty)
            data['tps'].append(tp)
            text += f"Ticker: {ticker}\nBuy: {buy:.2f}\nQty: {qty:.2f}\nTP(%): {tp:.2f}%\n"
        else:
            text += f"Ticker: {ticker}\n"
    log(text+"Alert: TRANSACTION\n")
    while True:
        chk = True
        clean()
        terminover(mode,tickers,terminal,aroiv,aprofitv,ainvested)
        aroiv = 0
        ainvested = 0
        aprofitv = 0
        for i in range(tickers):
            try:
                tickerv = data['tickers'][i]
                exchangev = exchange(tickerv)
                currencyv = currency(tickerv)
                changev = change(currencyv.upper())
                athv = ath(tickerv)
                lastv = last(tickerv)
                emav = ema(tickerv, 200, "2y", "1h")
                rsiv = rsi(tickerv, 14, "2y", "1h")
                bidv = bid(tickerv)
                askv = ask(tickerv)
                sharesv = shares(tickerv)
                volumev = volume(tickerv)
                marketcapv = marketcap(tickerv)
                bosv = bos(tickerv)
                if mode == "P":
                    buyv = float(data['buys'][i])
                    qtyv = data['qtys'][i]
                    tpv = float(data['tps'][i])
                    startv = data['clock'][i]
                    years, months, days, hours, minutes, seconds = stop(startv)
                    roiv = ((lastv - buyv) / buyv) * 100
                    investedv = buyv * qtyv
                    profitv = roiv / 100 * investedv * changev
                    aprofitv += profitv
                    ainvested += (investedv*changev)
                    aroiv = (aprofitv/ainvested) *100
                    msg = f"Terminal: {terminal}\nTicker: {tickerv}\nExchange: {exchangev}\nCurrency: {currencyv}\nChange: {changev:.4f}\nQuantity: {qtyv:.2f}\nInvested: {investedv:.2f}\nBuy: {buyv:.2f}\nLast: {lastv:.2f}\nTP(%): {tpv:.2f}%\nP&L(%): {roiv:.2f}%\nP&L(€): {profitv:.2f}€\nEMA: {emav:.2f}\nRSI: {rsiv:.2f}\nATH: {athv:.2f}\nBid: {bidv:.2f}\nAsk: {askv:.2f}\nSpread: {askv-bidv:.2f}\nShares: {sharesv:.2f}\nVolume: {volumev:.2f}\nMarket Cap: {marketcapv:.2f}\nElapsed time: {years}Y, {months}M, {days}d, {hours}h, {minutes}m, {seconds:.2f}s\nAlert: SELL\n"
                        #CONDITIONS POSITION MODE
                else:
                    msg = f"Terminal: {terminal}\nTicker: {tickerv}\nExchange: {exchangev}\nCurrency: {currencyv}\nChange: {changev:.4f}\nLast: {lastv:.2f}\nEMA: {emav:.2f}\nRSI: {rsiv:.2f}\nATH: {athv:.2f}\nBid: {bidv:.2f}\nAsk: {askv:.2f}\nSpread: {askv-bidv:.2f}\nShares: {sharesv:.2f}\nVolume: {volumev:.2f}\nMarket Cap: {marketcapv:.2f}\nAlert: BUY\n"
                    #CONDITIONS MONITOR MODE
                if(dev == "M"):
                    printallarm(tickerv, lastv, exchangev, currencyv, changev,emav, rsiv, athv,bidv,askv,volumev,marketcapv,sharesv, qtyv, investedv, buyv, tpv, roiv, profitv,  years, months, days, hours, minutes, seconds)
                if(dev == "C"):
                    if(chk):
                        initprint()
                        chk=False
                    printall(tickerv, lastv, exchangev, currencyv, changev,emav, rsiv, athv,bidv,askv,volumev,marketcapv,sharesv, qtyv, investedv, buyv, tpv, roiv, profitv,  years, months, days, hours, minutes, seconds)
            except Exception as e:
                clean()
        time.sleep(10)
clean()
n = int(input("Number of tickers :> "))
petrolium(n)