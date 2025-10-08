# 🗄️ MySQL Integration Guide for ToDo API

Esta guía te explica paso a paso cómo integrar tu ToDo API con MySQL usando MySQL Workbench.

## 🎯 ¿Por qué MySQL?

Actualmente la aplicación usa almacenamiento en memoria, lo cual es perfecto para desarrollo y testing, pero para producción necesitas persistencia de datos. MySQL te ofrece:

- **Persistencia**: Los datos se guardan permanentemente
- **Escalabilidad**: Maneja miles de usuarios simultáneos
- **Integridad**: Transacciones ACID y constraints
- **Performance**: Optimización de consultas y índices

## 📋 Prerrequisitos

1. **MySQL Server 8.0+** instalado
2. **MySQL Workbench** para gestión visual
3. **Python environment** configurado (ya lo tienes)

## 🚀 Pasos de Activación

### 1. Crear la Base de Datos

Abre **MySQL Workbench** y ejecuta:

```sql
-- Crear la base de datos
CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario específico (recomendado para seguridad)
CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'mi_password_seguro';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'localhost';
FLUSH PRIVILEGES;

-- Verificar que se creó correctamente
SHOW DATABASES;
USE todo_db;
```

### 2. Configurar Variables de Entorno

Crea o actualiza tu archivo `.env`:

```bash
# Copia desde .env.example
cp .env.example .env

# Edita .env con tus credenciales
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=todo_user
MYSQL_PASSWORD=mi_password_seguro
MYSQL_DATABASE=todo_db
```

### 3. Instalar Dependencias Adicionales

```bash
# Ya están en requirements.txt, pero si necesitas instalarlas por separado:
pip install alembic
```

### 4. Inicializar Migraciones con Alembic

```bash
# Inicializar Alembic
alembic init alembic

# Editar alembic.ini y cambiar la línea sqlalchemy.url
# Por: sqlalchemy.url = mysql+pymysql://todo_user:mi_password_seguro@localhost/todo_db
```

### 5. Modificar el Código para Usar MySQL

#### 5.1 Actualizar `todo_service.py`

Reemplaza el contenido actual con la versión que usa base de datos:

```python
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import Todo, TodoCreate, TodoUpdate, TodoStatus, TodoPriority
from database_models import TodoDB, TodoStatusEnum, TodoPriorityEnum
from database import get_db

class TodoService:
    """Business logic for Todo operations with MySQL storage"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_todo(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo in database"""
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
        """Get a todo by ID from database"""
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        return self._convert_to_pydantic(db_todo) if db_todo else None
    
    def list_todos(
        self, 
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        search: Optional[str] = None
    ) -> List[Todo]:
        """List todos with optional filters from database"""
        query = self.db.query(TodoDB)
        
        # Apply filters
        if status:
            query = query.filter(TodoDB.status == TodoStatusEnum(status))
        
        if priority:
            query = query.filter(TodoDB.priority == TodoPriorityEnum(priority))
        
        if search:
            search_filter = or_(
                TodoDB.title.ilike(f"%{search}%"),
                TodoDB.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Order by created_at (newest first)
        db_todos = query.order_by(TodoDB.created_at.desc()).all()
        
        return [self._convert_to_pydantic(todo) for todo in db_todos]
    
    def update_todo(self, todo_id: int, updates: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo in database"""
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if not db_todo:
            return None
        
        # Update fields if provided
        update_data = updates.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "status" and value:
                setattr(db_todo, field, TodoStatusEnum(value))
            elif field == "priority" and value:
                setattr(db_todo, field, TodoPriorityEnum(value))
            else:
                setattr(db_todo, field, value)
        
        # Always update the timestamp
        db_todo.updated_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(db_todo)
        return self._convert_to_pydantic(db_todo)
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by ID from database"""
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if db_todo:
            self.db.delete(db_todo)
            self.db.commit()
            return True
        return False
    
    def mark_completed(self, todo_id: int) -> Optional[Todo]:
        """Mark a todo as completed in database"""
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if not db_todo:
            return None
        
        db_todo.status = TodoStatusEnum.COMPLETED
        db_todo.updated_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(db_todo)
        return self._convert_to_pydantic(db_todo)
    
    def clear_completed(self) -> int:
        """Delete all completed todos from database"""
        deleted_count = self.db.query(TodoDB).filter(
            TodoDB.status == TodoStatusEnum.COMPLETED
        ).delete()
        self.db.commit()
        return deleted_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get todo statistics from database"""
        total = self.db.query(TodoDB).count()
        
        if total == 0:
            return {
                "total": 0,
                "by_status": {"pending": 0, "in_progress": 0, "completed": 0},
                "by_priority": {"low": 0, "medium": 0, "high": 0}
            }
        
        # Count by status
        status_counts = {
            "pending": self.db.query(TodoDB).filter(TodoDB.status == TodoStatusEnum.PENDING).count(),
            "in_progress": self.db.query(TodoDB).filter(TodoDB.status == TodoStatusEnum.IN_PROGRESS).count(),
            "completed": self.db.query(TodoDB).filter(TodoDB.status == TodoStatusEnum.COMPLETED).count()
        }
        
        # Count by priority
        priority_counts = {
            "low": self.db.query(TodoDB).filter(TodoDB.priority == TodoPriorityEnum.LOW).count(),
            "medium": self.db.query(TodoDB).filter(TodoDB.priority == TodoPriorityEnum.MEDIUM).count(),
            "high": self.db.query(TodoDB).filter(TodoDB.priority == TodoPriorityEnum.HIGH).count()
        }
        
        return {
            "total": total,
            "by_status": status_counts,
            "by_priority": priority_counts
        }
    
    def _convert_to_pydantic(self, db_todo: TodoDB) -> Todo:
        """Convert SQLAlchemy model to Pydantic model"""
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

#### 5.2 Actualizar `app.py` endpoints

Modifica los endpoints para usar dependency injection:

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

# Cambia la instancia global por dependency injection
# Elimina: from todo_service import todo_service

@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo"""
    service = TodoService(db)
    return service.create_todo(todo_data)

@app.get("/todos", response_model=TodoList)
def list_todos(
    status_filter: Optional[TodoStatus] = Query(None, alias="status"),
    priority_filter: Optional[TodoPriority] = Query(None, alias="priority"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all todos with optional filters"""
    service = TodoService(db)
    todos = service.list_todos(status=status_filter, priority=priority_filter, search=search)
    return TodoList(todos=todos, total=len(todos))

# ... continúa con el resto de endpoints siguiendo el mismo patrón
```

