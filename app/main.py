from fastapi import FastAPI
from app.articles import view
from app import health
from .logging import configure_logging, LogLevels
import logging


configure_logging(LogLevels.info)

app = FastAPI(title="Article Management API", version="1.0.0")

app.include_router(view.router)
app.include_router(health.router)

@app.on_event("startup")
async def startup_event():
    from app.config.redis import redis_client
    try:
        await redis_client.ping()
        logging.info("Connected to Redis")
    except Exception as e:
        logging.error(f"Failed to connect to Redis: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    from app.config.redis import redis_client
    await redis_client.close()
    await redis_client.connection_pool.disconnect()
    logging.info("Disconnected from Redis")