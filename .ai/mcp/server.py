#!/usr/bin/env python3
"""MCP server for pattern-first framework"""

import asyncio
import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
import re

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Try to import MCP, provide instructions if not available
try:
    from mcp.server import Server, Request
    from mcp.server.models import InitializationOptions
    from mcp.types import (
        Resource, 
        Tool, 
        TextContent,
        ImageContent,
        EmbeddedResource
    )
    from mcp.server.stdio import stdio_server
except ImportError:
    print("MCP SDK not installed. Install with: pip install mcp")
    print("Or create a virtual environment first:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install mcp pyyaml")
    sys.exit(1)

# Import our existing framework components
from agents.base_agent import PatternFirstAgent
from agents.infrastructure import InfrastructureAgent
from agents.frontend_ui import FrontendUIAgent

class PatternFrameworkServer(Server):
    """MCP server that exposes pattern-first framework functionality"""
    
    def __init__(self):
        super().__init__("pattern-framework")
        self.patterns_dir = Path(".ai/patterns")
        self.philosophy_path = Path(".ai/philosophy.md")
        
        # Initialize agents
        self.agents = {
            'infrastructure': InfrastructureAgent(),
            'frontend': FrontendUIAgent()
        }
        
    async def initialize(self, options: InitializationOptions) -> None:
        """Initialize the server with capabilities"""
        # Register handlers
        self.request_handlers["resources/list"] = self.handle_list_resources
        self.request_handlers["resources/read"] = self.handle_read_resource
        self.request_handlers["tools/list"] = self.handle_list_tools
        self.request_handlers["tools/call"] = self.handle_call_tool
        
    async def handle_list_resources(self, request: Request) -> List[Resource]:
        """List all available patterns and philosophy as resources"""
        resources = []
        
        # Add philosophy as a resource
        if self.philosophy_path.exists():
            resources.append(Resource(
                uri="pattern-framework://philosophy",
                name="Philosophy",
                description="Framework philosophy and principles",
                mimeType="text/markdown"
            ))
        
        # Add all patterns as resources
        if self.patterns_dir.exists():
            for pattern_file in self.patterns_dir.rglob("*.md"):
                relative_path = pattern_file.relative_to(self.patterns_dir)
                
                # Try to extract task from frontmatter
                try:
                    content = pattern_file.read_text()
                    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                    if match:
                        metadata = yaml.safe_load(match.group(1))
                        task = metadata.get('task', pattern_file.stem)
                    else:
                        task = pattern_file.stem
                except:
                    task = pattern_file.stem
                
                resources.append(Resource(
                    uri=f"pattern-framework://patterns/{relative_path}",
                    name=str(relative_path),
                    description=f"Pattern: {task}",
                    mimeType="text/markdown"
                ))
        
        return resources
    
    async def handle_read_resource(self, request: Request) -> str:
        """Read a specific pattern or philosophy"""
        uri = request.params.get("uri")
        
        if uri == "pattern-framework://philosophy":
            if self.philosophy_path.exists():
                return self.philosophy_path.read_text()
            return "Philosophy file not found"
        
        if uri.startswith("pattern-framework://patterns/"):
            path = uri.replace("pattern-framework://patterns/", "")
            pattern_path = self.patterns_dir / path
            if pattern_path.exists():
                return pattern_path.read_text()
            return f"Pattern not found: {path}"
        
        raise ValueError(f"Resource not found: {uri}")
    
    async def handle_list_tools(self, request: Request) -> List[Tool]:
        """List available tools"""
        return [
            Tool(
                name="generate_from_pattern",
                description="Generate code using existing patterns",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "What to generate (e.g., 'create homepage', 'setup nextjs project')"
                        }
                    },
                    "required": ["task"]
                }
            ),
            Tool(
                name="search_patterns",
                description="Search for existing patterns",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "domain": {
                            "type": "string",
                            "enum": ["frontend", "infrastructure", "api", "database"],
                            "description": "Optional domain filter"
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="list_all_patterns",
                description="List all available patterns",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="validate_code",
                description="Validate code against framework philosophy",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Code to validate"
                        }
                    },
                    "required": ["code"]
                }
            ),
            Tool(
                name="get_pattern_instructions",
                description="Get instructions for creating a new pattern",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Task the pattern should solve"
                        },
                        "domain": {
                            "type": "string",
                            "enum": ["frontend", "infrastructure", "api", "database"],
                            "description": "Domain for the pattern"
                        }
                    },
                    "required": ["task", "domain"]
                }
            )
        ]
    
    async def handle_call_tool(self, request: Request) -> Any:
        """Execute tool calls"""
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        
        if tool_name == "generate_from_pattern":
            return await self.generate_from_pattern(arguments.get("task"))
        
        elif tool_name == "search_patterns":
            return await self.search_patterns(
                arguments.get("query"),
                arguments.get("domain")
            )
        
        elif tool_name == "list_all_patterns":
            return await self.list_all_patterns()
        
        elif tool_name == "validate_code":
            return await self.validate_code(arguments.get("code"))
        
        elif tool_name == "get_pattern_instructions":
            return await self.get_pattern_instructions(
                arguments.get("task"),
                arguments.get("domain")
            )
        
        raise ValueError(f"Unknown tool: {tool_name}")
    
    async def generate_from_pattern(self, task: str) -> Dict:
        """Generate code from patterns using existing agents"""
        # Determine which agent to use
        task_lower = task.lower()
        
        if any(keyword in task_lower for keyword in ['setup', 'install', 'deploy', 'config', 'nextjs', 'project']):
            agent = self.agents['infrastructure']
        else:
            agent = self.agents['frontend']
        
        try:
            # Use the agent's execute method
            result = agent.execute(task)
            
            return {
                "success": True,
                "code": result,
                "domain": agent.domain,
                "message": f"Generated code for: {task}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to generate code: {str(e)}",
                "suggestion": "Check if a pattern exists for this task or create one"
            }
    
    async def search_patterns(self, query: str, domain: Optional[str] = None) -> Dict:
        """Search for patterns"""
        results = []
        
        search_dirs = [self.patterns_dir / domain] if domain else [self.patterns_dir]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            for pattern_file in search_dir.rglob("*.md"):
                content = pattern_file.read_text()
                
                # Parse frontmatter
                match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
                if match:
                    try:
                        metadata = yaml.safe_load(match.group(1))
                        task = metadata.get('task', '')
                        
                        # Check if query matches task or content
                        if query.lower() in task.lower() or query.lower() in content.lower():
                            results.append({
                                "path": str(pattern_file.relative_to(self.patterns_dir)),
                                "task": task,
                                "domain": pattern_file.parent.name,
                                "complexity": metadata.get('complexity', 0),
                                "tags": metadata.get('tags', [])
                            })
                    except:
                        pass
        
        return {
            "count": len(results),
            "patterns": results,
            "message": f"Found {len(results)} patterns matching '{query}'"
        }
    
    async def list_all_patterns(self) -> Dict:
        """List all available patterns organized by domain"""
        patterns_by_domain = {}
        
        if not self.patterns_dir.exists():
            return {
                "patterns": {},
                "message": "No patterns directory found"
            }
        
        for pattern_file in self.patterns_dir.rglob("*.md"):
            domain = pattern_file.parent.name
            
            if domain not in patterns_by_domain:
                patterns_by_domain[domain] = []
            
            # Parse frontmatter to get task
            try:
                content = pattern_file.read_text()
                match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                if match:
                    metadata = yaml.safe_load(match.group(1))
                    task = metadata.get('task', pattern_file.stem)
                else:
                    task = pattern_file.stem
            except:
                task = pattern_file.stem
            
            patterns_by_domain[domain].append({
                "file": pattern_file.name,
                "task": task
            })
        
        return {
            "patterns": patterns_by_domain,
            "total": sum(len(patterns) for patterns in patterns_by_domain.values()),
            "message": "All available patterns"
        }
    
    async def validate_code(self, code: str) -> Dict:
        """Validate code against philosophy"""
        errors = []
        warnings = []
        
        # Check for incomplete sections
        if 'TODO' in code:
            errors.append("Code contains TODO markers")
        if '...' in code and '// ...' not in code and '# ...' not in code:
            errors.append("Code contains placeholder ellipsis")
        if 'pass' in code and not 'password' in code.lower():
            warnings.append("Code contains 'pass' statement")
        
        # Check for minimum complexity
        if len(code.strip()) < 50:
            errors.append("Code too short to be a complete solution")
        
        # Check for common anti-patterns
        if 'any' in code and 'typescript' in code.lower():
            warnings.append("Consider using specific types instead of 'any'")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "message": "Validation complete" if not errors else "Validation failed"
        }
    
    async def get_pattern_instructions(self, task: str, domain: str) -> Dict:
        """Get instructions for creating a new pattern"""
        return {
            "instructions": f"""
To create a pattern for: "{task}"

1. Create a new file: .ai/patterns/{domain}/{task.lower().replace(' ', '-')}.md

2. Use this structure:

---
task: {task}
complexity: 1-5
tags: [relevant, tags, here]
dependencies: [required, packages]
tech_stack: [technologies, used]
manual_steps: true/false
language: typescript/bash/python
---

# {task.title()}

## Description
What this pattern accomplishes and when to use it

## Setup Instructions
Prerequisites and environment setup needed

## Usage
How to use the generated code in a project

## Notes
Additional context, warnings, or considerations

## Code
```language
// Complete, working code here
// No TODOs or placeholders
// Must follow philosophy constraints
```

3. Ensure the code:
   - Solves exactly one problem completely
   - Works without modification
   - Uses existing libraries (no reinvention)
   - Is production-ready
   - Has explicit dependencies

4. Save the file and the pattern will be available for generation
""",
            "file_path": f".ai/patterns/{domain}/{task.lower().replace(' ', '-')}.md",
            "domain": domain,
            "task": task
        }

async def main():
    """Run the MCP server"""
    server = PatternFrameworkServer()
    
    # Run using stdio transport (for Claude Desktop)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pattern-framework",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())