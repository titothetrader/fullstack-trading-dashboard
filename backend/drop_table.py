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
    empty_db = "DROP TABLE IF EXISTS " + str(db_table)
    print("Dropping table: " + str(db_table))
    cursor.execute(empty_db)
    connection.commit()

# EMPTY DATABASE
table = input("Provide table to drop: ")
emptyTable(table)