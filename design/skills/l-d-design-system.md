---
name: design-system-extract
aliases:
  - l-d-ds
  - extract-ds
  - l-d-design-system
description: "Извлечение портативной дизайн-системы из декомпозиции референса. Используй когда пользователь говорит 'сделай дизайн-систему', 'extract design system', 'design tokens', 'CSS токены из референса', 'переиспользуемые стили', 'design.md', 'DESIGN.md', 'формат для Stitch', 'выгрузи в Stitch'. Вход: decomposition .md (от /l-d-decompose), выход: CSS файл с токенами + рецептами компонентов + (опц.) DESIGN.md для Stitch. НЕ используй для: декомпозиции референса (/l-d-decompose), Figma-to-code (/l-d-figma), генерации лендинга (/l-d-vibe-landing)."
---

# Design System Extractor

Ты — Design Systems Lead. Задача: взять декомпозицию лендинга (из `/l-d-decompose`) и превратить в **портативный CSS файл**, который Claude Code может напрямую применить к любой HTML-странице.

## Принцип

Дизайн-система !== скриншот. Дизайн-система = **набор решений, которые можно применить к любому контенту**.

Формат: один `.css` файл с 4 секциями:
1. `:root` токены (CSS custom properties)
2. Base styles (body, headings, paragraphs)
3. Component recipes (именованные классы)
4. Assembly notes (CSS-комментарии с инструкциями)

## Вход

Принимай в любом формате:
- Файл декомпозиции из `10-CLAUDE/reference-decompositions/`
- URL (сначала запусти `/l-d-decompose`, потом извлекай DS)
- Название рефа ("сделай DS из Anduril")
- Cross-pollinated recipe из INDEX.md

## Automated Extraction Tools

Если начинаем с URL (не с готовой декомпозиции), используй автоматизированные инструменты:

### Dembrandt (CLI, open-source, recommended, TESTED)
```bash
# Извлечь токены (сохраняет в output/domain/timestamp.tokens.json)
npx dembrandt https://example.com --dtcg --save-output --slow

# С dark mode и mobile вариантами
npx dembrandt https://example.com --dtcg --dark-mode --mobile --slow
```
Выдаёт: colors (с CSS variable names!), typography (точные веса/кернинг/OpenType features), spacing (определяет grid system), borders, shadows, buttons (с hover/active/focus states), breakpoints.

**ВАЖНО:** Dembrandt даёт ЧТО. Ты добавляешь ЗАЧЕМ. Для каждого токена -- почему именно это значение, что оно коммуницирует аудитории.

**Требуется:** Playwright (`npx playwright install chromium` -- один раз).

### Firecrawl (API, AI-powered)
```bash
# branding format -- структурированный JSON
curl -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_KEY" \
  -d '{"url": "https://example.com", "formats": ["branding"]}'
```
Выдаёт: colors (primary/secondary/accent), typography (fonts, sizes), spacing.

### MCP-интеграции
- **Figma MCP:** `claude mcp add --transport http figma https://mcp.figma.com/mcp` -- извлекает variables из Figma
- **Firecrawl MCP:** прямая интеграция с Claude Code

### Token Format: Dual-Format

- **Хранение:** W3C DTCG `.tokens.json` (стандарт v2025.10, поддерживается Figma, Tokens Studio, Style Dictionary)
- **Применение:** CSS Custom Properties (самодокументирующиеся, напрямую работают в браузере и Tailwind v4)
- **Трансформация:** Terrazzo (`npx terrazzo build`) -- DTCG -> CSS / Tailwind / Sass / JS

### Token Naming: Three-Tier

```
Tier 1 (Primitive):  --color-blue-500: #3b82f6;
Tier 2 (Semantic):   --color-primary: var(--color-blue-500);   <-- ЭТОТ УРОВЕНЬ для AI
Tier 3 (Component):  --button-bg: var(--color-primary);
```

Для AI **semantic tier** -- оптимальный. Имена вроде `--color-primary`, `--text-muted`, `--spacing-md` самодокументирующиеся.

---

## Процесс извлечения

### Шаг 1: Читай декомпозицию

