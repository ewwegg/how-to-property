---
title: Core System Specification
type: CORE-SYSTEM
priority: P0
status: Active
ai_instructions: 'This document contains all immutable project decisions. Always reference this first for design and technical constraints.'
character_count: 9500
---

# Core System Specification

## Context Summary

**Purpose**: Single source of truth for all design decisions, technical architecture, and non-negotiable constraints for the website.

**Technical stack**

Core Framework:

- Node.js, version 20.0.0^, JavaScript runtime.
- Next.js, version 15.3.0^, React framework with App Router.
- React, version 19.1.0^, UI library.
- TypeScript, version 5.8.3^, Type-safe development.

Database & ORM:

- PostgreSQL (Neon), version (service), Serverless Postgres database.
- Prisma, version 6.13.0^, Type-safe ORM.

Authentication:

- NextAuth.js, version 4.24.11^, Simple auth for admin.

UI & Styling:

- Tailwind CSS, version 4.0.0^, Utility-first CSS.
- shadcn/ui, version (Latest), Component library.
- clsx, version 2.1.1^, Conditional styling.
- Lucide React, version 0.513.0^, Icon library.

Forms & Validation:

- React Hook Form, version 7.57.0^, Form management.
- Zod, version 3.25.56^, Schema validation.
- @hookform/resolvers, version 3.10.0^, Zod integration.

Animation:

- Framer Motion, version 12.16.0^, Animation library.

Deployment:

- Vercel, CLI, Zero-config deployment.

**Development Philosophy**

1. **MVP Everything First** - Ship the smallest possible version that demonstrates core value. No feature gets built beyond basic functionality until it proves essential.

2. **Single-Person Sustainability** - Choose technologies and patterns you can maintain alone. Avoid complex architectures that require team knowledge.

3. **AI-First Development** - Leverage AI tools for code generation, problem-solving, documentation, and testing before writing anything manually. AI is your primary development partner.

4. **Human-Approved Quality Gates** - All AI-generated code and architectural decisions must pass human review for logic, security, and maintainability.

5. **Component-Driven Architecture** - Build reusable, modular components from day one. Every piece of code should be designed for reuse across projects.

6. **Value-Driven Engineering** - Never refactor, optimize, or enhance anything without clear evidence it provides measurable user or business value. Every engineering decision requires justification.

7. **Proof Before Polish** - Validate demand and usage patterns with real users before investing in performance, scalability, or advanced features.

8. **Ruthless Scope Control** - Kill features aggressively. If it's not essential to the core value proposition, it doesn't get built.

9. **Rapid Iteration Cycles** - Deploy frequently, gather feedback quickly, and pivot fast. Optimize for learning speed over code perfection.

**Design Philosophy**

## Core Principles (Priority Order)

1. **Ship Working Code** - Working software over perfect documentation. Every line of code should provide value to users.

2. **Convention Over Configuration** - Use framework defaults (Next.js, Tailwind) unless there's a compelling reason to deviate.

3. **Progressive Enhancement** - Start simple, add complexity only when proven necessary through usage.

4. **Stable but Flexible Design** - Design system should be consistent but adaptable. Evolution is expected.

5. **Reversible Decisions** - Make changes easy to undo. Avoid one-way doors in architecture.

6. **Extend, Don't Duplicate** - Use Tailwind v4's `@theme` directive to override defaults, keep semantic utilities that add value.

7. **Component Ownership** - Components manage their own styling through variants, reducing scattered styles.

8. **Performance-First** - Choose approaches that support rapid iteration and modern browser features.

## When to Break These Principles

- **Prototyping**: Temporarily ignore design system to explore ideas quickly
- **Emergency Fixes**: Skip documentation requirements for critical production issues
- **Learning/Experimentation**: Try unconventional approaches in isolated branches
- **Third-party Integration**: Adapt to external library requirements when necessary
- **User Feedback**: Deviate from patterns when user testing reveals better approaches

**When to Use**: Reference this document first for any design or architectural decision. These are non-negotiable project constraints.

---

## System Layer (Project Identity)

### Core Mission

Building a fun, functional website for a 50-person birthday party with RSVP management, karaoke signup, and delightful interactions.

### Development Philosophy

