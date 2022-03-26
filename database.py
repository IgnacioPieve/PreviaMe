from pymongo import MongoClient
import config

client = MongoClient()
db = client[config.db_name]