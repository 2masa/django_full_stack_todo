from datetime import datetime, timedelta, timezone
from edgedb import AsyncIOClient
from fastapi import Depends, HTTPException,status
import typing
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path
from app.db import EdgedbClient
from app.config import settings
from fastapi.templating import Jinja2Templates
from bcrypt import checkpw as check_password
from jose import jwt, JWTError
from typing import Annotated, Optional, cast

from app.auth.models import Auth, UserDetails

templates = Jinja2Templates(directory=Path(__file__).parent.resolve(), autoescape=False)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_details(token: str = Depends(oauth2_schema)) -> UserDetails:
    try:
        payload = jwt.decode(token,settings.jwt_security_key, algorithms=[settings.jwt_security_algorithm])
        return UserDetails(**payload)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

CurrentUserDetails = Annotated[UserDetails, Depends(get_current_user_details)]

async def get_db_client_with_globals(user_details:CurrentUserDetails,client:EdgedbClient) -> AsyncIOClient:
    return cast(
        AsyncIOClient ,
        client.with_globals(
            current_user_id= user_details.id
        )
    )


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    data["exp"] = expire

    encoded_jwt = jwt.encode(data,settings.jwt_security_key, algorithm=settings.jwt_security_algorithm)

    return encoded_jwt


def verify_password(plain_password: str, hash_password: bytes):
    return check_password(plain_password.encode(), hash_password)


async def authenticate_user(email: str, password: str, client: EdgedbClient):
    credential = await client.query_single(
        query=templates.get_template("authenticate_user.edgeql").render(), email=email
    )
    if credential is None:
        raise ValueError("Incorrect email or password.")

    if not verify_password(password, credential.password):
        raise ValueError("Incorrect email or password.")
    user_id = str(credential.user.id)
    access_token = create_jwt_token(
        data={
            "id": user_id,
            "name": credential.user.name,
            "email": credential.user.email,
        },
        expires_delta=timedelta(minutes=settings.jwt_refresh_token_timeout_minutes),
    )

    refresh_token = create_jwt_token(
        data={"id": user_id}, expires_delta=timedelta(minutes=settings.jwt_refresh_token_timeout_minutes)
    )

    return Auth(access_token=access_token, refresh_token=refresh_token)
