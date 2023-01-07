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
    sqlTableStock = "CREATE TABLE IF NOT EXISTS stock (id int NOT NULL AUTO_INCREMENT, symbol varchar(255) NOT NULL, name varchar(255) NOT NULL, description varchar(1064) NOT NULL, status varchar(255) NOT NULL, tradable varchar(255) NOT NULL, exchange varchar(255) NOT NULL, currency varchar(255), country varchar(255), logo_url varchar(255), company_url varchar(255), sector varchar(255), industry varchar(255), market_cap float, dividend_share float, dividend_yield float, dividend_date varchar(255), eps float, beta float, pe_ratio float, revenue_ttm float, gross_profit_ttm float, year_week_high float, year_week_low float, fifty_ma float, two_hun_ma float, PRIMARY KEY (id), UNIQUE KEY symbol (symbol))"
    print("Creating table: stock")
    cursor.execute(sqlTableStock)
    connection.commit()
    
    sqlTablePrices = "CREATE TABLE IF NOT EXISTS stock_price (id int NOT NULL AUTO_INCREMENT, stock_id int, date date NOT NULL, open float NOT NULL, high float NOT NULL, low float NOT NULL, close float NOT NULL, volume float NOT NULL, alltime_high float NOT NULL, alltime_low float NOT NULL, m_avgerage float NOT NULL, PRIMARY KEY (id), KEY stock_id_idx (stock_id))"
    print("Creating table: stock_price")
    cursor.execute(sqlTablePrices)
    connection.commit()
    
    # sqlTableCrypto = "CREATE TABLE IF NOT EXISTS crypto (id int NOT NULL AUTO_INCREMENT, symbol varchar(255) NOT NULL, name varchar(255) NOT NULL, description varchar(255) NOT NULL, exchange varchar(255) NOT NULL, currency varchar(255) NOT NULL, country varchar(255) NOT NULL, logo_url varchar(255) NOT NULL, category varchar(255) NOT NULL, sector varchar(255) NOT NULL, industry varchar(255) NOT NULL, market_cap varchar(255) NOT NULL, dividend_share varchar(255) NOT NULL, dividend_yield varchar(255) NOT NULL, dividend_rate varchar(255) NOT NULL, eps varchar(255) NOT NULL, beta varchar(255) NOT NULL, pe_ratio varchar(255) NOT NULL, year_week_high varchar(255) NOT NULL, year_week_low varchar(255) NOT NULL, PRIMARY KEY (id), UNIQUE KEY symbol (symbol))"
    # print("Creating table: stock")
    # cursor.execute(sqlTableStock)
    # connection.commit()
    
createTables()