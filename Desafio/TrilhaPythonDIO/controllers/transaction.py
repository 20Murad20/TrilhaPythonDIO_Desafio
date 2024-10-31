from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update

from ..database import database
from ..models import accounts, transactions
from ..schemas import TransactionCreate, TransactionResponse

router = APIRouter()


@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate):
    query = select([accounts]).where(accounts.c.id == transaction.account_id)
    account = await database.fetch_one(query)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if transaction.type == "withdraw" and account["balance"] < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    balance = account["balance"] + transaction.amount if transaction.type == "deposit" else account["balance"] - transaction.amount

    transaction_query = transactions.insert().values(
        account_id=transaction.account_id,
        amount=transaction.amount,
        type=transaction.type,
    )
    await database.execute(transaction_query)

    update_query = update(accounts).where(accounts.c.id == transaction.account_id).values(balance=balance)
    await database.execute(update_query)

    return {**transaction.dict(), "created_at": "now"}
