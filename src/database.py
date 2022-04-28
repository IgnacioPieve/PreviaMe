from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import GEO2D

from config import db_name, db_string


class Database:
    db_client: AsyncIOMotorClient = None

    @staticmethod
    async def get_db():
        return Database.db_client[db_name]

    @staticmethod
    async def connect_db():
        """Create database connection."""
        Database.db_client = AsyncIOMotorClient(db_string)
        db = Database.db_client[db_name]

        # Add indexes to the database
        db["party"].create_index([("geopoint", GEO2D)])  # GeoPoints
        db["log"].create_index([("date", 1)])  # Date
        # db["party"].create_index([("name", "text")])    # Text search

    @staticmethod
    async def close_db():
        """Close database connection."""
        Database.db_client.close()
