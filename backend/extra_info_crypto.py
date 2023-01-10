import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import datetime
import requests

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

# DEFINE GLOBAL VARS
symbols = []
crypto_dict = {}

# DB FUNCTIONS - get all symbols
sql = "SELECT DISTINCT * from crypto_trade ORDER BY symbol ASC"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    symbol = row['symbol']
    symbols.append(symbol)
    crypto_dict[symbol] = row['id']
# print(symbols)

# Connect to Oanda API
def getCryptoInfo():
    params = {
        "count": 10,
        "granularity": 'H1',
    }
    cg_coins = os.getenv("CG_COINS_URL") 
    print(cg_coins)
    cg_coins_url = str(cg_coins) + "/list"
    response = requests.get(url = cg_coins_url, params = params)
    oandaAsset = response.json()
    print(oandaAsset[0])
    
getCryptoInfo()