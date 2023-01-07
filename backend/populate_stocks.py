import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
import datetime
import requests
# import asyncio


# ct stores current time
ct = datetime.datetime.now()

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
existingSymbols = []

# DB FUNCTIONS    
sql = "SELECT * from stock"
cursor.execute(sql)
records = cursor.fetchall()
existingSymbols = [row['symbol'] for row in records]

        
def insertStock(symbol, name, exchange, status, tradable):
    insert_stmt = "INSERT IGNORE INTO stock (symbol, name, exchange, status, tradable) VALUES (%s, %s, %s, %s, %s)"
    data = (symbol, name, exchange, status, tradable)
    # print(symbol, name, exchange, status, tradable)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
    
#########

# POPULATE DB WITH ALL ACTIVE SYMBOLS (STOCK & CRYPTO)
def populate_DB():
    for asset in alpacaAssets:
        try:
            if asset.status == 'active' and asset.tradable == True and asset.symbol not in existingSymbols:
                insertStock(asset.symbol, asset.name, asset.exchange, asset.status, asset.tradable)
                print(f"{ct}: Added new {asset.exchange} stock: {asset.symbol} - {asset.name}")
        except Exception as e:
            print(asset.symbol)
            print(e)


populate_DB()
