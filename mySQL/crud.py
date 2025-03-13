
from typing import Dict, Any
from sqlalchemy.orm import Session
from models import Client, Contact, Deposit, BalanceLog
from datetime import datetime


def create_client(db: Session, client_data: dict):
    # Create client instance and add to the database
    db_client = Client(
        age=client_data["age"],
        job=client_data["job"],
        marital=client_data["marital"],
        education=client_data["education"],
        default=client_data["default"],
        balance=client_data["balance"],
        housing=client_data["housing"],
        loan=client_data["loan"]
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    # Create Contact instance
    db_contact = Contact(
        client_id=db_client.id,
        contact_type=client_data["contact"],
        day=client_data["day"],
        month=client_data["month"],
        duration=client_data["duration"],
        campaign=client_data["campaign"],
        pdays=client_data["pdays"],
        previous=client_data["previous"],
        poutcome=client_data["poutcome"]
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    # Create Deposit instance
    db_deposit = Deposit(
        client_id=db_client.id,
        deposit=client_data["deposit"]
    )
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    
    # Create BalanceLog instance 
    db_balance_log = BalanceLog(
        client_id=db_client.id,
        old_balance=client_data["balance"],
        new_balance=client_data["balance"],
        change_time=str(datetime.now())
    )
    db.add(db_balance_log)
    db.commit()
    db.refresh(db_balance_log)

    return db_client


def get_clients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Client).offset(skip).limit(limit).all()

# Existing create_client and get_clients functions remain unchanged

def get_client(db: Session, client_id: int) -> Dict[str, Any]:
    """Get a single client with all related information"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None

    contact = db.query(Contact).filter(Contact.client_id == client_id).first()
    deposit = db.query(Deposit).filter(Deposit.client_id == client_id).first()
    balance_logs = db.query(BalanceLog).filter(BalanceLog.client_id == client_id).all()

    return {
        "client": client,
        "contact": contact,
        "deposit": deposit,
        "balance_logs": balance_logs
    }

def update_client(db: Session, client_id: int, client_data: dict) -> Dict[str, Any]:
    """Update client and related information"""
    # Get existing records
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        return None

    # Track balance changes
    old_balance = db_client.balance
    balance_changed = False

    # Update Client
    client_fields = ["age", "job", "marital", "education", "default", "balance", "housing", "loan"]
    for field in client_fields:
        if field in client_data:
            if field == "balance" and client_data[field] != old_balance:
                balance_changed = True
            setattr(db_client, field, client_data[field])
    db.commit()
    db.refresh(db_client)

    # Update Contact
    contact_fields = {
        "contact": "contact_type",
        "day": "day",
        "month": "month",
        "duration": "duration",
        "campaign": "campaign",
        "pdays": "pdays",
        "previous": "previous",
        "poutcome": "poutcome"
    }
    db_contact = db.query(Contact).filter(Contact.client_id == client_id).first()
    if db_contact:
        for data_field, model_field in contact_fields.items():
            if data_field in client_data:
                setattr(db_contact, model_field, client_data[data_field])
        db.commit()
        db.refresh(db_contact)

    # Update Deposit
    db_deposit = db.query(Deposit).filter(Deposit.client_id == client_id).first()
    if db_deposit and "deposit" in client_data:
        db_deposit.deposit = client_data["deposit"]
        db.commit()
        db.refresh(db_deposit)

    # Create new BalanceLog if balance changed
    if balance_changed:
        new_balance = client_data.get("balance", old_balance)
        db_balance_log = BalanceLog(
            client_id=client_id,
            old_balance=old_balance,
            new_balance=new_balance,
            change_time=str(datetime.now())
        )
        db.add(db_balance_log)
        db.commit()
        db.refresh(db_balance_log)

    return get_client(db, client_id)

def delete_client(db: Session, client_id: int) -> Dict[str, Any]:
    """Delete a client and all related information"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None

    # Store data for return before deletion
    result = get_client(db, client_id)

    # Delete related records
    db.query(Contact).filter(Contact.client_id == client_id).delete()
    db.query(Deposit).filter(Deposit.client_id == client_id).delete()
    db.query(BalanceLog).filter(BalanceLog.client_id == client_id).delete()
    
    # Delete client
    db.delete(client)
    db.commit()

    return result

# Existing get_clients function
def get_clients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Client).offset(skip).limit(limit).all()