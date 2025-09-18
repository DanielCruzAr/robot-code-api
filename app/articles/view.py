from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.articles.controller import (
    create_article, 
    get_articles, 
    get_article,
    search_articles, 
    update_article, 
    delete_article
)
from app.articles.schema import (
    ArticleCreate, 
    ArticleResponse, 
    PaginatedArticles, 
    ArticleUpdate
)
from app.utils.auth_utils import get_api_key
from ..rate_limiting import limiter


router = APIRouter(prefix="/articles", tags=["Articles"])


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute") 
async def create_article_view(
    request: Request,
    article: ArticleCreate, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key),
):
    return await create_article(db, article)


@router.get("/", response_model=PaginatedArticles)
@limiter.limit("20/minute")
def get_articles_view(
    request: Request,
    db: Session = Depends(get_db), 
    page: int = 1, 
    page_size: int = 10,
    title: Optional[str] = None,
    author: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    content: Optional[str] = None,
    api_key: str = Depends(get_api_key)
):
    return get_articles(
        db, 
        page=page, 
        page_size=page_size, 
        title=title, 
        author=author, 
        tags=tags, 
        content=content
    )


@router.get("/{article_id}", response_model=ArticleResponse)
@limiter.limit("20/minute")
async def get_article_view(
    request: Request,
    article_id: int, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    return await get_article(db, article_id)


@router.put("/{article_id}", response_model=ArticleResponse)
@limiter.limit("10/minute")
async def update_article_view(
    request: Request,
    article_id: int, 
    article: ArticleUpdate, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    return await update_article(db, article_id, article)


@router.delete("/{article_id}", status_code=204)
@limiter.limit("10/minute")
async def delete_article_view(
    request: Request,
    article_id: int, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    await delete_article(db, article_id)
    return {"detail": "Article deleted successfully."}


@router.get("/search/", response_model=PaginatedArticles)
@limiter.limit("50/minute")
async def search_articles_view(
    request: Request,
    q: str,
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 10,
    api_key: str = Depends(get_api_key)
):
    return search_articles(
        db,
        q,
        page=page,
        page_size=page_size
    )