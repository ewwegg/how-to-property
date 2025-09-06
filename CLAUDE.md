# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains documentation and design for a **Context-First Agent Framework** - a pattern-based AI code generation system that enforces philosophical constraints to ensure quality, consistency, and maintainability.

## Core Architecture

### Pattern-First Generation Philosophy
The framework's fundamental rule: **Code can only be generated from patterns**. Patterns are created under philosophical constraints before any code generation, ensuring every line follows established principles.

### Key Components

1. **Philosophy Engine** (`philosophy.md`): Active constraint system that guides pattern creation
2. **Domain Agents**: Specialized agents for different areas (infrastructure, frontend UI/logic, API, database, testing)
3. **Pattern Library**: Markdown files with minimal frontmatter metadata stored in `.ai/patterns/`
4. **Orchestrator**: Coordinates agent selection and ensures pattern-first workflow
5. **Vector Search**: LanceDB implementation for semantic pattern discovery

## Implementation Structure

When implementing this framework, follow this directory structure:
```
.ai/
├── agents/           # Domain-specific agents
├── patterns/         # Pattern library by domain
├── lib/              # Core utilities (vector search, validation)
├── philosophy.md     # Active philosophical constraints
├── orchestrator.py   # Main coordinator
└── .lancedb/        # Vector database storage
```

## Development Principles

### Pattern Requirements
Every pattern must:
- Solve exactly one problem completely
- Work without modification
- Include all manual setup steps
- Use minimum viable code
- Follow framework conventions
- Handle errors appropriately
- Include types/validation

### Anti-Patterns to Avoid
- Custom implementations when libraries exist
- Abstractions without immediate use
- TODO comments or placeholder code
- Configuration without purpose
- Premature optimization
- Multiple solutions for one problem
- Partial implementations

## Implementation Phases

### Phase 1: Core Foundation
Build pattern creation engine, initial domain agents, philosophy constraint system, and basic orchestrator. Focus on establishing pattern-first workflow where code can only come from validated patterns.

### Phase 2: Intelligence
Add pattern learning, composition system, usage-based evolution, and smart search capabilities while maintaining philosophical constraints.

### Phase 3: Ecosystem (Future)
Enable community pattern sharing with certification system and marketplace, only after proving pattern-first approach delivers value.

## Key Implementation Files

- `agent-framework.md`: Complete framework architecture and philosophy
- `implementation-phases.md`: Detailed implementation roadmap
- `phase-01.md`: Step-by-step guide for building from zero
- `framework-improvements.md`: Complete code examples and setup scripts
- `philosophy.md`: Core philosophical constraints

## Critical Success Factors

1. **Never generate free-form code** - Everything must come from patterns
2. **Validate patterns against philosophy** before saving
3. **Track pattern reuse metrics** to measure framework effectiveness
4. **Maintain strict pattern-first discipline** even for "one-off" tasks