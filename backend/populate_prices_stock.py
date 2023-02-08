import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import pytz
import datetime

# ct stores current time
market_timezone = pytz.timezone('America/New_York')
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# today = datetime.datetime.now() - datetime.timedelta(days=0)
today = datetime.datetime.now() - datetime.timedelta(days=1)
today = today.strftime("%Y-%m-%d")
# print(today)

# Load dotEnv
load_dotenv()

# Connect to PlanetScale DB
connection = mysql.connector.connect(
host=os.getenv("HOST"),
database=os.getenv("DATABASE"),
user=os.getenv("DB_USER"),
password=os.getenv("PASSWORD"),
ssl_ca=os.getenv("SSL_CERT"),
autocommit=True
)
try:
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
except Error as e:
    print("Error while connecting to MySQL", e)

# Connect to Alpaca Markets API
HEADERS = {'APCA-API-KEY-ID': os.getenv("ALPACA_KEY"),
           'APCA-API-SECRET-KEY': os.getenv("ALPACA_SECRET")}

api = tradeapi.REST(os.getenv("ALPACA_KEY"), os.getenv("ALPACA_SECRET"), os.getenv("ALPACA_BASE_URL"))

stock_client = StockHistoricalDataClient(os.getenv("ALPACA_KEY"),  os.getenv("ALPACA_SECRET"))


# DEFINE GLOBAL VARS
symbols = []
stock_dict = {}

# DB FUNCTIONS - get all symbols
sql = "SELECT DISTINCT * from stock ORDER BY symbol ASC"

# USE BELOW FOR EXISTING STOCKS BUT ARE MISSING PRICES
# sql = "SELECT DISTINCT symbol, id FROM stock WHERE id NOT IN (select distinct stock_id from stock_price) ORDER BY symbol DESC"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']
# print(symbols)
    
def insertPrices(symbol, date, high, open, low, close, volume, vwap, alltime_high, alltime_low):
    stock_id = stock_dict[symbol]
    insert_stmt = "REPLACE INTO stock_price (stock_id, date, high, open, low, close, volume, vwap, alltime_high, alltime_low) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (stock_id, date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
#######
    
# ITERATE BARS OF MANY STOCK DATA
def get_stocks_bars(symbols):
    request_params = StockBarsRequest(
                        symbol_or_symbols=symbols,
                        timeframe=TimeFrame.Day,
                        start=datetime.datetime.strptime("2022-07-01", '%Y-%m-%d'),
                 )

    bars = stock_client.get_stock_bars(request_params)
    # print(bars)
    
    bar_iter = api.get_bars_iter(symbols, tradeapi.TimeFrame.Day, "2022-07-01", today, adjustment='raw')
    prevSymbol = ''
    alltime_high = 0
    alltime_low = 10000000000000
    for bar in (bar_iter):
        # print(bar)
        # print(bar.S, symbol)
        for attr, value in bar.__dict__.items():
            # print(value)
            symbol = value["S"]
            date = datetime.datetime.strptime(value["t"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
            high = value["h"]
            open = value["o"]
            low = value["l"]
            close = value["c"]
            volume = value["v"]
            vwap = value["vw"]
            alltime_high = value["c"] if value["c"] > alltime_high else alltime_high
            alltime_low = value["c"] if value["c"] < alltime_low else alltime_low
            
            if symbol in symbols:
                if symbol != prevSymbol:
                    prevSymbol = symbol
                    print(f"{ct}: Processing bars for stock {symbol} from {date} to {today}")  
                insertPrices(symbol, date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
    connection.commit()


# GET 200 SIZE CHUNKS OF STOCKS TO FETCH PRICES OF
chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    # print(i)
    # print(i+chunk_size)
    symbol_chunk = symbols[i:i+chunk_size]
    # print(symbol_chunk)
    get_stocks_bars(symbol_chunk)