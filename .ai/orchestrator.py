#!/usr/bin/env python3
import sys
import os
sys.path.append('.ai')

from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

from agents.infrastructure import InfrastructureAgent
from agents.frontend_ui import FrontendUIAgent

class Orchestrator:
    """Coordinates agent selection and multi-agent workflows"""
    
    def __init__(self):
        self.agents = self.initialize_agents()
    
    def initialize_agents(self) -> Dict:
        """Initialize all available agents"""
        return {
            'infrastructure': InfrastructureAgent(),
            'frontend_ui': FrontendUIAgent()
        }
    
    def determine_agent(self, task: str) -> str:
        """Determine which agent should handle the task"""
        task_lower = task.lower()
        
        # Keywords for agent selection
        agent_keywords = {
            'infrastructure': ['setup', 'install', 'deploy', 'config', 'build', 'nextjs', 'next.js', 'project'],
            'frontend_ui': ['component', 'ui', 'button', 'form', 'layout', 'page', 'homepage', 'navigation']
        }
        
        for agent_name, keywords in agent_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                return agent_name
        
        # Default to frontend for UI tasks
        return 'frontend_ui'
    
    def execute_task(self, task: str) -> str:
        """Execute task with appropriate agent"""
        agent_name = self.determine_agent(task)
        print(f"\n🔍 Using {agent_name} agent for: {task}\n")
        
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")
        
        return agent.execute(task)
    
    def create_pattern(self, task: str) -> str:
        """Pattern creation is manual - provide instructions"""
        agent_name = self.determine_agent(task)
        domain = agent_name.replace('_', '')  # Convert frontend_ui to frontend
        
        return f"""
Pattern creation is a manual process to ensure philosophical alignment.

To create a pattern for: "{task}"

1. Create a new file in: .ai/patterns/{domain}/
2. Follow this structure:

---
task: {task}
complexity: 1-5
tags: [relevant, tags]
dependencies: [required, packages]
tech_stack: [technologies, used]
manual_steps: true/false
language: typescript/bash/python
---

# {task.title()}

## Description
What this pattern accomplishes

## Setup Instructions  
Prerequisites and environment setup

## Usage
How to use the generated code

## Notes
Additional context and considerations

## Code
```language
[Complete working code here]
```

3. Ensure the code is complete, tested, and follows philosophy
4. Save the file with a descriptive name
"""
    
    def search_patterns(self, query: str) -> List[str]:
        """Search all patterns across all domains"""
        results = []
        patterns_dir = Path(".ai/patterns")
        
        if not patterns_dir.exists():
            return ["No patterns directory found"]
        
        for pattern_file in patterns_dir.rglob("*.md"):
            content = pattern_file.read_text()
            if query.lower() in content.lower():
                results.append(str(pattern_file.relative_to(patterns_dir)))
        
        return results if results else ["No patterns found matching query"]
    
    def list_patterns(self) -> List[str]:
        """List all available patterns"""
        patterns_dir = Path(".ai/patterns")
        
        if not patterns_dir.exists():
            return ["No patterns directory found"]
        
        patterns = []
        for pattern_file in patterns_dir.rglob("*.md"):
            patterns.append(str(pattern_file.relative_to(patterns_dir)))
        
        return patterns if patterns else ["No patterns created yet"]

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("""
Pattern-First Framework Orchestrator

Usage:
  python .ai/orchestrator.py generate <task>    Generate code from patterns
  python .ai/orchestrator.py create <task>      Create a new pattern
  python .ai/orchestrator.py search <query>     Search existing patterns
  python .ai/orchestrator.py list               List all patterns

Examples:
  python .ai/orchestrator.py generate "setup nextjs project"
  python .ai/orchestrator.py generate "create homepage"
  python .ai/orchestrator.py create "create navigation component"
  python .ai/orchestrator.py search "homepage"
        """)
        sys.exit(1)
    
    orchestrator = Orchestrator()
    command = sys.argv[1]
    
    if command == "generate" and len(sys.argv) > 2:
        task = " ".join(sys.argv[2:])
        result = orchestrator.execute_task(task)
        print(result)
    
    elif command == "create" and len(sys.argv) > 2:
        task = " ".join(sys.argv[2:])
        result = orchestrator.create_pattern(task)
        print(result)
    
    elif command == "search" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        results = orchestrator.search_patterns(query)
        print(f"\n📚 Pattern search results for '{query}':")
        for result in results:
            print(f"  - {result}")
    
    elif command == "list":
        patterns = orchestrator.list_patterns()
        print("\n📚 Available patterns:")
        for pattern in patterns:
            print(f"  - {pattern}")
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see usage")
        sys.exit(1)

if __name__ == "__main__":
    main()