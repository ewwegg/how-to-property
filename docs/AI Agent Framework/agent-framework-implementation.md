# UV-Native AI Agent Framework - Implementation Blueprint

## Core Philosophy

This framework leverages **Astral UV** to create truly independent, instantly executable agents that embody minimal viable completeness. Each agent is a self-contained executable that can install its own dependencies in milliseconds and run without any environment setup.

**Why UV Changes Everything:**

- **10-100x faster** than traditional pip installation
- **Zero setup** - agents run directly without virtual environment activation
- **True isolation** - each agent has its own dependency scope
- **Instant execution** - dependencies cached and ready in milliseconds
- **Parallel safe** - multiple agents can run simultaneously without conflicts

## Repository Structure

```
your-saas/
├── .ai/
│   ├── agents/                     # Executable single-file agents
│   │   ├── api/
│   │   │   ├── create_endpoint      # No .py extension - directly executable
│   │   │   ├── add_validation
│   │   │   └── handle_errors
│   │   ├── frontend/
│   │   │   ├── create_form
│   │   │   ├── create_dashboard
│   │   │   └── add_component
│   │   ├── database/
│   │   │   ├── create_model
│   │   │   ├── run_migration
│   │   │   └── seed_data
│   │   └── [other categories]/
│   │
│   ├── orchestrator               # Main UV-powered orchestrator
│   ├── philosophy.yaml            # Core principles configuration
│   └── registry.yaml              # Agent registry and metadata
│
├── src/                           # Generated application code
├── pyproject.toml                 # UV project configuration
└── .python-version                # Python version for UV
```

## UV-First Design Principles

### 1. Every Agent is an Executable

```bash
# Direct execution - no 'python' command needed
.ai/agents/frontend/create_form

# With arguments
.ai/agents/api/create_endpoint --name users --method GET
```

### 2. Dependencies Inline with Code

Each agent declares its exact dependencies in the file header, UV handles the rest automatically.

### 3. Instant Dependency Resolution

UV maintains a global cache - first run might take seconds, subsequent runs are instantaneous.

### 4. Philosophy Through Execution

Philosophy isn't just evaluated - it determines which agents can run and how they execute.

## Execution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      UV ORCHESTRATOR                        │
│                  (Single UV-managed process)                │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├─→ Parse Command
                  ├─→ Philosophy Check
                  ├─→ Select Agent(s)
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT EXECUTION                          │
│                  (Isolated UV environment)                  │
│                                                             │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │   Agent 1    │  │   Agent 2    │  │   Agent 3    │   │
│   │  create_form │  │  add_validation  │  style_form  │   │
│   │              │  │              │  │              │   │
│   │  Dependencies:  │  Dependencies:  │  Dependencies:  │   │
│   │  - jinja2    │  │  - pydantic  │  │  - None      │   │
│   └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                             │
│         Each runs in parallel with own dependencies         │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     GENERATED CODE                          │
│                   Written to src/ directory                 │
└─────────────────────────────────────────────────────────────┘
```

## Agent Structure Template

```python
#!/usr/bin/env -S uv run --quiet --no-project
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   # Only what this specific agent needs
# ]
# ///
"""
Agent: {name}
Purpose: {specific_task}
Complexity: minimal
Philosophy: Complete solution with minimum complexity
"""

import sys
import json
from pathlib import Path

def validate_requirements(req: dict) -> bool:
    """Ensure we have everything needed"""
    # Minimal validation - assume defaults
    return True

def apply_philosophy(req: dict) -> dict:
    """Filter requirements through philosophy"""
    # Remove any non-essential features
    # Set sensible defaults
    # Enforce minimal approach
    return req

def generate_solution(req: dict) -> str:
    """Generate complete, working code"""
    # No TODOs, no placeholders
    # Complete implementation
    return "working code"

def main():
    # Parse input (from stdin for pipe-ability)
    input_data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}

    if not validate_requirements(input_data):
        print(json.dumps({"error": "Invalid requirements"}))
        return 1

    req = apply_philosophy(input_data)
    solution = generate_solution(req)

    # Output result
    result = {
        "success": True,
        "code": solution,
        "files": ["path/to/file.tsx"],
        "complexity": "minimal",
        "next_steps": ["enhance_when_validated"]
    }

    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Orchestrator Design

