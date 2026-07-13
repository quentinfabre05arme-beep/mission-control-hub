#!/usr/bin/env python3
"""
mcp_tool_registry.py
Model Context Protocol (MCP) Tool Registry
Based on 2025-2026 MCP Standard Research

Features:
- MCP-standardized tool definitions
- Universal tool integration for agents
- Cross-agent tool sharing
- Deterministic guardrails
- Observable action logging
"""

import json
from typing import Dict, List, Any, Optional, Callable, Type
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    WEB = "web"                    # Web search, fetch
    MEMORY = "memory"              # Memory search, retrieval
    COMMUNICATION = "communication"  # Messaging, notifications
    DATA = "data"                  # Data processing, analysis
    CONTENT = "content"            # Content generation, editing
    AUTOMATION = "automation"      # Scheduling, cron jobs
    SOCIAL = "social"                # Social media interactions
    SYSTEM = "system"              # System commands, files


class ToolPermission(Enum):
    READ = "read"                  # Read-only operations
    WRITE = "write"                # Write operations
    EXECUTE = "execute"            # Execute commands
    ADMIN = "admin"                # Administrative operations


@dataclass
class MCPTool:
    """MCP-compliant tool definition"""
    name: str
    description: str
    category: ToolCategory
    input_schema: Dict[str, Any]  # JSON Schema
    output_schema: Dict[str, Any]  # JSON Schema
    handler: Optional[Callable] = None
    permissions: List[ToolPermission] = field(default_factory=lambda: [ToolPermission.READ])
    rate_limit: Optional[int] = None  # Calls per minute
    requires_approval: bool = False
    registered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "permissions": [p.value for p in self.permissions],
            "rate_limit": self.rate_limit,
            "requires_approval": self.requires_approval,
            "registered_at": self.registered_at
        }


@dataclass
class ToolExecution:
    """Record of tool execution"""
    execution_id: str
    tool_name: str
    agent_id: str
    inputs: Dict[str, Any]
    outputs: Any
    success: bool
    error_message: Optional[str]
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "execution_id": self.execution_id,
            "tool_name": self.tool_name,
            "agent_id": self.agent_id,
            "inputs": self.inputs,
            "outputs": self.outputs if self.success else None,
            "success": self.success,
            "error_message": self.error_message,
            "duration_ms": round(self.duration_ms, 2),
            "timestamp": self.timestamp
        }


