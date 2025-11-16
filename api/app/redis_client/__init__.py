from fastapi import Depends
from redis.asyncio import Redis
from typing import Annotated

async def get_redis_connection(db_index=1) -> Redis:
    return await Redis(
        host="localhost",
        port=6379,
        auto_close_connection_pool=True,
        decode_responses=True,
        db=db_index
    ) 

RedisClient = Annotated[Redis,Depends(get_redis_connection)]