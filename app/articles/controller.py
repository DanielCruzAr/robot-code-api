from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.article import Article
from app.articles.schema import ArticleCreate, ArticleResponse
from app.services import cache_service
import logging


async def create_article(db: Session, article: ArticleCreate) -> ArticleResponse:
    db_article = db.query(Article).filter(
        (Article.title == article.title) & (Article.author == article.author)
    ).first()

    if db_article:
        logging.warn(f"Attempt to create duplicate article: {article.title} by {article.author}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Article with title '{article.title}' by author '{article.author}' already exists.",
        )
    
    new_article = Article(**article.model_dump())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    # Serialize the new article to JSON for caching
    article_schema = ArticleResponse.from_orm(new_article)

    # Set cache for the new article
    await cache_service.set_cache("article", new_article.id, article_schema.model_dump_json())
    logging.info(f"Article created with ID: {new_article.id}")

    return article_schema


def get_articles(db: Session) -> list[Article]:
    return db.query(Article).all()


async def get_article(db: Session, article_id: int) -> ArticleResponse:
    logging.info(f"Attempting to retrieve article with ID: {article_id} from cache...")
    cache_result = await cache_service.get_cache("article", article_id)
    if cache_result.get("success"):
        return ArticleResponse.model_validate_json(cache_result["value"])
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{article_id}' not found.",
        )
    article_schema = ArticleResponse.from_orm(article)
    
    # Set cache for the retrieved article
    logging.info(f"Caching article with ID: {article_id}")
    await cache_service.set_cache("article", article_id, article_schema.model_dump_json())

    return article_schema


async def update_article(db: Session, article_id: int, article_data: ArticleCreate) -> ArticleResponse:
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

    # Invalidate cache for the updated article
    await cache_service.delete_cache("article", article_id)
    logging.info(f"Article updated with ID: {article_id}")

    return article


async def delete_article(db: Session, article_id: int) -> None:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{article_id}' not found.",
        )
    
    db.delete(article)
    db.commit()

    # Invalidate cache for the deleted article
    await cache_service.delete_cache("article", article_id)
    logging.info(f"Article deleted with ID: {article_id}")