from app.config.redis import get_redis_client
import logging


async def set_cache(resource: str, key: int, value: str, expire: int = 120) -> None:
    try:
        redis = await get_redis_client()
        await redis.set(f"{resource}:{str(key)}", value, ex=expire)
        logging.info(f"Cache set successfully for key: {key}")
    except Exception as e:
        logging.error(f"Error setting cache for key: {key}, error: {str(e)}")

async def get_cache(resource: str, key: int) -> dict:
    try:
        redis = await get_redis_client()
        redis_key = f"{resource}:{str(key)}"
        value = await redis.get(redis_key)
        if value:
            logging.info(f"Cache hit for key: {redis_key}")
            return {"success": True, "value": value.decode('utf-8')}
        else:
            logging.warning(f"Cache miss for key: {redis_key}")
            return {"success": False, "error": "Key not found"}
    except Exception as e:
        logging.error(f"Error getting cache for key: {redis_key}, error: {str(e)}")
        return {"success": False, "error": str(e)}
    
async def delete_cache(resource: str, key: int) -> None:
    try:
        redis = await get_redis_client()
        redis_key = f"{resource}:{str(key)}"
        await redis.delete(redis_key)
        logging.info(f"Cache deleted successfully for key: {redis_key}")
    except Exception as e:
        logging.error(f"Error deleting cache for key: {redis_key}, error: {str(e)}")