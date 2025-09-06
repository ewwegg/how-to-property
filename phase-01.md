# Phase 1 Startup Guide: Pattern-First Development from Zero

## The Fundamental Shift

You never generate free-form code. Ever. Every piece of code comes from a pattern that was created under philosophical constraints. This guide shows how to build your framework and project simultaneously using pattern-first development.

## Starting State

- Empty repository
- No project files
- No framework
- Clear goal: Build a complete web application

## Step 1: Define Your Philosophy

Before any code, patterns, or agents, write your philosophy. This becomes the DNA of every pattern you'll create.

Create `.ai/philosophy.md`:

```markdown
# Core Philosophy

## Principles

1. **Minimal Viable Completeness**: The simplest solution that fully works
2. **No Reinvention**: Use existing libraries and components
3. **Production-First**: Every pattern must be deployable
4. **Clear Dependencies**: Every import must have a justification
5. **Human-Friendly**: Include clear instructions for manual steps

## Anti-Patterns

- Custom implementations of solved problems
- Abstractions without immediate benefit
- TODO comments or placeholder code
- Over-engineering for imaginary scale
- Configuration without purpose

## Constraints for Pattern Creation

Every pattern must:

- Solve exactly one problem completely
- Work without modification
- Include all necessary setup steps
- Use the minimum code required
- Follow established conventions
```

## Step 2: Create Your First Agent with Pattern Creation

Your first agent must be able to CREATE patterns, not just use them.

Create `.ai/agents/base_agent.py`:

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["anthropic", "pyyaml", "lancedb"]
# ///

import os
import yaml
from pathlib import Path
from anthropic import Anthropic
from abc import ABC, abstractmethod

class PatternFirstAgent(ABC):
    """Base agent that enforces pattern-first generation"""

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.philosophy = Path(".ai/philosophy.md").read_text()
        self.patterns_dir = Path(".ai/patterns")
        self.patterns_dir.mkdir(exist_ok=True)

    def execute(self, task: str) -> str:
        """Pattern-first execution flow"""

        # 1. Search for existing pattern
        pattern = self.find_pattern(task)

        if not pattern:
            print(f"No pattern found for: {task}")
            print("Creating new pattern with philosophical constraints...")

            # 2. Create pattern FIRST (this is the key)
            pattern = self.create_pattern(task)

            # 3. Validate pattern against philosophy
            if not self.validate_pattern(pattern):
                raise ValueError("Pattern violates philosophy")

            # 4. Save pattern for future use
            self.save_pattern(pattern, task)
            print(f"Pattern created and saved")

        # 5. Generate code FROM pattern (never free-form)
        code = self.generate_from_pattern(pattern, task)

        return code

    def create_pattern(self, task: str) -> dict:
        """Create a new pattern under philosophical constraints"""

        prompt = f"""Create a pattern for: {task}

PHILOSOPHY TO FOLLOW:
{self.philosophy}

REQUIREMENTS:
1. The pattern must be a complete, working solution
2. Use the simplest approach that fully solves the problem
3. Include all necessary imports and dependencies
4. Add clear setup instructions for any manual steps
5. No TODOs, placeholders, or incomplete sections

PATTERN FORMAT:
- Frontmatter: task, complexity (1-5), tags, dependencies
- Complete working code
- Setup instructions if needed
- Usage notes

Return a pattern that embodies these philosophical constraints."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        return self.parse_pattern(response.content[0].text)

    def validate_pattern(self, pattern: dict) -> bool:
        """Validate pattern against philosophy"""

        code = pattern.get("code", "")

        # No TODOs or placeholders
        if "TODO" in code or "..." in code or "pass" in code:
            print("❌ Pattern contains incomplete sections")
            return False

        # Must have actual implementation
        if len(code.strip()) < 50:
            print("❌ Pattern lacks substantial implementation")
            return False

        # Must specify dependencies clearly
        if not pattern.get("metadata", {}).get("dependencies"):
            print("⚠️ Pattern missing dependency list")

        print("✅ Pattern validated against philosophy")
        return True

    def generate_from_pattern(self, pattern: dict, task: str) -> str:
        """Generate code strictly from pattern"""

        prompt = f"""Generate code for: {task}

