---
name: figma-roundtrip
aliases:
  - l-d-figma
description: "Figma <-> Code раундтрип. Используй когда пользователь говорит 'сверстай из Figma', 'Figma to code', 'figma to html', 'перенеси дизайн в код', 'сделай из макета', 'from Figma', 'экспорт из Figma', 'верни в Figma', 'code to Figma'. Двунаправленный воркфлоу: читает дизайн из Figma (MCP), генерирует HTML/React, помогает вернуть обратно. НЕ используй для: лендинга по референсу сайта (/l-d-vibe-landing), методики копирайтинга (/l-d-landing), генерации дизайн-системы (/l-d-design-system), декомпозиции референсов (/l-d-decompose)."
---

# Figma <-> Code Roundtrip

Двунаправленный воркфлоу между Figma и кодом.

## Направление 1: Figma -> Code

### Шаги

1. **Получи ссылку** на фрейм в Figma (с `node-id` в URL)
2. Извлеки `fileKey` и `nodeId` из URL:
   - `https://figma.com/design/:fileKey/:fileName?node-id=:int1-:int2`
   - `nodeId` = `int1:int2`
3. Вызови `mcp__claude_ai_Figma__get_design_context` с fileKey и nodeId
4. Вызови `mcp__claude_ai_Figma__get_screenshot` для визуальной сверки
5. Конвертируй код в целевой стек (не обязательно React+Tailwind)
6. Все размеры — в vw относительно оригинального канваса:
   - `pixel_value / canvas_width * 100` = vw
   - Пример: 60px на 3840px канвасе = 1.5625vw

### Правила генерации

- Ассеты из Figma (img URLs) живут 7 дней
- Шрифты подключай через `@font-face { src: local() }` — пользователь должен иметь их установленными
- Используй `object-fit: cover` для фоновых изображений
- Все единицы — vw для масштабируемости
- Добавляй переключатель вариантов если нужно сравнение (кнопки в углу)

## Направление 2: Code -> Figma

### Реальность (на февраль 2026)

Официальный Figma MCP — **только чтение**. Нет `create_frame`, `push_design` и т.п.
"Code to Canvas" из блога Figma от 17.02.2026 — анонс/vision, не рабочая фича через MCP.

### Рабочие способы

**Способ A: html.to.design (рекомендуемый)**

1. Установить [Figma Plugin](https://www.figma.com/community/plugin/1159123024924461424)
2. Установить [Chrome Extension](https://chromewebstore.google.com/detail/htmltodesign/ldnheaepmnmbjjjahokphckbpgciiaed)
3. Открыть HTML в браузере
4. Нажать иконку расширения -> импорт в Figma как редактируемые слои

Варианты загрузки:
- **Chrome Extension** — захватывает отрендеренную страницу (лучше для локальных файлов)
- **File Tab** в плагине — копипаст HTML-кода
- **ZIP** — упаковать HTML + CSS + ассеты (до 32MB)

**Способ B: Plugin API через DevTools (хак)**

1. Открыть Figma в браузере
2. Через Chrome DevTools CDP MCP инжектить JS
3. Вызывать `figma.createFrame()`, `figma.createText()` и т.д.
4. Требует отдельный MCP-сервер для CDP

**Способ C: Web to Figma (альтернатива)**

[Плагин](https://www.figma.com/community/plugin/1297530151115228662) — вставить HTML-код напрямую в плагин

## Доступные MCP-инструменты Figma

| Тул | Направление | Описание |
|-----|-------------|----------|
| `get_design_context` | Figma -> Code | Структура + стили + ассеты -> код |
| `get_screenshot` | Figma -> Code | Скриншот ноды |
| `get_metadata` | Figma -> Code | XML-структура слоёв |
| `get_variable_defs` | Figma -> Code | Дизайн-токены |
| `get_code_connect_map` | Figma -> Code | Маппинг нод на компоненты |
| `generate_diagram` | Code -> FigJam | Только Mermaid.js (flowchart, gantt...) |
| `send_code_connect_mappings` | Code -> Figma | Маппинг нод на файлы кода |
| `create_design_system_rules` | Code -> Figma | Правила дизайн-системы |

## Советы

- При замене шрифта: визуальный размер != кегль. Тонкий шрифт нужно увеличивать на 25-35%
- Letter-spacing для тонких шрифтов: меньше чем для жирных (буквы "разваливаются")
- Всегда сверяй с `get_screenshot` — код может врать
- Для сравнения вариантов: кнопки-переключатели + CSS-классы на контейнере

## Аргументы

- `$ARGUMENTS` — URL фрейма в Figma ИЛИ путь к HTML-файлу для обратной конвертации. Если URL — направление Figma->Code. Если путь к файлу — направление Code->Figma.
