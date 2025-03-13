from pymongo import MongoClient
import pandas as pd

# Load dataset
file_path = "bank.csv"
df = pd.read_csv(file_path)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bank_db"]

# Insert Data into `clients` Collection
clients = []
for _, row in df.iterrows():
    client_data = {
        "age": row["age"],
        "job": row["job"],
        "marital": row["marital"],
        "education": row["education"],
        "default": row["default"],
        "balance": row["balance"],
        "housing": row["housing"],
        "loan": row["loan"]
    }
    inserted_client = db.clients.insert_one(client_data)
    client_id = inserted_client.inserted_id

    # Insert Data into `contacts` Collection
    contact_data = {
        "client_id": client_id,
        "contact_type": row["contact"],
        "day": row["day"],
        "month": row["month"],
        "duration": row["duration"],
        "campaign": row["campaign"],
        "pdays": row["pdays"],
        "previous": row["previous"],
        "poutcome": row["poutcome"]
    }
    db.contacts.insert_one(contact_data)

    # Insert Data into `deposits` Collection
    deposit_data = {
        "client_id": client_id,
        "deposit": row["deposit"]
    }
    db.deposits.insert_one(deposit_data)

    # Insert Data into `balance_logs` Collection
    balance_log = {
        "client_id": client_id,
        "old_balance": 0,
        "new_balance": row["balance"],
        "change_time": pd.Timestamp.now()
    }
    db.balance_logs.insert_one(balance_log)

print("Data successfully inserted into MongoDB!")
