# routes.py
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from crud import create_client, get_client, get_clients, update_client, delete_client
from config import SessionLocal

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

# Pydantic Models
class ContactResponse(BaseModel):
    id: int
    client_id: int
    contact_type: str
    day: int
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str

    model_config = {
        "from_attributes": True
    }

class DepositResponse(BaseModel):
    id: int
    client_id: int
    deposit: bool

    model_config = {
        "from_attributes": True
    }

class BalanceLogResponse(BaseModel):
    id: int
    client_id: int
    old_balance: int
    new_balance: int
    change_time: str

    model_config = {
        "from_attributes": True
    }

class ClientBase(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: bool
    balance: int
    housing: bool
    loan: bool

class ClientResponse(BaseModel):
    id: int
    age: int
    job: str
    marital: str
    education: str
    default: bool
    balance: int
    housing: bool
    loan: bool

    model_config = {
        "from_attributes": True
    }

class ClientDetailResponse(BaseModel):
    client: ClientResponse
    contact: ContactResponse
    deposit: DepositResponse
    balance_logs: List[BalanceLogResponse]

class ClientCreate(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: bool
    balance: int
    housing: bool
    loan: bool
    contact: str
    day: int
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str
    deposit: bool

class ClientUpdate(BaseModel):
    age: Optional[int] = None
    job: Optional[str] = None
    marital: Optional[str] = None
    education: Optional[str] = None
    default: Optional[bool] = None
    balance: Optional[int] = None
    housing: Optional[bool] = None
    loan: Optional[bool] = None
    contact: Optional[str] = None
    day: Optional[int] = None
    month: Optional[str] = None
    duration: Optional[int] = None
    campaign: Optional[int] = None
    pdays: Optional[int] = None
    previous: Optional[int] = None
    poutcome: Optional[str] = None
    deposit: Optional[bool] = None

# Routes
@router.post("/clients/", response_model=ClientDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_client_route(client_data: ClientCreate, db: Session = Depends(get_db)):
    try:
        db_client = create_client(db, client_data.dict())
        return get_client(db, db_client.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/clients/", response_model=List[ClientResponse])
async def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = get_clients(db, skip=skip, limit=limit)
    if not clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No clients found")
    return clients

@router.get("/clients/{client_id}", response_model=ClientDetailResponse)
async def read_client(client_id: int, db: Session = Depends(get_db)):
    client_data = get_client(db, client_id)
    if not client_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client_data

@router.put("/clients/{client_id}", response_model=ClientDetailResponse)
async def update_client_route(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db)
):
    updated_client = update_client(db, client_id, client_data.dict(exclude_unset=True))
    if not updated_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return updated_client

@router.delete("/clients/{client_id}", response_model=ClientDetailResponse)
async def delete_client_route(client_id: int, db: Session = Depends(get_db)):
    deleted_client = delete_client(db, client_id)
    if not deleted_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return deleted_client