# Autonomous Agent Orchestration Platform - MVP Roadmap

## Overview

This roadmap guides you through building an MVP where:
- A user submits a job
- The system stores the job
- An orchestrator creates a small fixed task plan
- A worker agent executes tasks
- The worker gets task context from an MCP server
- A simple RAI (Responsible AI) service validates the final output
- The final result can be retrieved by job ID

---

## 1. Milestones (In Order)

| # | Milestone | Goal | Est. Time |
|---|-----------|------|-----------|
| 1 | Project Setup | Establish structure, tooling, and dev environment | 2-4 hours |
| 2 | Core Data Models | Define Job, Task, and Result schemas | 2-3 hours |
| 3 | Job API | Submit and retrieve jobs via REST endpoints | 3-4 hours |
| 4 | In-Memory Storage | Store jobs/tasks without external DB first | 1-2 hours |
| 5 | Orchestrator (Fixed Plan) | Create a simple fixed task plan from a job | 2-3 hours |
| 6 | Worker Agent (Basic) | Execute a single task and return results | 3-4 hours |
| 7 | MCP Server Integration | Worker fetches task context from MCP | 4-6 hours |
| 8 | RAI Validation Service | Validate final output before returning | 2-3 hours |
| 9 | End-to-End Flow | Wire everything together, test full pipeline | 3-4 hours |
| 10 | Basic Error Handling | Handle failures gracefully | 2-3 hours |

**Total estimated time: 24-36 hours of focused work**

---

## 2. What to Build in Each Milestone

### Milestone 1: Project Setup

**Goal:** A clean, runnable project structure

**Build:**
- Create project folder structure:
  ```
  agent-platform/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py              # FastAPI entry point
  │   ├── api/                  # Route handlers
  │   ├── models/               # Pydantic schemas
  │   ├── services/             # Business logic
  │   ├── storage/              # Data persistence
  │   └── config.py             # Settings
  ├── mcp_server/               # MCP server implementation
  ├── tests/
  ├── docs/
  ├── requirements.txt
  ├── pyproject.toml
  └── README.md
  ```
- Set up virtual environment (`python -m venv venv`)
- Install initial dependencies: `fastapi`, `uvicorn`, `pydantic`
- Create a "hello world" FastAPI app that runs
- Verify VS Code + Copilot are working

**Exit criteria:** `uvicorn app.main:app --reload` runs and shows docs at `/docs`

---

### Milestone 2: Core Data Models

**Goal:** Clear definitions for all core entities

**Build:**
- `Job` model: id, input_data, status, created_at, result
- `Task` model: id, job_id, type, input, output, status
- `TaskPlan` model: job_id, tasks (list)
- `JobResult` model: job_id, output, validated, validation_notes
- Status enums: `pending`, `running`, `completed`, `failed`

**Key decisions:**
- Use Pydantic `BaseModel` for all schemas
- Use UUIDs for IDs (simple, no collisions)
- Keep models minimal—add fields later as needed

**Exit criteria:** Models import without errors, can be instantiated

---

### Milestone 3: Job API

**Goal:** Users can submit jobs and retrieve results

**Build:**
- `POST /jobs` - Submit a new job, returns job_id
- `GET /jobs/{job_id}` - Get job status and result
- `GET /jobs` - List all jobs (useful for debugging)
- Request/response schemas using Pydantic

**API design principles:**
- Return job_id immediately on submit (async pattern)
- Status field tells user where job is in pipeline
- Keep payloads simple (JSON dict for input_data)

**Exit criteria:** Can submit a job via `/docs` and see it in the list

---

### Milestone 4: In-Memory Storage

**Goal:** Store jobs without database complexity

**Build:**
- `JobStore` class with dict-based storage
- Methods: `create()`, `get()`, `update()`, `list_all()`
- `TaskStore` class (same pattern)
- Dependency injection setup in FastAPI

**Why in-memory first:**
- Zero setup friction
- Focus on business logic, not DB config
- Easy to swap for real DB later

**Exit criteria:** Jobs persist across API calls (while server runs)

---

### Milestone 5: Orchestrator (Fixed Plan)

**Goal:** Turn a job into a list of tasks

**Build:**
- `OrchestratorService` class
- Method: `create_plan(job) -> TaskPlan`
- Fixed plan for MVP (example):
  ```python
  def create_plan(self, job):
      return TaskPlan(
          job_id=job.id,
          tasks=[
              Task(type="fetch_context", input=job.input_data),
              Task(type="process", input={}),
              Task(type="validate", input={}),
          ]
      )
  ```
