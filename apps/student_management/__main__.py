from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('connection_string')
print(CONNECTION_STRING)
DB_NAME = os.getenv('db_name')

client = MongoClient(CONNECTION_STRING)
dbname = client[DB_NAME]

# CRUD

collection_name = dbname["students"]

student1 = {
    "Name": "Rodrigo",
    "Surname": "Lima",
    "Note 1": "8",
    "Note 2": "6"
}

collection_name.insert_one(student1)