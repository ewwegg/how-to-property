# Framework Implementation Guide

## Repository Structure

### Complete Project Layout

```
your-project/
├── .ai/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Abstract base class
│   │   ├── infrastructure.py     # Project setup agent
│   │   ├── frontend_ui.py        # UI component agent
│   │   ├── frontend_logic.py     # Client logic agent
│   │   ├── api.py               # Backend API agent
│   │   └── database.py          # Database operations agent
│   ├── patterns/
│   │   ├── infrastructure/
│   │   ├── frontend/
│   │   ├── api/
│   │   └── database/
│   ├── lib/
│   │   ├── vector_search.py     # LanceDB implementation
│   │   ├── pattern_validator.py # Pattern validation logic
│   │   └── metrics.py          # Usage tracking
│   ├── philosophy.md
│   ├── orchestrator.py          # Main coordinator
│   ├── config.yaml             # Framework configuration
│   └── .lancedb/              # Vector database storage
├── .claude/
│   └── claude.yaml            # Claude Code CLI config
├── .env                       # API keys
└── [your project files]
```

### Initial Setup Script

Create `.ai/setup.sh`:

```bash
#!/bin/bash

# Create directory structure
mkdir -p .ai/{agents,patterns,lib}
mkdir -p .ai/patterns/{infrastructure,frontend,api,database}
mkdir -p .claude

# Initialize Python package
touch .ai/__init__.py
touch .ai/agents/__init__.py

# Install Python dependencies
uv pip install anthropic lancedb sentence-transformers pyyaml

# Create config file
cat > .ai/config.yaml << 'EOF'
framework:
  version: "1.0.0"
  pattern_min_size: 50  # Minimum characters for valid pattern
  max_search_results: 5
  embedding_model: "all-MiniLM-L6-v2"

agents:
  enabled:
    - infrastructure
    - frontend_ui
    - frontend_logic
    - api
    - database

validation:
  enforce_philosophy: true
  require_manual_approval: false
  max_complexity: 5
EOF

echo "Framework initialized successfully"
```

## Claude Code CLI Integration

### Configuration File

Create `.claude/claude.yaml`:

```yaml
version: 1
project_context: |
  This project uses a pattern-first AI code generation framework.
  All code is generated from validated patterns that follow our philosophy.

slash_commands:
  - name: "generate"
    command: "python .ai/orchestrator.py generate"
    description: "Generate code from patterns"
    args:
      - name: "task"
        description: "What to generate"
        required: true

  - name: "pattern"
    command: "python .ai/orchestrator.py create-pattern"
    description: "Create a new pattern"
    args:
      - name: "task"
        description: "Pattern to create"
        required: true

  - name: "search"
    command: "python .ai/orchestrator.py search"
    description: "Search existing patterns"
    args:
      - name: "query"
        description: "Search query"
        required: true

  - name: "setup"
    command: "bash .ai/setup.sh"
    description: "Initialize framework"

default_command: "generate"

environment:
  ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
  PYTHONPATH: ".ai:${PYTHONPATH}"
```

### Orchestrator Implementation

Create `.ai/orchestrator.py`:

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["anthropic", "lancedb", "sentence-transformers", "pyyaml", "click"]
# ///

import click
import yaml
from pathlib import Path
from typing import Optional, Dict, List
import sys

from agents.infrastructure import InfrastructureAgent
from agents.frontend_ui import FrontendUIAgent
from agents.api import APIAgent
from agents.database import DatabaseAgent

