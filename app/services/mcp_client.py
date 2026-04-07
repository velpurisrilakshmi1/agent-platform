"""MCP Client for communicating with the MCP server."""

import asyncio
import subprocess
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """Client for communicating with the MCP server."""
    
    def __init__(self, server_script: str = "mcp_server/main.py"):
        self.server_script = server_script
        self._session: ClientSession | None = None
    
    async def get_context(self, query: str) -> dict[str, Any]:
        """
        Get context for a query from the MCP server.
        
        Starts the MCP server, calls the get_context tool, and returns the result.
        """
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[self.server_script],
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                # Call the get_context tool
                result = await session.call_tool("get_context", {"query": query})
                
                # Extract text content from the result
                context_text = ""
                for content in result.content:
                    if hasattr(content, 'text'):
                        context_text += content.text
                
                return {
                    "query": query,
                    "context": context_text,
                    "source": "mcp_server"
                }
    
    def get_context_sync(self, query: str) -> dict[str, Any]:
        """Synchronous wrapper for get_context."""
        return asyncio.run(self.get_context(query))


# Singleton instance
_mcp_client: MCPClient | None = None


def get_mcp_client() -> MCPClient:
    """Get or create the MCP client singleton."""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client
