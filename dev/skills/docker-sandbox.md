---
name: docker-sandbox
aliases:
  - l-d-sandbox
  - sandbox
description: "Запуск Claude Code в Docker Sandbox без подтверждений. Используй когда пользователь говорит 'запусти в песочнице', 'docker sandbox', 'sandbox mode', 'автономно напиши код', 'run in sandbox', 'безопасный режим разработки'. Для задач где нужна автономия без подтверждений. НЕ используй для: обычного кодинга (прямо здесь), удалённого запуска (l-d-local), генерации скаффолда (l-d-agent-sdk)."
---

# Docker Sandbox — Автономный Claude Code

Запуск задач программирования в изолированной песочнице без подтверждений.

## Текущая песочница

```
Имя: claude-lance-claude
Workspace: ~
Статус: активна
```

## Быстрый запуск

### Интерактивный режим
```bash
docker sandbox run claude-lance-claude
```

### С задачей (автономно)
```bash
docker sandbox exec claude-lance-claude bash -c 'source ~/.bashrc && claude -p "ЗАДАЧА" --allowedTools "Bash(command:*),Write,Read,Edit,Glob,Grep"'
```

## Примеры задач

### Рефакторинг
```bash
docker sandbox exec claude-lance-claude bash -c 'source ~/.bashrc && claude -p "Отрефактори модуль X, добавь типизацию" --allowedTools "Bash(command:*),Write,Read,Edit"'
```

### Написание тестов
```bash
docker sandbox exec claude-lance-claude bash -c 'source ~/.bashrc && claude -p "Напиши unit-тесты для функции Y" --allowedTools "Bash(command:*),Write,Read"'
```

### Исправление багов
```bash
docker sandbox exec claude-lance-claude bash -c 'source ~/.bashrc && claude -p "Исправь баг: описание" --allowedTools "Bash(command:*),Write,Read,Edit"'
```

## Управление

```bash
docker sandbox ls                         # список песочниц
docker sandbox stop claude-lance-claude   # остановить
docker sandbox rm claude-lance-claude     # удалить
docker sandbox create claude ~/project    # создать для другого проекта
```

## Важно

- Изменения **изолированы** в microVM
- Для сохранения: `git commit && git push` внутри песочницы
- Песочница видит файлы хоста (read), но пишет только внутрь VM
- Все команды выполняются **без подтверждений** (`--dangerously-skip-permissions`)

## Когда использовать

- Длительные задачи (рефакторинг большого модуля)
- Ночные/фоновые задачи
- Экспериментальный код (не страшно сломать)
- Автоматизация (CI/CD стиль)

## Когда НЕ использовать

- Быстрые правки (проще прямо в IDE)
- Работа с секретами (API ключи в .env)
- Задачи требующие диалога с пользователем
