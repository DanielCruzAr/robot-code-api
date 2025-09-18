import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from alembic import command
from alembic.config import Config

from app.main import app  # your FastAPI app
from app.config.database import get_db  # adjust import paths


TEST_DATABASE_URL = "postgresql://test:test@localhost:5433/test_db"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL 

engine = create_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Run migrations before/after tests
@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")  # path to your alembic.ini
    # Ensure env picks the TEST_DATABASE_URL
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    command.upgrade(alembic_cfg, "head")  # apply latest migrations
    yield
    command.downgrade(alembic_cfg, "base")  # clean slate after tests


# Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
