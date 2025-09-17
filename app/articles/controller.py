from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.article import Article
from app.articles.schema import ArticleCreate, ArticleResponse
from app.services import cache_service


async def create_article(db: Session, article: ArticleCreate) -> ArticleResponse:
    db_article = db.query(Article).filter(
        (Article.title == article.title) | (Article.author == article.author)
    ).first()

    if db_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Article with title '{article.title}' or author '{article.author}' already exists.",
        )
    
    new_article = Article(**article.model_dump())
    cache_res = cache_service.set_cache("article", new_article.id, new_article)
    if cache_res.get("message"):
        print("Cache set:", cache_res["message"])
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_articles(db: Session) -> list[Article]:
    return db.query(Article).all()


async def get_article(db: Session, article_id: int) -> ArticleResponse:
    cache_result = await cache_service.get_cache("article", article_id)
    if cache_result.get("success"):
        return cache_result["value"]
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{article_id}' not found.",
        )
    return article

def update_article(db: Session, article_id: int, article_data: ArticleCreate) -> ArticleResponse:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{article_id}' not found.",
        )
    
    for key, value in article_data.model_dump().items():
        setattr(article, key, value)
    
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article_id: int) -> None:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{article_id}' not found.",
        )
    
    db.delete(article)
    db.commit()