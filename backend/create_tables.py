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
    sqlTableStock = "CREATE TABLE IF NOT EXISTS stock (id int NOT NULL AUTO_INCREMENT, symbol varchar(255) NOT NULL, name varchar(255) NOT NULL, exchange varchar(255) NOT NULL, category varchar(255) NOT NULL, status varchar(255) NOT NULL, tradable varchar(255) NOT NULL, marginable varchar(255) NOT NULL, maintenance_margin_requirement varchar(255) NOT NULL, shortable varchar(255) NOT NULL, easy_to_borrow varchar(255) NOT NULL, fractionable varchar(255) NOT NULL, logo_url varchar(255), company_url varchar(255), asset_type varchar(255) NOT NULL, description varchar(1064), cik varchar(255), currency varchar(255), country varchar(255), sector varchar(255), industry varchar(255), address varchar(255), fiscal_year_end varchar(255), latest_quarter date, market_cap float, ebitda float, pe_ratio float, peg_ratio float, book_value float, dividend_per_share float, dividend_yield float, eps float, revenue_per_share_ttm float, profit_margin float, operating_margin_ttm float, return_on_assets_ttm float, return_on_equity_ttm float, revenue_ttm float, gross_profit_ttm float, diluted_eps_ttm float, q_earnings_growth_yoy float, q_revenue_growth_yoy float, analyst_target_price float, trailing_pe float, forward_pe float, price_to_sale_ratio_ttm float, price_to_book_ratio float, ev_to_revenue float, ev_to_ebitda float, beta float, year_week_high float, year_week_low float, fifty_ma float, two_hun_ma float, shares_outstanding float, dividend_date date, ex_dividend_date date, PRIMARY KEY (id), UNIQUE KEY symbol (symbol))"
    print("Creating table: stock")
    cursor.execute(sqlTableStock)
    connection.commit()
    
    sqlTableStockPrices = "CREATE TABLE IF NOT EXISTS stock_price (id int NOT NULL AUTO_INCREMENT, stock_id int, date date NOT NULL, open float NOT NULL, high float NOT NULL, low float NOT NULL, close float NOT NULL, volume float NOT NULL, vwap float NOT NULL, alltime_high float NOT NULL, alltime_low float NOT NULL, PRIMARY KEY (id), KEY stock_id_idx (stock_id))"
    print("Creating table: stock_price")
    cursor.execute(sqlTableStockPrices)
    connection.commit()
    
    sqlTableCryptoTrade = "CREATE TABLE IF NOT EXISTS crypto_trade (id int NOT NULL AUTO_INCREMENT, symbol varchar(255) NOT NULL, symbol_a varchar(255) NOT NULL, symbol_b varchar(255) NOT NULL, name varchar(255) NOT NULL, exchange varchar(255) NOT NULL, category varchar(255) NOT NULL, status varchar(255) NOT NULL, tradable varchar(255) NOT NULL, marginable varchar(255) NOT NULL, maintenance_margin_requirement varchar(255) NOT NULL, shortable varchar(255) NOT NULL, easy_to_borrow varchar(255) NOT NULL, fractionable varchar(255) NOT NULL, PRIMARY KEY (id), UNIQUE KEY symbol (symbol))"
    print("Creating table: crypto_trade")
    cursor.execute(sqlTableCryptoTrade)
    connection.commit()
    
    sqlTableCryptoPrices = "CREATE TABLE IF NOT EXISTS crypto_price (id int NOT NULL AUTO_INCREMENT, crypto_id int, date date NOT NULL, open float NOT NULL, high float NOT NULL, low float NOT NULL, close float NOT NULL, volume float NOT NULL, vwap float NOT NULL, alltime_high float NOT NULL, alltime_low float NOT NULL, PRIMARY KEY (id), KEY crypto_id_idx (crypto_id))"
    print("Creating table: crypto_price")
    cursor.execute(sqlTableCryptoPrices)
    connection.commit()
    
    sqlTableCryptoCoins = "CREATE TABLE IF NOT EXISTS crypto_coin (id int NOT NULL AUTO_INCREMENT, coingecko_id varchar(255) NOT NULL, symbol varchar(255) NOT NULL, name varchar(255) NOT NULL, asset_platform_id varchar(255), block_time_in_minutes float, hashing_algorithm varchar(255), categories varchar(255), description varchar(1064), homepage_url varchar(255), thumb_url Varchar(510), small_url Varchar(510), large_url Varchar(510), country_origin varchar(255), genesis_date date, sentiment_votes_up_percentage float, sentiment_votes_down_percentage float, market_cap_rank float, coingecko_rank float, coingecko_score float, developer_score float, community_score float, liquidity_score float, public_interest_score float, alltime_high float, alltime_high_date date, alltime_low float, alltime_low_date date, market_cap float, fully_diluted_valuation float, total_volume float, high_24h float, low_24h float, price_change_24h float, price_change_percentage_1h float, price_change_percentage_24h float, price_change_percentage_7d float, price_change_percentage_14d float, price_change_percentage_30d float, price_change_percentage_60d float, price_change_percentage_200d float, price_change_percentage_1y float, market_cap_change_24h float, market_cap_change_percentage_24h float, total_supply float, max_supply float, circulating_supply float, alexa_rank float, last_updated date, PRIMARY KEY (id), UNIQUE KEY coingecko_id (coingecko_id))"
    print("Creating table: crypto_coin")
    cursor.execute(sqlTableCryptoCoins)
    connection.commit()
    
    sqlTableExchanges = "CREATE TABLE IF NOT EXISTS crypto_exchange (id int NOT NULL AUTO_INCREMENT, coingecko_id varchar(255) NOT NULL, name varchar(255) NOT NULL, year_established varchar(255) NOT NULL, country varchar(255) NOT NULL, description varchar(1064), exchange_url varchar(255) NOT NULL, image_url varchar(255) NOT NULL, has_trading_incentive varchar(255) NOT NULL, trust_score float, trust_score_rank float, trade_volume_24h_btc float, trade_volume_24h_btc_normalized float, PRIMARY KEY (id), UNIQUE KEY coingecko_id (coingecko_id))"
    print("Creating table: crypto_exchanges")
    cursor.execute(sqlTableExchanges)
    connection.commit()
    
    sqlTableForex = "CREATE TABLE IF NOT EXISTS forex (id int NOT NULL AUTO_INCREMENT, forex_pair varchar(255) NOT NULL, pair_type varchar(255) NOT NULL, description varchar(1064), pairs_correlate varchar(255), pair_a varchar(255), pair_b varchar(255), country_a varchar(255), country_b varchar(255), currency_a varchar(255), currency_b varchar(255), currency_nickname_a varchar(255), currency_nickname_b varchar(255), central_bank_a varchar(255), central_bank_b varchar(255), flag_a varchar(510), flag_b varchar(510), PRIMARY KEY (id), UNIQUE KEY forex_pair (forex_pair))"
    print("Creating table: forex")
    cursor.execute(sqlTableForex)
    connection.commit()
    
    sqlTableForexPrices = "CREATE TABLE IF NOT EXISTS forex_price (id int NOT NULL AUTO_INCREMENT, forex_id int, date date NOT NULL, open float NOT NULL, high float NOT NULL, low float NOT NULL, close float NOT NULL, volume float NOT NULL, vwap float NOT NULL, alltime_high float NOT NULL, alltime_low float NOT NULL, PRIMARY KEY (id), KEY forex_id (forex_id))"
    print("Creating table: forex_price")
    cursor.execute(sqlTableForexPrices)
    connection.commit()
    
    sqlTableStrategy = "CREATE TABLE IF NOT EXISTS strategy (id int NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, strategy_code varchar(255) NOT NULL, description varchar(255), direction varchar(255), type varchar(255), time_horizon varchar(255), image_url varchar(255), trigger varchar(255), take_profit varchar(255), stop_loss varchar(255), PRIMARY KEY (id), UNIQUE KEY strategy_code (strategy_code))"
    print("Creating table: strategy")
    cursor.execute(sqlTableStrategy)
    connection.commit()
    
    sqlTableUseStrategy = "CREATE TABLE IF NOT EXISTS use_strategy (id int NOT NULL AUTO_INCREMENT, symbol_id varchar(255) NOT NULL, strategy_id varchar(255) NOT NULL, PRIMARY KEY (id), UNIQUE KEY symbol_id (symbol_id), UNIQUE KEY strategy_id (strategy_id))"
    print("Creating table: use_strategy")
    cursor.execute(sqlTableUseStrategy)
    connection.commit()
    
    
createTables()