The orchestrator itself is a UV-powered executable that coordinates agent execution:

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer",      # Better CLI than click for modern Python
#   "pyyaml",     # Configuration management
#   "rich",       # Beautiful terminal output
# ]
# ///
```

Key orchestrator responsibilities:

1. **Agent Discovery** - Find appropriate agents using registry
2. **Philosophy Enforcement** - Validate all operations against principles
3. **Parallel Execution** - Run multiple agents simultaneously when safe
4. **Result Assembly** - Combine outputs from multiple agents
5. **Code Generation** - Write results to appropriate locations

## Command Interface

```bash
# Install UV (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize project
uv init
cd your-saas

# Execute single agent
.ai/agents/frontend/create_form

# Use orchestrator
.ai/orchestrator execute "create user dashboard"

# Compose multiple agents
.ai/orchestrator compose "build auth system"

# Generate new agent if missing
.ai/orchestrator generate "create invoice system"

# Run agents in parallel
.ai/orchestrator parallel "create_form,add_validation,style_form"
```

## Key Advantages of UV-Native Design

### 1. **True Single-File Agents**

Each agent is completely self-contained with its dependencies. Copy an agent to any system with UV and it just works.

### 2. **Instant Startup**

After first run, UV caches everything. Subsequent executions start in milliseconds, not seconds.

### 3. **Parallel Execution**

Multiple agents can run simultaneously without environment conflicts:

```bash
# These all run in parallel, each with their own dependencies
parallel -j 10 ::: \
  .ai/agents/frontend/create_form \
  .ai/agents/api/create_endpoint \
  .ai/agents/database/create_model
```

### 4. **Version Isolation**

Different agents can use different versions of the same package without conflicts.

### 5. **Zero Configuration**

No virtual environments to create or activate. No requirements.txt to maintain. No pip install commands.

## Philosophy Configuration

```yaml
# .ai/philosophy.yaml
core_principles:
  minimal_executable:
    rule: "Every agent must be directly runnable"
    enforce: "No agent requires environment activation"

  instant_execution:
    rule: "Agents execute in under 1 second"
    enforce: "UV caching ensures instant dependency availability"

  complete_isolation:
    rule: "Agents cannot interfere with each other"
    enforce: "Each agent runs in its own UV scope"

  zero_setup:
    rule: "Copy agent anywhere and it works"
    enforce: "All dependencies inline, UV handles the rest"

execution_constraints:
  max_dependencies: 3 # Keep agents minimal
  max_execution_time: 5 # Seconds
  require_completion: true # No partial solutions
  require_validation: true # All agents self-test
```

## Registry Structure

```yaml
# .ai/registry.yaml
agents:
  create_form:
    path: agents/frontend/create_form
    executable: true
    dependencies: [] # No dependencies needed
    complexity: minimal
    execution_time: <1s

  create_endpoint:
    path: agents/api/create_endpoint
    executable: true
    dependencies: ["pydantic"] # For validation
    complexity: minimal
    execution_time: <1s

  create_dashboard:
    path: agents/frontend/create_dashboard
    executable: true
    dependencies: ["jinja2"] # For templating
    complexity: moderate
    execution_time: <2s

execution_stats:
  total_runs: 1847
  average_time: 0.73s
  cache_hit_rate: 94%
  success_rate: 99.2%
```

## Development Workflow

### Creating New Agent

```bash
# Use template to create new agent
.ai/orchestrator new-agent "create checkout flow"

# Agent is immediately executable
.ai/agents/billing/create_checkout

# Test in isolation
echo '{"product": "premium"}' | .ai/agents/billing/create_checkout
```

### Testing Agents

```bash
# Each agent has self-test capability
.ai/agents/frontend/create_form --test

# Run all agent tests in parallel
find .ai/agents -type f -executable | parallel {} --test

# Validate against philosophy
.ai/orchestrator validate .ai/agents/frontend/create_form
```

### Deployment

```bash
# Agents are portable - just copy them
scp .ai/agents/frontend/create_form production:/ai/agents/frontend/

# Or sync entire repository
rsync -av .ai/agents/ production:/ai/agents/
```

## Success Metrics

- **Execution Speed**: <1 second average (after cache)
- **Setup Time**: 0 seconds (just run)
- **Dependency Conflicts**: 0 (isolation)
- **Portability**: 100% (copy and run)
- **Parallel Execution**: Unlimited (no conflicts)

## Migration from Traditional Setup

```bash
# Traditional Python approach
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/create_form.py

# UV approach
.ai/agents/frontend/create_form

# 5 commands vs 1 command
# 30+ seconds vs <1 second
```

## Related Documents

- **UV Agent Code Guide**: Detailed code implementations
- **UV Agent Catalog**: Complete repository of UV-native agents

This blueprint establishes a framework where every agent is an instantly executable, self-contained solution that embodies our philosophy of minimal viable completeness.
