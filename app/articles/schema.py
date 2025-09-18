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
    title: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    published_at: Optional[datetime] = None
    body: Optional[str] = None


class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class PaginatedArticles(BaseModel):
    total: int
    page: int
    page_size: int
    articles: List[ArticleResponse]