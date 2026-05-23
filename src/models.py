# models.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class DepositRequest(BaseModel):
    amount: float

class TransferRequest(BaseModel):
    target_user: str
    amount: float

class TransactionHistory(BaseModel):
    type: str
    amount: float
    sender: str
    receiver: str
    date: str

class Token(BaseModel):
    access_token: str
    token_type: str