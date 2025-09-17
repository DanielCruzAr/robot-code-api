from dotenv import load_dotenv
import os
from redis.asyncio import Redis

load_dotenv()

# Redis client
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", 6379),
    db=os.getenv("REDIS_DB", 0)
)

async def get_redis_client() -> Redis:
    return redis_client