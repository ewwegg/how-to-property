# Notes

##

phases - MVP to Scale - this might be better phrased as "initial" and "additions"? or something similar - or maybe it's fine

do i need 175+ agents? or do i need an agent for "authentication" and then it selects relevant information within itself

- i guess these agents can be good, because they're complete minimal solutions... the "prompt" should be overarching which can combine them.

=======

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
