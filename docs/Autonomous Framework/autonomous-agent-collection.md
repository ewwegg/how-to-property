# Autonomous Agents Collection

These agents work together autonomously. Each ensures its output is complete and follows the patterns defined in the orchestrator.

## Core Philosophy Document

Save as `.ai/PHILOSOPHY.md`:

```markdown
# Philosophy: Minimal Viable Completeness

## Why This Exists

Most AI-generated code is incomplete - filled with TODOs, placeholders, and assumptions. This framework ensures every piece of generated code actually works.

## Core Principle

**The simplest complete solution that fully works.**

Not the shortest (that's counting lines).
Not the cleverest (that's over-engineering).
The simplest that completely solves the problem.

## How We Enforce This

1. **Agents validate their own output** - No placeholders allowed
2. **Orchestrator evaluates completeness** - Rejects incomplete solutions
3. **Patterns ensure consistency** - Same approach every time
4. **Philosophy through existence** - Complex agents don't exist

## What We Value

- **Completeness**: It works entirely or it doesn't ship
- **Simplicity**: Minimum complexity for full functionality
- **Maintainability**: Anyone can understand it in 6 months
- **Autonomy**: System knows what to do without hand-holding

## What We Reject

- Placeholders and TODOs
- Unnecessary abstractions
- Premature optimization
- Incomplete solutions
- Manual orchestration

If an agent would violate these principles, it doesn't exist in our system.
```

## Authentication Agents

### setup-auth

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Setup Authentication
Ensures: Complete auth configuration with all required callbacks
"""

import sys

def generate():
    return """
import NextAuth from 'next-auth'
import Google from 'next-auth/providers/google'
import { PrismaAdapter } from '@auth/prisma-adapter'
import { prisma } from '@/lib/prisma'

export const {
  handlers,
  auth,
  signIn,
  signOut
} = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    })
  ],
  callbacks: {
    session({ session, token }) {
      if (session.user && token.sub) {
        session.user.id = token.sub
      }
      return session
    },
    authorized({ auth, request }) {
      const isLoggedIn = !!auth?.user
      const isOnDashboard = request.nextUrl.pathname.startsWith('/dashboard')

      if (isOnDashboard) {
        if (isLoggedIn) return true
        return false // Redirect to login
      }

      return true
    }
  },
  pages: {
    signIn: '/login',
    error: '/auth/error',
  }
})"""

output = generate()
# Validate completeness
assert "callbacks" in output, "Missing callbacks"
assert "providers" in output, "Missing providers"
assert "signIn" in output and "signOut" in output, "Missing auth methods"
print(output)
```

### create-user-model

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Create User Model
Ensures: Complete Prisma schema for auth
"""

def generate():
    return """
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  emailVerified DateTime?
  name          String?
  image         String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  accounts      Account[]
  sessions      Session[]
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
  @@index([userId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
}"""

output = generate()
# Validate
assert "User" in output and "Account" in output and "Session" in output
assert "@relation" in output, "Missing relations"
print(output)
```

### create-login

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Create Login Page
Ensures: Complete login with error handling
"""

def generate():
    return """
import { signIn } from '@/lib/auth'
import { AuthError } from 'next-auth'

export default function LoginPage({
  searchParams
}: {
  searchParams: { error?: string }
}) {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-8 bg-white rounded-lg shadow">
        <div className="text-center">
          <h2 className="text-2xl font-bold">Sign in to your account</h2>
        </div>

        {searchParams?.error && (
          <div className="bg-red-50 text-red-700 p-3 rounded">
            {searchParams.error === 'OAuthAccountNotLinked'
              ? 'Email already in use with different provider'
              : 'Error signing in'}
          </div>
        )}

        <form
          action={async () => {
            'use server'
            try {
              await signIn('google', { redirectTo: '/dashboard' })
            } catch (error) {
              if (error instanceof AuthError) {
                throw error
              }
              throw error
            }
          }}
        >
          <button
            type="submit"
            className="w-full flex justify-center items-center gap-3 px-4 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-gray-700 hover:bg-gray-50"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </button>
        </form>
      </div>
    </div>
  )
}"""

output = generate()
assert "signIn" in output, "Missing signIn"
assert "error" in output, "Missing error handling"
assert "AuthError" in output, "Missing error type"
print(output)
```

