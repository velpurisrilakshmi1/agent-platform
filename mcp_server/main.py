"""MCP Server implementation with context retrieval tool."""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create the MCP server
server = Server("agent-platform-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_context",
            description="Retrieve context information for a given query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to get context for"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_context":
        query = arguments.get("query", "")
        
        # Mock context retrieval for MVP
        # In production, this could query a knowledge base, database, or API
        context = f"""Context for query: "{query}"

This is mock context data from the MCP server.
In a real implementation, this could include:
- Relevant documents from a knowledge base
- Data from external APIs
- Information from databases
- Previously processed results

The context helps the agent make informed decisions and produce better outputs.
"""
        
        return [TextContent(type="text", text=context)]
    
    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