USE THIS PATTERN:
{pattern.get('code')}

SETUP INSTRUCTIONS:
{pattern.get('setup', 'None required')}

CONSTRAINTS:
- Follow the pattern structure exactly
- Adapt only names and specific values
- Maintain the same complexity level
- Include all setup instructions

Generate the complete implementation based on this pattern."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    @abstractmethod
    def find_pattern(self, task: str) -> dict:
        """Search for existing patterns - implement in subclass"""
        pass

    @abstractmethod
    def save_pattern(self, pattern: dict, task: str):
        """Save pattern to library - implement in subclass"""
        pass

    @abstractmethod
    def parse_pattern(self, response: str) -> dict:
        """Parse AI response into pattern dict - implement in subclass"""
        pass
```

## Step 3: Create Your Infrastructure Agent

This agent creates patterns for project setup.

Create `.ai/agents/infrastructure.py`:

````python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["anthropic", "pyyaml", "lancedb"]
# ///

from base_agent import PatternFirstAgent
from pathlib import Path
import yaml
import json

class InfrastructureAgent(PatternFirstAgent):
    """Creates and uses patterns for project setup"""

    def find_pattern(self, task: str) -> dict:
        """Search for infrastructure patterns"""
        patterns_dir = Path(".ai/patterns/infrastructure")
        if not patterns_dir.exists():
            return None

        # Simple filesystem search for now
        for pattern_file in patterns_dir.glob("*.md"):
            content = pattern_file.read_text()
            if task.lower() in content.lower():
                return self.parse_pattern(content)

        return None

    def save_pattern(self, pattern: dict, task: str):
        """Save infrastructure pattern"""
        patterns_dir = Path(".ai/patterns/infrastructure")
        patterns_dir.mkdir(parents=True, exist_ok=True)

        # Create filename from task
        filename = task.lower().replace(" ", "-")[:50] + ".md"
        filepath = patterns_dir / filename

        # Format pattern as markdown
        content = f"""---
task: {pattern['metadata']['task']}
complexity: {pattern['metadata']['complexity']}
tags: {pattern['metadata']['tags']}
dependencies: {pattern['metadata']['dependencies']}
---

# {pattern['metadata']['task'].title()}

{pattern['description']}

## Code/Commands

```{pattern['language']}
{pattern['code']}
````

## Setup Instructions

{pattern['setup']}

## Usage Notes

