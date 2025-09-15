.PHONY: help install install-dev run test lint format clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  run          Run the FastAPI application"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  clean        Clean cache files"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker Compose"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	python run.py

test:
	pytest tests/ -v

lint:
	flake8 app/ tests/
	mypy app/

format:
	black app/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

docker-build:
	docker build -t robot-code-api .

docker-run:
	docker-compose up --build