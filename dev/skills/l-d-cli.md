---
name: cli-creator
aliases:
  - l-d-cli
description: "Создание composable CLI-инструмента из API docs, OpenAPI, curl, SDK или скрипта. Используй когда пользователь говорит 'создай CLI', 'сделай команду', 'build CLI', 'обёртка над API', 'CLI для сервиса', 'command-line tool', 'нужна утилита'. Создаёт durable tool на PATH с doctor, discovery, read/write, --json, companion skill. НЕ используй для: одноразовых скриптов (просто напиши скрипт), MCP-серверов (mcp-builder), Telegram-ботов (telegram-bot-builder), Agent SDK проектов (l-d-agent-sdk)."
---

# CLI Creator

Создание composable CLI, который можно вызывать из любого каталога. Для durable tools, не одноразовых скриптов.

## Шаг 1: Определение

Спроси у пользователя:

1. **Source** — откуда берём API: docs, OpenAPI spec, SDK, curl examples, существующий скрипт, web app (DevTools)
2. **Jobs** — конкретные задачи: `list drafts`, `download logs`, `search messages`, `upload media`
3. **Install name** — короткое имя: `gcal-block`, `tg-admin`, `claude-batch`

Размещение по умолчанию: `~/code/clis/<tool-name>`

Проверь что имя свободно:

```bash
command -v <tool-name> || true
```

## Шаг 2: Выбор runtime

Проверь что установлено:

```bash
command -v node pnpm npm python3 uv cargo rustc || true
```

Приоритет для наших проектов:

| Runtime | Когда |
|---------|-------|
| **Node.js/TypeScript** | Default. Есть SDK, наш стек, npm ecosystem |
| **Python** | Data, file transforms, CSV/SQLite, ML-adjacent |
| **Rust** | Performance-critical, standalone binary, no runtime deps |

Объяви выбор в одном предложении с причиной.

## Шаг 3: Command Contract

Скетч команд в чате **до кодирования**. Используй паттерн product nouns + verbs:

```bash
tool --help                          # все команды
tool --json doctor                   # self-check: auth, config, reachability
tool --json <noun> list              # discovery
tool --json <noun> resolve --name X  # slug/URL -> stable ID
tool --json <noun> get <id>          # read exact object
tool --json <noun> create --dry-run  # safe write preview
tool --json request get /v2/...      # raw escape hatch
```

### Обязательная поверхность

- **`doctor --json`** — проверка auth (source: env/config/flag/missing), config, endpoint reachability, версия. Работает даже без auth (сообщает что missing)
- **Discovery** — найти верхнеуровневые контейнеры (workspaces, projects, channels, queues)
- **Resolve** — имена, URL, slugs -> stable ID (чтобы не искать повторно)
- **Read** — точный объект по ID. Списки с `--limit`, cursor/offset
- **Write** — одно действие = одна команда. `--dry-run` где можно. НЕ прятать writes в broad commands типа `fix` или `auto`
- **`--json`** — везде. Stable shape. Ошибки тоже machine-readable. Без credentials в output
- **Raw escape** — `request get|post /path` с auth и JSON parsing

### JSON Policy

Документируй в README:
- API pass-through vs CLI envelope
- Success shape, error shape
- Один пример на каждый тип команды

## Шаг 4: Auth

Приоритет:

1. **ENV** — стандартное имя сервиса (`GITHUB_TOKEN`, `ANTHROPIC_API_KEY`)
2. **Config file** — `~/.<tool-name>/config.toml` или `~/.config/<tool-name>/config.json`
3. **Flag** — `--api-key` только для тестов (утекает в shell history)

Правила:
- Никогда не печатать полные токены
- `doctor --json` показывает: есть ли токен, откуда (env/config/flag/missing), что настроить

Для web apps из DevTools curls — создать sanitized endpoint notes:
- resource, method/path, headers, auth mechanism, CSRF, body, response IDs, pagination, errors
- **НИКОГДА** не коммитить cookies, bearer tokens, customer secrets

## Шаг 5: Build

1. **Inventory** — прочитать source: ресурсы, auth, pagination, IDs, rate limits, dangerous writes
2. **Sketch** — список команд в чате (Шаг 3)
3. **Scaffold** — CLI + README
4. **Implement** — `doctor` -> discovery -> resolve -> read -> один safe write -> raw escape
5. **Install on PATH** — чтобы `tool-name` работало отовсюду
6. **Smoke test** — из `/tmp`, не из source folder:
   ```bash
   command -v <tool-name>
   <tool-name> --help
   <tool-name> --json doctor
   ```
7. **Validate** — format, typecheck, unit tests для request builders, pagination, no-auth doctor, help output

Live write тестировать только с разрешения, через draft/dry-run.

## Runtime Defaults

### Node.js/TypeScript

```
commander или cac          — commands + help
native fetch или SDK       — HTTP
zod                        — validation (только на boundaries)
tsup                       — build
package.json bin           — installed command
```

Install: `pnpm install && pnpm build && pnpm link --global`
Или Makefile: `make install-local` -> wrapper в `~/.local/bin/`

### Python

```
argparse или typer         — commands
httpx или requests         — HTTP
json, csv, pathlib         — local files
pyproject.toml             — console script
```

Install: `make install-local` -> `~/.local/bin/` wrapper
Документировать: нужен uv/venv или system Python

### Rust

```
clap                       — commands + help
reqwest                    — HTTP
serde / serde_json         — payloads
toml                       — config
anyhow                     — errors
```

Install: `make install-local` -> cargo build --release -> `~/.local/bin/`

## Шаг 6: Companion Skill

После рабочего CLI — создать скилл-компаньон через `/l-k-subagent` или вручную.

Скилл пишется **в порядке использования**, не как tour of features:

```markdown
# <tool-name> CLI

## Проверка
tool-name --json doctor

## Первый запуск
tool-name --json <discovery-command>

## Типовой workflow
tool-name --json ...   # шаг 1
tool-name --json ...   # шаг 2

## Правила
- Используй --json при анализе output
- Создавай drafts по умолчанию
- НЕ publish/delete/retry без явного запроса пользователя
- `request get ...` только когда нет готовой команды

## Примеры
<3 copy-pasteable примера>
```

## Чеклист готовности

- [ ] `command -v <tool-name>` находит binary
- [ ] `--help` показывает все команды
- [ ] `--json doctor` работает без auth (сообщает missing)
- [ ] `--json doctor` работает с auth (all checks pass)
- [ ] Smoke test из `/tmp` проходит
- [ ] README с JSON policy
- [ ] Companion skill создан