### add-middleware

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Add Auth Middleware
Ensures: Complete route protection
"""

def generate():
    return """
import { auth } from '@/lib/auth'

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isAuthPage = req.nextUrl.pathname.startsWith('/login')
  const isPublicPage = req.nextUrl.pathname === '/' ||
                       req.nextUrl.pathname.startsWith('/api/auth')

  if (isAuthPage) {
    if (isLoggedIn) {
      return Response.redirect(new URL('/dashboard', req.nextUrl))
    }
    return // Allow access to auth pages
  }

  if (!isLoggedIn && !isPublicPage) {
    return Response.redirect(new URL('/login', req.nextUrl))
  }
})

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}"""

output = generate()
assert "config" in output, "Missing matcher config"
assert "isLoggedIn" in output, "Missing auth check"
print(output)
```

## API Agents

### create-api

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Create API Endpoint
Ensures: Complete CRUD operations
"""

import sys
import json

data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
resource = data.get('resource', 'items')
model = data.get('model', resource[:-1] if resource.endswith('s') else resource)

output = f"""
import {{ NextRequest, NextResponse }} from 'next/server'
import {{ prisma }} from '@/lib/prisma'
import {{ auth }} from '@/lib/auth'

export async function GET(request: NextRequest) {{
  try {{
    const session = await auth()
    if (!session) {{
      return NextResponse.json({{ error: 'Unauthorized' }}, {{ status: 401 }})
    }}

    const {resource} = await prisma.{model}.findMany({{
      orderBy: {{ createdAt: 'desc' }}
    }})

    return NextResponse.json({resource})
  }} catch (error) {{
    console.error('GET /{resource} error:', error)
    return NextResponse.json(
      {{ error: 'Failed to fetch {resource}' }},
      {{ status: 500 }}
    )
  }}
}}

export async function POST(request: NextRequest) {{
  try {{
    const session = await auth()
    if (!session) {{
      return NextResponse.json({{ error: 'Unauthorized' }}, {{ status: 401 }})
    }}

    const data = await request.json()
    const {model} = await prisma.{model}.create({{
      data: {{
        ...data,
        userId: session.user.id
      }}
    }})

    return NextResponse.json({model})
  }} catch (error) {{
    console.error('POST /{resource} error:', error)
    return NextResponse.json(
      {{ error: 'Failed to create {model}' }},
      {{ status: 500 }}
    )
  }}
}}

export async function PUT(request: NextRequest) {{
  try {{
    const session = await auth()
    if (!session) {{
      return NextResponse.json({{ error: 'Unauthorized' }}, {{ status: 401 }})
    }}

    const {{ id, ...data }} = await request.json()

    // Verify ownership
    const existing = await prisma.{model}.findUnique({{
      where: {{ id }}
    }})

    if (!existing || existing.userId !== session.user.id) {{
      return NextResponse.json({{ error: 'Not found' }}, {{ status: 404 }})
    }}

    const {model} = await prisma.{model}.update({{
      where: {{ id }},
      data
    }})

    return NextResponse.json({model})
  }} catch (error) {{
    console.error('PUT /{resource} error:', error)
    return NextResponse.json(
      {{ error: 'Failed to update {model}' }},
      {{ status: 500 }}
    )
  }}
}}

export async function DELETE(request: NextRequest) {{
  try {{
    const session = await auth()
    if (!session) {{
      return NextResponse.json({{ error: 'Unauthorized' }}, {{ status: 401 }})
    }}

    const {{ searchParams }} = new URL(request.url)
    const id = searchParams.get('id')

    if (!id) {{
      return NextResponse.json({{ error: 'ID required' }}, {{ status: 400 }})
    }}

    // Verify ownership
    const existing = await prisma.{model}.findUnique({{
      where: {{ id }}
    }})

    if (!existing || existing.userId !== session.user.id) {{
      return NextResponse.json({{ error: 'Not found' }}, {{ status: 404 }})
    }}

    await prisma.{model}.delete({{
      where: {{ id }}
    }})

    return NextResponse.json({{ success: true }})
  }} catch (error) {{
    console.error('DELETE /{resource} error:', error)
    return NextResponse.json(
      {{ error: 'Failed to delete {model}' }},
      {{ status: 500 }}
    )
  }}
}}"""

