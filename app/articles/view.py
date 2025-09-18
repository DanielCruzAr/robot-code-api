from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.articles.controller import (
    create_article, 
    get_articles, 
    get_article, 
    update_article, 
    delete_article
)
from app.articles.schema import (
    ArticleCreate, 
    ArticleResponse, 
    PaginatedArticles, 
    ArticleUpdate
)


router = APIRouter(prefix="/articles", tags=["Articles"])


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article_view(article: ArticleCreate, db: Session = Depends(get_db)):
    return await create_article(db, article)


@router.get("/", response_model=PaginatedArticles)
def get_articles_view(
    db: Session = Depends(get_db), 
    page: int = 1, 
    page_size: int = 10,
    title: Optional[str] = None,
    author: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    content: Optional[str] = None
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
async def get_article_view(article_id: int, db: Session = Depends(get_db)):
    return await get_article(db, article_id)


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article_view(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    return await update_article(db, article_id, article)


@router.delete("/{article_id}", status_code=204)
async def delete_article_view(article_id: int, db: Session = Depends(get_db)):
    await delete_article(db, article_id)
    return {"detail": "Article deleted successfully."}