- **AI-First Development**: AI agents perform development work with human oversight
- **Pragmatic Decisions**: Decisions can evolve based on real-world usage and feedback
- **Clarity Over Cleverness**: Boring code that works beats clever code that might break
- **Fun Over Professional**: Party website should feel playful, not corporate
- **Iteration Over Perfection**: Ship fast, learn from users, improve continuously

### Non-Negotiable Principles

1. **Component Hierarchy**: shadcn/ui → Compose → Extend → Custom (requires justification)
2. **Single Source of Truth**: Database state over client state
3. **Progressive Enhancement**: Core functionality works without JavaScript
4. **Mobile-First Design**: Assume most users RSVP from phones
5. **Human Approval Gates**: Every implementation requires explicit approval

---

## Task Layer (Requirements & Specifications)

### Design System Specifications

#### Color Palette (Immutable)

```css
--color-background: #292a5e; /* Midnight Navy - main background */
--color-foreground: #ffffff; /* White - primary text */
--color-card: #ffffff; /* White - card backgrounds */
--color-card-foreground: #292a5e; /* Navy - card text */
--color-primary: #c7395f; /* Hot Pink Mama - primary actions */
--color-primary-foreground: #ffffff;
--color-secondary: #ded4e8; /* Lavender Dream - secondary */
--color-secondary-foreground: #292a5e;
--color-accent: #e8ba40; /* Golden Honey - accents */
--color-accent-foreground: #292a5e;
--color-muted: rgba(41, 42, 94, 0.1);
--color-muted-foreground: rgba(41, 42, 94, 0.6);
```

#### Visual Hierarchy

- **Lavender Dream (60%)**: Primary backgrounds, soft canvas
- **Hot Pink Mama (25%)**: CTAs, active states, focus rings
- **Golden Honey (10%)**: Success states, badges, hover accents
- **Midnight Navy (5%)**: Text, shadows, dividers

#### Component Personality

- **Buttons**: 0.5rem radius, generous padding (1rem/2rem), 200ms transitions
- **Cards**: Multi-layer shadows, 0.75rem radius, lift on hover
- **Forms**: 3rem height inputs, 0.375rem radius, pink focus glow
- **Modals**: Glass blur signature (97% opacity, 1.25rem blur)

#### Animation Standards

- **Quick-Slow Pattern**: 200ms entrance, 300ms exit
- **Spring Physics**: stiffness ~400, damping ~30
- **Micro-interactions**: Scale, fade, slide (transform/opacity only)
- **Avoiding Button**: Evasive movement pattern on hover

### Technical Architecture

#### Core Stack (ADL-Approved)

| Technology        | Version  | Purpose                   | Decision Rationale                    |
| ----------------- | -------- | ------------------------- | ------------------------------------- |
| Next.js           | 15.4.6+  | Framework with App Router | Zero-config deployment, instant setup |
| React             | 19.1.0+  | UI Library                | Latest concurrent features            |
| TypeScript        | 5.8.3+   | Type Safety               | Strict mode enforced                  |
| Prisma            | 6.13.0+  | ORM                       | Type-safe database access             |
| PostgreSQL (Neon) | Service  | Database                  | Serverless, perfect free tier         |
| NextAuth.js       | 4.24.11+ | Authentication            | Simple hardcoded admin                |
| Tailwind CSS      | 4.0.0+   | Styling                   | Utility-first, v4 features            |
| shadcn/ui         | Latest   | Components                | Production-ready, customizable        |
| Framer Motion     | 12.16.0+ | Animations                | Best React animation library          |
| Vercel            | Platform | Deployment                | Zero-config, Next.js optimized        |

#### Architecture Patterns

- **Server Components First**: Reduce client bundle
- **Database as Truth**: Let Prisma/PostgreSQL handle state
- **Progressive Enhancement**: HTML first, enhance with JS
- **API Routes**: Next.js API routes for all backend logic

---

## Interaction Layer (How Systems Connect)

### Component Integration Flow

```
User Input → React Component → Server Action → Prisma → Database
                ↓                    ↓              ↓         ↓
          Framer Motion        Validation      Migration  Response
                ↓                    ↓              ↓         ↓
         Visual Feedback       Error State    Data Update  Success
```

