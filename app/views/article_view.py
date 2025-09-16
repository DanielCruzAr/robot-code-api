from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controllers.article_controller import (
    create_article, 
    get_articles, 
    get_article, 
    update_article, 
    delete_article
)
from app.schemas.article import ArticleCreate, ArticleResponse
from typing import List

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("/", response_model=ArticleResponse)
def create_article_view(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_article(db, article)


@router.get("/", response_model=List[ArticleResponse])
def get_articles_view(db: Session = Depends(get_db)):
    return get_articles(db)


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article_view(article_id: int, db: Session = Depends(get_db)):
    return get_article(db, article_id)


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article_view(article_id: int, article: ArticleCreate, db: Session = Depends(get_db)):
    return update_article(db, article_id, article)


@router.delete("/{article_id}", status_code=204)
def delete_article_view(article_id: int, db: Session = Depends(get_db)):
    delete_article(db, article_id)
    return {"detail": "Article deleted successfully."}