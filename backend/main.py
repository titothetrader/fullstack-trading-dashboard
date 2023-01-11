import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

# Load dotEnv
load_dotenv()

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
def getAllStocks(limit = 100):
    sql = "SELECT DISTINCT stock.id, stock.symbol, stock.name from stock JOIN stock_price ON stock.id = stock_price.stock_id WHERE stock_price.close != '' LIMIT " + str(limit)
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
    sql = f"SELECT * FROM forex WHERE forex_pair = '{pair}'"
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(records)
    return records


# Load FastAPI Routes
@app.get("/")
def index(request: Request):
    stocks = getAllStocks()
    # return{"title": "Dashboard", "stocks": stocks}
    return templates.TemplateResponse("index.html", {"request": request, "stocks": stocks})

@app.get("/getAllStocks/{limit}")
def index(request: Request, limit):
    # print(dir(request))
    stocks = getAllStocks(limit)
    # return{"title": "Dashboard", "stocks": stocks}
    return stocks

@app.get("/getStockDetails/{symbol}")
def index(request: Request, symbol):
    stock = getStockDetails(symbol)
    return stock

@app.get("/getAllCryptos/{limit}")
def index(request: Request, limit):
    # print(dir(request))
    cryptos = getAllCryptos(limit)
    # return{"title": "Dashboard", "stocks": stocks}
    return cryptos

@app.get("/getCryptoDetails/{symbol}")
def index(request: Request, symbol):
    symbol = symbol.replace("-", "/")
    cryptos = getCryptoDetails(symbol)
    # print(cryptos)
    return cryptos

@app.get("/getAllCoins/{limit}")
def index(request: Request, limit):
    # print(dir(request))
    coins = getAllCoins(limit)
    # return{"title": "Dashboard", "stocks": stocks}
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
    # print(cryptos)
    return exchange

@app.get("/getAllForex/{limit}")
def index(request: Request, limit):
    pairs = getAllForex(limit)
    return pairs

@app.get("/getForexDetails/{pair}")
def index(request: Request, pair):
    pair = getForexDetails(pair)
    # print(cryptos)
    return pair