class Orchestrator:
    """Coordinates agent selection and multi-agent workflows"""

    def __init__(self):
        self.config = self.load_config()
        self.agents = self.initialize_agents()

    def load_config(self) -> dict:
        config_path = Path(".ai/config.yaml")
        if config_path.exists():
            return yaml.safe_load(config_path.read_text())
        return {}

    def initialize_agents(self) -> Dict:
        """Initialize all available agents"""
        return {
            'infrastructure': InfrastructureAgent(),
            'frontend_ui': FrontendUIAgent(),
            'api': APIAgent(),
            'database': DatabaseAgent()
        }

    def determine_agent(self, task: str) -> str:
        """Determine which agent should handle the task"""
        task_lower = task.lower()

        # Keywords for agent selection
        agent_keywords = {
            'infrastructure': ['setup', 'install', 'deploy', 'config', 'build'],
            'frontend_ui': ['component', 'ui', 'button', 'form', 'layout', 'page'],
            'api': ['endpoint', 'route', 'api', 'server', 'middleware'],
            'database': ['schema', 'model', 'migration', 'query', 'prisma']
        }

        for agent_name, keywords in agent_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                return agent_name

        # Default to frontend for UI tasks
        return 'frontend_ui'

    def execute_task(self, task: str) -> str:
        """Execute task with appropriate agent"""
        agent_name = self.determine_agent(task)
        print(f"Using {agent_name} agent for: {task}")

        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")

        return agent.execute(task)

    def create_pattern(self, task: str) -> str:
        """Force creation of new pattern"""
        agent_name = self.determine_agent(task)
        agent = self.agents.get(agent_name)

        # Force pattern creation even if one exists
        pattern = agent.create_pattern(task)
        if agent.validate_pattern(pattern):
            agent.save_pattern(pattern, task)
            return f"Pattern created for: {task}"
        else:
            return "Pattern creation failed validation"

    def search_patterns(self, query: str) -> List[str]:
        """Search all patterns across all domains"""
        results = []
        patterns_dir = Path(".ai/patterns")

        for pattern_file in patterns_dir.rglob("*.md"):
            content = pattern_file.read_text()
            if query.lower() in content.lower():
                results.append(str(pattern_file.relative_to(patterns_dir)))

        return results

@click.group()
def cli():
    """Pattern-first code generation framework"""
    pass

@cli.command()
@click.argument('task')
def generate(task):
    """Generate code from patterns"""
    orchestrator = Orchestrator()
    result = orchestrator.execute_task(task)
    print(result)

@cli.command('create-pattern')
@click.argument('task')
def create_pattern(task):
    """Create a new pattern"""
    orchestrator = Orchestrator()
    result = orchestrator.create_pattern(task)
    print(result)

@cli.command()
@click.argument('query')
def search(query):
    """Search patterns"""
    orchestrator = Orchestrator()
    results = orchestrator.search_patterns(query)
    for result in results:
        print(f"  - {result}")

if __name__ == '__main__':
    cli()
```

## LanceDB Vector Search Implementation

Create `.ai/lib/vector_search.py`:

```python
import lancedb
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
from pathlib import Path
import yaml
import re

