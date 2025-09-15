# Robot Code API

A FastAPI-based REST API for robot management and operations. This project provides a clean, modern web API for managing robot entities with full CRUD operations.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **RESTful API**: Full CRUD operations for robot management
- **Automatic Documentation**: Interactive API docs with Swagger UI
- **Pydantic Models**: Data validation and serialization
- **Docker Support**: Containerized deployment
- **Testing**: Comprehensive test suite with pytest
- **Development Tools**: Linting, formatting, and development helpers

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd robot-code-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /api/v1/health/` - Detailed health check

### Robots
- `GET /api/v1/robots/` - List all robots
- `GET /api/v1/robots/{id}` - Get robot by ID
- `POST /api/v1/robots/` - Create new robot
- `PUT /api/v1/robots/{id}` - Update robot
- `DELETE /api/v1/robots/{id}` - Delete robot

## Project Structure

```
robot-code-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── health.py
│   │       │   └── robots.py
│   │       └── api.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   ├── schemas/
│   │   └── robot.py
│   ├── services/
│   │   └── robot_service.py
│   └── main.py
├── tests/
│   ├── test_main.py
│   └── test_robots.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
└── run.py
```

## Development

### Setup Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Copy environment template:
```bash
cp .env.example .env
```

### Using Make Commands

```bash
make help          # Show available commands
make install-dev   # Install development dependencies
make run           # Run the application
make test          # Run tests
make lint          # Run linting
make format        # Format code
make clean         # Clean cache files
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_robots.py
```

### Code Quality

The project includes several code quality tools:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **pytest**: Testing framework

## Docker

### Build and Run with Docker

```bash
# Build the image
docker build -t robot-code-api .

# Run the container
docker run -p 8000:8000 robot-code-api
```

### Using Docker Compose

```bash
# Start the service
docker-compose up

# Build and start
docker-compose up --build

# Run in background
docker-compose up -d
```

## Configuration

Environment variables can be set in a `.env` file or passed to the container:

- `ENVIRONMENT`: Application environment (development/production)
- `DEBUG`: Enable debug mode (true/false)
- `HOST`: Host to bind to (default: 0.0.0.0)
- `PORT`: Port to bind to (default: 8000)
- `SECRET_KEY`: Secret key for security (change in production)

## Robot Schema

```json
{
  "id": 1,
  "name": "Atlas",
  "model": "Humanoid-v2",
  "status": "active",
  "battery_level": 85.5,
  "location": "Lab A",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Next Steps

This is a basic skeleton. Consider adding:

- Database integration (PostgreSQL, MongoDB)
- Authentication and authorization
- Rate limiting
- Logging and monitoring
- CI/CD pipeline
- Additional robot operations (movement, tasks, etc.)
- Real-time updates with WebSockets
- Background task processing
