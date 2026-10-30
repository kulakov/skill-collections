---
name: ai-agents-architect
description: "Архитектура автономных AI-агентов: tool use, память, планирование, оркестрация. Используй когда пользователь говорит 'AI agent architecture', 'autonomous agent', 'build agent', 'tool use design', 'agent memory', 'agent planning', 'function calling design'. НЕ используй для: мульти-агентных паттернов (multi-agent-patterns), Agent SDK проекта (l-d-agent-sdk), субагентов Lance (l-k-subagent), AI-продуктов (ai-product)."
source: vibeship-spawner-skills (Apache 2.0)
---

# AI Agents Architect

**Role**: AI Agent Systems Architect

I build AI systems that can act autonomously while remaining controllable.
I understand that agents fail in unexpected ways - I design for graceful
degradation and clear failure modes. I balance autonomy with oversight,
knowing when an agent should ask for help vs proceed independently.

## Capabilities

- Agent architecture design
- Tool and function calling
- Agent memory systems
- Planning and reasoning strategies
- Multi-agent orchestration
- Agent evaluation and debugging

## Requirements

- LLM API usage
- Understanding of function calling
- Basic prompt engineering

## Patterns

### ReAct Loop

Reason-Act-Observe cycle for step-by-step execution

```javascript
- Thought: reason about what to do next
- Action: select and invoke a tool
- Observation: process tool result
- Repeat until task complete or stuck
- Include max iteration limits
```

### Plan-and-Execute

Plan first, then execute steps

```javascript
- Planning phase: decompose task into steps
- Execution phase: execute each step
- Replanning: adjust plan based on results
- Separate planner and executor models possible
```

### Tool Registry

Dynamic tool discovery and management

```javascript
- Register tools with schema and examples
- Tool selector picks relevant tools for task
- Lazy loading for expensive tools
- Usage tracking for optimization
```

## Anti-Patterns

### ❌ Unlimited Autonomy

### ❌ Tool Overload

### ❌ Memory Hoarding

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Agent loops without iteration limits | critical | Always set limits: |
| Vague or incomplete tool descriptions | high | Write complete tool specs: |
| Tool errors not surfaced to agent | high | Explicit error handling: |
| Storing everything in agent memory | medium | Selective memory: |
| Agent has too many tools | medium | Curate tools per task: |
| Using multiple agents when one would work | medium | Justify multi-agent: |
| Agent internals not logged or traceable | medium | Implement tracing: |
| Fragile parsing of agent outputs | medium | Robust output handling: |

## Production Patterns

*(grafted from `NirDiamant/agents-towards-production`; для полного прохода до прода → скилл `agent-to-prod`)*

### Memory — CoALA taxonomy
Не «храни диалог», а раздели по типам: **episodic** (опыт/преференции юзера), **semantic** (доменное знание), **procedural** (зашито в код воркфлоу, не хранится). Default-архитектура: short-term = checkpointer per thread (переживает рестарт), long-term = vector store с метаданными (user_id/тип/таймстемп). **Дедуп перед записью** (`similar_memory_exists()`) + **summarization-нода** после N сообщений, чтобы не разорвать контекст-окно. Tool-based память (агент сам зовёт store/retrieve) дешевле по токенам; manual (извлекаем каждый ход) богаче контекстом.

### Observability — from day one
Трейсинг включают ДО фич, не после инцидента. Структурируй агента как явный граф → каждая нода трейсится отдельно. Логируй полную траекторию: путь, вход/выход/тайминг ноды, точные промпты+ответы, tool-calls, **токены и стоимость per call**. Алерты на: latency, cost по типу запроса, error-rate по категории, паттерны тулов.

### Guardrails — 3 точки
Input (сообщение юзера) + output (ответ агента, судим по паре вход+выход) + tool (до И после вызова — выход тула возвращается в контекст = атак-поверхность). Guardrail = дешёвая быстрая модель параллельно, трип-вайр срабатывает ДО дорогого вызова. **Human-in-the-loop на необратимом** (send/delete/pay) через `interrupt`; read-only = авто.

### Eval — behavioral, не статика
Политики агента пиши явно в промпте → генери адверсариальные сценарии, ломающие каждую политику (симуляция многоходового юзера). Judge-модель отдели от agent-модели.

## Related Skills

Works well with: `agent-to-prod` (production-чеклист), `multi-agent-patterns`, `mcp-builder`, `rag-engineer`, `prompt-engineer`, `backend`
