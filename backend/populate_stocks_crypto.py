import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
import datetime
import requests
# import asyncio


# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# load dotEnv
load_dotenv()

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

# Connect to Alpaca Markets API
HEADERS = {'APCA-API-KEY-ID': os.getenv("ALPACA_KEY"),
           'APCA-API-SECRET-KEY': os.getenv("ALPACA_SECRET")}

api = tradeapi.REST(os.getenv("ALPACA_KEY"), os.getenv("ALPACA_SECRET"), os.getenv("ALPACA_BASE_URL"))

alpacaAssets = api.list_assets()

# DEFINE GLOBAL VARS
existingStocks = []
existingCryptos = []


# DB FUNCTIONS
sql = "SELECT DISTINCT * from stock ORDER BY symbol DESC"
cursor.execute(sql)
records = cursor.fetchall()
existingStocks = [row['symbol'] for row in records]

sql = "SELECT DISTINCT * from crypto_trade ORDER BY symbol DESC"
cursor.execute(sql)
records = cursor.fetchall()
existingCryptos = [row['symbol'] for row in records]

        
def insertStock(symbol, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable):
    insert_stmt = "INSERT IGNORE INTO stock (symbol, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (symbol, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable)
    # print(symbol, name, exchange, status, tradable)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
def insertCrypto(symbol, symbol_a, symbol_b, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable):
    insert_stmt = "INSERT IGNORE INTO crypto_trade (symbol, symbol_a, symbol_b, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (symbol, symbol_a, symbol_b, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable)
    # print(symbol, name, exchange, status, tradable)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
    
#########

# POPULATE DB WITH ALL ACTIVE SYMBOLS (STOCK & CRYPTO)
def populate_DB():
    # print(alpacaAssets[0])
    for asset in alpacaAssets:
        try:
            # print(asset)
            for attr, value in asset.__dict__.items():
                # print(value["class"])
                
                symbol = value["symbol"]
                
                symbolSplit = symbol.split('/')
                if len(symbolSplit) > 1:
                    symbol_a = symbolSplit[0]
                    symbol_b = symbolSplit[1]
                    
                name = value["name"]
                exchange = value["exchange"]
                category = value["class"]
                status = value["status"]
                tradable = value["tradable"]
                marginable = value["marginable"]
                maintenance_margin_requirement = value["maintenance_margin_requirement"]
                shortable = value["shortable"]
                easy_to_borrow = value["easy_to_borrow"]
                fractionable = value["fractionable"]
                
                # Add STOCKS to corresponding table
                if value["class"] == 'us_equity' and value["status"] == 'active' and value["tradable"] == True and value["symbol"] not in existingStocks:
                    insertStock(symbol, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable)
                    print(f"{ct}: {category} - Added new symbol: {symbol}")
                    
                # Add CRYPTO to corresponding table
                if value["class"] == 'crypto' and value["status"] == 'active' and value["tradable"] == True and value["symbol"] not in existingCryptos:
                    insertCrypto(symbol, symbol_a, symbol_b, name, exchange, category, status, tradable, marginable, maintenance_margin_requirement, shortable, easy_to_borrow, fractionable)
                    print(f"{ct}: {category} - Added new symbol: {symbol}")
        except Exception as e:
            print(alpacaAssets["symbol"])
            print(e)

populate_DB()
