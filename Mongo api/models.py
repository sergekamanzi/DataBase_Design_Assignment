from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

# Helper to handle MongoDB ObjectId
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class Client(BaseModel):
    id: Optional[PyObjectId] = None
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: float
    housing: str
    loan: str

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


class Contact(BaseModel):
    id: Optional[PyObjectId] = None
    client_id: PyObjectId
    contact_type: str
    day: int
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str

    class Config:
        orm_mode = True


class Deposit(BaseModel):
    id: Optional[PyObjectId] = None
    client_id: PyObjectId
    deposit: str

    class Config:
        orm_mode = True


class BalanceLog(BaseModel):
    id: Optional[PyObjectId] = None
    client_id: PyObjectId
    old_balance: float
    new_balance: float
    change_time: str

    class Config:
        orm_mode = True


