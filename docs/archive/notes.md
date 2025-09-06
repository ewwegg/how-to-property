# Notes

##

phases - MVP to Scale - this might be better phrased as "initial" and "additions"? or something similar - or maybe it's fine

do i need 175+ agents? or do i need an agent for "authentication" and then it selects relevant information within itself

- i guess these agents can be good, because they're complete minimal solutions... the "prompt" should be overarching which can combine them.

=======

## single file agents

Single file agents are exceptionally compatible with your AI-First Framework philosophy. They embody the same principles: complete solutions, minimal complexity, and focused scope.

## Key Benefits for Your Framework

1. Tasks Become Executable, Not Just Documented
   Instead of markdown files describing how to implement something, each task IS an implementation:
   python
   Instead of: knowledge/tasks/create-form.md
   You have: agents/create_form_agent.py
2. Philosophy Enforcement Through Agent Selection
   Your philosophy engine doesn't just filter patterns - it selects which agents to invoke based on simplicity and completeness.
3. Perfect Alignment with "Complete but Minimal"
   Each agent is a complete, working solution in a single file - the ultimate expression of your minimal viable philosophy.

your-project/
├── .ai/
│ ├── philosophy/
│ │ └── core.yaml
│ │
│ ├── agents/ # Single file agents
│ │ ├── api/
│ │ │ ├── create_endpoint.py
│ │ │ ├── add_validation.py
│ │ │ └── handle_errors.py
│ │ ├── frontend/
│ │ │ ├── create_form.py
│ │ │ ├── add_table.py
│ │ │ └── setup_routing.py
│ │ └── database/
│ │ ├── add_migration.py
│ │ └── create_index.py
│ │
│ ├── orchestrator/ # Enhanced context engine
│ │ ├── agent_selector.py # Chooses which agents
│ │ ├── context_engine.py # Assembles agent + context
│ │ └── philosophy.py # Evaluates agent fitness
│ │
│ └── knowledge/ # Lightweight metadata
│ └── agent_registry.yaml # Maps tasks to agents

**improvement** I think it would be best to have an "API agent", "frontend agent", "database agent", and have the more specific tasks as markdown so they can be more descriptive, for example the api agent would decide which files are relevant to the task it's been given and ecide which files to read from 'create_endpoint.py', 'add_validation.py', 'handle_errors.py'.

How can i keep the agent flexible, but provide context for project consistency. I don't want to provide complete code solutions

I would prefer a simple vector search rather than a registry, or some kind of hybrid if it makes sense.

Single file agents creates code that documents itself.

Workflow

1. Intent Analysis & Philosophy Check
2. Agent Discovery & Selection with Generation Fallback
3. Agent Task selection & Execution Planning (is it task selection, or is there a better name for it grabbing relevant documents like paterns)
4. Dependency Resolution
5. Execution
6. Review
7. Output and decision summary

## Why UV is Critical for Single File Agents

True Single File: With UV, each agent is genuinely self-contained with its dependencies declared in the file
Instant Execution: No pip install wait times - UV caches everything
Parallel Execution: Multiple agents can run simultaneously without conflicts
Version Isolation: Each agent can use different package versions
Zero Configuration: No virtual environment setup or activation

The framework should leverage UV for:

Agent execution: Each agent runs in its own UV-managed environment
Dependency management: Agents declare their exact needs
Testing: Run agent tests instantly without setup
Development: Fast iteration with immediate dependency availability

With UV, the philosophy becomes even stronger:
Truly minimal: No global dependencies, each agent has only what it needs
Actually isolated: Agents can't interfere with each other
Instantly executable: Zero setup time from code to execution

## The GOAL

Core Insight: AI loads too much context. Solution: Dynamic context assembly - give AI only what's needed for the specific task.
Philosophy as Filter: a function that removes complexity before the AI even sees options.
Minimal Viable Completeness: The smallest solution that fully solves the problem.
Single File Agents: Tasks become executable, not documented.

## additional needs

Claude Code CLI Integration: Full slash command support with configuration examples
yamlslash_commands:

- name: "agent"
  command: ".ai/run"

Philosophy Document: Clear markdown file (.ai/PHILOSOPHY.md) explaining why this exists and how it works - provides essential context without being configuration
Autonomous Orchestration: The orchestrator understands patterns and dependencies

Users type /build auth system
System knows to run: setup-auth → create-user-model → create-login → add-middleware
No manual ordering required

Outcome Evaluation: Focus on completeness, simplicity, and maintainability

Each agent self-validates its output
Orchestrator evaluates for completeness

# Task Oriented

## This is what AI agents actually do:

task = "create RSVP form"
context_needed = [
"form_patterns",
"validation_rules",
"color_tokens",
"naming_conventions"
]
**Not: "Load all of implementation-patterns.md and core-system.md"**

## Micro documents organised by task

