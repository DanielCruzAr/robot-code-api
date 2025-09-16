from fastapi import FastAPI
from app.views import article_view

app = FastAPI(title="Article Management API", version="1.0.0")

app.include_router(article_view.router)
