import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.articles import controller as article_service
from app.articles.schema import ArticleCreate, ArticleUpdate, ArticleResponse, PaginatedArticles
from app.models.article import Article
from .conftest import override_get_db


class TestArticleService:
    
    @pytest.fixture
    def db_session(self):
        """Get database session from dependency override"""
        db = next(override_get_db())
        try:
            yield db
        finally:
            # Clean up any test data
            db.query(Article).delete()
            db.commit()
            db.close()
    
    @pytest.fixture
    def sample_article_data(self):
        """Sample article data for testing"""
        return {
            "title": "Test Article",
            "author": "Test Author",
            "body": "This is a test article body",
            "tags": ["test", "article"],
            "published_at": datetime.now()
        }
    
    @pytest.fixture
    def sample_article_create(self, sample_article_data):
        """Sample ArticleCreate schema"""
        return ArticleCreate(**sample_article_data)
    
    @pytest.fixture
    def sample_article_update(self):
        """Sample ArticleUpdate schema"""
        return ArticleUpdate(
            title="Updated Article",
            body="Updated body content"
        )


class TestCreateArticle(TestArticleService):
    
    @patch('app.articles.controller.cache_service.set_cache')
    @pytest.mark.asyncio
    async def test_create_article_success(self, mock_set_cache, db_session, sample_article_create):
        """Test successful article creation"""
        # Setup
        mock_set_cache.return_value = None
        
        # Execute
        result = await article_service.create_article(db_session, sample_article_create)
        
        # Assert
        assert isinstance(result, ArticleResponse)
        assert result.title == sample_article_create.title
        assert result.author == sample_article_create.author
        assert result.body == sample_article_create.body
        assert result.id is not None
        mock_set_cache.assert_called_once()
        
        # Verify article was actually saved to database
        saved_article = db_session.query(Article).filter(Article.id == result.id).first()
        assert saved_article is not None
        assert saved_article.title == sample_article_create.title
    
    @pytest.mark.asyncio
    async def test_create_article_duplicate_raises_exception(self, db_session, sample_article_create):
        """Test that creating duplicate article raises HTTPException"""
        # Setup - create an article first
        existing_article = Article(**sample_article_create.model_dump())
        db_session.add(existing_article)
        db_session.commit()
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await article_service.create_article(db_session, sample_article_create)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in exc_info.value.detail


class TestGetArticles(TestArticleService):
    
    def test_get_articles_without_filters(self, db_session, sample_article_data):
        """Test getting articles without any filters"""
        # Setup - create test articles
        article1 = Article(**sample_article_data)
        article2_data = sample_article_data.copy()
        article2_data["title"] = "Second Article"
        article2 = Article(**article2_data)
        
        db_session.add(article1)
        db_session.add(article2)
        db_session.commit()
        
        # Execute
        result = article_service.get_articles(db_session, page=1, page_size=10)
        
        # Assert
        assert isinstance(result, PaginatedArticles)
        assert result.total == 2
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.articles) == 2
    
    def test_get_articles_with_title_filter(self, db_session, sample_article_data):
        """Test getting articles with title filter"""
        # Setup - create test articles with different titles
        article1 = Article(**sample_article_data)
        article2_data = sample_article_data.copy()
        article2_data["title"] = "Different Title"
        article2_data["author"] = "Different Author"
        article2 = Article(**article2_data)
        
        db_session.add(article1)
        db_session.add(article2)
        db_session.commit()
        
        # Execute
        result = article_service.get_articles(
            db_session, page=1, page_size=10, title="Test"
        )
        
        # Assert
        assert isinstance(result, PaginatedArticles)
        assert len(result.articles) == 1
        assert result.articles[0].title == "Test Article"
    
    def test_get_articles_with_author_filter(self, db_session, sample_article_data):
        """Test getting articles with author filter"""
        # Setup - create test articles with different authors
        article1 = Article(**sample_article_data)
        article2_data = sample_article_data.copy()
        article2_data["title"] = "Different Title"
        article2_data["author"] = "Different Author"
        article2 = Article(**article2_data)
        
        db_session.add(article1)
        db_session.add(article2)
        db_session.commit()
        
        # Execute
        result = article_service.get_articles(
            db_session, page=1, page_size=10, author="Test Author"
        )
        
        # Assert
        assert isinstance(result, PaginatedArticles)
        assert len(result.articles) == 1
        assert result.articles[0].author == "Test Author"
    
    def test_get_articles_with_tags_filter(self, db_session, sample_article_data):
        """Test getting articles with tags filter"""
        # Setup - create test articles with different tags
        article1 = Article(**sample_article_data)
        article2_data = sample_article_data.copy()
        article2_data["title"] = "Different Title"
        article2_data["author"] = "Different Author"
        article2_data["tags"] = ["python", "fastapi"]
        article2 = Article(**article2_data)
        
        db_session.add(article1)
        db_session.add(article2)
        db_session.commit()
        
        # Execute
        result = article_service.get_articles(
            db_session, page=1, page_size=10, tags=["test"]
        )
        
        # Assert
        assert isinstance(result, PaginatedArticles)
        assert len(result.articles) == 1
        assert "test" in result.articles[0].tags
    
    def test_get_articles_with_content_filter(self, db_session, sample_article_data):
        """Test getting articles with content filter"""
        # Setup - create test articles with different content
        article1 = Article(**sample_article_data)
        article2_data = sample_article_data.copy()
        article2_data["title"] = "Different Title"
        article2_data["author"] = "Different Author"
        article2_data["body"] = "This is completely different content"
        article2 = Article(**article2_data)
        
        db_session.add(article1)
        db_session.add(article2)
        db_session.commit()
        
        # Execute
        result = article_service.get_articles(
            db_session, page=1, page_size=10, content="test article"
        )
        
        # Assert
        assert isinstance(result, PaginatedArticles)
        assert len(result.articles) == 1
        assert "test article" in result.articles[0].body.lower()
    
    def test_get_articles_pagination(self, db_session, sample_article_data):
        """Test pagination logic"""
        # Setup - create multiple test articles
        for i in range(5):
            article_data = sample_article_data.copy()
            article_data["title"] = f"Article {i}"
            article_data["author"] = f"Author {i}"
            article = Article(**article_data)
            db_session.add(article)
        db_session.commit()
        
        # Execute - get page 2 with page size 2
        result = article_service.get_articles(db_session, page=2, page_size=2)
        
        # Assert
        assert isinstance(result, PaginatedArticles)
        assert result.total == 5
        assert result.page == 2
        assert result.page_size == 2
        assert len(result.articles) == 2


