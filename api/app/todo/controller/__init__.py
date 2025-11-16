from pathlib import Path
from uuid import UUID
from app.auth import EdgedbClientWithGlobals
from app.todo.models import TodoCreate, TodoUpdate
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).parent.resolve(), autoescape=False)


async def create_todo(input: TodoCreate, client: EdgedbClientWithGlobals):
    return await client.query_single(
        query=templates.get_template("create.edgeql").render(),
        title=input.title,
        status=input.status,
        priority=input.priority,
        description=input.description,
    )


async def update_todo(input: TodoUpdate, client: EdgedbClientWithGlobals):
    return await client.query_single(
        query=templates.get_template("update.edgeql").render(),
        title=input.title,
        status=input.status,
        priority=input.priority,
        description=input.description,
        id = input.id
    )



async def get_all(client: EdgedbClientWithGlobals):
    return await client.query(
        query=templates.get_template("get.edgeql").render()
    )

async def get_by_id(client: EdgedbClientWithGlobals):
    return await client.query(
        query=templates.get_template("get.edgeql").render(),
    )


async def delete_todos(ids:list[UUID],client: EdgedbClientWithGlobals):
    return await client.query(
        query=templates.get_template("delete.edgeql").render(),
        ids=ids
    )
