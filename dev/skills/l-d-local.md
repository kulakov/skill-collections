---
name: local-model
aliases:
  - l-d-local
  - claude-local
description: "Запуск Claude Code с локальной моделью через Ollama. Используй когда пользователь говорит 'локальная модель', 'Ollama', 'запусти локально', 'local model', 'offline mode', 'без API', 'экономия токенов'. Прогрев, выбор модели, запуск сессии. НЕ используй для: Docker sandbox (docker-sandbox), Agent SDK проектов (l-d-agent-sdk), обычной работы с Claude API."
---

# Local Model — Claude Code + Ollama

Скилл для запуска Claude Code с локальной моделью через Ollama на M3 Max 36GB.

## Доступные модели

| Модель | Размер | Назначение |
|--------|--------|------------|
| devstral-small-2-64k | 15GB | Код, рефакторинг, мелкие фиксы (рекомендуется) |
| qwen2.5-coder:32b | 19GB | Альтернатива для кода |
| deepseek-coder-v2:16b | 8.9GB | Лёгкая модель для простых задач |

## Пошаговый запуск

### 1. Проверить что Ollama запущен

```bash
curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; [print(m['name']) for m in json.load(sys.stdin)['models']]"
```

### 2. Прогреть модель (обязательно при первом запуске)

```bash
curl -s http://localhost:11434/api/generate -d '{"model":"devstral-small-2-64k","prompt":"hi","stream":false}' | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK, load:', round(d.get('load_duration',0)/1e9,1), 's')"
```

Без прогрева первый ответ занимает 3+ минуты (загрузка 15GB в GPU).

### 3. Запустить Claude Code

```bash
claude-local                                    # интерактивный режим
claude-local devstral-small-2-64k -p "задача"   # одноразовый запрос
claude-local qwen2.5-coder:32b                  # другая модель
```

Shell-функция `claude-local` определена в `~/.zshrc`:
```bash
claude-local() {
  local model="${1:-devstral-small-2-64k}"
  shift 2>/dev/null
  ANTHROPIC_API_KEY=ollama ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_BASE_URL=http://localhost:11434 claude --model "$model" "$@"
}
```

## Когда использовать локально vs облако

**Локально (экономия, приемлемое качество):**
- Рутинный рефакторинг, мелкие фиксы
- Генерация CLAUDE.md, документации
- Docker sandbox задачи
- Простые скиллы (translate, file-organizer)

**Облако (нужен deep reasoning):**
- thinking-partner, коуч-сессии
- thesis-extraction, big-summary
- Контент от имени Lance (стиль)
- spec-driven на сложных фичах

## Известные ограничения

- count_tokens возвращает 404 (норма — Ollama не поддерживает)
- `ollama launch claude` не работает в v0.15.5 (MLX баг)
- Startup: 20-30 сек на загрузку MCP/skills + время прогрева модели
- Нет prompt caching, batch processing, PDF support
