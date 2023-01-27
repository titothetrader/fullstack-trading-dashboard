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
import pytz
import math
import datetime

# Load dotEnv
load_dotenv()

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.datetime.now() - datetime.timedelta(days=16) 
# today = datetime.datetime.now()
# today = today.strftime("%Y-%m-%d")
today = today.strftime("%Y-%m-%d")
print(today)

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


# GLOBAL VARS
strategy_id = ''
alpacaStocks = []
alpacaCrypto = []
oandaForex = []
limit_price = 0

date_format = "%Y-%m-%d %H:%M:%S"
start_minute_bar = datetime.datetime.strptime(f"{today} 09:30:00", date_format).replace(tzinfo=pytz.UTC)
end_minute_bar = datetime.datetime.strptime(f"{today} 09:45:00", date_format).replace(tzinfo=pytz.UTC)

# end_minute_bar = f"{today} 09:45:00+00:00"
# now_aware = unaware.replace(tzinfo=pytz.UTC)
print(start_minute_bar)
print(end_minute_bar)


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

def getStockOpeningRange(symbols):
    bar_iter = stock_api.get_bars_iter(symbols, tradeapi.TimeFrame.Minute, today, adjustment='raw')
    # print(bar_iter)
    
    prevSymbol = ''
    opening_high = 0
    opening_low = 10000000000000
    opening_range_bars = []
    after_opening_range_bars = []
    after_opening_range_breakout = []
    
    for bar in (bar_iter):
        # print(bar)
        # print(bar.S, symbol)
        for attr, value in bar.__dict__.items():
            # print(value)
            symbol = value["S"]
            # date = value["t"]
            date = datetime.datetime.strptime(value["t"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
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
                    "opening_low": opening_low
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
                        opening_range = 0
                        
                if (date >= start_minute_bar) & (date < end_minute_bar):
                    # print(symbol, date)
                    opening_range_bars.append(bar)
                    # print(opening_range_bars)
                elif (date >= end_minute_bar):
                    # print(symbol, date, close, opening_high, math.isclose(close + .1, opening_high))
                    after_opening_range_bars.append(bar)
                    # if math.isclose(close, opening_high, abs_tol=9):
                    if round(close, 1) > round(opening_high, 2):
                        print('Breakout: ', symbol, date, close, opening_high)
                        after_opening_range_breakout.append(bar)
                
                if after_opening_range_breakout:
                    limit_price = after_opening_range_breakout[0]["close"]
                    print(limit_price)
                
    
        # print(opening_high, opening_low, opening_range)
                    
        
    

getStockOpeningRange(alpacaStocks)
# getCryptoOpeningRange(alpacaCrypto)
# getForexOpeningRange(oandaForex)