class MCPToolRegistry:
    """
    Model Context Protocol Tool Registry
    Implements universal tool standard for AI agents
    """
    
    def __init__(self):
        self.tools: Dict[str, MCPTool] = {}
        self.execution_log: List[ToolExecution] = []
        self.agent_permissions: Dict[str, Dict[str, List[ToolPermission]]] = {}
        
        # Register built-in tools
        self._register_builtin_tools()
        
        logger.info("MCP Tool Registry initialized")
    
    def _register_builtin_tools(self):
        """Register built-in standard tools"""
        
        # Web search tool
        self.register_tool(MCPTool(
            name="web_search",
            description="Search the web for current information",
            category=ToolCategory.WEB,
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "count": {"type": "integer", "description": "Number of results", "default": 10},
                    "freshness": {"type": "string", "enum": ["day", "week", "month", "year"], "default": "week"}
                },
                "required": ["query"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "snippet": {"type": "string"}
                            }
                        }
                    },
                    "total_results": {"type": "integer"}
                }
            },
            permissions=[ToolPermission.READ]
        ))
        
        # Web fetch tool
        self.register_tool(MCPTool(
            name="web_fetch",
            description="Fetch and extract content from a URL",
            category=ToolCategory.WEB,
            input_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to fetch"},
                    "extract_mode": {"type": "string", "enum": ["markdown", "text", "html"], "default": "markdown"},
                    "max_chars": {"type": "integer", "description": "Maximum characters to return", "default": 5000}
                },
                "required": ["url"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "title": {"type": "string"},
                    "url": {"type": "string"}
                }
            },
            permissions=[ToolPermission.READ]
        ))
        
        # Memory search tool
        self.register_tool(MCPTool(
            name="memory_search",
            description="Search long-term memory for relevant information",
            category=ToolCategory.MEMORY,
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "corpus": {"type": "string", "enum": ["memory", "sessions", "all"], "default": "memory"},
                    "max_results": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"},
                                "source": {"type": "string"},
                                "relevance_score": {"type": "number"}
                            }
                        }
                    }
                }
            },
            permissions=[ToolPermission.READ]
        ))
        
        # Memory get tool
        self.register_tool(MCPTool(
            name="memory_get",
            description="Read specific content from memory",
            category=ToolCategory.MEMORY,
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to memory file"},
                    "corpus": {"type": "string", "default": "memory"},
                    "from": {"type": "integer", "description": "Starting line", "default": 1},
                    "lines": {"type": "integer", "description": "Number of lines", "default": 100}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "path": {"type": "string"},
                    "truncated": {"type": "boolean"}
                }
            },
            permissions=[ToolPermission.READ]
        ))
        
        # File read tool
        self.register_tool(MCPTool(
            name="file_read",
            description="Read content from a file",
            category=ToolCategory.SYSTEM,
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "offset": {"type": "integer", "description": "Starting line", "default": 1},
                    "limit": {"type": "integer", "description": "Maximum lines", "default": 2000}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "path": {"type": "string"},
                    "truncated": {"type": "boolean"}
                }
            },
            permissions=[ToolPermission.READ]
        ))
        
        # File write tool
        self.register_tool(MCPTool(
            name="file_write",
            description="Write content to a file",
            category=ToolCategory.SYSTEM,
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "path": {"type": "string"},
                    "bytes_written": {"type": "integer"}
                }
            },
            permissions=[ToolPermission.WRITE],
            requires_approval=True
        ))
        
        # Cron job tool
        self.register_tool(MCPTool(
            name="cron_add",
            description="Add a new cron job",
            category=ToolCategory.AUTOMATION,
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Job name"},
                    "schedule": {"type": "object", "description": "Schedule configuration"},
                    "payload": {"type": "object", "description": "Job payload"}
                },
                "required": ["name", "schedule", "payload"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "job_id": {"type": "string"}
                }
            },
            permissions=[ToolPermission.EXECUTE],
            requires_approval=True
        ))
        
        # Content optimization tool
        self.register_tool(MCPTool(
            name="content_optimize",
            description="Optimize content for specific platforms",
            category=ToolCategory.CONTENT,
            input_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to optimize"},
                    "platform": {"type": "string", "enum": ["x", "linkedin", "general"], "default": "general"},
                    "content_type": {"type": "string", "enum": ["text", "image", "video", "thread"], "default": "text"}
                },
                "required": ["content"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "optimized_content": {"type": "string"},
                    "recommendations": {"type": "array", "items": {"type": "string"}},
                    "score": {"type": "number"}
                }
            },
            permissions=[ToolPermission.READ]
        ))
    
    def register_tool(self, tool: MCPTool) -> bool:
        """
        Register a new MCP-compliant tool
        
        Args:
            tool: MCPTool definition
        
        Returns:
            True if registered successfully
        """
        if tool.name in self.tools:
            logger.warning(f"Tool {tool.name} already registered, updating")
        
        self.tools[tool.name] = tool
        logger.info(f"Registered MCP tool: {tool.name} ({tool.category.value})")
        return True
    
    def get_tool(self, tool_name: str) -> Optional[MCPTool]:
        """Get tool by name"""
        return self.tools.get(tool_name)
    
    def list_tools(self, category: Optional[ToolCategory] = None) -> List[MCPTool]:
        """List all tools, optionally filtered by category"""
        if category:
            return [t for t in self.tools.values() if t.category == category]
        return list(self.tools.values())
    
    def grant_permissions(self, agent_id: str, tool_name: str, 
                         permissions: List[ToolPermission]):
        """Grant permissions to an agent for a tool"""
        if agent_id not in self.agent_permissions:
            self.agent_permissions[agent_id] = {}
        
        self.agent_permissions[agent_id][tool_name] = permissions
        logger.info(f"Granted {permissions} to {agent_id} for {tool_name}")
    
    def check_permission(self, agent_id: str, tool_name: str,
                        required: ToolPermission) -> bool:
        """Check if agent has permission for a tool"""
        agent_perms = self.agent_permissions.get(agent_id, {})
        tool_perms = agent_perms.get(tool_name, [])
        
        # Admin permission grants all
        if ToolPermission.ADMIN in tool_perms:
            return True
        
        # Write includes Read
        if required == ToolPermission.READ and ToolPermission.WRITE in tool_perms:
            return True
        
        return required in tool_perms
    
    def execute_tool(self, tool_name: str, agent_id: str,
                    inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool
        
        Args:
            tool_name: Name of the tool
            agent_id: ID of the executing agent
            inputs: Tool inputs
        
        Returns:
            Execution result
        """
        import time
        
        tool = self.get_tool(tool_name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool not found: {tool_name}"
            }
        
        # Validate inputs against schema
        validation = self._validate_inputs(inputs, tool.input_schema)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Invalid inputs: {validation['errors']}"
            }
        
        # Check permissions
        if not self.check_permission(agent_id, tool_name, ToolPermission.EXECUTE):
            if tool.permissions and ToolPermission.EXECUTE in tool.permissions:
                return {
                    "success": False,
                    "error": f"Agent {agent_id} lacks EXECUTE permission for {tool_name}"
                }
        
        # Check if approval required
        if tool.requires_approval:
            # In production, would queue for approval
            logger.warning(f"Tool {tool_name} requires approval, executing with audit")
        
        # Execute
        start_time = time.time()
        execution_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        
        try:
            if tool.handler:
                outputs = tool.handler(**inputs)
                success = True
                error_message = None
            else:
                # Simulated execution for demo
                outputs = {"status": "simulated", "tool": tool_name}
                success = True
                error_message = None
                
        except Exception as e:
            outputs = None
            success = False
            error_message = str(e)
        
        duration_ms = (time.time() - start_time) * 1000
        
        # Log execution
        execution = ToolExecution(
            execution_id=execution_id,
            tool_name=tool_name,
            agent_id=agent_id,
            inputs=inputs,
            outputs=outputs,
            success=success,
            error_message=error_message,
            duration_ms=duration_ms
        )
        self.execution_log.append(execution)
        
        if success:
            logger.info(f"Tool {tool_name} executed in {duration_ms:.2f}ms")
        else:
            logger.error(f"Tool {tool_name} failed: {error_message}")
        
        return {
            "success": success,
            "execution_id": execution_id,
            "outputs": outputs,
            "error": error_message,
            "duration_ms": duration_ms
        }
    
    def _validate_inputs(self, inputs: Dict, schema: Dict) -> Dict:
        """Validate inputs against JSON schema"""
        errors = []
        
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        
        # Check required fields
        for field in required:
            if field not in inputs:
                errors.append(f"Missing required field: {field}")
        
        # Validate types (simplified)
        for field, value in inputs.items():
            if field in properties:
                expected_type = properties[field].get("type")
                if expected_type == "string" and not isinstance(value, str):
                    errors.append(f"Field {field} should be string")
                elif expected_type == "integer" and not isinstance(value, int):
                    errors.append(f"Field {field} should be integer")
                elif expected_type == "object" and not isinstance(value, dict):
                    errors.append(f"Field {field} should be object")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def get_execution_log(self, agent_id: Optional[str] = None,
                         tool_name: Optional[str] = None) -> List[ToolExecution]:
        """Get execution log with optional filters"""
        filtered = self.execution_log
        
        if agent_id:
            filtered = [e for e in filtered if e.agent_id == agent_id]
        
        if tool_name:
            filtered = [e for e in filtered if e.tool_name == tool_name]
        
        return filtered
    
    def export_registry(self) -> Dict:
        """Export full registry state"""
        return {
            "tools": {name: tool.to_dict() for name, tool in self.tools.items()},
            "tool_count": len(self.tools),
            "execution_count": len(self.execution_log),
            "registered_at": datetime.utcnow().isoformat()
        }
    
    def generate_tool_manifest(self) -> str:
        """Generate tool manifest for agent consumption"""
        manifest = {
            "schema_version": "1.0",
            "protocol": "mcp",
            "tools": [tool.to_dict() for tool in self.tools.values()],
            "categories": list(set(t.category.value for t in self.tools.values()))
        }
        return json.dumps(manifest, indent=2)


# Example usage
if __name__ == "__main__":
    # Initialize registry
    registry = MCPToolRegistry()
    
    print("=" * 60)
    print("MCP TOOL REGISTRY")
    print("=" * 60)
    
    # List all tools
    print("\nREGISTERED TOOLS:")
    for tool in registry.list_tools():
        print(f"- {tool.name}: {tool.description}")
        print(f"  Category: {tool.category.value}")
        print(f"  Permissions: {[p.value for p in tool.permissions]}")
        print(f"  Requires approval: {tool.requires_approval}")
        print()
    
    # List by category
    print("\nWEB TOOLS:")
    web_tools = registry.list_tools(ToolCategory.WEB)
    for tool in web_tools:
        print(f"- {tool.name}")
    
    # Generate manifest
    print("\n" + "=" * 60)
    print("TOOL MANIFEST (for agents):")
    print("=" * 60)
    print(registry.generate_tool_manifest())
    
    # Simulate execution
    print("\n" + "=" * 60)
    print("SIMULATED TOOL EXECUTION:")
    print("=" * 60)
    
    result = registry.execute_tool(
        tool_name="web_search",
        agent_id="research_agent_001",
        inputs={"query": "AI agent capabilities 2026", "count": 5}
    )
    
    print(json.dumps(result, indent=2))
    
    # Check execution log
    print("\n" + "=" * 60)
    print("EXECUTION LOG:")
    print("=" * 60)
    
    for execution in registry.get_execution_log():
        print(f"{execution.tool_name}: {execution.timestamp} - {'✅' if execution.success else '❌'}")
