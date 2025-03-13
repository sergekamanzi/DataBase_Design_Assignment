# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import Base
from sqlalchemy.dialects.mysql import VARCHAR

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    job = Column(String(100))
    marital = Column(String(50))
    education = Column(String(100))
    default = Column(String(50))
    balance = Column(Float)
    housing = Column(String(50))
    loan = Column(String(50))

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    contact_type = Column(String(100))
    day = Column(Integer)
    month = Column(String(50))
    duration = Column(Integer)
    campaign = Column(Integer)
    pdays = Column(Integer)
    previous = Column(Integer)
    poutcome = Column(String(100))
    client = relationship("Client", back_populates="contacts")

class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    deposit = Column(String(50))
    client = relationship("Client", back_populates="deposits")

class BalanceLog(Base):
    __tablename__ = "balance_logs"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    old_balance = Column(Float)
    new_balance = Column(Float)
    change_time = Column(String(50))
    client = relationship("Client", back_populates="balance_logs")

Client.contacts = relationship("Contact", back_populates="client")
Client.deposits = relationship("Deposit", back_populates="client")
Client.balance_logs = relationship("BalanceLog", back_populates="client")
