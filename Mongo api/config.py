from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://willykalisa:Sandra*2020@cluster0.y9yqh.mongodb.net/"
DATABASE_NAME = "bank_db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
