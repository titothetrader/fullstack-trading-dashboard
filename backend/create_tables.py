import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector

# Load dotEnv
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
    
# DB FUNCTIONS - create tables
def createTables():
    sqlTableStock = "CREATE TABLE IF NOT EXISTS stock (id int NOT NULL AUTO_INCREMENT, symbol varchar(255) NOT NULL, name varchar(255) NOT NULL, exchange varchar(255) NOT NULL, category varchar(255) NOT NULL, status varchar(255) NOT NULL, tradable varchar(255) NOT NULL, marginable varchar(255) NOT NULL, maintenance_margin_requirement varchar(255) NOT NULL, shortable varchar(255) NOT NULL, easy_to_borrow varchar(255) NOT NULL, fractionable varchar(255) NOT NULL, logo_url varchar(255), company_url varchar(255), asset_type varchar(255) NOT NULL, description Varchar(1064), cik varchar(255), currency varchar(255), country varchar(255), sector varchar(255), industry varchar(255), address varchar(255), fiscal_year_end varchar(255), latest_quarter date, market_cap float, ebitda float, pe_ratio float, peg_ratio float, book_value float, dividend_per_share float, dividend_yield float, eps float, revenue_per_share_ttm float, profit_margin float, operating_margin_ttm float, return_on_assets_ttm float, return_on_equity_ttm float, revenue_ttm float, gross_profit_ttm float, diluted_eps_ttm float, q_earnings_growth_yoy float, q_revenue_growth_yoy float, analyst_target_price float, trailing_pe float, forward_pe float, price_to_sale_ratio_ttm float, price_to_book_ratio float, ev_to_revenue float, ev_to_ebitda float, beta float, year_week_high float, year_week_low float, fifty_ma float, two_hun_ma float, shares_outstanding float, dividend_date date, ex_dividend_date date, PRIMARY KEY (id), UNIQUE KEY symbol (symbol))"
    print("Creating table: stock")
    cursor.execute(sqlTableStock)
    connection.commit()
    
    sqlTableStockPrices = "CREATE TABLE IF NOT EXISTS stock_price (id int NOT NULL AUTO_INCREMENT, stock_id int, date date NOT NULL, open float NOT NULL, high float NOT NULL, low float NOT NULL, close float NOT NULL, volume float NOT NULL, vwap float NOT NULL, alltime_high float NOT NULL, alltime_low float NOT NULL, PRIMARY KEY (id), KEY stock_id_idx (stock_id))"
    print("Creating table: stock_price")
    cursor.execute(sqlTableStockPrices)
    connection.commit()
    
    sqlTableCryptoTrade = "CREATE TABLE IF NOT EXISTS crypto_trade (id int NOT NULL AUTO_INCREMENT, symbol varchar(255) NOT NULL, name varchar(255) NOT NULL, exchange varchar(255) NOT NULL, category varchar(255) NOT NULL, status varchar(255) NOT NULL, tradable varchar(255) NOT NULL, marginable varchar(255) NOT NULL, maintenance_margin_requirement varchar(255) NOT NULL, shortable varchar(255) NOT NULL, easy_to_borrow varchar(255) NOT NULL, fractionable varchar(255) NOT NULL, PRIMARY KEY (id), UNIQUE KEY symbol (symbol))"
    print("Creating table: crypto_trade")
    cursor.execute(sqlTableCryptoTrade)
    connection.commit()
    
    sqlTableCryptoPrices = "CREATE TABLE IF NOT EXISTS crypto_price (id int NOT NULL AUTO_INCREMENT, crypto_id int, date date NOT NULL, open float NOT NULL, high float NOT NULL, low float NOT NULL, close float NOT NULL, volume float NOT NULL, vwap float NOT NULL, alltime_high float NOT NULL, alltime_low float NOT NULL, PRIMARY KEY (id), KEY crypto_id_idx (crypto_id))"
    print("Creating table: crypto_price")
    cursor.execute(sqlTableCryptoPrices)
    connection.commit()
    
    sqlTableExchanges = "CREATE TABLE IF NOT EXISTS crypto_exchange (id int NOT NULL AUTO_INCREMENT, coingecko_id varchar(255) NOT NULL, name varchar(255) NOT NULL, year_established varchar(255) NOT NULL, country varchar(255) NOT NULL, description Varchar(1064), exchange_url varchar(255) NOT NULL, image_url varchar(255) NOT NULL, has_trading_incentive varchar(255) NOT NULL, trust_score float, trust_score_rank float, trade_volume_24h_btc float, trade_volume_24h_btc_normalized float, PRIMARY KEY (id), UNIQUE KEY coingecko_id (coingecko_id))"
    print("Creating table: crypto_exchanges")
    cursor.execute(sqlTableExchanges)
    connection.commit()
    
createTables()