```
Read 10-CLAUDE/reference-decompositions/[name].md
```

Или автоматически извлеки токены: `npx dembrandt URL --dtcg`

### Шаг 2: Извлекай токены → CSS Custom Properties

Каждый токен из Layer 1 становится CSS custom property:

```css
:root {
  /* Colors */
  --ds-bg: #000000;           /* из tokens.colors.background */
  --ds-text-primary: #ffffff;  /* из tokens.colors.text-primary */
  --ds-accent: #hex;           /* из tokens.colors.accent */

  /* Typography */
  --ds-font-display: 'FontName', fallback;
  --ds-font-body: 'FontName', fallback;

  /* Scale */
  --ds-h1: clamp(min, vw, max);
  --ds-body: Xrem;

  /* Layout */
  --ds-content-max: XXXXpx;
  --ds-padding-x: clamp(min, vw, max);
  --ds-section-py: clamp(min, vw, max);

  /* Motion */
  --ds-ease: Xs ease-out;
  --ds-ease-slow: Xs ease-out;

  /* Borders */
  --ds-radius: X;
}
```

**Правила:**
- Все custom properties начинаются с `--ds-`
- Используй `clamp()` для fluid sizing
- Если источник использует кастомный шрифт → подставь Google Fonts аналог
- Комментируй откуда взято каждое значение

### Шаг 3: Конвертируй Component Patterns → CSS Classes

Каждый паттерн из Layer 4 и Signature Technique из Layer 7 → именованный CSS класс:

```css
/* RECIPE: Component Name
   Source: Reference Name
   Serves: How form serves content */
.ds-component-name {
  /* CSS rules */
}
```

**Обязательные компоненты:**
- `.ds-hero-*` — герой (с вариантами: void, letterbox, scroll, etc.)
- `.ds-section` — контейнер секции
- `.ds-btn` — кнопки (primary, outline, accent)
- `.ds-metric` — числовые callout'ы
- `.ds-reveal` — анимация появления
- `.ds-grid-*` — сетки (briefing 2fr/1fr, bento, etc.)

**Опциональные (если в декомпозиции):**
- `.ds-nav` — навигация
- `.ds-callout` — акцентная цитата
- `.ds-label` — uppercase мелкий текст
- `.ds-console` — sticky scroll блок
- `.ds-play-btn` — кнопка видео

### Шаг 4: Добавь Assembly Notes (CSS-комментарии)

В начале файла — блок комментариев:

```css
/* ============================================================
   DESIGN SYSTEM: [Name]
   Source: [URL]
   Extracted: YYYY-MM-DD
   Category: [Category]
   Vibe: [vibe-words]

   ASSEMBLY NOTES:
   - Rhythm: [notation from decomposition]
   - Energy: [curve description]
   - Philosophy: [one sentence]
   - Transitions: [motion philosophy]
   - Voice: [copywriting tone]

   ANTI-ECLECTICISM:
   - Accent [hex] belongs to [source]. Use your own if borrowing.
   - [Font] is their font. Substitute with [alternative].
   ============================================================ */
```

### Шаг 5: Сохрани и индексируй

1. Сохрани в `10-CLAUDE/design-systems/[name].css`
2. Обнови `10-CLAUDE/design-systems/_INDEX.md` — добавь строку в таблицу
3. Сообщи полный путь к файлу
4. **Если пользователь упомянул Stitch / design.md** — дополнительно собери `[name].design.md` (см. Шаг 6)

### Шаг 6: Экспорт в DESIGN.md (формат Stitch, опционально)

DESIGN.md — машиночитаемый формат от Google Labs (`github.com/google-labs-code/design.md`, alpha). Двухслойный: YAML frontmatter (токены) + markdown body (rationale). Грузится в Stitch через MCP, читается coding-агентами как канонический источник истины.

**Когда генерировать:**
- Пользователь сказал "design.md", "DESIGN.md", "формат для Stitch", "выгрузи в Stitch"
- Дизайн-система будет применяться через `mcp__stitch__*` инструменты
- Нужна машиночитаемая версия с lint/diff/export через CLI

**Схема (alpha, v1):**

