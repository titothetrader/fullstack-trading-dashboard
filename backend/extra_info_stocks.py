import os
from dotenv import load_dotenv
import requests
from mysql.connector import Error
import mysql.connector
import datetime


# ct stores current time
ct = datetime.datetime.now()

# load dotEnv
load_dotenv()

# DEFINE GLOBAL VARS
existingSymbols = []
stockData = {
    "Description": '',
    "Currency": '',
    "Country": '',
    "logo_url": '',
    "company_url": '',
    "Sector": '',
    "Industry": '',
    "MarketCapitalization": 0,
    "DividendPerShare": 0,
    "DividendYield": 0,
    "DividendDate": "",
    "EPS": 0,
    "Beta": 0,
    "PERatio": 0,
    "RevenueTTM": 0,
    "GrossProfitTTM": 0,
    "52WeekHigh": 0,
    "52WeekLow": 0,
    "50DayMovingAverage": 0,
    "200DayMovingAverage": 0,
}

avLabels = ['Description', 'Currency', 'Country', 'Sector', 'Industry', 'MarketCapitalization', 'PERatio', 'DividendPerShare', 'DividendYield', 'EPS', 'RevenueTTM', 'GrossProfitTTM', 'Beta', '52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage', 'DividendDate' ]

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
    
# DB FUNCTIONS - get existing stocks in DB

# Get all symbols in stock alphabetically
# sql = "SELECT * from stock ORDER BY symbol"

# Get unique symbols that have price joined by stock id
sql = "select distinct symbol from stock_price JOIN stock on stock_price.stock_id = stock.id;"
cursor.execute(sql)
records = cursor.fetchall()
existingSymbols = [row['symbol'] for row in records]
# print(existingSymbols)

# def updateStock(symbol, description, currency, country, logo_url, company_url, sector, industry, market_cap, dividend_share, dividend_yield, dividend_date, eps, beta, pe_ratio, revenue_ttm, gross_profit_ttm, year_week_high, year_week_low, fifty_ma, two_hun_ma):
def updateStock(symbol, description, currency, country, logo_url, company_url, sector, industry, market_cap, dividend_share, dividend_yield, dividend_date, eps, beta, pe_ratio, revenue_ttm, gross_profit_ttm, year_week_high, year_week_low, fifty_ma, two_hun_ma):
    insert_stmt = "UPDATE IGNORE stock SET description = %s, currency = %s, country = %s, logo_url = %s, company_url = %s, sector = %s, industry = %s, market_cap = %s, dividend_share = %s, dividend_yield = %s, dividend_date = %s, eps = %s, beta = %s, pe_ratio = %s, revenue_ttm = %s, gross_profit_ttm = %s, year_week_high = %s, year_week_low = %s, fifty_ma = %s, two_hun_ma = %s WHERE symbol = %s"
        
    data = (description, currency, country, logo_url, company_url, sector, industry, market_cap, dividend_share, dividend_yield, dividend_date, eps, beta, pe_ratio, revenue_ttm, gross_profit_ttm, year_week_high, year_week_low, fifty_ma, two_hun_ma, symbol)
    
    # data = (description, currency, country, logo_url, company_url, sector, industry, market_cap, dividend_share, dividend_yield, dividend_date, eps, beta, pe_ratio, revenue_ttm, gross_profit_ttm, year_week_high, year_week_low, fifty_ma, two_hun_ma)
    
    # print(description, currency, country, logo_url, company_url, sector, industry, market_cap, dividend_share, dividend_yield, dividend_date, eps, beta, pe_ratio, revenue_ttm, gross_profit_ttm, year_week_high, year_week_low, fifty_ma, two_hun_ma)
    cursor.execute(insert_stmt, data)
    print(str(ct)+": " + symbol + " details updated! (i.e. " + sector + ")")
    connection.commit()
    
    
    

# Connect to Alpha Vantage API
def getAlphaVantageInfo(symbol):
    params = {
        "apikey": os.getenv("AV_API_KEY"),
        "symbol": {symbol},
    }
    av_url = os.getenv("AV_OVERVIEW_URL")
    response = requests.get(url = av_url, params = params)
    avAsset = response.json()
    # print(avAsset.keys())
    d_avAsset = avAsset.items()
    val_avAsset = avAsset.values()
    # print(val_avAsset)
    for key in avAsset:
        # print(key, '->', avAsset[key])
        if key in avLabels:
            # print(key)
            stockData[key] = avAsset[key]
               
    updateStock(symbol, stockData["Description"],  stockData["Currency"], stockData["Country"], 'image_url', 'company_url', stockData["Sector"], stockData["Industry"], stockData["MarketCapitalization"], stockData["DividendPerShare"], stockData["DividendYield"], stockData["DividendDate"], stockData["EPS"], stockData["Beta"], stockData["PERatio"], stockData["RevenueTTM"], stockData["GrossProfitTTM"], stockData["52WeekHigh"], stockData["52WeekLow"], stockData["50DayMovingAverage"], stockData["200DayMovingAverage"])
    
    return stockData


# Go through Symbols in DB and update info
# Alpha Vantage API only allows 5 calls a min, 500 a day
uniqueExistingSymbols = set(existingSymbols)
for symbol in uniqueExistingSymbols:
    # print(symbol)
    getAlphaVantageInfo(symbol)
