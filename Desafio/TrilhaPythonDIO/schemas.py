from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class TransactionBase(BaseModel):
    account_id: int
    amount: float = Field(gt=0, description="Amount must be positive")


class TransactionCreate(TransactionBase):
    type: str


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime


class AccountCreate(BaseModel):
    user_id: int


class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    transactions: List[TransactionResponse] = []
