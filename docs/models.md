# Models - Data Structures Explained

Models define the **shape of data** in our system. Think of them as templates or blueprints.

---

## Location: `app/models/`

---

## `enums.py` - Status Labels

Enums are like labels or tags. They limit what values a field can have.

### JobStatus
```python
PENDING    # Job received, waiting to start
RUNNING    # Job is being processed
COMPLETED  # Job finished successfully
FAILED     # Job encountered an error
```

### TaskStatus
Same as JobStatus, but for individual tasks within a job.

### TaskType
```python
FETCH_CONTEXT  # Get information from MCP server
PROCESS        # Do the main work
VALIDATE       # Check if output is safe
```

---

## `job.py` - Job-Related Models

### Job
The main unit of work. When you submit a request, a Job is created.

| Field | What it is |
|-------|------------|
| `id` | Unique identifier (UUID) |
| `input_data` | What you submitted (your query) |
| `status` | Current state (pending/running/completed/failed) |
| `created_at` | When the job was created |
| `result` | Final output (once completed) |

**Example:**
```json
{
  "id": "abc-123",
  "input_data": {"query": "What is Python?"},
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "result": {...}
}
```

### JobInput
What you send when creating a job.
```json
{"data": {"query": "your question here"}}
```

### JobResult
The final output after processing.
| Field | What it is |
|-------|------------|
| `job_id` | Which job this result belongs to |
| `output` | The actual result data |
| `validated` | Did it pass RAI checks? (true/false) |
| `validation_notes` | Details about validation |

---

## `task.py` - Task-Related Models

### Task
One step in the job's plan. Jobs are broken into tasks.

| Field | What it is |
|-------|------------|
| `id` | Unique identifier |
| `job_id` | Which job this task belongs to |
| `type` | What kind of task (fetch_context/process/validate) |
| `input` | Data this task needs |
| `output` | What this task produced |
| `status` | Current state of this task |
| `error` | Error message if failed |

### TaskPlan
A list of tasks for a job.
```python
TaskPlan(
    job_id="abc-123",
    tasks=[Task1, Task2, Task3]
)
```

### TaskResult
Output from executing a single task.
| Field | What it is |
|-------|------------|
| `task_id` | Which task this is for |
| `success` | Did it work? (true/false) |
| `output` | What was produced |
| `error` | Error message if failed |

---

## Why Pydantic?

We use **Pydantic** for models because:
1. **Automatic validation** - Catches bad data early
2. **Type hints** - IDE shows you what fields exist
3. **JSON conversion** - Easy to send/receive over HTTP
4. **Documentation** - FastAPI generates API docs automatically

---

## Quick Reference

| Model | Purpose | Lives in |
|-------|---------|----------|
| `Job` | Main unit of work | `job.py` |
| `JobInput` | What you send to create a job | `job.py` |
| `JobResult` | Final output of a job | `job.py` |
| `Task` | One step in processing | `task.py` |
| `TaskPlan` | List of tasks for a job | `task.py` |
| `TaskResult` | Output of one task | `task.py` |
