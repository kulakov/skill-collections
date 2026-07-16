# Agency Starter Template — Claude Code Instructions

## Project Type
This is a [PROJECT_TYPE] project for [CLIENT_NAME].
Stack: Next.js 15 + Tailwind CSS v4 + shadcn/ui + Vercel

## CMS Policy
- NEVER suggest or choose a CMS. CMS is decided before coding starts and specified in the project spec.
- If no CMS is specified, default to NO CMS (content in markdown/JSON files).
- Front-end and CMS must be independently deployable.
- No embedded CMS (e.g. Payload-in-Next.js).

## CSS Rules
- ONLY use Tailwind CSS utility classes. Never write custom CSS or `<style>` tags.
- Use shadcn/ui components for all UI elements. Check available components before building custom ones.
- Use the `cn()` utility for conditional classes.
- Never use `!important`.
- For layout: use flex/grid utilities, never floats.
- Responsive: mobile-first (sm:, md:, lg:, xl:).

## Component Architecture
- Every visual element must be a reusable component in `src/components/`.
- Components must not affect elements outside their boundary.
- Use composition over inheritance.
- Check existing shadcn/ui components before creating custom ones.

## Security (MANDATORY)
- NEVER hardcode API keys, tokens, or secrets. Use environment variables.
- ALWAYS validate and sanitize user input on the server side.
- ALWAYS set security headers: Content-Security-Policy, X-Frame-Options, X-Content-Type-Options.
- ALWAYS implement CSRF protection on forms.
- ALWAYS use parameterized queries (never string concatenation for SQL).
- For auth: use established libraries (NextAuth, Lucia, Clerk). Never roll your own.
- Run `npm audit` before every deploy.

## Workflow
- Follow SDD: requirements -> design -> tasks -> implement
- One task per Claude Code session. `/clear` between tasks.
- Use subagents for research (don't pollute main context).
- Run `/security-reviewer` after implementing auth, forms, or API routes.
- Run Playwright visual tests after each page completion.

## File Structure
```
src/
  app/           # Next.js App Router pages
  components/    # Reusable UI components
  lib/           # Utilities, API clients, helpers
  styles/        # Only globals.css with @tailwind directives
public/          # Static assets
content/         # Markdown/JSON content (if no CMS)
specs/           # SDD specification files
```
