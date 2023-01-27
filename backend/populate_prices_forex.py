import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import datetime
import pytz
import requests

# Load dotEnv
load_dotenv()

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.datetime.now() - datetime.timedelta(days=1)
today = today.strftime("%Y-%m-%d")
# print(today)

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

# DEFINE GLOBAL VARS
pairs = []
forex_dict = {}

# DB FUNCTIONS - get all symbols
# sql = "SELECT DISTINCT * from stock ORDER BY symbol DESC"
sql = "SELECT DISTINCT forex_pair, id FROM forex WHERE id NOT IN (select distinct forex_id from forex_price) ORDER BY forex_pair ASC"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    pair = row['forex_pair']
    pairs.append(pair)
    forex_dict[pair] = row['id']
# print(pairs)

def insertForexPrices(pair, date, high, open, low, close, volume, vwap, alltime_high, alltime_low):
    forex_id = forex_dict[pair]
    insert_stmt = "REPLACE INTO forex_price (forex_id, date, high, open, low, close, volume, vwap, alltime_high, alltime_low) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (forex_id, date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
#######
    
# ITERATE BARS OF MANY FOREX DATA
# Connect to Oanda API
def getOandaInfo(symbol):
    params = {
        # "count": 10,
        "granularity": 'D',
        "from": "2022-07-01",
        "to": {today}
    }
    headers = {
        "Authorization": os.getenv("OANDA_KEY")
    }
    oanda_base = os.getenv("OANDA_BASE_URL") 
    oanda_url = str(oanda_base) + "/v3/instruments/"+symbol+"/candles"
    response = requests.get(url = oanda_url, headers = headers, params = params)
    oandaAsset = response.json()
    # print(oandaAsset)
    
    pair = symbol
    
    # print(oandaAsset["candles"][0]["mid"])
    alltime_high = 0
    alltime_low = 10000000000000
    for bar in oandaAsset["candles"]:
        # print(bar["time"])
        date = datetime.datetime.strptime(bar["time"], "%Y-%m-%dT%H:%M:%S.000000000Z").replace(tzinfo=pytz.UTC)
        high = float(bar["mid"]["h"])
        open = float(bar["mid"]["o"])
        low = float(bar["mid"]["l"])
        close = float(bar["mid"]["c"])
        volume = float(bar["volume"])
        vwap = ((high + low + close) / 3) / volume
        alltime_high = close if close > alltime_high else alltime_high
        alltime_low = close if close < alltime_low else alltime_low
        
        if pair in pairs:
            insertForexPrices(pair, date, high, open, low, close, volume, vwap, alltime_high, alltime_low)
    print(f"{ct}: Processing bars for forex {pair} from {date} to {today}")
            
    
oanda_pairs = os.getenv("OANDA_PAIRS")
oanda_pairs = oanda_pairs.split(',')
for pair in oanda_pairs:
    print(pair)
    getOandaInfo(pair)