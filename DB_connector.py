CURRENT_DATABASE_NAME = "TestDatabase" # name of current database

import mysql.connector # MySQL fro python
import cryptography # encode and decode data for databases
import json # databases info

avaible_databases = {} # list of avaible databases

with open("databases.json", "r") as _avaible_databases:
    avaible_databases = json.loads(_avaible_databases.read()) # loading daatabases info
    _avaible_databases.close()
    del _avaible_databases

HOST = avaible_databases[CURRENT_DATABASE_NAME]["Host"] # Database info
USER = avaible_databases[CURRENT_DATABASE_NAME]["User"]
PASSWORD = avaible_databases[CURRENT_DATABASE_NAME]["Password"]
DATABASE = avaible_databases[CURRENT_DATABASE_NAME]["Database"]


database = mysql.connector.connect( # connecting to database
  host=HOST,
  user=USER,
  passwd=PASSWORD,
  database=DATABASE
)

data = database.cursor() # get database data

acc_id = "acc_id"
acc_name = "acc_name"
acc_username = "acc_usrname"
acc_showRealName = "acc_showRealName"
acc_balance = "acc_balance"


'''DONT CHANGE THIS FILE'''