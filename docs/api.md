# API Endpoints - How to Talk to the Platform

The API is how you interact with the platform over HTTP.

---

## Location: `app/api/jobs.py`

---

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### 1. Create a Job

**POST** `/jobs`

Submit a new job for processing. The platform will:
1. Create the job
2. Run the full pipeline (orchestrate → execute → validate)
3. Return the completed result

**Request:**
```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"data": {"query": "What is Python?"}}'
```

**Response (201 Created):**
```json
{
  "id": "71c57775-8a15-4c20-a63c-cc0843eb6a73",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "input_data": {"query": "What is Python?"},
  "result": {
    "job_id": "71c57775-8a15-4c20-a63c-cc0843eb6a73",
    "output": {
      "validated": true,
      "validation_notes": "All validation checks passed",
      "final_output": "Processed result for: What is Python?"
    },
    "validated": true,
    "validation_notes": "All validation checks passed"
  }
}
```

---

### 2. List All Jobs

**GET** `/jobs`

See all jobs that have been submitted.

**Request:**
```bash
curl http://localhost:8000/jobs
```

**Response (200 OK):**
```json
[
  {
    "id": "71c57775-...",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "input_data": {"query": "What is Python?"},
    "result": {...}
  },
  {
    "id": "abc-123-...",
    "status": "failed",
    "created_at": "2024-01-15T10:25:00",
    "input_data": {"query": "bad query"},
    "result": null
  }
]
```

---

### 3. Get Single Job

**GET** `/jobs/{job_id}`

Get details of a specific job by its ID.

**Request:**
```bash
curl http://localhost:8000/jobs/71c57775-8a15-4c20-a63c-cc0843eb6a73
```

**Response (200 OK):**
```json
{
  "id": "71c57775-8a15-4c20-a63c-cc0843eb6a73",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "input_data": {"query": "What is Python?"},
  "result": {...}
}
```

**Response (404 Not Found):**
```json
{"detail": "Job not found"}
```

---

### 4. Health Check

**GET** `/health`

Check if the platform is running.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Agent Orchestration Platform"
}
```

---

## Interactive Documentation

FastAPI automatically generates interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from your browser!

---

## Error Responses

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request (invalid input) |
| 404 | Not found |
| 500 | Internal server error |

**Error format:**
```json
{"detail": "Error message here"}
```

---

## Testing with PowerShell

```powershell
# Create a job
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/jobs" `
  -ContentType "application/json" `
  -Body '{"data": {"query": "Hello world"}}'

# List all jobs
Invoke-RestMethod -Uri "http://localhost:8000/jobs"

# Get specific job
Invoke-RestMethod -Uri "http://localhost:8000/jobs/YOUR-JOB-ID"
```