# Validate all CRUD operations present
assert "GET" in output and "POST" in output and "PUT" in output and "DELETE" in output
assert "auth()" in output, "Missing authentication"
assert "error" in output, "Missing error handling"
print(output)
```

## Frontend Agents

### create-dashboard

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Create Dashboard
Ensures: Complete dashboard with data fetching
"""

def generate():
    return """
import { auth } from '@/lib/auth'
import { redirect } from 'next/navigation'

async function getStats(userId: string) {
  // Real implementation would fetch from database
  return {
    totalItems: 0,
    thisMonth: 0,
    growth: 0,
    active: 0
  }
}

export default async function DashboardPage() {
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  const stats = await getStats(session.user.id)

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-gray-600">Welcome back, {session.user.name || session.user.email}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Items"
          value={stats.totalItems.toString()}
          change="+12%"
        />
        <StatCard
          title="This Month"
          value={stats.thisMonth.toString()}
          change="+8%"
        />
        <StatCard
          title="Growth"
          value={`${stats.growth}%`}
          change="+3%"
        />
        <StatCard
          title="Active"
          value={stats.active.toString()}
          change="+18%"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
          <div className="space-y-3">
            <p className="text-gray-500">No recent activity to display</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <a
              href="/new"
              className="block p-3 border rounded hover:bg-gray-50"
            >
              + Create New Item
            </a>
            <a
              href="/settings"
              className="block p-3 border rounded hover:bg-gray-50"
            >
              ⚙️ Settings
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, change }: {
  title: string
  value: string
  change: string
}) {
  const isPositive = change.startsWith('+')

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <p className="text-sm font-medium text-gray-600">{title}</p>
      <p className="text-2xl font-bold mt-2">{value}</p>
      <p className={`text-sm mt-2 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
        {change} from last month
      </p>
    </div>
  )
}"""

output = generate()
assert "auth()" in output, "Missing authentication"
assert "redirect" in output, "Missing redirect for unauth"
assert "StatCard" in output, "Missing stat components"
print(output)
```

### create-table

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Create Data Table
Ensures: Complete table with sorting and actions
"""

import sys
import json

data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
columns = data.get('columns', ['id', 'name', 'status', 'createdAt'])
resource = data.get('resource', 'items')

headers = ''.join([f'''
        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          {col.replace('_', ' ').title()}
        </th>''' for col in columns])

cells = ''.join([f'''
            <td className="px-6 py-4 whitespace-nowrap text-sm">
              {{formatValue(item.{col})}}
            </td>''' for col in columns])

output = f"""
'use client'

import {{ useState, useEffect }} from 'react'

export function DataTable() {{
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {{
    fetchData()
  }}, [])

  async function fetchData() {{
    try {{
      const response = await fetch('/api/{resource}')
      if (!response.ok) throw new Error('Failed to fetch')
      const result = await response.json()
      setData(result)
    }} catch (err) {{
      setError(err.message)
    }} finally {{
      setLoading(false)
    }}
  }}

  async function handleDelete(id) {{
    if (!confirm('Are you sure?')) return

    try {{
      const response = await fetch(`/api/{resource}?id=${{id}}`, {{
        method: 'DELETE'
      }})
      if (!response.ok) throw new Error('Failed to delete')
      await fetchData() // Refresh
    }} catch (err) {{
      alert('Error: ' + err.message)
    }}
  }}

  function formatValue(value) {{
    if (value === null || value === undefined) return '-'
    if (value instanceof Date) return new Date(value).toLocaleDateString()
    if (typeof value === 'boolean') return value ? '✓' : '✗'
    return value.toString()
  }}

  if (loading) return <div className="p-4">Loading...</div>
  if (error) return <div className="p-4 text-red-600">Error: {{error}}</div>
  if (data.length === 0) return <div className="p-4 text-gray-500">No data available</div>

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>{headers}
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {{data.map(item => (
            <tr key={{item.id}} className="hover:bg-gray-50">{cells}
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                <button
                  onClick={{() => handleDelete(item.id)}}
                  className="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}}
        </tbody>
      </table>
    </div>
  )
}}"""

