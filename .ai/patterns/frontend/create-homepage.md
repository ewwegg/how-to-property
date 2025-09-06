---
complexity: 3
created: '2025-09-06T13:22:48.018969'
dependencies:
- react
- next
- tailwindcss
- framer-motion
- lucide-react
language: typescript
manual_steps: false
tags:
- homepage
- hero
- features
- landing
task: Create homepage with hero section and features
tech_stack:
- nextjs
- react
- typescript
- tailwind
- framer-motion
updated: '2025-09-06T13:22:48.018972'
version: 1.0.0
---

# Create homepage with hero section and features

## Description

Complete homepage implementation with animated hero section, feature cards, and call-to-action using Next.js, Tailwind CSS, and Framer Motion.

## Setup Instructions

Ensure the following are installed:
- shadcn/ui Button component: `npx shadcn@latest add button`
- Framer Motion: `npm install framer-motion`
- Lucide React icons: `npm install lucide-react`

## Usage

Replace the contents of app/page.tsx with this component. The component provides:
- Animated hero section with CTA buttons
- Feature cards grid with icons and descriptions
- Call-to-action section with gradient background
- Fully responsive design with mobile-first approach

## Notes

This pattern provides a complete, production-ready homepage. All animations are performant using Framer Motion's optimized rendering. The component follows accessibility best practices and uses semantic HTML structure.

## Code

```typescript
import { Button } from "@/components/ui/button"
import { ArrowRight, Zap, Shield, Rocket } from "lucide-react"
import { motion } from "framer-motion"

export default function HomePage() {
  const features = [
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Optimized performance with Next.js 15 and React 19"
    },
    {
      icon: Shield,
      title: "Secure by Default",
      description: "Enterprise-grade security with built-in best practices"
    },
    {
      icon: Rocket,
      title: "Ready to Scale",
      description: "Production-ready architecture that grows with your needs"
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative px-6 lg:px-8 py-24 sm:py-32">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Build something amazing
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
              Start your next project with a modern stack. Fast, secure, and ready to scale.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Button size="lg" className="gap-2">
                Get Started
                <ArrowRight className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="lg">
                Learn More
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 sm:py-32 bg-gray-50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Everything you need
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Built with the best tools and practices
            </p>
          </div>
          
          <div className="mx-auto mt-16 max-w-7xl">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <motion.div
                    key={feature.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    className="relative bg-white p-8 rounded-2xl shadow-sm hover:shadow-lg transition-shadow"
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                        <Icon className="h-6 w-6 text-primary" />
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {feature.title}
                      </h3>
                    </div>
                    <p className="mt-4 text-gray-600">
                      {feature.description}
                    </p>
                  </motion.div>
                )
              })}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="mx-auto max-w-2xl text-center bg-gradient-to-r from-primary/10 to-primary/5 rounded-3xl p-12"
          >
            <h2 className="text-3xl font-bold tracking-tight text-gray-900">
              Ready to get started?
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Join thousands of developers building with our platform
            </p>
            <div className="mt-8">
              <Button size="lg" className="gap-2">
                Start Building
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
```
