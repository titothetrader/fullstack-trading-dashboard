import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector

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
    
### DATABASE FUNCTIONS
def emptyTable(db_table):
    empty_db = "TRUNCATE TABLE " + str(db_table)
    cursor.execute(empty_db)

# EMPTY DATABASE
table = os.getenv('TABLE_TO_EMPTY')
emptyTable(table)