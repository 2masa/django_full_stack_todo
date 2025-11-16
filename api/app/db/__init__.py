
import tempfile
from typing import AsyncGenerator
from edgedb import AsyncIOClient, create_async_client
from typing import Annotated

from fastapi import Depends

from app.config import settings

with tempfile.NamedTemporaryFile(mode="w", delete=False) as ca_file:
    ca_file.write(settings.geldb_tls_ca_data)
    ca_file_path = ca_file.name  # store the path


async def db_client() -> AsyncGenerator[AsyncIOClient, AsyncIOClient]:
    client: AsyncIOClient = create_async_client(
        user=settings.geldb_user,
        password=settings.geldb_password,
        database=settings.geldb_branch_name,
        port=settings.geldb_port,
        host=settings.geldb_host,
        tls_security=settings.geldb_tls_security,
        tls_ca=settings.geldb_tls_ca_data,
        wait_until_available=300,
    )
    await client.ensure_connected()
    try:
        yield client
    finally:
        await client.aclose()

EdgedbClient = Annotated[AsyncIOClient, Depends(db_client)]
