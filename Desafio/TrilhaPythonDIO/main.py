from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from controllers import account, transaction
from database import database
from security import JWTBearer
from exceptions import AccountNotFoundError, BusinessError

app = FastAPI(title="Bank API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router, prefix="/accounts", tags=["accounts"])
app.include_router(transaction.router, prefix="/transactions", tags=["transactions"], dependencies=[Depends(JWTBearer())])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.exception_handler(AccountNotFoundError)
async def account_not_found_exception_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Account not found"})

@app.exception_handler(BusinessError)
async def business_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
