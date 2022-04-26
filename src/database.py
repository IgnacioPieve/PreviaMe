from motor import motor_asyncio
from pymongo import GEO2D

from config import db_string, db_name

client = motor_asyncio.AsyncIOMotorClient(db_string)
db = client[db_name]

# Add indexes to the database
db["party"].create_index([("geopoint", GEO2D)])  # GeoPoints
# db["party"].create_index([("name", "text")])    # Text search