- Store tasks in TaskStore
- Update job status to `running`

**Key insight:** Keep the plan hardcoded. Dynamic planning is post-MVP.

**Exit criteria:** Submitting a job creates tasks in storage

---

### Milestone 6: Worker Agent (Basic)

**Goal:** Execute a single task

**Build:**
- `WorkerAgent` class
- Method: `execute(task) -> TaskResult`
- Simple switch/match on task type
- Mock implementations for each task type
- Update task status after execution

**Keep it synchronous for MVP:**
- No background workers yet
- Process tasks in sequence during job submission
- Async/queues come later

**Exit criteria:** Tasks get executed and have output

---

### Milestone 7: MCP Server Integration

**Goal:** Worker fetches context from MCP

**Build:**
- Basic MCP server (separate process or module)
- Single tool: `get_context(query) -> context_data`
- MCP client in worker agent
- Worker calls MCP during `fetch_context` task

**MCP setup (simplified):**
- Use `mcp` Python package
- Server exposes one tool
- Client connects via stdio or HTTP
- Return mock context data for MVP

**Exit criteria:** Worker successfully calls MCP and uses response

---

### Milestone 8: RAI Validation Service

**Goal:** Validate final output before returning

**Build:**
- `RAIService` class
- Method: `validate(output) -> ValidationResult`
- Simple rule-based checks for MVP:
  - Output not empty
  - No blocked words/patterns
  - Length within bounds
- Return: `is_valid`, `notes`

**Keep it simple:**
- No LLM calls for validation in MVP
- Hardcoded rules are fine
- Log validation results

**Exit criteria:** Final output is validated, result includes validation status

---

### Milestone 9: End-to-End Flow

**Goal:** Full pipeline works

**Build:**
- Wire together: API → Storage → Orchestrator → Worker → MCP → RAI → Result
- Single entry point that processes entire job
- Update job with final result
- Return complete result on `GET /jobs/{id}`

**Test the full flow:**
1. POST /jobs with test input
2. System creates plan, runs tasks, validates
3. GET /jobs/{id} returns completed result

**Exit criteria:** Can run full flow via API, get validated result

---

### Milestone 10: Basic Error Handling

**Goal:** Graceful failure handling

**Build:**
- Try/except around task execution
- Set task/job status to `failed` on error
- Store error messages in result
- Return meaningful error responses from API
- Add basic logging throughout

**Exit criteria:** Failures don't crash server, errors are visible

---

## 3. What to Postpone Until Later

| Feature | Why Postpone | When to Add |
|---------|--------------|-------------|
| **Database (PostgreSQL, etc.)** | Adds setup complexity | After MVP works end-to-end |
| **Background workers (Celery, etc.)** | Needs message broker | When jobs take >30 seconds |
| **Dynamic task planning** | Requires LLM integration | After fixed flow is solid |
| **Authentication/Authorization** | Security is complex | Before any deployment |
| **Multiple worker agents** | Concurrency complexity | When scaling is needed |
| **Retry logic** | Edge case handling | After basic errors work |
| **Monitoring/Metrics** | Operational concern | Before production |
| **Docker/Containers** | Deployment complexity | Before sharing/deploying |
| **WebSocket for status** | Real-time adds complexity | When polling isn't enough |
| **LLM-based RAI checks** | Costs money, needs API keys | After rules-based works |
| **Rate limiting** | Production concern | Before public access |
| **Job cancellation** | State management complexity | After basic flow stable |
| **Multi-tenancy** | Architecture complexity | When multiple users needed |

---

## 4. Common Beginner Mistakes to Avoid

### Architecture Mistakes

1. **Building everything at once**
   - ❌ Trying to implement all components simultaneously
   - ✅ Build one milestone completely before starting the next

2. **Starting with the hardest part**
   - ❌ Beginning with MCP integration or RAI service
   - ✅ Start with Job API and storage—get data flowing first

3. **Over-engineering early**
   - ❌ Adding abstraction layers, factories, complex patterns
   - ✅ Write simple, direct code. Refactor when patterns emerge

4. **Premature database integration**
   - ❌ Setting up PostgreSQL on day one
   - ✅ Use in-memory storage, swap DB later (takes 30 mins)

### Coding Mistakes

5. **Not using Pydantic properly**
   - ❌ Manual dict validation, inconsistent schemas
   - ✅ Define models once, use everywhere

6. **Ignoring FastAPI dependency injection**
   - ❌ Creating service instances inside route handlers
   - ✅ Use `Depends()` for services and storage