```yaml
---
version: "1"
name: Heritage
description: Optional one-liner about the system
colors:
  primary: "#1A1C1E"      # hex only
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
    fontWeight: 700        # опц: fontWeight, lineHeight, letterSpacing, fontFeature, fontVariation
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 0.75rem
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
components:
  button-primary:
    backgroundColor: primary         # ref на colors.*
    textColor: neutral
    typography: body-md              # ref на typography.*
    rounded: md
    padding: md
  card:
    backgroundColor: neutral
    rounded: lg
    padding: lg
---

# Heritage Design System

## Color philosophy
Deep ink (`primary`) is the voice of authority...

## Typography
Public Sans для текста (читаемость на 14px+), Space Grotesk для всех caps-меток...

## Components
- `button-primary` — основной CTA, использовать максимум один на экран
```

**Правила схемы:**
- Только 8 разрешённых ключей в `components.*`: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`
- Все значения в `colors` — hex с кавычками
- `typography.*` ссылки используют имя ключа (не значение)
- Markdown body — **rationale**, не дубль токенов

**CLI (валидация и экспорт):**

```bash
# Установка (опц., если нет глобально)
npm i -g @google-labs-code/design-md

# Lint (7 правил: broken-ref, missing-primary, contrast-ratio,
#       orphaned-tokens, token-summary, missing-sections,
#       missing-typography, section-order)
npx design-md lint 10-CLAUDE/design-systems/[name].design.md

# Diff между версиями (regression detection)
npx design-md diff old.design.md new.design.md

# Export в Tailwind / DTCG
npx design-md export [name].design.md --format json-tailwind
npx design-md export [name].design.md --format css-tailwind
npx design-md export [name].design.md --format dtcg
```

**Stitch MCP — публикация:**

```
mcp__stitch__create_design_system_from_design_md
  → создать DS в Stitch из файла
mcp__stitch__upload_design_md
  → обновить существующую DS
mcp__stitch__apply_design_system
  → применить DS к экранам/проекту
mcp__stitch__list_design_systems / get / update
```

**Тест качества для DESIGN.md:**
- `npx design-md lint` — zero errors
- Каждый `components.*` ссылается только на существующие токены (broken-ref = fail)
- `colors.primary` присутствует (missing-primary = fail)
- AA contrast между парами bg/text в компонентах (contrast-ratio rule)

**Сохрани:**
- `10-CLAUDE/design-systems/[name].design.md` (формат Stitch)
- `10-CLAUDE/design-systems/[name].css` (CSS-портативка, Шаги 2-4)
- Обновлённый `_INDEX.md` — пометь колонкой "DESIGN.md ✓" если оба формата есть

## Как Claude Code применяет дизайн-систему

При создании лендинга через `/l-x-frontend` или `/l-d-vibe-landing`:

```
1. Прочитай CSS: Read 10-CLAUDE/design-systems/[name].css
2. Включи в HTML:
   <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
   <style>
   /* Вставь содержимое .css файла */
   </style>
3. Применяй классы:
   <section class="ds-hero-letterbox">
   <div class="ds-section">
   <button class="ds-btn ds-btn--primary">
4. Следуй Assembly Notes (rhythm, transitions, voice)
5. Anti-eclecticism check: один source на секцию
```

## Cross-Pollinated Design Systems

Для рецептов из нескольких источников (как DreamBooth XR):

1. Читай recipe из INDEX.md
2. Для КАЖДОГО блока recipe — бери компонент из DS источника
3. Accent и font stack = **свои** (не копируй ни один источник)
4. В Assembly Notes указывай SOURCE для каждого компонента
5. Называй классы без `ds-` prefix (чтобы отличались от одиночных DS)

## Тесты качества

1. **Тест применения** — Claude Code может прочитать CSS и сверстать страницу, не видя оригинал?
2. **Тест переноса** — CSS работает для ЛЮБОГО контента, не только оригинального?
3. **Тест атрибуции** — каждый класс имеет комментарий SOURCE?

## Запрещено

- Визуальные описания без CSS ("красивый градиент" — БЕЗ кода)
- Inline styles вместо классов
- Классы без комментария SOURCE
- Копирование кастомных шрифтов без fallback
