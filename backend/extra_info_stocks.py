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
"AssetType": '',
"Description": '',
"CIK": '',
"Currency": '',
"Country": '',
"Sector": '',
"Industry": '',
"Address": '',
"FiscalYearEnd": '',
"LatestQuarter": '',
"MarketCapitalization": '',
"EBITDA": 0,
"PERatio": 0,
"PEGRatio": 0,
"BookValue": 0,
"DividendPerShare": 0,
"DividendYield": 0,
"EPS": 0,
"RevenuePerShareTTM": 0,
"ProfitMargin": 0,
"OperatingMarginTTM": 0,
"ReturnOnAssetsTTM": 0,
"ReturnOnEquityTTM": 0,
"RevenueTTM": 0,
"GrossProfitTTM": 0,
"DilutedEPSTTM": 0,
"QuarterlyEarningsGrowthYOY": 0,
"QuarterlyRevenueGrowthYOY": 0,
"AnalystTargetPrice": 0,
"TrailingPE": 0,
"ForwardPE": 0,
"PriceToSalesRatioTTM": 0,
"PriceToBookRatio": 0,
"EVToRevenue": 0,
"EVToEBITDA": 0,
"Beta": 0,
"52WeekHigh": 0,
"52WeekLow": 0,
"50DayMovingAverage": 0,
"200DayMovingAverage": 0,
"SharesOutstanding": 0,
"DividendDate": '',
"ExDividendDate": '',

}

avLabels = ["AssetType", "Description", "CIK", "Currency", "Country", "Sector", "Industry", "Address", "FiscalYearEnd", "LatestQuarter", "MarketCapitalization", "EBITDA", "PERatio", "PEGRatio", "BookValue", "DividendPerShare", "DividendYield", "EPS", "RevenuePerShareTTM", "ProfitMargin", "OperatingMarginTTM", "ReturnOnAssetsTTM", "ReturnOnEquityTTM", "RevenueTTM", "GrossProfitTTM", "DilutedEPSTTM", "QuarterlyEarningsGrowthYOY", "QuarterlyRevenueGrowthYOY", "AnalystTargetPrice", "TrailingPE", "ForwardPE", "PriceToSalesRatioTTM", "PriceToBookRatio", "EVToRevenue", "EVToEBITDA", "Beta", "52WeekHigh", "52WeekLow", "50DayMovingAverage", "200DayMovingAverage", "SharesOutstanding", "DividendDate", "ExDividendDate"]

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
# sql = "SELECT * from stock ORDER BY symbol DESC"

# Get unique symbols that have price joined by stock id
sql = "SELECT DISTINCT symbol, stock.id FROM stock_price JOIN stock ON stock_price.stock_id = stock.id WHERE stock.description = ''"

cursor.execute(sql)
records = cursor.fetchall()
existingSymbols = [row['symbol'] for row in records]
# print(existingSymbols)

def updateStock(symbol, asset_type, description, cik, currency, country, sector, industry, address, fiscal_year_end, latest_quarter, market_cap, ebitda, pe_ratio, peg_ratio, book_value, dividend_per_share, dividend_yield, eps, revenue_per_share_ttm, profit_margin, operating_margin_ttm, return_on_assets_ttm, return_on_equity_ttm, revenue_ttm, gross_profit_ttm, diluted_eps_ttm, q_earnings_growth_yoy, q_revenue_growth_yoy, analyst_target_price, trailing_pe, forward_pe, price_to_sale_ratio_ttm, price_to_book_ratio, ev_to_revenue, ev_to_ebitda, beta, year_week_high, year_week_low, fifty_ma, two_hun_ma, shares_outstanding, dividend_date, ex_dividend_date):
    insert_stmt = "UPDATE IGNORE stock SET asset_type = %s, description = %s, cik = %s, currency = %s, country = %s, sector = %s, industry = %s, address = %s, fiscal_year_end = %s, latest_quarter = %s, market_cap = %s, ebitda = %s, pe_ratio = %s, peg_ratio = %s, book_value = %s, dividend_per_share = %s, dividend_yield = %s, eps = %s, revenue_per_share_ttm = %s, profit_margin = %s, operating_margin_ttm = %s, return_on_assets_ttm = %s, return_on_equity_ttm = %s, revenue_ttm = %s, gross_profit_ttm = %s, diluted_eps_ttm = %s, q_earnings_growth_yoy = %s, q_revenue_growth_yoy = %s, analyst_target_price = %s, trailing_pe = %s, forward_pe = %s, price_to_sale_ratio_ttm = %s, price_to_book_ratio = %s, ev_to_revenue = %s, ev_to_ebitda = %s, beta = %s, year_week_high = %s, year_week_low = %s, fifty_ma = %s, two_hun_ma = %s, shares_outstanding = %s, dividend_date = %s, ex_dividend_date = %s WHERE symbol = %s"
        
    data = (asset_type, description, cik, currency, country, sector, industry, address, fiscal_year_end, latest_quarter, market_cap, ebitda, pe_ratio, peg_ratio, book_value, dividend_per_share, dividend_yield, eps, revenue_per_share_ttm, profit_margin, operating_margin_ttm, return_on_assets_ttm, return_on_equity_ttm, revenue_ttm, gross_profit_ttm, diluted_eps_ttm, q_earnings_growth_yoy, q_revenue_growth_yoy, analyst_target_price, trailing_pe, forward_pe, price_to_sale_ratio_ttm, price_to_book_ratio, ev_to_revenue, ev_to_ebitda, beta, year_week_high, year_week_low, fifty_ma, two_hun_ma, shares_outstanding, dividend_date, ex_dividend_date, symbol)
    

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
               
    updateStock(symbol, stockData["AssetType"], stockData["Description"], stockData["CIK"], stockData["Currency"], stockData["Country"], stockData["Sector"], stockData["Industry"], stockData["Address"], stockData["FiscalYearEnd"], stockData["LatestQuarter"], stockData["MarketCapitalization"], stockData["EBITDA"], stockData["PERatio"], stockData["PEGRatio"], stockData["BookValue"], stockData["DividendPerShare"], stockData["DividendYield"], stockData["EPS"], stockData["RevenuePerShareTTM"], stockData["ProfitMargin"], stockData["OperatingMarginTTM"], stockData["ReturnOnAssetsTTM"], stockData["ReturnOnEquityTTM"], stockData["RevenueTTM"], stockData["GrossProfitTTM"], stockData["DilutedEPSTTM"], stockData["QuarterlyEarningsGrowthYOY"], stockData["QuarterlyRevenueGrowthYOY"], stockData["AnalystTargetPrice"], stockData["TrailingPE"], stockData["ForwardPE"], stockData["PriceToSalesRatioTTM"], stockData["PriceToBookRatio"], stockData["EVToRevenue"], stockData["EVToEBITDA"], stockData["Beta"], stockData["52WeekHigh"], stockData["52WeekLow"], stockData["50DayMovingAverage"], stockData["200DayMovingAverage"], stockData["SharesOutstanding"], stockData["DividendDate"], stockData["ExDividendDate"])
    
    return stockData


# Go through Symbols in DB and update info
# Alpha Vantage API only allows 5 calls a min, 500 a day
uniqueExistingSymbols = set(existingSymbols)
for symbol in uniqueExistingSymbols:
    # print(symbol)
    getAlphaVantageInfo(symbol)