7. **No type hints**
   - ❌ `def process(data):`
   - ✅ `def process(data: JobInput) -> JobResult:`

8. **Swallowing exceptions**
   - ❌ `except: pass`
   - ✅ Log errors, update status, return meaningful messages

### Process Mistakes

9. **Not testing the API manually**
   - ❌ Writing code without trying it
   - ✅ Use FastAPI `/docs` constantly while building

10. **Skipping the happy path first**
    - ❌ Handling edge cases before core flow works
    - ✅ Get success case working, then handle failures

11. **Not version controlling early**
    - ❌ Waiting until "it's ready" to commit
    - ✅ Commit after each milestone (or more often)

12. **Giant commits**
    - ❌ One commit with everything
    - ✅ Small, focused commits with clear messages

### Design Mistakes

13. **Mixing concerns**
    - ❌ API routes containing business logic
    - ✅ Routes call services, services contain logic

14. **Hardcoding configuration**
    - ❌ `mcp_url = "http://localhost:8001"`
    - ✅ Use `config.py` or environment variables

15. **Forgetting status tracking**
    - ❌ Jobs/tasks with no way to check progress
    - ✅ Always update status at each state transition

---

## 5. Suggested Local Development Workflow

### Initial Setup (Once)

```bash
# Create project folder
mkdir agent-platform
cd agent-platform

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic python-dotenv

# Initialize git
git init
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
```

### Daily Development Workflow

```bash
# 1. Activate environment
.\venv\Scripts\activate

# 2. Start the server (in terminal 1)
uvicorn app.main:app --reload --port 8000

# 3. Open browser to http://localhost:8000/docs

# 4. Code in VS Code, test in browser/docs

# 5. For MCP server (in terminal 2, when needed)
python -m mcp_server.main
```

### VS Code Setup

**Recommended extensions:**
- Python (Microsoft)
- Pylance
- GitHub Copilot

**Recommended settings (`.vscode/settings.json`):**
```json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true
}
```

### Testing Workflow

1. **Manual testing first:** Use FastAPI `/docs` to test endpoints
2. **Add automated tests later:** Use `pytest` + `httpx` for API tests
3. **Test each milestone:** Don't move on until current milestone works

### Debugging Tips

1. **Use print statements liberally** (or `logging.info`)
2. **Check `/docs` for request/response schemas**
3. **Read FastAPI error messages carefully**—they're helpful
4. **Use VS Code debugger** for complex issues

### Git Workflow (Simple)

```bash
# After completing each milestone
git add .
git commit -m "Milestone X: Brief description"

# Create a branch for experiments
git checkout -b experiment/feature-name

# Return to main when experiment works
git checkout main
git merge experiment/feature-name
```

### Recommended Development Order Within Each Milestone

1. **Define models/schemas** (data structures)
2. **Create service class** (business logic)
3. **Add storage/persistence** (if needed)
4. **Create API routes** (expose via HTTP)
5. **Test manually** via `/docs`
6. **Commit** when working

---

## Quick Reference: File Purposes

```
app/
├── main.py           # FastAPI app, startup, middleware
├── config.py         # Settings (URLs, feature flags)
├── api/
│   ├── jobs.py       # Job-related routes
│   └── health.py     # Health check endpoint
├── models/
│   ├── job.py        # Job, JobInput, JobResult
│   └── task.py       # Task, TaskPlan
├── services/
│   ├── orchestrator.py   # Creates task plans
│   ├── worker.py         # Executes tasks
│   ├── mcp_client.py     # Talks to MCP server
│   └── rai.py            # Validates outputs
└── storage/
    ├── base.py       # Storage interface
    ├── memory.py     # In-memory implementation
    └── job_store.py  # Job-specific storage
```

---

## Success Checklist

Before considering MVP "done":

- [ ] Can submit a job via POST request
- [ ] Job creates a task plan automatically
- [ ] Worker executes all tasks in plan
- [ ] Worker fetches context from MCP server
- [ ] Final output is validated by RAI service
- [ ] Can retrieve completed job with result
- [ ] Errors don't crash the server
- [ ] All code is committed to git

---

## Next Steps After MVP

1. **Add persistence:** PostgreSQL or SQLite
2. **Add async processing:** Background workers
3. **Add real MCP tools:** Multiple context sources
4. **Improve RAI:** LLM-based validation
5. **Add authentication:** API keys or OAuth
6. **Containerize:** Docker for deployment
7. **Add tests:** pytest for reliability

---

*Document created: MVP Roadmap v1.0*
*Stack: Python, FastAPI, VS Code, GitHub Copilot*