{pattern['notes']}
"""

        filepath.write_text(content)
        print(f"Pattern saved: {filepath}")

    def parse_pattern(self, response: str) -> dict:
        """Parse response into pattern structure"""
        # This is simplified - real implementation would be more robust
        pattern = {
            'metadata': {
                'task': 'parsed from response',
                'complexity': 1,
                'tags': [],
                'dependencies': []
            },
            'description': '',
            'language': 'bash',
            'code': response,  # Would extract code block
            'setup': 'Extracted from response',
            'notes': ''
        }

        return pattern

if **name** == "**main**":
import sys
agent = InfrastructureAgent()
task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "setup nextjs project"
result = agent.execute(task)
print(result)

````

## Step 4: Create Your First Pattern

Run the infrastructure agent to create your first pattern:

```bash
export ANTHROPIC_API_KEY=your-key
python .ai/agents/infrastructure.py "setup nextjs project with typescript tailwind and shadcn"
````

The agent will:

1. Search for existing pattern (won't find one)
2. CREATE a pattern under philosophical constraints
3. Validate the pattern
4. Save it to `.ai/patterns/infrastructure/`
5. Generate code from that pattern

The created pattern might look like:

````markdown
---
task: setup nextjs project with typescript tailwind and shadcn
complexity: 2
tags: [setup, nextjs, typescript, tailwind, shadcn]
dependencies: [nodejs, npm]
---

# Setup Nextjs Project With Typescript Tailwind And Shadcn

Complete Next.js project initialization with full tech stack.

## Code/Commands

```bash
# Create Next.js project with exact configuration
npx create-next-app@latest . \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias '@/*' \
  --yes

# Install essential production dependencies
npm install \
  clsx@2.1.1 \
  tailwind-merge \
  tailwindcss-animate

# Initialize shadcn-ui with configuration
npx shadcn@latest init \
  --yes \
  --defaults \
  --skip-font

# Create required project structure
mkdir -p components/ui lib hooks
```
````

## Setup Instructions

1. Ensure Node.js 20+ is installed
2. Run from empty directory
3. Commands execute in sequence
4. Total setup time: ~2 minutes

## Usage Notes

This pattern creates the minimal viable Next.js setup. Add additional dependencies only as needed for specific features.

````

## Step 5: Pattern-Driven Development

Now every task follows this flow:

### Task: "Create a navigation component"

```bash
python .ai/agents/frontend.py "create navigation component"
````

**What happens:**

1. No navigation pattern exists
2. Agent creates pattern with philosophy:
   - Must use shadcn/ui (not custom)
   - Must be responsive (complete)
   - Must include mobile menu (no TODOs)
3. Pattern is saved
4. Code is generated from pattern
5. You get principled navigation code

### Task: "Create another navigation with dark mode"

```bash
python .ai/agents/frontend.py "create navigation with dark mode toggle"
```

**What happens:**

1. Navigation pattern exists
2. Agent generates from existing pattern
3. Adapts for dark mode requirement
4. Still follows all philosophical constraints

## Step 6: Growing Your Pattern Library

Your pattern library grows through actual development needs:

```
.ai/patterns/
├── infrastructure/
│   ├── setup-nextjs-project.md
│   ├── setup-database-prisma.md
│   └── deploy-to-vercel.md
├── frontend/
│   ├── navigation-component.md
│   ├── hero-section.md
│   ├── form-with-validation.md
│   └── data-table.md
├── api/
│   ├── rest-endpoint.md
│   ├── server-action.md
│   └── auth-handler.md
└── database/
    ├── prisma-schema.md
    └── migration.md
```

Each pattern was created because you needed it, under philosophical constraints, and validated before use.

## Key Differences from Traditional Development

### Traditional AI-Assisted Flow

1. Ask AI for code
2. Get something (good or bad)
3. Debug and fix
4. Maybe it follows your principles
5. Hope for consistency

### Pattern-First Flow

1. Ask for code
2. Pattern created under constraints (or reused)
3. Get principled code
4. No debugging philosophy violations
5. Guaranteed consistency

## Measuring Success

Track these metrics to validate the approach:

```python
# Add to your base agent
class PatternFirstAgent:
    def log_metrics(self, task: str, pattern_reused: bool, generation_time: float):
        metrics = {
            'task': task,
            'pattern_reused': pattern_reused,
            'generation_time': generation_time,
            'patterns_total': len(list(Path('.ai/patterns').rglob('*.md'))),
            'reuse_rate': self.calculate_reuse_rate()
        }

        # Log to .ai/metrics.jsonl
        with open('.ai/metrics.jsonl', 'a') as f:
            f.write(json.dumps(metrics) + '\n')
```

Success indicators:

- Pattern reuse > 50% after 20 patterns
- Zero philosophy violations in generated code
- Pattern creation time < 2x free-form generation
- No post-generation fixes needed

## Common Challenges and Solutions

### "This is too rigid!"

It feels rigid at first because you're front-loading the thinking. But consider:

- Time creating pattern: 2 minutes
- Time debugging bad generation: 10+ minutes
- Pattern reuse: infinite value

### "What about one-off scripts?"

One-offs often aren't. Create the pattern anyway because:

- You'll likely need it again
- Others might need it
- It documents the solution properly

### "Pattern creation is slow"

Yes, the first pattern for each task type is slower. But:

- Second use is instant
- No debugging time
- No philosophy violations to fix
- Compounds in value over time

## Next Steps

1. **Build 10 patterns** through real tasks
2. **Measure reuse rate** after one week
3. **Add vector search** when you have 20+ patterns
4. **Create second agent** when patterns exist
5. **Add orchestration** only after multi-agent patterns emerge

Remember: You're not building a framework then using it. You're building it THROUGH using it, with philosophy enforced at every step.

---

End of Document
