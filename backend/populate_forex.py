import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import datetime
import requests

# load dotEnv
load_dotenv()

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
    
getOandaInfo("EUR_USD")