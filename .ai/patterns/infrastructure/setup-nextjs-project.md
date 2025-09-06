---
complexity: 2
created: '2025-09-06T13:27:06.362995'
dependencies:
- nodejs
- npm
language: bash
manual_steps: true
tags:
- setup
- nextjs
- typescript
- tailwind
- shadcn
task: Setup Next.js project with TypeScript, Tailwind, and shadcn/ui
tech_stack:
- nextjs
- react
- typescript
- tailwind
- shadcn
updated: '2025-09-06T13:27:06.362999'
version: 1.0.0
---

# Setup Next.js project with TypeScript, Tailwind, and shadcn/ui

## Description

Complete Next.js project initialization with TypeScript, Tailwind CSS, and shadcn/ui component library configured for immediate development.

## Setup Instructions

Prerequisites:
- Node.js 20.0.0+ installed
- Commands must execute in sequence

IMPORTANT:
- If running in existing directory with files, the --force flag will overwrite
- Remove --force flag if you want to be prompted about each conflict
- Consider backing up existing files before running

Environment:
- Creates new Next.js app with App Router
- TypeScript configuration
- Tailwind CSS with default config
- shadcn/ui component system

## Usage

Execute all commands in order from the project root directory. 
The setup creates a production-ready Next.js application with:
- App Router architecture
- TypeScript support
- Tailwind CSS styling
- shadcn/ui components
- Utility functions for className management

## Notes

This pattern creates the minimal viable Next.js setup. 
After running, you'll have:
- Complete Next.js project structure
- Ready-to-use component library
- Development server available via npm run dev
- Production build via npm run build

## Code

```bash
# Initialize Next.js in current directory
# Use --force flag to override existing files (remove if you want prompts)
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*" --yes --force

# Install utility dependencies for component library
npm install clsx tailwind-merge tailwindcss-animate

# Initialize shadcn/ui with defaults
npx shadcn@latest init --yes --defaults

# Create project structure
mkdir -p components/ui lib hooks

# Create cn utility helper
cat > lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF

# Install essential shadcn components
npx shadcn@latest add button
```
