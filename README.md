# Petrolium
Petrolium is an innovative stock trading alert system! It uses Telegram API to send message in addiction of the Python "requests" library.

# How does It work?
- In your investment account you buy the stock you choose at market price with a certain amount of money.
- Then you configure Petrolium (in 24/7 server) setting Buy price, TP (Take-Profit), Terminal (to recognise working window) and even Capital invested.
- Once the price of the stock rise and hit Take-Profit, you will receive notification on Telegram
- Petrolium check stock price every minute!

 # It is a trading bot?
 No, It isn't. However It is useful to earn on short-period of time (of course the period will depends by market price and the TP you insert).

# How to configure API for message?
1. You create Telegram account.
2. You search for "BotFather" and write /start and then /newbot
3. Once you completed step told by "BotFather" you will receive a token that you will insert in python code.
4. In order to obtain ChatID, search for "YourBot" on Telegram, and then go to this link:
   https://api.telegram.org/botTOKENHERE/getUpdates (substitute TOKENHERE with your real token)
5. Then send a message to your bot by telegram and reload that page.
6. Afterwards you click on "format code", and then you will find ID in "chat{id{ID HERE}}"

# Where are the ticker of stock?
1. You can find the stock ticker or symbol here: https://finance.yahoo.com/markets/stocks/most-active/
2. For crypto there is an example in the code.

 # How to setup It in Linux Machine?
 1. Install Python3 and pythn3-pip.
 2. Execute these following lines:

```pip install time``` 

```pip install os``` 

```pip install pandas``` 

```pip install requests``` 

```pip install yfinance```

```pip install ccxt``` 
