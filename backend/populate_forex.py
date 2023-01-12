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
ssl_ca=os.getenv("SSL_CERT")
)
try:
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
except Error as e:
    print("Error while connecting to MySQL", e)
    
# DB Functions
def insertForex(forex_pair, pair_type, description, pairs_correlate, pair_a, pair_b, country_a, country_b, currency_a, currency_b, currency_nickname_a, currency_nickname_b, central_bank_a, central_bank_b, flag_a, flag_b):
    insert_stmt = "INSERT IGNORE INTO forex (forex_pair, pair_type, description, pairs_correlate, pair_a, pair_b, country_a, country_b, currency_a, currency_b, currency_nickname_a, currency_nickname_b, central_bank_a, central_bank_b, flag_a, flag_b) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (forex_pair, pair_type, description, pairs_correlate, pair_a, pair_b, country_a, country_b, currency_a, currency_b, currency_nickname_a, currency_nickname_b, central_bank_a, central_bank_b, flag_a, flag_b)
    cursor.execute(insert_stmt, data)
    connection.commit()
    
#######
    

# Load Forex CSV file of OANDA pairs
with open('input_table_forex.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            forex_pair = row[0]
            pair_type = row[1]
            description = row[2]
            pairs_correlate = row[3]
            pair_a = row[4]
            pair_b = row[5]
            country_a = row[6]
            country_b = row[7]
            currency_a = row[8]
            currency_b = row[9]
            currency_nickname_a = row[10]
            currency_nickname_b = row[11]
            central_bank_a = row[12]
            central_bank_b = row[13]
            flag_a = row[14]
            flag_b = row[15]
            print(forex_pair, currency_nickname_a, currency_nickname_b)
            insertForex(forex_pair, pair_type, description, pairs_correlate, pair_a, pair_b, country_a, country_b, currency_a, currency_b, currency_nickname_a, currency_nickname_b, central_bank_a, central_bank_b, flag_a, flag_b)

    print(f'Processed {line_count} lines.')
    
    