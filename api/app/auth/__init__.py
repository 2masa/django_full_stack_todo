from app.db import EdgedbClient
from app.auth.controller import authenticate_user, get_db_client_with_globals
from fastapi import Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from edgedb import AsyncIOClient

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404:{"description":"Not found"}}
)
EdgedbClientWithGlobals = Annotated[AsyncIOClient, Depends(get_db_client_with_globals)]


@router.post("/login")
async def login_for_access_token(client: EdgedbClient,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    try:
        return await authenticate_user(client=client,email=form_data.username,password=form_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )