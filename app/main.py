from fastapi import FastAPI
from app.articles import view


app = FastAPI(title="Article Management API", version="1.0.0")

app.include_router(view.router)

@app.on_event("startup")
async def startup_event():
    from app.config.redis import redis_client
    try:
        await redis_client.ping()
        print("Connected to Redis")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    from app.config.redis import redis_client
    await redis_client.close()
    await redis_client.connection_pool.disconnect()