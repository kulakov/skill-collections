---
description: "Google Sheets — чтение, запись, конвертация markdown<->Sheets. Используй когда пользователь говорит 'запиши в таблицу', 'прочитай таблицу', 'обнови sheets', 'Google Sheets', 'spreadsheet', 'таблица', 'залей в Sheets', 'скачай из Sheets', 'markdown в таблицу', 'таблицу в markdown', 'покажи что в табличке', 'данные из гугла', или даёт ссылку docs.google.com/spreadsheets. НЕ используй для: Excel/XLSX файлов на диске, CSV-файлов (bash), Google Docs (другой API), таблицы подписок (subscriptions)."
---

# Google Sheets — чтение, запись, конвертация

MCP-сервер: `gsheets` (mcp-gsheets)
Service account: `claude-sheets@gen-lang-client-0475653459.iam.gserviceaccount.com`

## Подключение таблицы

- **Приватная:** расшарить на service account email как Editor
- **Публичная** (Anyone with link): ничего не нужно

## Извлечение Spreadsheet ID

Из URL `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit...` → берём `SPREADSHEET_ID`.

Если пользователь дал URL — извлеки ID автоматически, не спрашивай.

## Операции

### 1. Прочитать данные

Инструмент: `sheets_get_values`
Параметры: `spreadsheetId`, `range` (формат `Sheet1!A1:Z100` или просто `Sheet1`)

Если лист не указан — сначала `sheets_get_metadata` чтобы узнать имена листов.

### 2. Записать данные

Инструмент: `sheets_update_values`
Параметры: `spreadsheetId`, `range`, `values` (двумерный массив)

### 3. Добавить строки в конец

Инструмент: `sheets_append_values`
Параметры: `spreadsheetId`, `range` (лист), `values`

### 4. Создать новый лист

Инструмент: `sheets_insert_sheet`
Параметры: `spreadsheetId`, `title`

### 5. Очистить диапазон

Инструмент: `sheets_clear_values`
Параметры: `spreadsheetId`, `range`

## Конвертация Markdown <-> Sheets

### Markdown → Sheets

1. Распарси markdown-таблицу: заголовки = первая строка, данные = остальные
2. `sheets_update_values` с range `Sheet1!A1` и values = [[заголовки], [строка1], [строка2], ...]
3. Покажи сколько строк/столбцов записано

### Sheets → Markdown

1. `sheets_get_values` — получи данные
2. Первая строка = заголовки, остальные = данные
3. Сформатируй как markdown-таблицу с выравниванием
4. Выведи пользователю

## Формат вывода

После любой операции — краткий отчёт:
- Что сделано (прочитано N строк / записано N строк / создан лист "X")
- Если чтение — покажи данные как markdown-таблицу (до 30 строк, если больше — спроси)

## Ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| 403 Forbidden | Таблица не расшарена | Расшарить на `claude-sheets@gen-lang-client-0475653459.iam.gserviceaccount.com` |
| 404 Not Found | Неверный spreadsheetId | Проверить URL |
| Sheets API not enabled | API не включён | Включить в Google Cloud Console |
| MCP not available | Сервер не запущен | Рестартнуть Claude Code |
