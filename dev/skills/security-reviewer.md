---
description: "Security reviewer subagent. Используй когда пользователь говорит 'security review code', 'проверь код на уязвимости', 'security scan', 'найди уязвимости в коде'. Запускает субагента для ревью безопасности. НЕ используй для: OWASP справочника (owasp-security), code review (senior-review)."
allowed-tools: Agent, Read, Grep, Glob
---

# Security Reviewer

Launch a security reviewer subagent to analyze the current project's code.

<instructions>
1. Identify the project root (look for package.json, CLAUDE.md, or similar)
2. Launch an Agent with this prompt:

```
You are a senior security engineer. Review all source code in this project for:

1. **Injection vulnerabilities** (SQL, XSS, command injection, template injection)
2. **Authentication and authorization flaws** (missing checks, privilege escalation, IDOR)
3. **Secrets or credentials in code** (hardcoded API keys, tokens, passwords)
4. **Insecure data handling** (PII exposure, missing encryption, unsafe serialization)
5. **Missing CSRF protection** on forms and state-changing endpoints
6. **Missing security headers** (CSP, X-Frame-Options, X-Content-Type-Options)
7. **Exposed API keys in client-side code** (check .env, config files, frontend bundles)
8. **Missing database access controls** (RLS, row-level security)
9. **Dependency vulnerabilities** (run npm audit or equivalent)
10. **Input validation** (server-side validation on all user inputs)

For each finding:
- File path and line number
- Severity: CRITICAL / HIGH / MEDIUM / LOW
- OWASP Top 10:2025 category (A01-A10)
- Specific fix recommendation with code example

Output format:
## Security Review Report
### CRITICAL (fix immediately)
### HIGH (fix before deploy)
### MEDIUM (fix soon)
### LOW (improve when convenient)
### Summary: X findings (Y critical, Z high)
```

3. Return the subagent's report to the user
</instructions>
