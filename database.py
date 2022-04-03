from motor import motor_asyncio
from config import db_string, db_name

client = motor_asyncio.AsyncIOMotorClient(db_string)
db = client[db_name]