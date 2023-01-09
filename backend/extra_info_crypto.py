import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import datetime
import requests

# load dotEnv
load_dotenv()

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
    print(oandaAsset)
    
getCryptoInfo()