
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://willykalisa:Sandra*2020@cluster0.y9yqh.mongodb.net/"
# MongoDB connection
DB_NAME = "bank_db"
COLLECTION_NAME = "predictions"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
