import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

# Load dotEnv
load_dotenv()

# Load App and Routes    
app = FastAPI()

# Load FastAPI CORS
origins = ['https://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000', '*:*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)
 
# Load Fast API Jinja templates
templates = Jinja2Templates(directory="./templates")

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

# GLOBAL VARS
symbols = []
stock_dict = dict()

# DB FUNCTIONS - get all symbols
def getAllStocks(limit = 100):
    sql = "SELECT * from stock LIMIT " + str(limit)
    cursor.execute(sql)
    records = cursor.fetchall()
    return records

def getStockDetails(symbol):
    sql_details = "SELECT * from stock WHERE symbol = '" + str(symbol) + "'"
    cursor.execute(sql_details)
    details = cursor.fetchall()
    sql_prices = "SELECT stock_price.id, symbol, name, date, high, open, low, close, volume from stock JOIN stock_price ON stock.id = stock_price.stock_id WHERE symbol = '" + str(symbol) + "' ORDER BY stock_price.date"
    cursor.execute(sql_prices)
    prices = cursor.fetchall()
    results = {
        "details": details,
        "prices": prices
    }
    return results


# Load FastAPI Routes
@app.get("/")
def index(request: Request):
    stocks = getAllStocks()
    # return{"title": "Dashboard", "stocks": stocks}
    return templates.TemplateResponse("index.html", {"request": request, "stocks": stocks})

@app.get("/getAllStocks/{limit}")
def index(request: Request, limit):
    # print(dir(request))
    stocks = getAllStocks(limit)
    # return{"title": "Dashboard", "stocks": stocks}
    return stocks

@app.get("/getStockDetails/{symbol}")
def index(request: Request, symbol):
    stock = getStockDetails(symbol)
    return stock