### 6. Crear y Aplicar Migraciones

```bash
# Crear migración inicial
alembic revision --autogenerate -m "Create todos table"

# Aplicar migración
alembic upgrade head

# Verificar en MySQL Workbench que la tabla se creó
```

### 7. Probar la Integración

```bash
# Ejecutar tests para verificar que todo funciona
pytest tests/ -v

# Iniciar la aplicación
python app.py

# Probar con curl o Postman
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test MySQL", "description": "Testing MySQL integration"}'
```

## 🔍 Verificación en MySQL Workbench

Después de crear algunos todos, puedes verificar en MySQL Workbench:

```sql
-- Ver la estructura de la tabla
DESCRIBE todos;

-- Ver todos los registros
SELECT * FROM todos;

-- Ver estadísticas
SELECT 
    status, 
    COUNT(*) as count 
FROM todos 
GROUP BY status;
```

## 🚨 Troubleshooting

### Problema: Error de conexión
```bash
# Verificar que MySQL está corriendo
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# Verificar credenciales
mysql -u todo_user -p -h localhost
```

### Problema: Error de permisos
```sql
-- En MySQL Workbench, verificar permisos
SHOW GRANTS FOR 'todo_user'@'localhost';

-- Si necesario, otorgar permisos nuevamente
GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'localhost';
FLUSH PRIVILEGES;
```

### Problema: Error de encoding
```sql
-- Verificar charset de la base de datos
SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME 
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME = 'todo_db';
```

## 📈 Beneficios Obtenidos

Después de la migración a MySQL tendrás:

✅ **Persistencia de datos** - Los todos no se pierden al reiniciar
✅ **Escalabilidad** - Soporta miles de usuarios
✅ **Integridad** - Constraints y transacciones ACID
✅ **Backup/Recovery** - Herramientas nativas de MySQL
✅ **Monitoring** - Logs y métricas de base de datos
✅ **Concurrencia** - Múltiples usuarios simultáneos

## 🔄 Migración de Datos

Si ya tienes datos en la aplicación actual y quieres migrarlos:

```python
# Script de migración (migration_script.py)
from todo_service import TodoService as MemoryService
from database import SessionLocal
from todo_service_mysql import TodoService as MySQLService

def migrate_data():
    # Obtener datos de memoria
    memory_service = MemoryService()
    todos = memory_service.list_todos()
    
    # Migrar a MySQL
    db = SessionLocal()
    mysql_service = MySQLService(db)
    
    for todo in todos:
        mysql_service.create_todo(TodoCreate(
            title=todo.title,
            description=todo.description,
            priority=todo.priority
        ))
    
    db.close()
    print(f"Migrated {len(todos)} todos to MySQL")

if __name__ == "__main__":
    migrate_data()
```

## 🎯 Próximos Pasos

Una vez que tengas MySQL funcionando:

1. **Indices**: Optimiza consultas frecuentes
2. **Connection Pooling**: Para mejor performance
3. **Backup Strategy**: Automatiza backups regulares
4. **Monitoring**: Configura alertas de performance
5. **Replication**: Para alta disponibilidad

¡Listo para producción! 🚀