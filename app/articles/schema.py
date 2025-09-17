from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str = Field(..., unique=True)
    author: str
    tags: List[str] = []
    published_at: Optional[datetime] = None
    body: str

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
