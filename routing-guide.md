---
title: AI Agent Quick Routing Decision Tree
type: GUIDE
priority: P0
ai_instructions: 'START HERE. This document routes you to exactly what you need without reading everything.'
---

# AI Agent Quick Routing Guide

## How to Use This Guide

1. **Identify your task type** from the categories below
2. **Follow the decision path** to find which document layers you need
3. **Load only those specific sections** - not entire documents
4. **Skip everything else** - you don't need it for your current task

---

## When NOT to Use This Guide

- **Emergency hotfixes** - Load everything needed immediately, fix first, document later
- **Prototyping/experimentation** - Context efficiency not a priority when exploring
- **Trivial changes** - Don't overthink context for typo fixes or color tweaks
- **Learning new patterns** - Load more context to understand the full picture
- **External integrations** - Framework conventions may override internal patterns

## Integration with Other Files

- If task requires approval → See workflow-orchestration.md (but check complexity tier first)
- If task involves new patterns → See implementation-patterns.md
- If task questions design principles → See core-system.md
- When files conflict → Framework conventions win

## 🎯 Task Router

### "I need to CREATE A NEW COMPONENT"

```
LOAD:
1. CORE-SYSTEM.md → Task Layer → Design System Specifications (colors, variants)
2. IMPLEMENTATION-PATTERNS.md → Task Layer → Component Patterns → Base Component Structure
3. (Optional) IMPLEMENTATION-PATTERNS.md → Response Layer → Component Validation Checklist

SKIP: All workflow documentation, MAP processes, changelog procedures
TIME TO CONTEXT: ~30 seconds
```

### "I need to FIX A BUG"

```
LOAD:
1. IMPLEMENTATION-PATTERNS.md → Task Layer → Error Handling Patterns
2. WORKFLOW-ORCHESTRATION.md → Interaction Layer → Bug Fix Workflow (8 steps)
3. WORKFLOW-ORCHESTRATION.md → Task Layer → Changelog Entry Structure

SKIP: Design specifications, component patterns, MAP creation
TIME TO CONTEXT: ~20 seconds
```

### "I need to ADD A NEW FEATURE"

```
LOAD:
1. WORKFLOW-ORCHESTRATION.md → Task Layer → MAP Document Creation Workflow
2. CORE-SYSTEM.md → System Layer → Development Philosophy (for priority order)
3. IMPLEMENTATION-PATTERNS.md → System Layer → Implementation Priority Order

THEN AFTER MAP APPROVAL:
4. Follow "CREATE A NEW COMPONENT" path above

SKIP: Bug fix workflows, documentation standards
TIME TO CONTEXT: ~45 seconds
```

### "I need to STYLE SOMETHING"

```
LOAD:
1. CORE-SYSTEM.md → Task Layer → Design System Specifications
   - Color Palette (exact values)
   - Visual Hierarchy (60/25/10/5 rule)
   - Component Personality (radius, padding, shadows)
2. DES-style-guide.md → Color System Configuration
   - How to properly use @theme to extend Tailwind

PRINCIPLE: Use @theme to override Tailwind's defaults
- .text-sm will use YOUR size (0.875rem)
- Never create .text-small when .text-sm exists
- Keep semantic utilities like .font-heading

SKIP: All implementation code, workflows, patterns
TIME TO CONTEXT: ~20 seconds
```

### "I need to NAME FILES OR VARIABLES"

```
LOAD:
1. IMPLEMENTATION-PATTERNS.md → Task Layer → Naming Conventions
   - File & Directory Naming (exact patterns)
   - Variable & Function Patterns (exact examples)

SKIP: Everything else
TIME TO CONTEXT: ~10 seconds
```

### "I need to SET UP DATABASE/API"

```
LOAD:
1. CORE-SYSTEM.md → Task Layer → Technical Architecture → Core Stack
2. IMPLEMENTATION-PATTERNS.md → Task Layer → Database Patterns
3. IMPLEMENTATION-PATTERNS.md → Task Layer → Query Patterns

SKIP: UI patterns, workflows, design specs
TIME TO CONTEXT: ~25 seconds
```

### "I need to ADD ANIMATIONS"

```
LOAD:
1. CORE-SYSTEM.md → Task Layer → Design System → Animation Standards
2. IMPLEMENTATION-PATTERNS.md → Task Layer → Animation Patterns
   - Stagger Children Pattern
   - Page Transition Pattern

SKIP: Database, workflows, naming conventions
TIME TO CONTEXT: ~15 seconds
```

### "I need to REQUEST APPROVAL"

```
LOAD:
1. WORKFLOW-ORCHESTRATION.md → Interaction Layer → Communication Patterns → Requesting Approval
2. WORKFLOW-ORCHESTRATION.md → Response Layer → Verification Checklists (pick relevant one)

SKIP: Implementation details, design specs
TIME TO CONTEXT: ~10 seconds
```

### "I need to WRITE TESTS"

```
LOAD:
1. IMPLEMENTATION-PATTERNS.md → Response Layer → Component Validation Checklist
2. WORKFLOW-ORCHESTRATION.md → Response Layer → Implementation Verification
3. IMPLEMENTATION-PATTERNS.md → Interaction Layer → Test Immediately (section 3)

SKIP: Design, workflows, database patterns
TIME TO CONTEXT: ~20 seconds
```

