from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from sqlalchemy.sql import func
from app.config.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(ARRAY(String))
    author = Column(String(100), nullable=False, index=True)
    published_at = Column(DateTime, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
