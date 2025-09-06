# Pattern-First Framework

## Core Principle

**Code can only be generated from patterns.** No free-form code generation is allowed.

## Architecture

### Framework Components
- ✅ **Philosophy constraints** (`.ai/philosophy.md`) - Enforces quality principles
- ✅ **Base agent** (`agents/base_agent.py`) - Pattern search, validation, and generation
- ✅ **Domain agents** - Search and use patterns only (no inline creation)
  - Infrastructure agent (`agents/infrastructure.py`) 
  - Frontend UI agent (`agents/frontend_ui.py`)
- ✅ **Orchestrator** (`orchestrator.py`) - Routes tasks to appropriate agents

### Key Design Decisions
- **Agents cannot create patterns inline** - All patterns must be created manually to ensure philosophical alignment
- **Pattern search is based on task metadata** - Not keyword matching in content
- **Context comes before code** - Setup, usage, and notes precede the implementation

### Available Patterns
- `infrastructure/setup-nextjs-project.md` - Next.js project setup (handles existing directories)
- `frontend/create-homepage.md` - Homepage with hero, features, CTA

## How It Works

1. **Request code generation**
   ```bash
   python3 .ai/orchestrator.py generate "setup nextjs project"
   ```

2. **Framework searches for pattern**
   - If pattern exists: Generate code from it
   - If no pattern: Create pattern under philosophical constraints first

3. **Pattern validation**
   - No TODOs or incomplete sections
   - Minimum complexity requirements
   - Required metadata present

4. **Code generation from pattern**
   - Pattern provides complete, working solution
   - Context (setup, usage, notes) comes before code
   - Code is production-ready

## Commands

```bash
# Generate code from patterns
python3 .ai/orchestrator.py generate <task>

# Create new pattern
python3 .ai/orchestrator.py create <task>

# Search patterns
python3 .ai/orchestrator.py search <query>

# List all patterns
python3 .ai/orchestrator.py list
```

## Pattern Structure

Every pattern follows this format:

1. **Frontmatter** - Metadata (task, complexity, dependencies)
2. **Description** - What the pattern accomplishes
3. **Setup Instructions** - Prerequisites and environment
4. **Usage** - How to use the generated code
5. **Notes** - Additional context
6. **Code** - Complete, working implementation

## Next Steps for Framework Development

1. Add vector search for better pattern discovery
2. Implement pattern composition (combining multiple patterns)
3. Add pattern versioning and evolution tracking
4. Create more domain agents (API, database, testing)
5. Build pattern quality metrics and analytics