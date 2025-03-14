from config import db
from bson import ObjectId
from datetime import datetime

# Helper function to convert ObjectId to string
def serialize_document(document):
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    return document

# CREATE: Insert a new client with related data
async def create_client_with_details(data: dict):
    client_data = {
        "age": data["age"],
        "job": data["job"],
        "marital": data["marital"],
        "education": data["education"],
        "default": data["default"],
        "balance": data["balance"],
        "housing": data["housing"],
        "loan": data["loan"]
    }
    client_result = await db.clients.insert_one(client_data)
    client_id = str(client_result.inserted_id)

    contact_data = {
        "client_id": client_id,
        "contact_type": data["contact"],
        "day": data["day"],
        "month": data["month"],
        "duration": data["duration"],
        "campaign": data["campaign"],
        "pdays": data["pdays"],
        "previous": data["previous"],
        "poutcome": data["poutcome"]
    }
    await db.contacts.insert_one(contact_data)

    deposit_data = {
        "client_id": client_id,
        "deposit": data["deposit"]
    }
    await db.deposits.insert_one(deposit_data)

    balance_log = {
        "client_id": client_id,
        "old_balance": 0,
        "new_balance": data["balance"],
        "change_time": datetime.utcnow()
    }
    await db.balance_logs.insert_one(balance_log)

    return {"message": "Client and related data inserted successfully", "client_id": client_id}

# READ: Retrieve a client with all related data
async def get_client_details(client_id: str):
    client = await db.clients.find_one({"_id": ObjectId(client_id)})
    contact = await db.contacts.find_one({"client_id": client_id})
    deposit = await db.deposits.find_one({"client_id": client_id})
    balance_logs = await db.balance_logs.find({"client_id": client_id}).to_list(100)

    if not client:
        return None

    return {
        "client": serialize_document(client),
        "contact": serialize_document(contact),
        "deposit": serialize_document(deposit),
        "balance_logs": [serialize_document(log) for log in balance_logs]
    }

# UPDATE: Modify client and related data
async def update_client(client_id: str, update_data: dict):
    client = await db.clients.find_one({"_id": ObjectId(client_id)})
    if not client:
        return None

    # Update client data
    await db.clients.update_one({"_id": ObjectId(client_id)}, {"$set": update_data})

    # If balance is updated, log the change
    if "balance" in update_data:
        balance_log = {
            "client_id": client_id,
            "old_balance": client["balance"],
            "new_balance": update_data["balance"],
            "change_time": datetime.utcnow()
        }
        await db.balance_logs.insert_one(balance_log)

    # Update related data if included in the update request
    if "contact" in update_data:
        await db.contacts.update_one({"client_id": client_id}, {"$set": update_data["contact"]})
    
    if "deposit" in update_data:
        await db.deposits.update_one({"client_id": client_id}, {"$set": {"deposit": update_data["deposit"]}})

    return {"message": "Client and related data updated successfully"}

# DELETE: Remove client and all related data
async def delete_client(client_id: str):
    client = await db.clients.find_one({"_id": ObjectId(client_id)})
    if not client:
        return None

    await db.clients.delete_one({"_id": ObjectId(client_id)})
    await db.contacts.delete_one({"client_id": client_id})
    await db.deposits.delete_one({"client_id": client_id})
    await db.balance_logs.delete_many({"client_id": client_id})

    return {"message": "Client and related data deleted successfully"}



