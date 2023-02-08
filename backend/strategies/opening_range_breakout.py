import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
# from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
# from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
# from alpaca.data.timeframe import TimeFrame
# from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
import requests
import pytz
import math
import datetime

# Load dotEnv
load_dotenv()

# GLOBAL VARS
# ct stores current time
market_timezone = pytz.timezone('America/New_York')
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# today = datetime.datetime.now() - datetime.timedelta(days=16) 
today = datetime.datetime.now()
start_date = datetime.datetime(today.year, today.month, today.day, 9)
start_date = market_timezone.localize(start_date).isoformat()
end_date = market_timezone.localize(today - datetime.timedelta(minutes=15)).isoformat()
# today = today.strftime("%Y-%m-%d")
today = today.strftime("%Y-%m-%d")
# print(today)
# print(start_date)
# print(end_date)


date_format = "%Y-%m-%d %H:%M:%S"
start_minute_bar = datetime.datetime.strptime(f"{today} 09:30:00", date_format).isoformat()
end_minute_bar = datetime.datetime.strptime(f"{today} 09:45:00", date_format).isoformat()

# end_minute_bar = f"{today} 09:45:00+00:00"
# now_aware = unaware.replace(tzinfo=pytz.UTC)
# print(start_minute_bar)
# print(end_minute_bar)



strategy_id = ''
alpacaStocks = []
alpacaCrypto = []
oandaForex = []


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

stock_api = tradeapi.REST(os.getenv("ALPACA_KEY"), os.getenv("ALPACA_SECRET"), os.getenv("ALPACA_BASE_URL"))

# crypto_client = CryptoHistoricalDataClient()
# stock_client = StockHistoricalDataClient(os.getenv("ALPACA_KEY"),  os.getenv("ALPACA_SECRET"))



def getStrategyId():
    sql = "SELECT id FROM strategy WHERE strategy_code = 'opening_range_breakout'"
    cursor.execute(sql)
    records = cursor.fetchone()
    strategy_id = records["id"]
    # print(strategy_id)
    return strategy_id

def getStrategySymbols():
    strategy_id = getStrategyId()
    sql = f"SELECT * FROM apply_strategy WHERE strategy_id = '{strategy_id}'"
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(records)
    for record in records:
        # print(record["asset_type"])
        if record["asset_type"] == "stock":
            alpacaStocks.append(record["symbol"])
        elif record["asset_type"] == "crypto":
            alpacaCrypto.append(record["symbol"])
        elif record["asset_type"] == "forex":
            oandaForex.append(record["symbol"])
            
    
getStrategySymbols()

print(alpacaStocks)
print(alpacaCrypto)
print(oandaForex)


# STOCKS
def getStockOpeningRange(symbols):
    bar_iter = stock_api.get_bars_iter(symbols, tradeapi.TimeFrame.Minute, start_date, end_date, adjustment='raw')
    # print(bar_iter)
    
    prevSymbol = ''
    opening_high = 0
    opening_low = 10000000000000
    opening_range_bars = []
    after_opening_range_bars = []
    after_opening_range_breakout = []
    limit_price = 0
    is_breakout = False
    
    for bar in (bar_iter):
        # print(bar)
        # print(bar.S, symbol)
        for attr, value in bar.__dict__.items():
            # print(value)
            symbol = value["S"]
            date = value["t"]
            high = value["h"]
            open = value["o"]
            low = value["l"]
            close = value["c"]
            volume = value["v"]
            vwap = value["vw"]
            opening_high = value["c"] if value["c"] > opening_high else opening_high
            opening_low = value["c"] if value["c"] < opening_low else opening_low
            opening_range = opening_high - opening_low
            
            bar = {
                    "date": date,
                    "high": high,
                    "open": open,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "vwap": vwap,
                    "opening_high": opening_high,
                    "opening_low": opening_low,
                    "opening_range": opening_range
                    }
            
            if symbol in symbols:
                if symbol != prevSymbol:
                        prevSymbol = symbol
                        # print(opening_high, opening_low, opening_range)
                        # print(f"{ct}: Processing bars for stock {symbol} from {date} to {today}")
                        opening_range_bars = []
                        after_opening_range_breakout = []
                        opening_high = close
                        opening_low = close
                        limit_price = close
                        opening_range = 0
                        is_breakout = False
                        
                if (date >= start_minute_bar) & (date < end_minute_bar):
                    print(symbol, date)
                    opening_range_bars.append(bar)
                    # print(opening_range_bars)
                elif (date >= end_minute_bar):
                    # print(symbol, date, close, opening_high, round(close, 1) > round(opening_high, 2))
                    after_opening_range_bars.append(bar)
                    # if math.isclose(close, opening_high, abs_tol=9):
                    if round(close, 1) > round(opening_high, 2) and not is_breakout:
                        print('Breakout: ', symbol, date, close, opening_high)
                        after_opening_range_breakout.append(bar)
                        is_breakout = True
                
                if after_opening_range_breakout:
                    limit_price = after_opening_range_breakout[0]["close"]
                
    if is_breakout:
        print(limit_price)
        # print(opening_high, opening_low, opening_range)
                    

# CRYPTO
def getCryptoBars(symbols, timeframe, next_page_token = None):
    symbolList = ""
    for element in symbols:
        symbolList += element + ","
    symbolList = symbolList.rstrip(symbolList[-1])
    # print(symbolList)
    params = {
        "symbols": symbolList,
        "timeframe": timeframe,
        "start": start_date,
        "end": end_date,
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
def getCryptoOpeningRange(symbols):
    # GET 200 SIZE CHUNKS OF STOCKS TO FETCH PRICES OF
    chunk_size = 200
    for i in range(0, len(symbols), chunk_size):
        # print(i)
        # print(i+chunk_size)
        symbol_chunk = symbols[i:i+chunk_size]
        # print(symbol_chunk)
        timeframe = '1Min'
        barsData = {}
        cryptoBars = getCryptoBars(symbol_chunk,timeframe)
        # print(cryptoBars)
        barsData = cryptoBars["bars"]
        next_page_token = cryptoBars["next_page_token"]
        # print(next_page_token)
        while next_page_token != None:
            nextBars = getCryptoBars(symbol_chunk,timeframe, next_page_token)
            nextBarsData = nextBars["bars"]
            barsData.update(nextBarsData)
            next_page_token = nextBars["next_page_token"]     
            # print(next_page_token, type(next_page_token))
            # print("--------")
        
        # print(barsData)
        for keys in barsData:
            # print(len(barsData[keys]))
            prevSymbol = ''
            alltime_high = 0
            alltime_low = 10000000000000
        
            for value in barsData[keys]:
                symbol = keys
                # print(value["t"])
                date = value["t"]
                high = value["h"]
                open = value["o"]
                low = value["l"]
                close = value["c"]
                volume = value["v"]
                vwap = value["vw"]
                alltime_high = value["c"] if value["c"] > alltime_high else alltime_high
                alltime_low = value["c"] if value["c"] < alltime_low else alltime_low
                
                if symbol in symbol_chunk:
                    if symbol != prevSymbol:
                        prevSymbol = symbol
                        print(f"{ct}: Processing bars for crypto {symbol} from {start_date} to {end_date}")  
                        # print(date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
    


    

# FOREX

getStockOpeningRange(alpacaStocks)
getCryptoOpeningRange(alpacaCrypto)
# getForexOpeningRange(oandaForex)