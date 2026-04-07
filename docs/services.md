# Services - The Business Logic

Services contain the "brains" of the platform. They do the actual work.

---

## Location: `app/services/`

---

## 1. Job Processor (`job_processor.py`)

**What it does:** Coordinates the entire pipeline from start to finish.

**Think of it as:** A project manager who makes sure everything happens in order.

**How it works:**
```
1. Get the job from storage
2. Create a task plan (using Orchestrator)
3. Execute all tasks (using Worker)
4. Store the result
5. Update job status
```

**Key method:**
```python
processor.process(job_id)  # Runs the full pipeline
```

**Error handling:**
- If any task fails → job status = "failed"
- Logs every step for debugging

---

## 2. Orchestrator (`orchestrator.py`)

**What it does:** Creates a plan (list of tasks) for each job.

**Think of it as:** A recipe creator who decides what steps are needed.

**How it works:**
```
Job: "What is Python?"
    ↓
Orchestrator creates:
    Task 1: fetch_context (get relevant info)
    Task 2: process (handle the query)
    Task 3: validate (check the output)
```

**Key method:**
```python
orchestrator.create_plan(job)  # Returns a TaskPlan
```

**MVP simplification:**
- Always creates the same 3 tasks (fixed plan)
- Future: Could use AI to decide what tasks are needed

---

## 3. Worker Agent (`worker.py`)

**What it does:** Executes individual tasks.

**Think of it as:** A worker who follows instructions and gets things done.

**How it works:**
```
For each task in the plan:
    1. Check task type
    2. Run the appropriate handler
    3. Store the output
    4. Pass data to next task
```

**Task handlers:**

| Task Type | What it does |
|-----------|--------------|
| `fetch_context` | Gets context from MCP server |
| `process` | Processes the query with context |
| `validate` | Runs RAI validation checks |

**Key methods:**
```python
worker.execute(task)       # Run one task
worker.execute_all(tasks)  # Run all tasks in sequence
worker.get_final_output()  # Get the validated result
```

---

## 4. MCP Client (`mcp_client.py`)

**What it does:** Connects to the MCP server to get context.

**Think of it as:** A researcher who fetches relevant information.

**How it works:**
```
Worker: "I need context for 'What is Python?'"
    ↓
MCP Client → MCP Server → Returns context
    ↓
Worker: "Now I can process with this info"
```

**Key method:**
```python
client.get_context_sync(query)  # Returns context data
```

**Fallback:**
- If MCP server fails → uses mock context instead
- Never crashes the pipeline

---

## 5. RAI Service (`rai.py`)

**What it does:** Validates output to ensure it's safe and appropriate.

**Think of it as:** A safety inspector who checks everything before release.

**What it checks:**

| Check | What it catches |
|-------|-----------------|
| Empty output | Blank or too short responses |
| Length limits | Outputs that are too long |
| Blocked patterns | Sensitive data (passwords, keys) |
| Injection attacks | Script/SQL injection attempts |

**Key method:**
```python
rai.validate(output)  # Returns ValidationResult
```

**Response:**
```python
ValidationResult(
    is_valid=True,
    notes=["All validation checks passed"]
)
```

---

## How Services Work Together

```
┌───────────────────────────────────────────────────────────┐
│                    JOB PROCESSOR                          │
│                                                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │ Orchestrator│───▶│   Worker    │───▶│ RAI Service │   │
│  │(make plan)  │    │(run tasks)  │    │(validate)   │   │
│  └─────────────┘    └──────┬──────┘    └─────────────┘   │
│                            │                              │
│                            ▼                              │
│                     ┌─────────────┐                       │
│                     │ MCP Client  │                       │
│                     │(get context)│                       │
│                     └─────────────┘                       │
└───────────────────────────────────────────────────────────┘
```

---

## Logging

All services log their actions:
```
INFO - Processing job abc-123
INFO - Creating task plan for job abc-123
INFO - Created plan with 3 tasks
INFO - Executing task xyz-456 (type: fetch_context)
INFO - Task xyz-456 completed successfully
INFO - Job abc-123 validated: True
INFO - Job abc-123 completed successfully
```

Check logs to debug issues!
