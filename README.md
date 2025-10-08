# 📋 ToDo API - FastAPI

A modern, scalable ToDo API built with FastAPI, featuring comprehensive CRUD operations, testing with Pytest, and production-ready containerization.

## ✨ Features

- **🚀 FastAPI**: Modern, fast (high-performance) web framework for building APIs
- **📝 Full CRUD Operations**: Create, Read, Update, Delete todos
- **🔍 Advanced Filtering**: Filter by status, priority, and search functionality
- **📊 Statistics**: Get insights about your todos
- **✅ Comprehensive Testing**: Unit and integration tests with Pytest
- **🐳 Docker Ready**: Containerized for easy deployment
- **📚 Auto Documentation**: Interactive API docs with Swagger UI
- **🗄️ Database Ready**: Prepared for MySQL integration with SQLAlchemy

## 🏗️ Architecture

```
ToDo_PythonFastApi/
├── app.py              # FastAPI application & endpoints
├── todo_service.py     # Business logic & CRUD operations  
├── models.py           # Pydantic models & schemas
├── config.py           # Configuration & settings
├── requirements.txt    # Dependencies
├── Dockerfile         # Container definition
├── tests/             # Test suite
│   ├── test_app.py    # API endpoint tests
│   └── test_service.py # Business logic tests
└── .github/
    └── workflows/
        └── ci.yml     # GitHub Actions CI/CD
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/valentino-v/ToDo_PythonFastApi.git
   cd ToDo_PythonFastApi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the application**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📖 API Endpoints

### Health Check
- `GET /health` - Check API health status

### Todos
- `POST /todos` - Create a new todo
- `GET /todos` - List all todos (with filtering)
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo
- `PATCH /todos/{id}/complete` - Mark todo as completed

### Bulk Operations
- `DELETE /todos/completed` - Delete all completed todos

### Statistics
- `GET /todos/stats` - Get todo statistics

### Query Parameters for Listing

- `status`: Filter by status (`pending`, `in_progress`, `completed`)
- `priority`: Filter by priority (`low`, `medium`, `high`)
- `search`: Search in title and description

**Example requests:**
```bash
# Get all pending todos
GET /todos?status=pending

# Get high priority todos
GET /todos?priority=high

# Search for todos containing "project"
GET /todos?search=project

# Combined filters
GET /todos?status=pending&priority=high&search=API
```

## 🧪 Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v
```

## 🐳 Docker

### Build and run with Docker

```bash
# Build the image
docker build -t todo-api .

# Run the container
docker run -p 8000:8000 todo-api
```

### Using Docker Compose (if you have docker-compose.yml)

```bash
docker-compose up --build
```

## 📊 Example Usage

### Create a Todo
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API documentation",
    "priority": "high"
  }'
```

### Get All Todos
```bash
curl "http://localhost:8000/todos"
```

### Update a Todo
```bash
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "status": "in_progress"
  }'
```

### Mark as Completed
```bash
curl -X PATCH "http://localhost:8000/todos/1/complete"
```

## 🗄️ MySQL Integration

This application is prepared for MySQL integration. To enable MySQL:

### Prerequisites
- MySQL Server 8.0+
- MySQL Workbench (optional, for GUI management)

### Setup Steps

1. **Install MySQL dependencies** (already in requirements.txt)
   ```bash
   pip install sqlalchemy pymysql alembic
   ```

2. **Create database in MySQL Workbench**
   ```sql
   CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Update environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MySQL credentials
   ```

4. **Create database models** (see MySQL Integration section below)

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

## 🔧 Configuration

Configuration is handled through environment variables. Copy `.env.example` to `.env` and adjust values:

```bash
cp .env.example .env
```

### Available Settings

- `APP_NAME`: Application name
- `DEBUG`: Enable debug mode
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `MYSQL_HOST`: MySQL host
- `MYSQL_PORT`: MySQL port
- `MYSQL_USER`: MySQL username
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_DATABASE`: MySQL database name

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=false` in environment
- [ ] Configure proper MySQL database
- [ ] Set up reverse proxy (nginx)
- [ ] Configure SSL/TLS
- [ ] Set up monitoring and logging
- [ ] Configure backup strategies

### GitHub Actions CI/CD

This project includes a GitHub Actions workflow that:

- Runs tests on Python 3.11
- Checks code quality with SonarQube
- Builds Docker image
- Runs security scans

## 📈 Performance

- **FastAPI**: High performance, on par with NodeJS and Go
- **In-memory storage**: Ultra-fast for development and testing
- **MySQL ready**: Scalable database backend
- **Docker optimized**: Multi-stage builds for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Roadmap

- [ ] MySQL/PostgreSQL integration
- [ ] User authentication and authorization
- [ ] File attachments for todos
- [ ] WebSocket real-time updates
- [ ] Email notifications
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics and reporting

## 📞 Support

If you have any questions or need help:

- Open an issue on GitHub
- Check the [documentation](http://localhost:8000/docs) when running
- Review the test files for usage examples

---

**Built with ❤️ using FastAPI and Python**