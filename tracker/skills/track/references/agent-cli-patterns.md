# Agent CLI Patterns

Reference для проектирования CLI, которые AI-агенты (Claude Code, Codex) вызывают самостоятельно.

Источник: адаптация [openai/skills/cli-creator](https://github.com/openai/skills/blob/main/skills/.curated/cli-creator/references/agent-cli-patterns.md) под нашу экосистему.

## Ментальная модель

CLI = command layer для агента. Превращает сервис, API, лог, базу в shell-команды, которые агент вызывает повторно из любого каталога.

Хороший CLI для агента = composable primitives. Не одна команда "сделай всё расследование", а: discover -> resolve -> read -> inspect -> draft -> upload.

## Help как интерфейс

`--help` пишется для будущего агента, у которого есть только binary и задача. Каждая команда = short description + literal flag names из продукта/API.

Top-level help должен отвечать:
- Какие контейнеры можно обнаружить?
- Какие объекты можно прочитать?
- Какие ID можно resolve?
- Какие файлы скачать/загрузить?
- Какие write actions есть?
- Где raw escape hatch?

## Preferred Command Shape

Product nouns, then verbs:

```bash
tool --json doctor
tool --json accounts list
tool --json projects list
tool --json channels resolve --name codex
tool --json messages search "exact phrase"
tool --json messages context <id> --before 3 --after 3
tool --json logs download <url> --failed --out ./logs
tool --json media upload --file ./image.png
tool --json drafts create --body-file draft.json
```

Consistency > cleverness. Не мешать стили без причины.

## Полезные паттерны из зрелых CLI

```bash
# Field selection
tool issues list --json number,title,url,state
tool issues list --json number,title --jq '.[] | select(.state == "open")'

# Human default, JSON opt-in
tool pods get <name>
tool pods get <name> -o json

# Workflow verbs (не только REST nouns)
tool logs tail
tool webhooks listen --forward-to localhost:4242/webhooks
```

## Порядок проектирования: Discovery -> Resolve -> Read -> Context

1. **Discover** — broad containers: workspaces, accounts, repos, projects, channels, queues
2. **Resolve** — human input (name, URL, slug, permalink) -> stable ID
3. **Read** — exact object by ID: issue, thread, draft, customer, job
4. **Context** — anchor + surroundings: nearby messages, parent thread, audit history

Не заставляй агента повторно искать то, для чего уже есть stable ID.

## Text, JSON, Files, Exit Codes

### --json
- JSON только в stdout
- Progress/diagnostics -> stderr
- Success + error shapes документированы
- Redact: tokens, cookies, secrets, private headers

### Downloads/exports
- `--out` path для файлов
- В JSON: file path, byte count, source URL/ID, follow-up command

### Exit codes
- 0 = success (включая empty result)
- Non-zero = auth failure, invalid input, network error, API error
- `doctor --json` работает даже без auth (report missing, не crash)

## Pagination

Shallow default, explicit knobs для breadth:

```bash
tool messages search "topic" --limit 10
tool messages search "topic" --limit 50 --all-pages --max-pages 3
tool drafts list --limit 20 --offset 40
```

Return `next_cursor`, `next_url`, `offset`, `page_count` — что real для provider.

## Raw Escape Hatch

Repair hatch, не main interface. Всё ещё использует configured auth, base URL, JSON parsing, redaction, error handling.

```bash
tool --json request get /v2/me          # safe read
tool --json request post /v2/... --data '...'  # live write — treat as real
```

## Companion Skill Pattern

Меньше чем CLI README. Учит порядку:

```markdown
Start:
  tool --json doctor
  tool --json accounts list

For [common job]:
  tool --json ...

Rules:
- --json при анализе output
- Drafts by default
- Не publish/delete/retry без запроса user
- `request get ...` только когда нет high-level команды
```

## Применение в нашей экосистеме

| CLI Pattern | Наш аналог |
|---|---|
| `doctor --json` | Диагностика скилла: auth, config, зависимости |
| Discovery -> Resolve | MCP tools: list resources -> get specific |
| Companion skill | Уже есть: skills catalog + description triggers |
| Raw escape hatch | `request` команда для API без готовой обёртки |
| `--json` everywhere | Structured output для pipe между агентами |
