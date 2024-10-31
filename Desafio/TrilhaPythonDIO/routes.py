from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models, auth
from .database import SessionLocal, init_db



router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.username == account.username).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(account.password)
    db_account = models.Account(username=account.username, hashed_password=hashed_password)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.post("/token")
def login(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Account).filter(models.Account.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    # Token validation and account fetching logic goes here
    # Perform deposit or withdrawal logic
    pass

@router.get("/accounts/{account_id}/transactions/", response_model=List[schemas.Transaction])
def get_transactions(account_id: int, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    # Fetch transactions for the account
    pass

init_db()