class PatternVectorSearch:
    """Semantic search for patterns using LanceDB"""

    def __init__(self, db_path: str = ".ai/.lancedb"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.db = lancedb.connect(db_path)
        self.table_name = "patterns"
        self.initialize_table()

    def initialize_table(self):
        """Create or load the patterns table"""
        if self.table_name not in self.db.table_names():
            # Create empty table with schema
            schema = {
                "vector": self.model.encode("sample").tolist(),
                "path": "",
                "task": "",
                "content": "",
                "domain": "",
                "complexity": 1,
                "tags": []
            }
            self.table = self.db.create_table(self.table_name, [schema])
        else:
            self.table = self.db.open_table(self.table_name)

    def index_pattern(self, pattern_path: Path):
        """Index a single pattern file"""
        content = pattern_path.read_text()

        # Parse frontmatter
        metadata = self.parse_frontmatter(content)

        # Generate embedding
        embedding_text = f"{metadata.get('task', '')} {' '.join(metadata.get('tags', []))} {content}"
        vector = self.model.encode(embedding_text).tolist()

        # Prepare record
        record = {
            "vector": vector,
            "path": str(pattern_path),
            "task": metadata.get('task', ''),
            "content": content,
            "domain": pattern_path.parent.name,
            "complexity": metadata.get('complexity', 1),
            "tags": metadata.get('tags', [])
        }

        # Add to table
        self.table.add([record])

    def parse_frontmatter(self, content: str) -> dict:
        """Extract YAML frontmatter from markdown"""
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        return {}

    def search(self, query: str, limit: int = 5, domain: Optional[str] = None) -> List[Dict]:
        """Search for relevant patterns"""
        # Generate query embedding
        query_vector = self.model.encode(query).tolist()

        # Build search query
        search = self.table.search(query_vector).limit(limit)

        # Filter by domain if specified
        if domain:
            search = search.where(f"domain = '{domain}'")

        # Execute search
        results = search.to_list()

        return results

    def reindex_all(self):
        """Reindex all patterns"""
        # Clear existing table
        self.db.drop_table(self.table_name)
        self.initialize_table()

        # Index all patterns
        patterns_dir = Path(".ai/patterns")
        for pattern_file in patterns_dir.rglob("*.md"):
            self.index_pattern(pattern_file)

        print(f"Indexed {len(list(patterns_dir.rglob('*.md')))} patterns")
```

## Pattern Metadata Schema

### Required Frontmatter Format

Every pattern must include this frontmatter:

```yaml
---
task: string # One-line description of what this solves
complexity: integer (1-5) # 1=trivial, 5=complex multi-step
tags: [string, ...] # Searchable keywords
dependencies: [string, ...] # Required packages/libraries
tech_stack: [string, ...] # Technologies used (nextjs, react, etc)
manual_steps: boolean # Whether human intervention needed
version: string # Pattern version (1.0.0)
created: date # ISO date
updated: date # ISO date
---
```

### Pattern Structure Template

````markdown
---
task: Create responsive navigation with mobile menu
complexity: 2
tags: [navigation, header, responsive, mobile, menu]
dependencies: [react, next, tailwindcss, "@radix-ui/react-navigation-menu"]
tech_stack: [nextjs, react, typescript, tailwind]
manual_steps: true
version: 1.0.0
created: 2024-01-15
updated: 2024-01-15
---

# [Task Title]

[One paragraph description of what this pattern accomplishes]

## Code

```[language]
[Complete, working code implementation]
```
````

## Setup Instructions

[Step-by-step manual setup if required]

## Usage

[How to use this pattern in a project]

## Notes

[Any additional context or warnings]

````

## Complete Base Agent Implementation

Create `.ai/agents/base_agent.py`:

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["anthropic", "pyyaml", "lancedb", "sentence-transformers"]
# ///

import os
import yaml
import json
from pathlib import Path
from anthropic import Anthropic
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional, List
import re

from lib.vector_search import PatternVectorSearch

class PatternFirstAgent(ABC):
    """Base agent that enforces pattern-first generation"""

    def __init__(self, domain: str):
        self.domain = domain
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.philosophy = Path(".ai/philosophy.md").read_text()
        self.patterns_dir = Path(f".ai/patterns/{domain}")
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        self.vector_search = PatternVectorSearch()
        self.config = self.load_config()

    def load_config(self) -> dict:
        config_path = Path(".ai/config.yaml")
        if config_path.exists():
            return yaml.safe_load(config_path.read_text())
        return {}

    def execute(self, task: str) -> str:
        """Pattern-first execution flow with error handling"""
        try:
            # 1. Search for existing pattern
            pattern = self.find_pattern(task)

            if not pattern:
                print(f"No pattern found for: {task}")
                print("Creating new pattern with philosophical constraints...")

                # 2. Create pattern under constraints
                pattern = self.create_pattern(task)

                # 3. Validate pattern
                validation_result = self.validate_pattern(pattern)
                if not validation_result['valid']:
                    raise ValueError(f"Pattern validation failed: {validation_result['errors']}")

                # 4. Save pattern
                pattern_path = self.save_pattern(pattern, task)
                print(f"Pattern created and saved: {pattern_path}")

                # 5. Index for search
                self.vector_search.index_pattern(Path(pattern_path))

            # 6. Generate code from pattern
            code = self.generate_from_pattern(pattern, task)

            # 7. Log metrics
            self.log_metrics(task, pattern is not None)

            return code

        except Exception as e:
            return self.handle_error(e, task)

    def find_pattern(self, task: str) -> Optional[Dict]:
        """Search for existing patterns using vector search"""
        results = self.vector_search.search(task, limit=3, domain=self.domain)

        if results:
            # Return the most relevant pattern
            best_match = results[0]
            return self.parse_pattern_file(best_match['path'])

        return None

    def create_pattern(self, task: str) -> Dict:
        """Create a new pattern under philosophical constraints"""
        prompt = f"""Create a pattern for: {task}

PHILOSOPHY TO FOLLOW:
{self.philosophy}

REQUIREMENTS:
1. Complete, working solution with no placeholders
2. Simplest approach that fully solves the problem
3. All necessary imports and dependencies listed
4. Clear setup instructions for manual steps
5. Production-ready code

OUTPUT FORMAT:
Provide the pattern with these sections:
- Frontmatter (YAML): task, complexity, tags, dependencies, tech_stack, manual_steps
- Description: One paragraph explaining what this accomplishes
- Code: Complete implementation
- Setup Instructions: Any manual steps required
- Usage: How to use this pattern
- Notes: Additional context

Return ONLY the pattern content, no other text."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        return self.parse_pattern_response(response.content[0].text)

    def validate_pattern(self, pattern: Dict) -> Dict:
        """Comprehensive pattern validation"""
        errors = []
        warnings = []

        # Check required metadata
        required_metadata = ['task', 'complexity', 'tags', 'dependencies']
        for field in required_metadata:
            if field not in pattern.get('metadata', {}):
                errors.append(f"Missing required metadata: {field}")

        # Check code quality
        code = pattern.get('code', '')
        if len(code.strip()) < self.config.get('framework', {}).get('pattern_min_size', 50):
            errors.append("Pattern code too short")

        if 'TODO' in code or '...' in code or 'pass' in code:
            errors.append("Pattern contains incomplete sections")

        # Check complexity
        complexity = pattern.get('metadata', {}).get('complexity', 0)
        max_complexity = self.config.get('validation', {}).get('max_complexity', 5)
        if complexity > max_complexity:
            warnings.append(f"Pattern complexity {complexity} exceeds recommended max {max_complexity}")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def save_pattern(self, pattern: Dict, task: str) -> str:
        """Save pattern to filesystem"""
        # Generate filename
        filename = re.sub(r'[^\w\s-]', '', task.lower())
        filename = re.sub(r'[-\s]+', '-', filename)[:50] + '.md'
        filepath = self.patterns_dir / filename

        # Format pattern as markdown
        content = self.format_pattern_markdown(pattern)

        # Write to file
        filepath.write_text(content)

        return str(filepath)

    def format_pattern_markdown(self, pattern: Dict) -> str:
        """Format pattern dictionary as markdown"""
        metadata = pattern.get('metadata', {})

        # Add timestamps
        metadata['created'] = datetime.now().isoformat()
        metadata['updated'] = datetime.now().isoformat()
        metadata['version'] = '1.0.0'

        frontmatter = yaml.dump(metadata, default_flow_style=False)

        return f"""---
{frontmatter}---

# {metadata.get('task', 'Pattern')}

{pattern.get('description', '')}

## Code

```{pattern.get('language', 'typescript')}
{pattern.get('code', '')}
````

## Setup Instructions

{pattern.get('setup', 'No additional setup required.')}

## Usage

{pattern.get('usage', '')}

## Notes

{pattern.get('notes', '')}
"""

    def generate_from_pattern(self, pattern: Dict, task: str) -> str:
        """Generate code from pattern with adaptations"""
        prompt = f"""Generate code for: {task}

USE THIS PATTERN AS REFERENCE:
{pattern.get('code')}

PATTERN METADATA:

- Task: {pattern.get('metadata', {}).get('task')}
- Dependencies: {pattern.get('metadata', {}).get('dependencies')}

REQUIREMENTS:

1. Follow the pattern structure
2. Adapt names and values for the specific task
3. Maintain the same complexity level
4. Include all setup instructions from the pattern

Generate complete, working code based on this pattern."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def handle_error(self, error: Exception, task: str) -> str:
        """Handle errors gracefully"""
        error_message = f"Error processing task '{task}': {str(error)}"

        # Log error
        self.log_error(error_message)

        # Return helpful error message
        return f"""

## Error Encountered

{error_message}

### Troubleshooting Steps:

1. Check that your ANTHROPIC_API_KEY is set
2. Ensure the philosophy.md file exists
3. Verify the pattern directory structure
4. Try creating the pattern manually first

### Fallback Action:

You can create the pattern manually in:
{self.patterns_dir}

Then run the task again.
"""

    def log_metrics(self, task: str, pattern_reused: bool):
        """Track usage metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'domain': self.domain,
            'pattern_reused': pattern_reused,
            'patterns_total': len(list(self.patterns_dir.glob('*.md')))
        }

        metrics_file = Path('.ai/metrics.jsonl')
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(metrics) + '\n')

    def log_error(self, error_message: str):
        """Log errors for debugging"""
        error_log = Path('.ai/errors.log')
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {error_message}\n")

    @abstractmethod
    def parse_pattern_response(self, response: str) -> Dict:
        """Parse AI response into pattern dictionary - implement in subclass"""
        pass

    @abstractmethod
    def parse_pattern_file(self, filepath: str) -> Dict:
        """Parse pattern file into dictionary - implement in subclass"""
        pass

````

## Error Handling and Recovery

### Pattern Creation Failures

When pattern creation fails, the system:

1. **Validation Failures**: Shows specific validation errors
2. **API Failures**: Retries with exponential backoff
3. **Philosophy Violations**: Provides detailed feedback on what violated principles
4. **Manual Override**: Allows manual pattern creation with instructions

### Generation Failures

Recovery strategies for generation issues:

```python
def recover_from_generation_failure(self, task: str, error: Exception):
    """Multi-level recovery strategy"""

    # Level 1: Try alternative patterns
    alternative_patterns = self.find_similar_patterns(task)
    if alternative_patterns:
        return self.generate_from_pattern(alternative_patterns[0], task)

    # Level 2: Decompose task
    subtasks = self.decompose_task(task)
    if subtasks:
        return self.generate_composite_solution(subtasks)

    # Level 3: Create minimal pattern
    minimal_pattern = self.create_minimal_pattern(task)
    if minimal_pattern:
        return self.generate_from_pattern(minimal_pattern, task)

    # Level 4: Return manual instructions
    return self.provide_manual_instructions(task)
````

## Testing and Validation Framework

Create `.ai/lib/pattern_validator.py`:

```python
import subprocess
from pathlib import Path
from typing import Dict, List

class PatternValidator:
    """Validate patterns work correctly"""

    def validate_pattern_code(self, pattern: Dict) -> Dict:
        """Test that pattern code is syntactically valid"""
        code = pattern.get('code', '')
        language = pattern.get('language', 'typescript')

        validators = {
            'typescript': self.validate_typescript,
            'python': self.validate_python,
            'bash': self.validate_bash
        }

        validator = validators.get(language)
        if validator:
            return validator(code)

        return {'valid': True, 'errors': []}

    def validate_typescript(self, code: str) -> Dict:
        """Validate TypeScript code"""
        # Write to temp file
        temp_file = Path('/tmp/test.tsx')
        temp_file.write_text(code)

        # Run TypeScript compiler in check mode
        result = subprocess.run(
            ['npx', 'tsc', '--noEmit', str(temp_file)],
            capture_output=True,
            text=True
        )

        return {
            'valid': result.returncode == 0,
            'errors': result.stderr.split('\n') if result.stderr else []
        }

    def validate_python(self, code: str) -> Dict:
        """Validate Python code"""
        try:
            compile(code, '<string>', 'exec')
            return {'valid': True, 'errors': []}
        except SyntaxError as e:
            return {'valid': False, 'errors': [str(e)]}

    def validate_bash(self, code: str) -> Dict:
        """Validate Bash scripts"""
        result = subprocess.run(
            ['bash', '-n'],
            input=code,
            capture_output=True,
            text=True
        )

        return {
            'valid': result.returncode == 0,
            'errors': result.stderr.split('\n') if result.stderr else []
        }
```

---

End of Document
