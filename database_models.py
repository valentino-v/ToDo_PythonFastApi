"""
Database models for MySQL integration using SQLAlchemy

This file contains the SQLAlchemy models that correspond to the Pydantic models.
Uncomment and use these when you want to integrate with MySQL.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class TodoStatusEnum(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TodoPriorityEnum(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TodoDB(Base):
    """SQLAlchemy model for Todo table"""
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TodoStatusEnum), default=TodoStatusEnum.PENDING, nullable=False, index=True)
    priority = Column(Enum(TodoPriorityEnum), default=TodoPriorityEnum.MEDIUM, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', status='{self.status.value}')>"

"""
Usage example when integrating with MySQL:

# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.mysql_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In your service:
def create_todo_db(db: Session, todo_data: TodoCreate) -> TodoDB:
    db_todo = TodoDB(
        title=todo_data.title,
        description=todo_data.description,
        priority=TodoPriorityEnum(todo_data.priority)
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
"""