# ToDo API - FastAPI

Una API REST simple para gestión de tareas construida con FastAPI, de [sistema_pagos_mio](https://github.com/valentino-v/sistema_pagos_mio).

## Características

### Endpoints de la API

- **GET /tasks**: Listar todas las tareas
- **POST /tasks**: Crear una nueva tarea
- **GET /tasks/{id}**: Obtener detalle de una tarea específica
- **PUT /tasks/{id}**: Actualizar una tarea existente
- **DELETE /tasks/{id}**: Eliminar una tarea

### Modelos de Datos

#### Task
```json
{
  "id": 1,
  "title": "Título de la tarea",
  "description": "Descripción opcional",
  "status": "pending"
}
```

#### Estados disponibles
- `pending`: Tarea pendiente (por defecto)
- `in_progress`: Tarea en progreso
- `done`: Tarea completada

## Tecnologías

- **FastAPI**: Framework web moderno para APIs
- **Pydantic v2**: Validación de datos y serialización
- **pytest**: Framework de testing
- **httpx**: Cliente HTTP asíncrono para tests
- **uvicorn**: Servidor ASGI para desarrollo

## Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/valentino-v/ToDo_PythonFastApi.git
cd ToDo_PythonFastApi
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
uvicorn app:app --reload
```

### 5. Acceder a la documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

Ejecutar todos los tests:
```bash
pytest
```

Ejecutar tests con verbose:
```bash
pytest -v
```

## Arquitectura

El proyecto sigue una arquitectura limpia con separación de responsabilidades:

```
├── app.py              # FastAPI app y endpoints
├── models.py           # Modelos Pydantic
├── todo_service.py     # Lógica de negocio
├── tests/             
│   ├── test_app.py     # Tests de endpoints
│   ├── test_service.py # Tests del servicio
│   └── conftest.py     # Configuración de tests
├── requirements.txt    # Dependencias
└── README.md
```

### Componentes

1. **app.py**: Contiene la aplicación FastAPI y la definición de endpoints REST
2. **models.py**: Define los modelos de datos usando Pydantic v2
3. **todo_service.py**: Implementa la lógica de negocio y almacenamiento en memoria
4. **tests/**: Contiene tests unitarios y de integración

## Uso de la API

### Crear una tarea
```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Mi primera tarea", "description": "Descripción de la tarea"}'
```

### Listar todas las tareas
```bash
curl -X GET "http://localhost:8000/tasks"
```

### Obtener una tarea específica
```bash
curl -X GET "http://localhost:8000/tasks/1"
```

### Actualizar una tarea
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Tarea actualizada", "status": "in_progress"}'
```

### Eliminar una tarea
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Notas de desarrollo

- La aplicación usa almacenamiento en memoria para simplicidad
- Los datos se pierden al reiniciar el servidor
- Para producción, se recomienda integrar con una base de datos real
- El proyecto está configurado para desarrollo con hot-reload

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.