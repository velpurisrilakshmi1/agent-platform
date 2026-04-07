# Autonomous Agent Orchestration Platform

An MVP platform where users can submit jobs that are orchestrated by an agent system with MCP integration and RAI validation.

## Quick Start

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000/docs to see the API documentation.

## Project Structure

```
agent-platform/
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── config.py         # Settings
│   ├── api/              # Route handlers
│   ├── models/           # Pydantic schemas
│   ├── services/         # Business logic
│   └── storage/          # Data persistence
├── mcp_server/           # MCP server implementation
├── tests/                # Test files
├── docs/                 # Documentation
└── requirements.txt
```

## Development

See [docs/mvp_roadmap.md](docs/mvp_roadmap.md) for the development roadmap.
