# Configuration & Main Entry Point

These files set up and run the application.

---

## `app/config.py` - Settings

**What it does:** Stores all configuration in one place.

### Settings Available

| Setting | Default | What it's for |
|---------|---------|---------------|
| `app_name` | "Agent Orchestration Platform" | Display name |
| `debug` | True | Enable debug mode |
| `host` | "0.0.0.0" | Server bind address |
| `port` | 8000 | Server port |
| `mcp_server_url` | "http://localhost:8001" | MCP server location |

### Using Environment Variables

Settings can be overridden with environment variables:

```bash
# .env file
APP_NAME=My Custom Platform
DEBUG=false
PORT=9000
```

```python
# In code
from app.config import settings
print(settings.app_name)  # "My Custom Platform"
```

### Why Pydantic Settings?

- **Type safety** - Settings are validated
- **Environment loading** - Reads from `.env` files
- **Defaults** - Provides sensible defaults
- **Documentation** - Self-documenting configuration

---

## `app/main.py` - Application Entry Point

**What it does:** Creates and configures the FastAPI application.

### What It Sets Up

```python
# 1. Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 2. Application lifecycle
@asynccontextmanager
async def lifespan(app):
    logger.info("Starting...")  # On startup
    yield
    logger.info("Shutting down...")  # On shutdown

# 3. FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Autonomous Agent Orchestration Platform MVP",
    version="0.1.0",
)

# 4. Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal error"})

# 5. Routes
app.include_router(jobs_router)
```

### Built-in Endpoints

| Endpoint | What it does |
|----------|--------------|
| `GET /` | Returns "Agent Platform is running" |
| `GET /health` | Health check for monitoring |
| `GET /docs` | Interactive API documentation |
| `GET /redoc` | Alternative documentation |

---

## Running the Application

### Development (with auto-reload)
```bash
uvicorn app.main:app --reload --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Virtual Environment
```bash
# Windows
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Linux/Mac
./venv/bin/python -m uvicorn app.main:app --reload
```

---

## Error Handling

The app catches and handles errors gracefully:

### ValueError (400 Bad Request)
```python
# When you raise ValueError
raise ValueError("Job not found")

# API returns
{"detail": "Job not found"}
```

### Any Other Exception (500 Internal Error)
```python
# When something unexpected happens
raise RuntimeError("Database connection failed")

# API returns
{"detail": "Internal server error"}
```

---

## Logging Output

When the server runs, you'll see:
```
2024-01-15 10:30:00 - app.main - INFO - Starting Agent Orchestration Platform
2024-01-15 10:30:01 - uvicorn - INFO - Application startup complete
2024-01-15 10:30:05 - app.services.job_processor - INFO - Processing job abc-123
2024-01-15 10:30:05 - app.services.worker - INFO - Executing task xyz-456
```

---

## File Summary

| File | Purpose |
|------|---------|
| `config.py` | All settings in one place |
| `main.py` | Creates FastAPI app, sets up errors/logging |
| `__init__.py` | Makes `app` a Python package |

---

## Quick Reference

```python
# Access settings anywhere
from app.config import settings
print(settings.port)  # 8000

# Access the app
from app.main import app
# Use with uvicorn: uvicorn app.main:app
```
