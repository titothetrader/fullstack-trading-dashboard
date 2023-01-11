import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import datetime
import requests

# Load dotEnv
load_dotenv()

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Connect to Oanda API
def getOandaInfo(symbol):
    params = {
        "count": 10,
        "granularity": 'H1',
    }
    headers = {
        "Authorization": os.getenv("OANDA_KEY")
    }
    oanda_base = os.getenv("OANDA_BASE_URL") 
    oanda_url = str(oanda_base) + "/v3/instruments/"+symbol+"/candles"
    response = requests.get(url = oanda_url, headers = headers, params = params)
    oandaAsset = response.json()
    print(oandaAsset)
    
oanda_pairs = os.getenv("OANDA_PAIRS")
oanda_pairs = oanda_pairs.split(',')
for pair in oanda_pairs:
    print(pair)
    getOandaInfo(pair)