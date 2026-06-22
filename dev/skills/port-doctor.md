---
description: "Управление локальными сервисами и портами. Используй когда пользователь говорит 'порты', 'ports', 'port doctor', 'сервис висит', 'kill port', 'что занимает порт'. НЕ используй для: Docker sandbox (docker-sandbox), деплоя (session-finish)."
allowed-tools: Bash, Read, Edit, Write
---

# Port Doctor — Управление сервисами

Скрипт: `~/lance-claude/10-CLAUDE/port-doctor/port-doctor.sh`
Реестр: `~/lance-claude/10-CLAUDE/port-doctor/ports.json`
Состояние: `~/lance-claude/10-CLAUDE/port-doctor/state.json`

## Команды

Пользователь вызывает `/port-doctor [команда] [сервис]`:

| Аргумент | Действие |
|----------|----------|
| (пусто) или `status` | Показать статус всех сервисов |
| `on <service>` | Включить + запустить + запомнить |
| `off <service>` | Выключить + остановить + запомнить |
| `start` | Запустить все enabled |
| `stop` | Остановить все |
| `ports` | Карта портов |
| `conflicts` | Найти конфликты |

## Выполнение

1. Разбери аргументы из `$ARGUMENTS`: первое слово = команда, второе = сервис
2. Запусти `port-doctor.sh` с нужными аргументами
3. Покажи результат пользователю

```bash
~/lance-claude/10-CLAUDE/port-doctor/port-doctor.sh $ARGUMENTS
```

Если пользователь просит "включи X" или "запусти X" — используй `on X`.
Если "выключи X" или "останови X" — используй `off X`.
Если просто спрашивает что работает — используй `status`.
