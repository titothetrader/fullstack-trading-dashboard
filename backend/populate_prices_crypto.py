import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
import requests
import pytz
import datetime

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.datetime.now() - datetime.timedelta(days=0)
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

# DEFINE GLOBAL VARS
symbols = []
crypto_dict = {}

# DB FUNCTIONS - get all symbols
sql = "SELECT DISTINCT * from crypto_trade ORDER BY symbol DESC"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    symbol = row['symbol']
    symbols.append(symbol)
    crypto_dict[symbol] = row['id']
# print(symbols)
    
def insertPrices(symbol, date, high, open, low, close, volume, vwap, alltime_high, alltime_low):
    crypto_id = crypto_dict[symbol]
    insert_stmt = "REPLACE INTO crypto_price (crypto_id, date, high, open, low, close, volume, vwap, alltime_high, alltime_low) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (crypto_id, date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
#######

# Connect to Alpaca API
def getCryptoBars(symbols, timeframe, next_page_token = None):
    symbolList = ""
    for element in symbols:
        symbolList += element + ","
    symbolList = symbolList.rstrip(symbolList[-1])
    # print(symbolList)
    params = {
        "symbols": symbolList,
        "timeframe": timeframe,
        "start": "2022-07-01",
        "end": today,
        "page_token": next_page_token,
    }
    if next_page_token == None:
        params.popitem()
    
    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_KEY"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET"),
    }
    alpaca_crypto_base = os.getenv("ALPACA_CRYPTO_URL") 
    alpaca_crypto_url = str(alpaca_crypto_base) + "/bars"
    response = requests.get(url = alpaca_crypto_url, headers = headers, params = params)
    cryptoAsset = response.json()
    # print(cryptoAsset)
    return cryptoAsset
    
    
# ITERATE BARS OF MANY CRYPTO DATA
def get_crypto_bars(symbols):
    timeframe = '1Day'
    barsData = {}
    cryptoBars = getCryptoBars(symbols,timeframe)
    barsData = cryptoBars["bars"]
    next_page_token = cryptoBars["next_page_token"]
    # print(next_page_token)
    while next_page_token != None:
        nextBars = getCryptoBars(symbols,timeframe, next_page_token)
        nextBarsData = nextBars["bars"]
        barsData.update(nextBarsData)
        next_page_token = nextBars["next_page_token"]     
        # print(next_page_token, type(next_page_token))
        # print("--------")
    
    # print(barsData)
    for keys in barsData:
        print(len(barsData[keys]))
        prevSymbol = ''
        alltime_high = 0
        alltime_low = 10000000000000
    
        for value in barsData[keys]:
            symbol = keys
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
                    print(f"{ct}: Processing bars for crypto {symbol} from {date} to {today}")  
                    # print(date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
                insertPrices(symbol, date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
    connection.commit()




# GET 200 SIZE CHUNKS OF STOCKS TO FETCH PRICES OF
chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    # print(i)
    # print(i+chunk_size)
    symbol_chunk = symbols[i:i+chunk_size]
    # print(symbol_chunk)
    get_crypto_bars(symbol_chunk)