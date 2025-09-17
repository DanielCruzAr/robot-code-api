from app.config.redis import get_redis_client

async def set_cache(key: str, value: str, expire: int = 60) -> dict:
    try:
        redis = await get_redis_client()
        await redis.set(key, value, ex=expire)
        return {"message": "Cache set successfully"}
    except Exception as e:
        return {"message": str(e)}

async def get_cache(resource: str, key: int) -> dict:
    try:
        redis = await get_redis_client()
        redis_key = f"{resource}:{str(key)}"
        value = await redis.get(redis_key)
        if value:
            return {"success": True, "value": value.decode('utf-8')}
        else:
            return {"success": False, "error": "Key not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}