# MCP Server - Context Provider

The MCP (Model Context Protocol) server provides external context to help process jobs.

---

## Location: `mcp_server/main.py`

---

## What is MCP?

MCP is a protocol for AI systems to access external tools and data sources.

**Think of it as:** A way for the worker to ask for help or look things up.

---

## What Our MCP Server Does

Provides a single tool: `get_context`

```
Worker: "I need context for 'What is Python?'"
    ↓
MCP Server: "Here's relevant information about Python..."
    ↓
Worker: "Thanks, now I can give a better answer"
```

---

## The Tool

### `get_context`

**Input:**
```json
{"query": "What is Python?"}
```

**Output:**
```
Context for query: "What is Python?"

This is mock context data from the MCP server.
In a real implementation, this could include:
- Relevant documents from a knowledge base
- Data from external APIs
- Information from databases
- Previously processed results
```

---

## How It Works

### Server Side (`mcp_server/main.py`)

```python
# Define available tools
@server.list_tools()
async def list_tools():
    return [Tool(name="get_context", ...)]

# Handle tool calls
@server.call_tool()
async def call_tool(name, arguments):
    if name == "get_context":
        query = arguments["query"]
        return context_for_query(query)
```

### Client Side (`app/services/mcp_client.py`)

```python
# Call the MCP server
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        result = await session.call_tool("get_context", {"query": query})
```

---

## Running the MCP Server

The MCP server runs as a subprocess when the worker needs context:

```
Worker starts
    ↓
Need context? → Start MCP server process
    ↓
Call "get_context" tool
    ↓
Get response → MCP process ends
```

---

## Communication

MCP uses **stdio** (standard input/output) for communication:

```
┌────────────┐  stdin   ┌────────────┐
│   Worker   │─────────▶│ MCP Server │
│  (Client)  │◀─────────│            │
└────────────┘  stdout  └────────────┘
```

---

## Future Enhancements

The MVP uses mock data. In production, you could:

| Enhancement | What it does |
|-------------|--------------|
| Knowledge base | Search documents for relevant info |
| Database queries | Look up stored data |
| Web search | Find current information online |
| API calls | Get data from external services |
| Embeddings | Use AI to find semantically similar content |

### Example: Real Knowledge Base

```python
@server.call_tool()
async def call_tool(name, arguments):
    if name == "get_context":
        query = arguments["query"]
        
        # Search vector database
        results = vector_db.search(query, limit=5)
        
        # Format as context
        context = "\n".join([r.text for r in results])
        
        return [TextContent(type="text", text=context)]
```

---

## Why MCP?

1. **Standardized protocol** - Works with many AI systems
2. **Extensible** - Easy to add new tools
3. **Secure** - Tools run in controlled environment
4. **Modular** - Can swap implementations easily

---

## Testing

Run the MCP server directly:
```bash
python -m mcp_server.main
```

Or test through the worker:
```python
from app.services.mcp_client import get_mcp_client

client = get_mcp_client()
context = client.get_context_sync("What is Python?")
print(context)
```
