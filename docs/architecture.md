# Agent Platform - Architecture Overview

This document explains how the entire platform works in simple terms.

## What Does This Platform Do?

Think of this platform as a smart assistant factory:
1. You give it a **job** (a question or task)
2. It **plans** how to handle it
3. It **fetches** helpful information
4. It **processes** your request
5. It **validates** the output is safe
6. It gives you the **result**

---

## The Flow (Step by Step)

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   You       │────▶│   Job API    │────▶│ Orchestrator│────▶│   Worker    │
│  (Submit)   │     │  (Receives)  │     │  (Plans)    │     │ (Executes)  │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
                                                                    │
                           ┌────────────────────────────────────────┘
                           ▼
                    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                    │ MCP Server  │────▶│  Processor  │────▶│ RAI Service │
                    │  (Context)  │     │ (Processes) │     │ (Validates) │
                    └─────────────┘     └─────────────┘     └─────────────┘
                                                                    │
                           ┌────────────────────────────────────────┘
                           ▼
                    ┌─────────────┐
                    │   Result    │
                    │ (Returned)  │
                    └─────────────┘
```

---

## Key Components

### 1. **Job API** (`app/api/jobs.py`)
The front door. Users submit jobs here and get results back.

### 2. **Orchestrator** (`app/services/orchestrator.py`)
The planner. Takes a job and creates a step-by-step plan (tasks).

### 3. **Worker Agent** (`app/services/worker.py`)
The doer. Executes each task in the plan one by one.

### 4. **MCP Server** (`mcp_server/main.py`)
The knowledge source. Provides context/information to help process the job.

### 5. **RAI Service** (`app/services/rai.py`)
The safety checker. Makes sure output is safe and appropriate.

### 6. **Job Processor** (`app/services/job_processor.py`)
The coordinator. Ties everything together and runs the full pipeline.

### 7. **Storage** (`app/storage/`)
The memory. Keeps track of all jobs and tasks (in-memory for MVP).

---

## Example Walkthrough

**You send:** `{"data": {"query": "What is Python?"}}`

1. **Job API** creates a new Job with ID `abc-123`
2. **Orchestrator** creates 3 tasks: fetch_context → process → validate
3. **Worker** runs each task:
   - Task 1: Gets context from MCP Server
   - Task 2: Processes the query with context
   - Task 3: Validates output with RAI Service
4. **Result** returned: `"Processed result for: What is Python?"`

---

## Folder Structure

```
agent-platform/
├── app/                    # Main application code
│   ├── api/                # HTTP endpoints (the front door)
│   ├── models/             # Data structures (Job, Task, etc.)
│   ├── services/           # Business logic (the brains)
│   └── storage/            # Data storage (the memory)
├── mcp_server/             # External context provider
├── tests/                  # Test files
└── docs/                   # Documentation (you are here)
```

---

## What's Next After MVP?

- **Database**: Replace in-memory storage with PostgreSQL
- **Async Processing**: Handle long-running jobs in background
- **Authentication**: Add user accounts and API keys
- **Real AI**: Connect to LLMs for smarter processing
- **Docker**: Package for easy deployment
