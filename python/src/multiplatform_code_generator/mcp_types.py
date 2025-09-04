"""
Simplified MCP types and protocol implementation.
"""

import json
import sys
import asyncio
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from pydantic import BaseModel


class Tool(BaseModel):
    """MCP Tool definition."""
    name: str
    description: str
    inputSchema: Dict[str, Any]


class TextContent(BaseModel):
    """Text content for MCP responses."""
    type: str = "text"
    text: str


class CallToolResult(BaseModel):
    """Result of a tool call."""
    content: List[TextContent]


@dataclass
class MCPRequest:
    """MCP request message."""
    jsonrpc: str
    id: Union[str, int]
    method: str
    params: Optional[Dict[str, Any]] = None


@dataclass 
class MCPResponse:
    """MCP response message."""
    jsonrpc: str
    id: Union[str, int]
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class SimpleMCPServer:
    """Simplified MCP server implementation."""
    
    def __init__(self, name: str):
        """Initialize the server."""
        self.name = name
        self.tools: List[Tool] = []
        self.tool_handlers: Dict[str, callable] = {}
        
    def add_tool(self, tool: Tool, handler: callable):
        """Add a tool and its handler."""
        self.tools.append(tool)
        self.tool_handlers[tool.name] = handler
    
    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an MCP request."""
        try:
            request = MCPRequest(**request_data)
            
            if request.method == "tools/list":
                return self._create_response(request.id, {
                    "tools": [tool.dict() for tool in self.tools]
                })
            
            elif request.method == "tools/call":
                tool_name = request.params.get("name")
                arguments = request.params.get("arguments", {})
                
                if tool_name not in self.tool_handlers:
                    return self._create_error_response(request.id, f"Unknown tool: {tool_name}")
                
                try:
                    result = await self.tool_handlers[tool_name](arguments)
                    return self._create_response(request.id, result.dict())
                except Exception as e:
                    return self._create_error_response(request.id, str(e))
            
            else:
                return self._create_error_response(request.id, f"Unknown method: {request.method}")
                
        except Exception as e:
            return self._create_error_response(getattr(request, 'id', 0), f"Invalid request: {e}")
    
    def _create_response(self, request_id: Union[str, int], result: Dict[str, Any]) -> Dict[str, Any]:
        """Create a success response."""
        response = MCPResponse(jsonrpc="2.0", id=request_id, result=result)
        return asdict(response)
    
    def _create_error_response(self, request_id: Union[str, int], error_message: str) -> Dict[str, Any]:
        """Create an error response."""
        response = MCPResponse(
            jsonrpc="2.0", 
            id=request_id, 
            error={"code": -1, "message": error_message}
        )
        return asdict(response)
    
    async def run_stdio(self):
        """Run the server using stdio transport."""
        print(f"🚀 {self.name} MCP server started on stdio", file=sys.stderr)
        
        try:
            while True:
                # Read request from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request_data = json.loads(line)
                    response = await self.handle_request(request_data)
                    
                    # Write response to stdout
                    print(json.dumps(response), flush=True)
                    
                except json.JSONDecodeError as e:
                    error_response = self._create_error_response(0, f"Invalid JSON: {e}")
                    print(json.dumps(error_response), flush=True)
                
        except KeyboardInterrupt:
            pass
        finally:
            print("🛑 MCP server stopped", file=sys.stderr)