### Design Token Flow

1. **Definition**: CSS custom properties in globals.css
2. **Application**: Semantic tokens only (never raw hex values)
3. **Component Usage**: Via CVA variants or Tailwind utilities
4. **Override Strategy**: Component variants, not inline styles

### Data Flow Architecture

1. **Forms**: React Hook Form → Zod validation → Server Action
2. **Authentication**: NextAuth → JWT session → Route protection
3. **Database**: Prisma schema → Type generation → Query builder
4. **Email**: Server action → Resend API → Email delivery

### File Organization Patterns

```
/src
  /app                    # Next.js App Router
    /(auth)              # Auth group routes
    /api                 # API routes
    layout.tsx           # Root layout
    globals.css          # Global styles + theme
  /components
    /ui                  # shadcn/ui components
    /forms              # Form components
    /layout             # Layout components
  /lib
    /utils              # Utility functions
    /db                 # Database utilities
  /types                # TypeScript definitions
```

---

## Response Layer (Validation & Quality Gates)

### Design Validation Checklist

- [ ] ✅ All colors use semantic tokens (no hex values in components)
- [ ] ✅ Components use established variants (no inline styles)
- [ ] ✅ Animations use Framer Motion (no CSS animations)
- [ ] ✅ Glass blur modals maintain signature style
- [ ] ✅ Mobile-responsive at all breakpoints
- [ ] ✅ Accessibility: ARIA labels, keyboard navigation

### Technical Validation Requirements

- [ ] ✅ TypeScript strict mode passes
- [ ] ✅ No console errors in development
- [ ] ✅ All forms have error states
- [ ] ✅ Loading states for async operations
- [ ] ✅ Database migrations reviewed
- [ ] ✅ Environment variables documented

### Performance Budgets

- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Cumulative Layout Shift: < 0.1
- Bundle size: < 200KB (initial)

### Security Requirements

- [ ] ✅ Input validation on all forms
- [ ] ✅ SQL injection prevention (Prisma)
- [ ] ✅ XSS protection (React default)
- [ ] ✅ Admin routes protected
- [ ] ✅ Environment secrets secured

---

## Decision Log (Immutable)

### Accepted Trade-offs

- **Basic admin security**: Acceptable for guest list data
- **Cold starts**: Acceptable for low-traffic site
- **No edit/delete**: Reduces complexity for one-time event
- **Console.log debugging**: Over structured logging
- **Single DB table**: Over normalized schema

### Forbidden Patterns

- ❌ Component-specific CSS files
- ❌ Non-semantic Tailwind classes
- ❌ Inline color values (#hex or rgb())
- ❌ Direct database queries (must use Prisma)
- ❌ Client-side routing (use Next.js navigation)
- ❌ External component libraries (except shadcn/ui)
- ❌ localStorage/sessionStorage usage

### Risk Mitigations

- Test RSVP flow thoroughly before launch
- Manual database backup before event
- CSV export fallback if admin fails
- Test emails with personal account first

---

## Quick Reference Tables

### Component Variant Matrix

| Component | Variants                              | Sizes      | Required Props |
| --------- | ------------------------------------- | ---------- | -------------- |
| Button    | default, brand, ghost, destructive    | sm, md, lg | variant, size  |
| Card      | default, elevated, party, interactive | -          | variant        |
| Input     | default, ghost, party                 | sm, md, lg | variant, size  |
| Badge     | default, success, warning             | -          | variant        |

### Route Protection Matrix

| Route Pattern | Protection        | Redirect |
| ------------- | ----------------- | -------- |
| /admin/\*     | NextAuth required | /login   |
| /api/admin/\* | Session check     | 401      |
| /rsvp         | Public            | -        |
| /             | Public            | -        |

### Environment Variables

| Variable        | Purpose         | Required |
| --------------- | --------------- | -------- |
| DATABASE_URL    | Neon PostgreSQL | ✅       |
| NEXTAUTH_SECRET | Auth encryption | ✅       |
| NEXTAUTH_URL    | Auth callback   | ✅       |
| RESEND_API_KEY  | Email service   | ✅       |
| ADMIN_PASSWORD  | Hardcoded admin | ✅       |

---

**END OF DOCUMENT**
