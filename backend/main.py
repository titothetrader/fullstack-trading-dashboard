import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import datetime

# Load dotEnv
load_dotenv()

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.datetime.now() - datetime.timedelta(days=1)
today = today.strftime("%Y-%m-%d")
# print(today)

# Load App and Routes    
app = FastAPI()

# Load FastAPI CORS
origins = ['https://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000', '*:*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)
 
# Load Fast API Jinja templates
templates = Jinja2Templates(directory="./templates")

# Connect to PlanetScale DB
connection = mysql.connector.connect(
host=os.getenv("HOST"),
database=os.getenv("DATABASE"),
user=os.getenv("DB_USER"),
password=os.getenv("PASSWORD"),
ssl_ca=os.getenv("SSL_CERT")
)
try:
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
except Error as e:
    print("Error while connecting to MySQL", e)

# GLOBAL VARS
symbols = []
stock_dict = dict()

# DB FUNCTIONS - get all symbols
## STOCKS
def getAllStocks(limit = 100, filter = ''):
    if filter == '' or filter == 'null':
        sql = "SELECT DISTINCT stock.id, stock.symbol, stock.name from stock JOIN stock_price ON stock.id = stock_price.stock_id WHERE stock_price.close != '' LIMIT " + str(limit)
            
    if filter == 'new_intraday_highs':
        sql = "SELECT DISTINCT stock.id, stock.symbol, stock.name from stock JOIN stock_price ON stock.id = stock_price.stock_id WHERE stock_price.close != '' LIMIT " + str(limit)
        
    if filter == 'new_closing_highs':
        print(today)
        sql = f"SELECT DISTINCT symbol, name, id, date, close from (SELECT p.stock_id, s.symbol, s.name, s.id, p.date, p.close, p.alltime_high from stock_price as p join stock as s on s.id = p.stock_id where close = alltime_high group by stock_id, date, close order by date desc) as t1 where date = '{today}'"
        
    if filter == 'new_intraday_lows':
        sql = "SELECT DISTINCT stock.id, stock.symbol, stock.name from stock JOIN stock_price ON stock.id = stock_price.stock_id WHERE stock_price.close != '' LIMIT " + str(limit)
        
    if filter == 'new_closing_lows':
        sql = f"SELECT DISTINCT id, symbol, name, date, close from (SELECT p.stock_id, s.symbol, s.name, s.id, p.date, p.close, p.alltime_low from stock_price as p join stock as s on s.id = p.stock_id where close = alltime_low group by stock_id, date, close order by date desc) as t1 where date = '{today}'"
    cursor.execute(sql)
    records = cursor.fetchall()
    return records

def getStockDetails(symbol):
    sql_details = "SELECT * from stock WHERE symbol = '" + str(symbol) + "'"
    cursor.execute(sql_details)
    details = cursor.fetchall()
    sql_prices = "SELECT * from stock JOIN stock_price ON stock.id = stock_price.stock_id WHERE symbol = '" + str(symbol) + "' ORDER BY stock_price.date"
    cursor.execute(sql_prices)
    prices = cursor.fetchall()
    results = {
        "details": details,
        "prices": prices
    }
    return results

## CRYPTOS
def getAllCryptos(limit = 100):
    sql = "SELECT * from crypto_trade LIMIT " + str(limit)
    cursor.execute(sql)
    records = cursor.fetchall()
    return records

def getCryptoDetails(symbol):
    # print("getCryptoDetails")
    sql_details = "SELECT * from crypto_trade WHERE symbol = '" + str(symbol) + "'"
    cursor.execute(sql_details)
    details = cursor.fetchall()
    sql_prices = "SELECT * from crypto_trade JOIN crypto_price ON crypto_trade.id = crypto_price.crypto_id WHERE crypto_trade.symbol = '" + str(symbol) + "' ORDER BY crypto_price.date"
    cursor.execute(sql_prices)
    prices = cursor.fetchall()
    results = {
        "details": details,
        "prices": prices
    }
    return results

## CRYPTO COIN
def getAllCoins(limit):
    sql = "SELECT * FROM crypto_coin LIMIT " + str(limit)
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(records)
    return records
    
def getCryptoCoin(symbol):
    sql = f"SELECT * FROM crypto_coin WHERE symbol = '{symbol}'"
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(records)
    return records

## CRYPTO EXCHANGES
def getAllCryptoExchanges(limit = 100):
    sql = "SELECT * FROM crypto_exchange LIMIT " + str(limit)
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(records)
    return records

def getCryptoExchangeDetails(exchange_id):
    sql = f"SELECT * FROM crypto_exchange WHERE coingecko_id = '{exchange_id}'"
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(records)
    return records

## FOREX
def getAllForex(limit = 100):
    sql = "SELECT * FROM forex LIMIT " + str(limit)
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(records)
    return records

def getForexDetails(pair):
    sql_details = f"SELECT * FROM forex WHERE forex_pair = '{pair}'"
    cursor.execute(sql_details)
    details = cursor.fetchall()
    sql_prices = "SELECT * from forex JOIN forex_price ON forex.id = forex_price.forex_id WHERE forex.forex_pair = '" + str(pair) + "' ORDER BY forex_price.date"
    cursor.execute(sql_prices)
    prices = cursor.fetchall()
    results = {
        "details": details,
        "prices": prices
    }
    return results
    

## STRATEGIES
def getAllStrategies():
    sql = "SELECT * FROM strategy ORDER BY name ASC"
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(stratRecords)
    return records

def getStrategyDetails(strategyCode):
    sql = f"SELECT * FROM strategy WHERE strategy_code = '{strategyCode}'"
    cursor.execute(sql)
    records = cursor.fetchall()
    return records
    

# -----------------------
# -----------------------
# Load FastAPI Routes
@app.get("/")
def index(request: Request):
    # stock_filter = request.query_params.get('filter', False)
    # print(stock_filter)
    stocks = getAllStocks()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": stocks})

# STOCKS
@app.get("/getAllStocks/{limit}")
async def index(limit = 10, filter = ''):
    # print(filter)
    stocks = getAllStocks(limit, filter)
    return stocks

@app.get("/getStockDetails/{symbol}")
def index(request: Request, symbol):
    stock = getStockDetails(symbol)
    return stock

# CRYPTOS
@app.get("/getAllCryptos/{limit}")
def index(request: Request, limit):
    cryptos = getAllCryptos(limit)
    return cryptos

@app.get("/getCryptoDetails/{symbol}")
def index(request: Request, symbol):
    symbol = symbol.replace("-", "/")
    cryptos = getCryptoDetails(symbol)
    return cryptos

@app.get("/getAllCoins/{limit}")
def index(request: Request, limit):
    coins = getAllCoins(limit)
    return coins

@app.get("/getCryptoCoin/{symbol}")
def index(request: Request, symbol):
    coin = getCryptoCoin(symbol)
    return coin

@app.get("/getAllCryptoExchanges/{limit}")
def index(request: Request, limit):
    exchanges = getAllCryptoExchanges(limit)
    return exchanges

@app.get("/getCryptoExchangeDetails/{exchange_id}")
def index(request: Request, exchange_id):
    exchange = getCryptoExchangeDetails(exchange_id)
    return exchange

# FOREX
@app.get("/getAllForex/{limit}")
def index(request: Request, limit):
    pairs = getAllForex(limit)
    return pairs

@app.get("/getForexDetails/{pair}")
def index(request: Request, pair):
    pair = getForexDetails(pair)
    return pair

# STRATEGIES
@app.get("/getAllStrategies")
def index(request: Request):
    strategies = getAllStrategies()
    return strategies

@app.get("/getStrategyDetails/{strategyCode}")
def index(request: Request, strategyCode):
    strategy = getStrategyDetails(strategyCode)
    return strategy