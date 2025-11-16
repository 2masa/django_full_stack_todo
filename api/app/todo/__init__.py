

from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.auth import EdgedbClientWithGlobals
from app.todo.controller import create_todo, delete_todos, get_all, update_todo
from app.todo.models import TodoCreate, TodoUpdate

router = APIRouter(
    prefix="/todo",
    tags=["Todo"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create(input:TodoCreate,client:EdgedbClientWithGlobals):
    try:
        return await create_todo(
            input=input,
            client=client,
        )
    except Exception as e:
        return HTTPException(
            status_code=409,
            detail=str(e),
        )


@router.patch("/")
async def update(input:TodoUpdate, client:EdgedbClientWithGlobals):
    try:
        return await update_todo(input=input,client=client)
    except Exception as e:
        return HTTPException(
            status_code=409,
            detail=e,
        )

@router.get("/")
async def get(client:EdgedbClientWithGlobals):
    try:
        return await get_all(
            client=client
        )
    except Exception as e:
        return HTTPException(
            status_code=409,
            detail=str(e),
        )

@router.get("/id")
async def get_by_id(client:EdgedbClientWithGlobals):
    try:
        pass
    except Exception as e:
        return HTTPException(
            status_code=409,
            detail=e,
        )

@router.delete("/")
async def delete(ids:list[UUID],client:EdgedbClientWithGlobals):
    try:
        return await delete_todos(ids=ids,client=client)
    except Exception as e:
        return HTTPException(
            status_code=409,
            detail=e,
        )
