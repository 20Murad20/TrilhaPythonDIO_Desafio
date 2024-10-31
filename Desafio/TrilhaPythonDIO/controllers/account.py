from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import database
from ..models import accounts
from ..schemas import AccountCreate, AccountResponse

router = APIRouter()


@router.post("/accounts", response_model=AccountResponse)
async def create_account(account: AccountCreate):
    query = accounts.insert().values(user_id=account.user_id)
    account_id = await database.execute(query)
    return {**account.dict(), "id": account_id, "balance": 0}


@router.get("/accounts/{user_id}", response_model=AccountResponse)
async def get_account(user_id: int):
    query = select([accounts]).where(accounts.c.user_id == user_id)
    account = await database.fetch_one(query)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
