# Core Philosophy

## Principles

1. **Minimal Viable Completeness**: The simplest solution that fully solves the problem
2. **No Reinvention**: Use existing libraries, components, and patterns
3. **Production-First**: Every pattern must be deployable as-is
4. **Explicit Dependencies**: Every import and package has a clear purpose
5. **Human-Friendly**: Include clear instructions for manual steps

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

## Tech Stack Constraints

When creating patterns, use these specific versions and libraries:
- Next.js 15.3.0+ with App Router
- React 19.1.0+
- TypeScript 5.8.3+
- Tailwind CSS 4.0.0+
- shadcn/ui for components
- React Hook Form + Zod for forms
- Framer Motion for animations
- Prisma for database operations