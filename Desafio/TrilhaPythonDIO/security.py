import time
from typing import Annotated
from uuid import uuid4
import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    sub: int
    exp: float
    jti: str


def sign_jwt(user_id: int) -> str:
    now = time.time()
    payload = {
        "sub": user_id,
        "exp": now + (60 * 30),
        "jti": uuid4().hex,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def decode_jwt(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        token = await super().__call__(request)
        return await decode_jwt(token.credentials)