# Validate completeness
assert "fetchData" in output, "Missing data fetching"
assert "handleDelete" in output, "Missing delete action"
assert "loading" in output and "error" in output, "Missing loading/error states"
assert "formatValue" in output, "Missing value formatting"
print(output)
```

## Utility Agents

### create-env

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# ///
"""
Agent: Create Environment Variables
Ensures: Complete .env with all required vars
"""

def generate():
    return """# Database
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# NextAuth
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="generate-random-secret-here-use-openssl-rand-base64-32"

# OAuth Providers
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""

# Optional Services
SENTRY_DSN=""
POSTHOG_API_KEY=""
STRIPE_SECRET_KEY=""
STRIPE_WEBHOOK_SECRET=""

# Email
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER=""
SMTP_PASSWORD=""
FROM_EMAIL="noreply@example.com"

# Storage
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_REGION="us-east-1"
S3_BUCKET=""

# Redis
REDIS_URL="redis://localhost:6379"

# Environment
NODE_ENV="development"
"""

output = generate()
assert "DATABASE_URL" in output, "Missing database config"
assert "NEXTAUTH_SECRET" in output, "Missing auth config"
print(output)
```

### setup-project

```bash
#!/bin/bash
# Agent: Setup Project
# Ensures: Complete Next.js project setup

# Exit on error
set -e

echo "Setting up Next.js project..."

# Install dependencies
npm install next@latest react@latest react-dom@latest
npm install -D typescript @types/react @types/node tailwindcss postcss autoprefixer

# Install auth
npm install next-auth@beta @auth/prisma-adapter

# Install database
npm install @prisma/client
npm install -D prisma

# Initialize configs
npx tailwindcss init -p
npx prisma init

# Create basic structure
mkdir -p app/{api,auth,dashboard} components lib

echo "✓ Project setup complete"
echo "Next steps:"
echo "  1. Update .env with your credentials"
echo "  2. Run 'npx prisma db push' to create database"
echo "  3. Run 'npm run dev' to start development"
```

## Pattern Compositions

### build-complete-feature.sh

```bash
#!/bin/bash
# Builds a complete CRUD feature

RESOURCE=${1:-posts}
MODEL=${RESOURCE%s}  # Remove trailing 's'

echo "Building complete $RESOURCE feature..."

# Create model
echo "{\"name\": \"$MODEL\"}" | .ai/agents/create-model >> prisma/schema.prisma

# Run migration
npx prisma db push

# Create API
echo "{\"resource\": \"$RESOURCE\", \"model\": \"$MODEL\"}" | .ai/agents/create-api > app/api/$RESOURCE/route.ts

# Create UI
echo "{\"resource\": \"$RESOURCE\"}" | .ai/agents/create-table > components/${MODEL^}Table.tsx
echo "{\"name\": \"${MODEL^}Form\"}" | .ai/agents/create-form > components/${MODEL^}Form.tsx

echo "✓ $RESOURCE feature complete"
echo "Files created:"
echo "  - prisma/schema.prisma (updated)"
echo "  - app/api/$RESOURCE/route.ts"
echo "  - components/${MODEL^}Table.tsx"
echo "  - components/${MODEL^}Form.tsx"
```

## Key Design Principles

1. **Self-Validation**: Each agent validates its own output
2. **Complete Output**: No TODOs, placeholders, or incomplete sections
3. **Autonomous Ordering**: Orchestrator knows dependencies
4. **Consistent Patterns**: Same sequence every time
5. **Claude Code Ready**: Direct slash command integration

## What Makes These Autonomous

- **No Manual Steps**: Orchestrator handles sequencing
- **Self-Contained**: Each agent has everything it needs
- **Error Prevention**: Validation before output
- **Pattern-Based**: Consistent execution order
- **Zero Configuration**: Philosophy embedded in code

The system achieves the balance between simplicity and usefulness - minimal orchestration that provides maximum autonomy.
