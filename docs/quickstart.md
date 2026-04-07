# Quick Start Guide

Get the Agent Platform running in 5 minutes!

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/velpurisrilakshmi1/agent-platform.git
cd agent-platform
```

---

## Step 2: Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Start the Server

**Windows:**
```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

**Mac/Linux:**
```bash
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Step 5: Test It!

### Option A: Browser
Open http://localhost:8000/docs for interactive testing.

### Option B: Command Line

**Create a job:**
```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"data": {"query": "What is Python?"}}'
```

**PowerShell:**
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/jobs" `
  -ContentType "application/json" `
  -Body '{"data": {"query": "What is Python?"}}'
```

---

## Expected Response

```json
{
  "id": "abc123...",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "input_data": {"query": "What is Python?"},
  "result": {
    "validated": true,
    "validation_notes": "All validation checks passed",
    "final_output": "Processed result for: What is Python?"
  }
}
```

---

## What Just Happened?

1. ✅ You submitted a job
2. ✅ Orchestrator created a 3-task plan
3. ✅ Worker fetched context from MCP server
4. ✅ Worker processed your query
5. ✅ RAI service validated the output
6. ✅ You got the result!

---

## Common Commands

| Task | Command |
|------|---------|
| Start server | `uvicorn app.main:app --reload` |
| Run tests | `pytest` |
| Check health | `curl http://localhost:8000/health` |
| View logs | Check terminal output |
| Stop server | `Ctrl+C` |

---

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
uvicorn app.main:app --reload --port 8001
```

### "venv not activated"
Make sure you see `(venv)` in your terminal prompt.

---

## Next Steps

1. **Read the docs** - Check other files in `/docs`
2. **Try the API** - Visit http://localhost:8000/docs
3. **Explore the code** - Start with `app/main.py`
4. **Make changes** - Server auto-reloads!

---

## Project Structure

```
agent-platform/
├── app/
│   ├── api/          # HTTP endpoints
│   ├── models/       # Data structures
│   ├── services/     # Business logic
│   └── storage/      # Data storage
├── mcp_server/       # Context provider
├── docs/             # You are here!
└── tests/            # Test files
```

---

## Need Help?

- Check the [Architecture Overview](architecture.md)
- Read about [Services](services.md)
- See the [API Documentation](api.md)
