
import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
import requests
import datetime

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.datetime.now() - datetime.timedelta(days=1)
today = today.strftime("%Y-%m-%d")
# print(today)

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
    
# DB FUNCTIONS - get all symbols
sql = "SELECT DISTINCT * from crypto_trade ORDER BY symbol ASC"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    symbol = row['symbol']
    # symbols.append(symbol)
    # crypto_dict[symbol] = row['id']
# print(symbols)
    
def insertExchanges(coingecko_id, name, year_established, country, description, exchange_url, image_url, has_trading_incentive, trust_score, trust_score_rank, trade_volume_24h_btc, trade_volume_24h_btc_normalized):
    insert_stmt = "INSERT IGNORE INTO crypto_exchange (coingecko_id, name, year_established, country, description, exchange_url, image_url, has_trading_incentive, trust_score, trust_score_rank, trade_volume_24h_btc, trade_volume_24h_btc_normalized) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (coingecko_id, name, year_established, country, description, exchange_url, image_url, has_trading_incentive, trust_score, trust_score_rank, trade_volume_24h_btc, trade_volume_24h_btc_normalized)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
#######
    
# Connect to CoinGecko Exchanges
def getExchangesInfo():
    exchanges_url = os.getenv("CG_EXCHANGES_URL")
    response = requests.get(url = exchanges_url)
    exchangesAsset = response.json()
    # print(exchangesAsset[0])
    for exchange in exchangesAsset:
        coingecko_id = exchange["id"]
        name = exchange["name"]
        year_established = exchange["year_established"]
        country = exchange["country"]
        description = exchange["description"]
        exchange_url = exchange["url"]
        image_url = exchange["image"]
        has_trading_incentive = exchange["has_trading_incentive"]
        trust_score = exchange["trust_score"]
        trust_score_rank = exchange["trust_score_rank"]
        trade_volume_24h_btc = exchange["trade_volume_24h_btc"]
        trade_volume_24h_btc_normalized = exchange["trade_volume_24h_btc_normalized"]

        print(f"{ct}: Adding exchange {name}")  
        insertExchanges(coingecko_id, name, year_established, country, description, exchange_url, image_url, has_trading_incentive, trust_score, trust_score_rank, trade_volume_24h_btc, trade_volume_24h_btc_normalized)
        connection.commit()

getExchangesInfo()

