import yfinance as yf
import ta
import time
import alpaca_trade_api as tradeapi
import logging
import os
import platform
import smtplib
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S %d/%m/%Y',
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ]
)

API_KEY = 'ALPACA API KEY'
API_SECRET = 'ALPACA API SECRET'
BASE_URL = "https://paper-api.alpaca.markets"
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'SENDMAIL' 
SENDER_PASSWORD = 'PASSWORD'  
RECIPIENT_EMAIL = 'RECEIVEREMAIL'  

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

symbols = [
    'AAPL']
tickersprice = {symbol: None for symbol in symbols}
condition1 = {symbol: True for symbol in symbols}
condition2 = {symbol: False for symbol in symbols}
qtyv = {symbol: 0 for symbol in symbols}
t = 0.5 

def clean():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
def log(message):
    time.sleep(t)  
    logging.info(message.upper())
def network(t=0.5):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    dev_null = 'NUL' if platform.system().lower() == 'windows' else '/dev/null'
    
    while True:
        response = os.system(f"ping {param} 1 8.8.8.8 > {dev_null} 2>&1")
        if response == 0:
            log(f"NETWORK AVAILABLE")
            break 
        else:
            clean()
            log(f"NETWORK NOT AVAILABLE RETRYING IN 5 SECONDS")
            time.sleep(t) 
def email(subject, body, retries=5, delay=5, benchmark_file="Benchmark.xlsx"):
    network()
    att = 0
    while att < retries:
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECIPIENT_EMAIL
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            if os.path.exists(benchmark_file):
                with open(benchmark_file, "rb") as file:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={benchmark_file}')
                    msg.attach(part)
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                text = msg.as_string()
                server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
                log(f"EMAIL SENT: {subject}")
                return
        except Exception as e:
            log(f"ERROR SENDING EMAIL: {e}")
            att += 1
            if att < retries:
                log(f"ATTEMPT OF SENDING EMAIL NUMBER {att} OF {retries}")
                time.sleep(delay)
            else:
                log(f"FAILED SENDING EMAIL AFTER {retries} ATTEMPTS")
                return
def fetchdata(symbol, period="2y", interval="1h"):
    network()
    try:
        log(f"FETCHING DATA FOR {symbol}")
        return yf.Ticker(symbol).history(period=period, interval=interval)
    except Exception as e:
        log(f"ERROR FETCHING DATA FOR {symbol}: {e}")
        return None
def last(symbol, period="1d", interval="1m"):
    network()
    try:
        log(f"FETCHING LAST PRICE FOR {symbol}")
        data = yf.Ticker(symbol).history(period=period, interval=interval)
        return data.iloc[-1]['Close']
    except Exception as e:
        log(f"ERROR FETCHING LAST PRICE FOR {symbol}: {e}")
        return None
