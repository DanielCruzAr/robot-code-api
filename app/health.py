from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis

from app.config.database import get_db
from app.config.redis import get_redis_client
from app.utils.auth_utils import get_api_key


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/db", summary="Check database connectivity")
def check_db(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@router.get("/redis", summary="Check Redis connectivity")
def check_redis(redis_client: redis.Redis = Depends(get_redis_client), api_key: str = Depends(get_api_key)):
    try:
        redis_client.ping()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}