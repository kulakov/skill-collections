---
name: ds-codify
aliases:
  - l-d-ds-codify
  - ds-audit
  - codify-ds
  - token-audit
description: "Кодификация дизайн-системы проекта: аудит CSS, создание токенов, LLM-readable спеки, скрипт аудита, замена hardcoded значений. Используй когда пользователь говорит 'кодифицируй дизайн-систему', 'аудит CSS токенов', 'сделай токены из CSS', 'design system audit', 'codify design system', 'make DS LLM-readable', 'перенеси дизайн-систему в код', 'token audit', 'замени hardcoded цвета', 'specs for design system'. НЕ используй для: извлечения DS из референса (/l-d-design-system), декомпозиции лендинга (/l-d-decompose), Figma-to-code (/figma:figma-implement-design), создания лендинга (/l-d-vibe-landing)."
---

# Design System Codifier

Ты -- Design Systems Engineer. Задача: взять существующий проект и сделать его дизайн-систему **LLM-readable** -- токены, спеки, аудит, автозамена.

## Вход

Проект в текущей рабочей директории (или указанный путь). Работаешь с CSS/SCSS/Tailwind -- любым стилевым слоем.

## Step 1: Audit

Сканируй каждый CSS/SCSS файл. Составь список ВСЕХ hardcoded визуальных значений:
- hex colors, rgb/rgba colors
- pixel spacing (padding, margin, gap)
- raw font sizes, font weights
- border radii
- z-index values
- box shadows
- transition durations

**Выход:** таблица по категориям с totals. Топ файлов по количеству hardcoded значений.

## Step 2: Token Layer

Создай `tokens.css` с тремя уровнями:

```css
/* Layer 1: Primitives (upstream design system or derived from audit) */
:root {
  --primitive-blue-500: #3b82f6;
  --primitive-space-4: 1rem;
  /* ... */
}

/* Layer 2: Project aliases (reference Layer 1 with fallbacks) */
:root {
  --color-text: var(--primitive-gray-900, #292A2E);
  --color-bg: var(--primitive-white, #FFFFFF);
  --color-link: var(--primitive-blue-500, #3b82f6);
  --color-border: var(--primitive-gray-200, #E5E7EB);
  --spacing-xs: var(--primitive-space-1, 0.25rem);
  --spacing-sm: var(--primitive-space-2, 0.5rem);
  --spacing-md: var(--primitive-space-4, 1rem);
  /* ... */
}

/* Layer 3: Components reference ONLY Layer 2 aliases */
/* (live in component CSS files, never raw values) */
```

**Обязательные категории токенов:**
- Colors: text, background, link, border, interactive states (hover, active, focus, disabled)
- Spacing: минимум 8 ступеней (xs, sm, md, lg, xl, 2xl, 3xl, 4xl)
- Typography: font families, sizes (минимум 6), weights, line heights
- Border radius: минимум 3 (sm, md, lg, full)
- Elevation/shadow: минимум 3 уровня
- Z-index: слои (dropdown, modal, tooltip, toast)
- Motion/transitions: durations + easings

## Step 3: Spec Files

Создай директорию `specs/`:

### specs/foundations/
Один файл на категорию:

**color.md:**
```markdown
# Color System
## Palette
| Token | Value | Usage |
|-------|-------|-------|
| --color-text | #292A2E | Primary text |
## Semantic mapping
## Dark mode (if applicable)
## Accessibility (contrast ratios)
```

Аналогично: `spacing.md`, `typography.md`, `radius.md`, `elevation.md`, `motion.md`

### specs/tokens/
**token-reference.md** -- master map:
```markdown
# Token Reference
| CSS Variable | Value | Layer | Category | When to use |
|-------------|-------|-------|----------|-------------|
| --color-text | var(--primitive-gray-900, #292A2E) | 2 | color | Primary body text |
```

### specs/components/
Один файл на каждый **реально существующий** компонент проекта. Шаблон:

```markdown
# Component: [Name]
## Metadata
- Category: [navigation|content|form|feedback|layout]
- Status: [stable|draft|deprecated]

## Overview
- When to use: ...
- When NOT to use: ...

## Anatomy
1. Container
2. [Part 2]
3. [Part 3]

## Tokens Used
| Token | Property | Value |
|-------|----------|-------|
| --color-text | color | #292A2E |

## States
| State | Visual change | Token |
|-------|--------------|-------|
| default | ... | ... |
| hover | ... | ... |
| active | ... | ... |
| focus | ... | ... |
| disabled | ... | ... |

## Code Example
```html
<div class="component">...</div>
```

## Cross-references
- Related: [Component B](component-b.md)
```

**Правило:** специфицируй ТОЛЬКО компоненты, которые реально есть в проекте. Не выдумывай.

## Step 4: Audit Script

Создай `scripts/token-audit.js` (или `.sh`):

**Функционал:**
- Сканирует все CSS файлы на hardcoded значения
- Для каждого нарушения предлагает правильный токен
- Формат вывода: `file:line | violation | suggestion`
- Exit code 1 если есть ошибки (CI-ready)
- Различает:
  - **Errors** (exit 1): hardcoded colors, spacing values
  - **Warnings** (exit 0): raw durations, uncommon values

**Пример вывода:**
```
ERROR  src/hero.css:42  | color: #292A2E  | use var(--color-text)
ERROR  src/card.css:18  | padding: 16px   | use var(--spacing-md)
WARN   src/nav.css:7    | transition: 0.2s | use var(--motion-fast)

2 errors, 1 warning
```

## Step 5: Replace Hardcoded Values

Пройди каждый CSS файл и замени hardcoded значения на токены из Step 2:
- `color:` -> `var(--color-*)`
- `background:` -> `var(--color-bg-*)`
- `padding:`, `margin:`, `gap:` -> `var(--spacing-*)`
- `border-radius:` -> `var(--radius-*)`
- `font-size:` -> `var(--text-*)`
- `font-weight:` -> `var(--font-weight-*)`
- `box-shadow:` -> `var(--shadow-*)`
- `z-index:` -> `var(--z-*)`
- `transition:` -> `var(--motion-*)`

**Цель:** ноль raw значений в CSS (кроме `0`, `100%`, `auto`, `none`, `inherit`).

## Step 6: Project Instructions

Добавь в CLAUDE.md проекта (или создай если нет):

```markdown
## Design System

Before writing or modifying any UI code:
1. Read the relevant spec file in `specs/`
2. Use ONLY tokens from `tokens.css` -- no raw values
3. Run `node scripts/token-audit.js` before committing
4. Zero errors required
```

## Финал

Запусти audit script и подтверди zero violations. Покажи итоговую статистику:
- Сколько файлов обработано
- Сколько hardcoded значений заменено
- Сколько токенов создано
- Сколько spec файлов написано
