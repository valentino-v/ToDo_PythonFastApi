"""
MySQL Database setup and configuration

To activate MySQL integration, follow these steps:
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database_models import Base
from config import settings
from typing import Generator

# Create engine
engine = create_engine(
    settings.mysql_url,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=settings.debug  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
MYSQL ACTIVATION GUIDE FOR MYSQL WORKBENCH USERS:

1. Install MySQL Server (if not already installed):
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Install MySQL Server 8.0+

2. Open MySQL Workbench and create database:
   ```sql
   CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. Create a user (optional, but recommended):
   ```sql
   CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'CHANGE_THIS_PASSWORD';
   GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Update your .env file:
   ```
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=todo_user  # or root
   MYSQL_PASSWORD=CHANGE_THIS_PASSWORD
   MYSQL_DATABASE=todo_db
   ```

5. Install additional dependencies:
   ```bash
   pip install alembic
   ```

6. Initialize Alembic (database migrations):
   ```bash
   alembic init alembic
   ```

7. Update alembic.ini file:
   - Change sqlalchemy.url to use your database URL
   - Or set it to read from your config

8. Create initial migration:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

9. Apply migration:
   ```bash
   alembic upgrade head
   ```

10. Update todo_service.py to use database instead of in-memory storage

Example updated todo_service.py methods:

```python
from sqlalchemy.orm import Session
from database_models import TodoDB, TodoStatusEnum, TodoPriorityEnum
from database import get_db

class TodoService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_todo(self, todo_data: TodoCreate) -> Todo:
        db_todo = TodoDB(
            title=todo_data.title,
            description=todo_data.description,
            priority=TodoPriorityEnum(todo_data.priority)
        )
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return self._convert_to_pydantic(db_todo)
    
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        return self._convert_to_pydantic(db_todo) if db_todo else None
    
    def _convert_to_pydantic(self, db_todo: TodoDB) -> Todo:
        return Todo(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            status=db_todo.status.value,
            priority=db_todo.priority.value,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at
        )
```

11. Update app.py endpoints to inject database dependency:

```python
from database import get_db

@app.post("/todos", response_model=Todo)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db)):
    service = TodoService(db)
    return service.create_todo(todo_data)
```
"""