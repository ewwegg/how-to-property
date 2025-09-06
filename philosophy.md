# Philosophy

## Principles

**Minimal Viable Completeness**  
The simplest solution that fully solves the problem. Not the shortest, not the cleverest - the simplest complete solution.

**No Reinvention**  
Use existing libraries, components, and patterns. If shadcn/ui has it, use it. If the framework provides it, use it.

**Production-First**  
Every pattern must be deployable as-is. No toy examples, no simplified versions - real code for real use.

**Explicit Dependencies**  
Every import and package has a clear purpose. No "might need it later" additions.

## Pattern Requirements

Every pattern must:

- Solve exactly one problem completely
- Work without modification
- Include all manual setup steps
- Use the minimum viable code
- Follow framework conventions
- Handle errors appropriately
- Include types (TypeScript) or validation (schemas)

## Anti-Patterns

- Custom implementations when libraries exist
- Abstractions without immediate use
- TODO comments or placeholder code
- Configuration without purpose
- Premature optimization
- Multiple solutions for one problem
- Partial implementations requiring assembly

## Code Constraints

- Prefer composition over inheritance
- Use framework defaults over custom configuration
- Include environment variables in setup instructions
- Make side effects explicit and isolated
- Keep components/functions focused on a single responsibility
- Use descriptive names over comments