### "I need to UPDATE DOCUMENTATION"

```
LOAD:
1. WORKFLOW-ORCHESTRATION.md → Task Layer → Documentation Standards
2. WORKFLOW-ORCHESTRATION.md → Interaction Layer → Documentation Update Workflow

SKIP: All code patterns, design specs
TIME TO CONTEXT: ~15 seconds
```

---

## 🔍 Quick Lookup Matrix

| If you need...          | Go to Document          | Section                   | Layer       |
| ----------------------- | ----------------------- | ------------------------- | ----------- |
| **Color values**        | CORE-SYSTEM             | Design System             | Task        |
| **Component template**  | IMPLEMENTATION-PATTERNS | Component Patterns        | Task        |
| **File naming**         | IMPLEMENTATION-PATTERNS | Naming Conventions        | Task        |
| **Tech stack versions** | CORE-SYSTEM             | Technical Architecture    | Task        |
| **MAP template**        | WORKFLOW-ORCHESTRATION  | MAP Document Structure    | Task        |
| **Changelog format**    | WORKFLOW-ORCHESTRATION  | Changelog Entry Structure | Task        |
| **Error handling**      | IMPLEMENTATION-PATTERNS | Error Handling Patterns   | Task        |
| **Approval process**    | WORKFLOW-ORCHESTRATION  | Approval Gate Process     | Interaction |
| **Test checklist**      | IMPLEMENTATION-PATTERNS | Component Validation      | Response    |
| **Forbidden patterns**  | CORE-SYSTEM             | Decision Log              | System      |

---

## 💡 Smart Context Loading Examples

### Example 1: "Create an RSVP form with email validation"

```python
# AI Agent loads:
context = {
  "design": load("CORE-SYSTEM.md", "Task Layer", "Design System", ["Colors", "Forms"]),
  "pattern": load("IMPLEMENTATION-PATTERNS.md", "Task Layer", "Form Pattern with Validation"),
  "naming": load("IMPLEMENTATION-PATTERNS.md", "Task Layer", "Naming", ["Components"])
}
# Total context: ~2000 tokens instead of 30,000
```

### Example 2: "Fix the admin dashboard not loading"

```python
# AI Agent loads:
context = {
  "errors": load("IMPLEMENTATION-PATTERNS.md", "Task Layer", "Error Handling Patterns"),
  "auth": load("CORE-SYSTEM.md", "Interaction Layer", "Data Flow Architecture", ["Authentication"]),
  "debug": load("IMPLEMENTATION-PATTERNS.md", "Response Layer", "Pattern Compliance Validation")
}
# Total context: ~1500 tokens instead of 30,000
```

### Example 3: "Add hover animation to cards"

```python
# AI Agent loads:
context = {
  "animation": load("CORE-SYSTEM.md", "Task Layer", "Animation Standards"),
  "cards": load("CORE-SYSTEM.md", "Task Layer", "Component Personality", ["Cards"]),
  "pattern": load("IMPLEMENTATION-PATTERNS.md", "Task Layer", "Animation Patterns")
}
# Total context: ~1000 tokens instead of 30,000
```

---

## 🚀 Progressive Context Loading

### Level 1: Minimal Context (Start Here)

- **What**: Just the specific pattern or value you need
- **When**: You know exactly what to implement
- **Example**: Getting color values or naming pattern

### Level 2: Standard Context (Most Common)

- **What**: Pattern + validation rules
- **When**: Implementing a feature
- **Example**: Creating a component with its checklist

### Level 3: Full Context (Complex Tasks)

- **What**: Multiple layers across 2-3 documents
- **When**: New feature from scratch, debugging complex issues
- **Example**: Full MAP → Implementation → Testing workflow

---

## 🎪 Decision Rules

### IF task involves UI/visual:

→ **ALWAYS** start with CORE-SYSTEM.md Design specifications

### IF task involves code:

→ **ALWAYS** check IMPLEMENTATION-PATTERNS.md for existing patterns

### IF task needs approval:

→ **ALWAYS** check WORKFLOW-ORCHESTRATION.md for process

### IF task is failing/broken:

→ **FIRST** check CORE-SYSTEM.md Decision Log for forbidden patterns
→ **THEN** check IMPLEMENTATION-PATTERNS.md Anti-Patterns

### IF task is completely new:

→ **START** with WORKFLOW-ORCHESTRATION.md MAP creation
→ **WAIT** for approval before loading other contexts

---

## 📊 Context Efficiency Metrics

| Old Approach (8 files)   | New Approach (Smart Loading) | Improvement   |
| ------------------------ | ---------------------------- | ------------- |
| 80,000 characters loaded | 8,000 characters loaded      | 90% reduction |
| 8 files opened           | 2-3 sections loaded          | 75% faster    |
| 5 minutes to find info   | 30 seconds to find info      | 10x faster    |
| High chance of confusion | Direct path to answer        | 95% accuracy  |

---

## 🔄 Update Patterns

When you CREATE something new that doesn't exist:

1. Implement it
2. Document the pattern in IMPLEMENTATION-PATTERNS.md → Pattern Library
3. Update this routing guide if it's a common task

When you FIND an error in documentation:

1. Fix the error in the source document
2. Update any cross-references
3. No need to update other documents (single source of truth)

---

**END OF ROUTING GUIDE**
