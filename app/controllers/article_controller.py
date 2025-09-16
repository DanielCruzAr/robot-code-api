from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.article import Article
from app.schemas.article import ArticleCreate


def create_article(db: Session, article: ArticleCreate) -> Article:
    db_article = db.query(Article).filter(
        (Article.title == article.title) | (Article.author == article.author)
    ).first()

    if db_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Article with title '{article.title}' or author '{article.author}' already exists.",
        )
    
    new_article = Article(**article.model_dump())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_articles(db: Session) -> list[Article]:
    return db.query(Article).all()


def get_article(db: Session, article_id: int) -> Article:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{article_id}' not found.",
        )
    return article

def update_article(db: Session, article_id: int, article_data: ArticleCreate) -> Article:
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