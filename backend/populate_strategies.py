import os
import csv
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi
import requests
import datetime

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.datetime.now() - datetime.timedelta(days=1)
today = today.strftime("%Y-%m-%d")
# print(today)

# Load dotEnv
load_dotenv()

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
    
# DB Functions
def insertStrategy(name, strategy_code, description, direction, type, time_horizon, image_url, trigger, take_profit, stop_loss):
    insert_stmt = "REPLACE INTO strategy (name, strategy_code, description, direction, type, time_horizon, image_url, trigger, take_profit, stop_loss) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (name, strategy_code, description, direction, type, time_horizon, image_url, trigger, take_profit, stop_loss)
    cursor.execute(insert_stmt, data)
    connection.commit()
#######
    

# Load Forex CSV file of OANDA pairs
with open('input_table_strategy.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            name = row[0]
            strategy_code = row[1]
            description = row[2]
            direction = row[3]
            type = row[4]
            time_horizon = row[5]
            image_url = row[6]
            trigger = row[7]
            take_profit = row[8]
            stop_loss = row[9]
            print(name, direction, type, time_horizon)
            insertStrategy(name, strategy_code, description, direction, type, time_horizon, image_url, trigger, take_profit, stop_loss)

    print(f'Processed {line_count} lines.')