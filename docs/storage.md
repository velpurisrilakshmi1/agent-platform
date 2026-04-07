# Storage - Data Persistence

Storage components keep track of all jobs and tasks in memory.

---

## Location: `app/storage/`

---

## How It Works

For the MVP, we use **in-memory storage** (Python dictionaries):
- Fast and simple
- No database setup required
- Data is lost when server restarts

**Future:** Replace with PostgreSQL or another database.

---

## 1. Job Store (`job_store.py`)

**What it does:** Stores and retrieves jobs.

**Think of it as:** A filing cabinet for all job records.

### Methods

| Method | What it does |
|--------|--------------|
| `create(job)` | Save a new job |
| `get(job_id)` | Find a job by ID |
| `update(job)` | Update an existing job |
| `update_status(job_id, status)` | Change job status |
| `set_result(job_id, result)` | Save job result |
| `list_all()` | Get all jobs |
| `delete(job_id)` | Remove a job |

### Usage

```python
from app.storage import get_job_store

store = get_job_store()

# Create
job = Job(input_data={"query": "Hello"})
store.create(job)

# Read
job = store.get(job.id)

# Update
store.update_status(job.id, JobStatus.COMPLETED)

# List
all_jobs = store.list_all()
```

### How data is stored

```python
# Internal structure
{
    UUID("abc-123"): Job(...),
    UUID("def-456"): Job(...),
}
```

---

## 2. Task Store (`task_store.py`)

**What it does:** Stores tasks and task plans.

**Think of it as:** A to-do list manager for job tasks.

### Methods

| Method | What it does |
|--------|--------------|
| `create_task(task)` | Save a new task |
| `get_task(task_id)` | Find a task by ID |
| `update_task(task)` | Update an existing task |
| `update_task_status(task_id, status)` | Change task status |
| `get_tasks_by_job(job_id)` | Get all tasks for a job |
| `create_plan(plan)` | Save a task plan |
| `get_plan(job_id)` | Get the plan for a job |

### Usage

```python
from app.storage import get_task_store

store = get_task_store()

# Create a plan (also stores individual tasks)
store.create_plan(task_plan)

# Get all tasks for a job
tasks = store.get_tasks_by_job(job_id)

# Update task status
store.update_task_status(task_id, TaskStatus.COMPLETED)
```

---

## Dependency Injection

FastAPI uses "dependency injection" to provide storage to routes:

```python
from fastapi import Depends
from app.storage import JobStore, get_job_store

@router.get("/jobs")
async def list_jobs(store: JobStore = Depends(get_job_store)):
    return store.list_all()
```

**Benefits:**
- Easy to test (mock the storage)
- Easy to swap implementations later
- Clean separation of concerns

---

## Singleton Pattern

Storage uses singletons so all parts of the app share the same data:

```python
# This creates ONE instance shared everywhere
job_store = JobStore()

def get_job_store() -> JobStore:
    return job_store
```

Without this, each request would have its own empty storage!

---

## Limitations (MVP)

| Limitation | Why it's OK for MVP | Future Fix |
|------------|---------------------|------------|
| Data lost on restart | Fast iteration | Use database |
| No concurrent safety | Single user testing | Add locks/transactions |
| Memory limits | Small datasets | Database pagination |
| No persistence | Development only | PostgreSQL/SQLite |

---

## Upgrading to Database

When ready, you'll:
1. Create database tables matching the models
2. Replace dictionary operations with SQL queries
3. Keep the same interface (methods stay the same)

Example of what changes:
```python
# Before (in-memory)
def get(self, job_id):
    return self._jobs.get(job_id)

# After (database)
def get(self, job_id):
    return db.query(Job).filter(Job.id == job_id).first()
```

The rest of the app won't need changes!
