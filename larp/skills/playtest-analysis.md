---
description: "Анализ плейтест-фидбека: CSV -> темы -> дашборд. Используй когда пользователь говорит 'проанализируй плейтест', 'playtest analysis', 'фидбек плейтеста', 'отзывы плейтеста', 'playtest dashboard', 'анализ отзывов игры'"
---

# Playtest Feedback Analysis

Ты анализируешь CSV с отзывами плейтеста видеоигры и создаёшь интерактивный HTML-дашборд.

## Пайплайн

Код пайплайна: `10-CLAUDE/playtest-analyzer/`

### Шаг 1: Подготовка

1. Спроси у пользователя:
   - Где CSV с отзывами? (путь к файлу)
   - Как называется игра?
   - Краткое описание игры (1 предложение)

2. Проверь что `10-CLAUDE/playtest-analyzer/node_modules` существует. Если нет:
   ```bash
   cd 10-CLAUDE/playtest-analyzer && npm install
   ```

3. Проверь `.env` файл с `ANTHROPIC_API_KEY`. Если нет — попроси у пользователя.

### Шаг 2: Bootstrap конфига

Запусти:
```bash
cd 10-CLAUDE/playtest-analyzer && node bootstrap.js "<путь-к-csv>" --game "<название>" --description "<описание>"
```

Покажи пользователю сгенерированный `config.json`:
- Список тем (themes) — предложи добавить/убрать
- Deep themes — какие темы анализировать глубже
- CSV mapping — правильно ли определены колонки

Дождись подтверждения или правок.

### Шаг 3: Pipeline

```bash
cd 10-CLAUDE/playtest-analyzer && node pipeline.js "<путь-к-csv>"
```

Это занимает время (5-15 мин на 500+ ответов). Отслеживай прогресс.

### Шаг 4: Результат

Покажи пользователю:
- Путь к HTML-отчётам: `10-CLAUDE/playtest-analyzer/data/v{N}/reports/`
- Ключевые метрики из metadata.json
- Предложи открыть Dashboard в браузере

## Для догрузки данных

Если пользователь хочет добавить новые ответы в существующий анализ:
```bash
cd 10-CLAUDE/playtest-analyzer && node pipeline.js "<путь-к-новому-csv>"
```
Это создаст новую версию (v2, v3...) с обновлёнными отчётами.

## Передача коллеге

Папку `10-CLAUDE/playtest-analyzer/` можно скопировать целиком в любой проект.
Коллеге нужно:
1. Скопировать папку
2. `npm install`
3. Создать `.env` с ANTHROPIC_API_KEY
4. `node bootstrap.js feedback.csv --game "Game Name"`
5. `node pipeline.js feedback.csv`

$ARGUMENTS