/context
/tasks
/api
create-endpoint.md
add-authentication.md
implement-rate-limiting.md
/frontend
create-form.md
add-data-table.md
implement-infinite-scroll.md
/database
add-migration.md
optimize-query.md
add-index.md
/testing
write-unit-test.md
add-e2e-test.md
/deployment
setup-ci-cd.md
configure-monitoring.md
/references
color-tokens.json # Just the values
tech-stack.json # Just the versions
naming-rules.md # Just the conventions
/decisions
2024-01-15-chose-nextjs.md
2024-01-20-color-palette.md
/values
design-tokens.json
api-endpoints.json
database-schema.json

## Agents Need

Need specific, atomic information
Build context through retrieval (dynamic context assembly)

## Context Assembler

1. Identify task type and complexity
2. Apply philosophical constraints
3. Retrieve relevant micro-task-documents
4. choose relevant agent/s
5. Assemble minimal context

### What it does:

- Receives task description from AI
- Searches knowledge base for relevant patterns
- Applies philosophy filtering
- Returns minimal required context

### Key methods you'll implement:

assemble_context(task_description) -> context_dict
get_relevant_patterns(task) -> patterns
minimize_context(full_context) -> minimal_context

## Philosophy

philosophy's value - it prevents over-engineering and maintains vision alignment.

**Philosophy as Constraints, Not Preambles**

### task-metadata/create-feature.yaml

constraints:
max_complexity: "mvp" # Blocks over-engineering
approval_required: false if no new dependencies
forbidden_patterns:

- "custom_components" # Use existing shadcn
  - "custom_authentication" # Use existing auth
  - "custom_state_management" # Use framework defaults
  - "premature_optimization"

decision_filters: - "Will this work for 100 users? Ship it." - "Can we buy this instead of building?" - "Is there a simpler solution that's 80% as good?"

## philosophy/core.yaml

```yaml
core_principles:
  efficiency_first:
    rule: "Can this be simpler?"
    evaluation: "Would removing this feature break core value?"
    anti_pattern: "Building for imaginary scale problems"

  customer_value:
    rule: "Does this directly improve user experience?"
    evaluation: "Can a user notice this improvement today?"
    anti_pattern: "Backend optimizations before frontend works"

  minimal_viable:
    rule: "Ship the smallest thing that delivers complete value"
    evaluation: "Is every line necessary for the feature to work?"
    anti_pattern: "Shipping broken features to seem 'agile'"

  compound_progress:
    rule: "Each task should enable the next"
    evaluation: "What does this unlock?"
    anti_pattern: "Building isolated perfect components"

decision_framework:
  always_ask:
    - "What's the simplest solution that completely works?"
    - "Can we validate this assumption with less code?"
    - "Are we solving a real problem or an interesting one?"
    - "What would we build if we had to deploy today?"
```

## Task Micro-Files with Built-In Philosophy

````
---
task: create-user-dashboard
value_delivered: "Users can see their key metrics"
complexity_score: 3
---

# Task: Create User Dashboard

## Minimal Viable Implementation
```tsx
// This COMPLETELY works but nothing more
export function Dashboard() {
  const stats = useStats() // Just 3-4 key numbers
  return <StatsGrid stats={stats} />
}
````

### Philosophy as Evaluation, Not Restriction

````python
def evaluate_solution(solution, task_requirements):
    """
    Philosophy evaluates HOW WELL solution achieves goals,
    not WHETHER it fits arbitrary constraints
    """

    # GOOD evaluations
    scores = {
        "completeness": solution.meets_all_requirements(),
        "simplicity": solution.no_unnecessary_complexity(),
        "maintainability": solution.easy_to_understand(),
        "value_delivery": solution.solves_user_problem(),
    }

    # BAD evaluations (arbitrary)
    # NOT: "line_count": solution.lines < 100
    # NOT: "file_count": solution.files <= 3
    # NOT: "dependency_limit": solution.deps <= 2

    return sum(scores.values()) / len(scores)


### Complexity Scoring Instead of Time

Replace time budgets with **complexity scores** that philosophy evaluates:

```yaml
# Complexity is about decision depth, not time
complexity_rubric:
  1: "Single file, single responsibility, no decisions"
  2: "Standard pattern, minor adaptations"
  3: "Combining patterns, some design decisions"
  4: "New pattern needed, architectural impact"
  5: "Multiple system changes, data migration"

  # Philosophy needs human approval so the following can be determined:
  # - Customer data proves necessity
  # - Simpler solution attempted and failed
  # - Technical debt payment (measured)
````

## Arbitrary Limits Are Anti-Philosophy

Arbitrary limits these are fake simplicity - optimizing for metrics instead of outcomes.

### What is measured

quality_signals:

- "Solves the stated problem completely"
- "No unnecessary abstractions"
- "Dependencies justified by value"
- "Code clarity over brevity"
- "Maintenance burden is minimal"

## document patterns

---

id: user-authentication
complexity_factors:

- "OAuth flow handling"
- "Session management"
- "Security requirements"

---

# Pattern: User Authentication

## Simplest Complete Solution

```typescript
// Uses NextAuth because it handles complexity for us
// Line count is irrelevant - this is the simplest way
// to get secure, complete authentication
```