def ema(data):
    try:
        log("CALCULATING EMA")
        return data['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    except Exception as e:
        log(f"ERROR CALCULATING EMA: {e}")
        return None
def rsi(data):
    try:
        log("CALCULATING RSI")
        return ta.momentum.RSIIndicator(data['Close'], window=14).rsi().iloc[-1]
    except Exception as e:
        log(f"ERROR CALCULATING RSI: {e}")
        return None
def bos(symbol,last, period="5d", interval="1m"):
    network()
    try:
        log(f"CALCULATING BOS FOR {symbol}")
        data = yf.Ticker(symbol).history(period=period, interval=interval)
        if(last >= data['Close'].max() - (data['Close'].max()*0.009)):
            return True
        else:
            return False
    except Exception as e:
        log(f"ERROR CALCULATING BOS FOR {symbol}: {e}")
        return False
def ath(symbol, period="max", interval="1d"):
    network()
    try:
        log(f"FETCHING ATH FOR {symbol}")
        data = yf.Ticker(symbol).history(period=period, interval=interval)
        return data['Close'].max()
    except Exception as e:
        log(f"ERROR FETCHING ATH FOR {symbol}: {e}")
        return None
def ordersizing(symbol, lastv, cash_percentage=0.05):
    network()
    try:
        log(f"CALCULATING QUANTITY FOR {symbol}")
        account = api.get_account()
        cash = float(account.cash)
        qty = int((cash * cash_percentage) / lastv)
        return qty if qty >= 1 else 0
    except Exception as e:
        log(f"ERROR CALCULATING QUANTITY FOR {symbol}: {e}")
        return 0
def excel(buy_price, last_price, filename="Benchmark.xlsx"):
    try:
        header_fill = PatternFill(start_color="46bdc6", end_color="46bdc6", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True, size=12)
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        if os.path.exists(filename):
            wb = openpyxl.load_workbook(filename)
            sheet = wb.active
        else:
            wb = openpyxl.Workbook()
            sheet = wb.active
            
            sheet['A1'] = 'Date'
            sheet['B1'] = 'Benchmark'
            sheet['C1'] = 'Profit (%)'
            sheet['A1'].fill = header_fill
            sheet['B1'].fill = header_fill
            sheet['C1'].fill = header_fill
            sheet['A1'].font = header_font
            sheet['B1'].font = header_font
            sheet['C1'].font = header_font
            sheet['A1'].alignment = header_alignment
            sheet['B1'].alignment = header_alignment
            sheet['C1'].alignment = header_alignment
            sheet.column_dimensions['A'].width = 20
            sheet.column_dimensions['B'].width = 20
            sheet.column_dimensions['C'].width = 20
            sheet.column_dimensions['D'].width = 20
            sheet.row_dimensions[1].height = 20
            sheet['A2'] = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            sheet['B2'] = round(100, 2)
            sheet['C2'] = round(0, 2)
        
        profit_percent = round(((last_price - buy_price) / buy_price) * 100, 2)
        previous_benchmark = sheet['B' + str(sheet.max_row)].value
        new_benchmark = round(previous_benchmark * (1 + profit_percent / 100), 2)
        
        sheet.append([datetime.now().strftime('%H:%M:%S %d/%m/%Y'), new_benchmark, profit_percent])
        
        for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=3):
            for cell in row:
                border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                cell.border = border
                cell.alignment = Alignment(horizontal="center", vertical="center")

        chart = LineChart()
        chart.title = "Petrolium Benchmark"
        chart.style = 13
        chart.x_axis.title = 'Date'
        chart.y_axis.title = 'Benchmark'
        chart.y_axis.number_format = '0.00'
        data = Reference(sheet, min_col=2, min_row=1, max_col=2, max_row=sheet.max_row)
        categories = Reference(sheet, min_col=1, min_row=2, max_row=sheet.max_row)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)
        chart.series[0].graphicalProperties.line.solidFill = "46bdc6"
        chart.series[0].graphicalProperties.line.width = 40000
        chart.legend = None
        sheet.add_chart(chart, "G5")
        
        sheet['E1'] = "Max"
        sheet['E1'].fill = header_fill
        sheet['E1'].font = header_font
        sheet['E1'].alignment = header_alignment
        sheet['E1'].border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
        sheet['E2'] = round(max([cell.value for cell in sheet['B'][1:]]), 2)

        sheet.column_dimensions['E'].width = 20
        sheet['E2'].alignment = Alignment(horizontal="center", vertical="center")
        sheet['E2'].border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
        
        wb.save(filename)
        log(f"EXCEL FILE UPDATED SUCCESSFULLY")
    
    except Exception as e:
        log(f"EXCEL FILE NOT UPDATED: {e}")
def ordermaker(symbol, qty, action,buyv=0,lastv=0):
    network()
    try:
        log(f"PLACING {action.upper()} ORDER FOR {symbol}")
        if action == 'buy':
            email(f"BUY ORDER FOR {symbol}", f"Successfully bought {qty} stocks of {symbol}!")
            api.submit_order(symbol, qty, 'buy', 'market', 'gtc')
        elif action == 'sell':
            excel(buyv,lastv)
            api.submit_order(symbol, qty, 'sell', 'market', 'gtc')
            email(f"SELL ORDER FOR {symbol}", f"Successfully sold {qty} stocks of {symbol}!")
        return True
    except Exception as e:
        log(f"ERROR PLACING {action.upper()} ORDER FOR {symbol}: {e}")
        return False
def petrolium():
    clean()
    email(f"PETROLIUM IS WORKING", f"Server is running properly!")
    while True:
        clean()
        for symbol in symbols:
            check = None
            try:
                data = fetchdata(symbol)
                if data is None:
                    continue
                time.sleep(t)
                lastv = last(symbol)
                if lastv is None:
                    continue
                time.sleep(t)
                emav = ema(data)
                rsiv = rsi(data)
                if emav is None or rsiv is None:
                    continue
                bosv = bos(symbol,lastv)
                athv = ath(symbol)
                if bos is None or athv is None:
                    continue

                if condition1[symbol] and rsiv < 30 and emav > lastv:             
                    condition1[symbol], condition2[symbol] = False, True
                    log(f"BUY CONDITIONS 1 SATISFIED FOR {symbol}")

                if condition2[symbol] and bosv:
                    log(f"BUY CONDITIONS 2 SATISFIED FOR {symbol}")
                    qty = ordersizing(symbol, lastv)

                    if lastv <= athv - (athv * 0.03) and qty >= 1:
                        log(f"BUY CONDITIONS 3 SATISFIED FOR {symbol}")
                        check = ordermaker(symbol, qty, 'buy')
                        if(check):
                            tickersprice[symbol] = lastv
                            condition2[symbol] = False
                        else:
                            condition1[symbol], condition2[symbol], tickersprice[symbol] = True, False, None 
                    else:
                        condition1[symbol], condition2[symbol], tickersprice[symbol] = True, False, None
                elif tickersprice[symbol] and (lastv - tickersprice[symbol]) / tickersprice[symbol] * 100 > 3:
                    check = ordermaker(symbol, qtyv[symbol], 'sell',tickersprice[symbol],lastv)
                    if(check):
                        condition1[symbol], condition2[symbol], tickersprice[symbol] = True, False, None
            except Exception as e:
                log(f"ERROR IN TRADING LOOP FOR {symbol}: {e}")
            time.sleep(t)
petrolium()