class TestGetArticle(TestArticleService):
    
    @patch('app.articles.controller.cache_service.get_cache')
    @pytest.mark.asyncio
    async def test_get_article_from_cache_success(self, mock_get_cache, db_session):
        """Test getting article from cache successfully"""
        # Setup
        article_json = '{"id": 1, "title": "Test Article", "author": "Test Author", "body": "Test body", "tags": ["test"], "published_at": "2023-01-01T00:00:00", "created_at": "2023-01-01T00:00:00", "updated_at": null}'
        mock_get_cache.return_value = {"success": True, "value": article_json}
        
        # Execute
        result = await article_service.get_article(db_session, 1)
        
        # Assert
        assert isinstance(result, ArticleResponse)
        assert result.id == 1
        assert result.title == "Test Article"
        mock_get_cache.assert_called_once_with("article", 1)
    
    @patch('app.articles.controller.cache_service.get_cache')
    @patch('app.articles.controller.cache_service.set_cache')
    @pytest.mark.asyncio
    async def test_get_article_from_db_cache_miss(self, mock_set_cache, mock_get_cache, db_session, sample_article_data):
        """Test getting article from database when cache miss"""
        # Setup - create test article
        article = Article(**sample_article_data)
        db_session.add(article)
        db_session.commit()
        db_session.refresh(article)
        
        mock_get_cache.return_value = {"success": False}
        mock_set_cache.return_value = None
        
        # Execute
        result = await article_service.get_article(db_session, article.id)
        
        # Assert
        assert isinstance(result, ArticleResponse)
        assert result.id == article.id
        assert result.title == article.title
        mock_get_cache.assert_called_once_with("article", article.id)
        mock_set_cache.assert_called_once()
    
    @patch('app.articles.controller.cache_service.get_cache')
    @pytest.mark.asyncio
    async def test_get_article_not_found(self, mock_get_cache, db_session):
        """Test getting non-existent article raises HTTPException"""
        # Setup
        mock_get_cache.return_value = {"success": False}
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await article_service.get_article(db_session, 999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail


class TestUpdateArticle(TestArticleService):
    
    @patch('app.articles.controller.cache_service.delete_cache')
    @pytest.mark.asyncio
    async def test_update_article_success(self, mock_delete_cache, db_session, sample_article_data, sample_article_update):
        """Test successful article update"""
        # Setup - create test article
        article = Article(**sample_article_data)
        db_session.add(article)
        db_session.commit()
        db_session.refresh(article)
        
        mock_delete_cache.return_value = None
        
        # Execute
        result = await article_service.update_article(db_session, article.id, sample_article_update)
        
        # Assert
        assert result.id == article.id
        assert result.title == "Updated Article"
        assert result.body == "Updated body content"
        mock_delete_cache.assert_called_once_with("article", article.id)
        
        # Verify changes were persisted
        updated_article = db_session.query(Article).filter(Article.id == article.id).first()
        assert updated_article.title == "Updated Article"
        assert updated_article.body == "Updated body content"
    
    @pytest.mark.asyncio
    async def test_update_article_not_found(self, db_session, sample_article_update):
        """Test updating non-existent article raises HTTPException"""
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await article_service.update_article(db_session, 999, sample_article_update)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_update_article_duplicate_title_author(self, db_session, sample_article_data):
        """Test updating article with duplicate title/author combination"""
        # Setup - create two articles
        article1 = Article(**sample_article_data)
        db_session.add(article1)
        
        article2_data = sample_article_data.copy()
        article2_data["title"] = "Different Title"
        article2_data["author"] = "Different Author"
        article2 = Article(**article2_data)
        db_session.add(article2)
        db_session.commit()
        
        # Try to update article2 to have same title/author as article1
        update_data = ArticleUpdate(
            title=article1.title,
            author=article1.author
        )
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await article_service.update_article(db_session, article2.id, update_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in exc_info.value.detail


class TestDeleteArticle(TestArticleService):
    
    @patch('app.articles.controller.cache_service.delete_cache')
    @pytest.mark.asyncio
    async def test_delete_article_success(self, mock_delete_cache, db_session, sample_article_data):
        """Test successful article deletion"""
        # Setup - create test article
        article = Article(**sample_article_data)
        db_session.add(article)
        db_session.commit()
        db_session.refresh(article)
        
        mock_delete_cache.return_value = None
        
        # Execute
        await article_service.delete_article(db_session, article.id)
        
        # Assert
        mock_delete_cache.assert_called_once_with("article", article.id)
        
        # Verify article was actually deleted from database
        deleted_article = db_session.query(Article).filter(Article.id == article.id).first()
        assert deleted_article is None
    
    @pytest.mark.asyncio
    async def test_delete_article_not_found(self, db_session):
        """Test deleting non-existent article raises HTTPException"""
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await article_service.delete_article(db_session, 999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail