---
name: design-oracle
description: "Извлекает дизайн-систему живого сайта по URL через браузер (Playwright): цвета, типографика, spacing, радиусы, компоненты, UX-паттерны, КОМПОЗИЦИЮ (type scale, grid-колонки, выравнивание, ритм секций, паттерны компоновки) и АНИМАЦИИ (CSS transitions с easing, @keyframes, transforms, библиотеки Framer/GSAP/Lenis/AOS, scroll-driven, smooth scroll) → экспорт в DESIGN.md, Tailwind config, React-стабы и JSON-токены. Используй когда пользователь говорит 'проанализируй дизайн сайта', 'извлеки дизайн-систему с сайта', 'какие цвета и шрифты на этом сайте', 'какие анимации на сайте', 'забери анимации с сайта', 'какая композиция/компоновка', 'вытащи токены с URL', 'design tokens с сайта', 'analyze website design', 'extract design system', 'прогони сайт через design oracle', даёт ссылку на сайт и просит разобрать его оформление. НЕ используй для: ручной декомпозиции референса-картинки (l-d-decompose), Figma→код (l-d-figma), вёрстки лендинга по референсу (l-d-vibe-landing), справочника стилей/палитр/брендов без живого сайта (ui-ux-pro-max), генерации дизайн-системы с нуля (l-d-design-system)."
metadata:
  type: tool-wrapper
  app: /Users/lance/lance-claude/10-CLAUDE/design-oracle
---

# Design Oracle

Обёртка над приложением [Design Oracle](https://github.com/jomvick/design-oracle).
Анализирует **живой URL** через headless-браузер и извлекает дизайн-систему.
Запускается через standalone-раннер `run_oracle.py` — **без Docker, Redis и FastAPI**
(только venv + Playwright Chromium).

## Когда срабатывает

Пользователь даёт ссылку на сайт и хочет разобрать его оформление: цвета, шрифты,
spacing, компоненты, UX-паттерны, либо просит готовые design tokens / Tailwind config
с чужого сайта.

## Как запускать

Приложение установлено в `/Users/lance/lance-claude/10-CLAUDE/design-oracle`.

```bash
cd /Users/lance/lance-claude/10-CLAUDE/design-oracle
.venv/bin/python run_oracle.py "<URL>" <slug>
```

- `<URL>` — полный адрес с `https://`
- `<slug>` — опционально; если не задан, генерится из домена

> Playwright ходит в сеть и запускает браузер — выполняй с
> `dangerouslyDisableSandbox: true` (сетевой доступ + Chromium процесс),
> либо предупреди, если запуск заблокирован песочницей.

Первый запуск медленнее. Если venv/Chromium отсутствуют — переустанови:

```bash
python3 -m venv .venv
.venv/bin/pip install "playwright==1.60.*" "beautifulsoup4==4.*" "Pillow==12.*" "tinycss2==1.*"
.venv/bin/python -m playwright install chromium
```

## Результат

Артефакты пишутся в `analyses/<slug>/`:

| Файл | Что внутри |
|------|------------|
| `APPLY_DESIGN.md` | **инструкция для агента-приёмника** — манифест файлов, выбор канала по стеку, инлайн-сводка значений, обязательные гочи (шрифты→OSS, сверка цвета) |
| `DESIGN.md` | человекочитаемый отчёт (стиль, палитра, типографика, компоненты, паттерны, композиция, анимации) |
| `design-tokens.json` | структурированные токены (source of truth) |
| `tokens.css` | CSS custom properties (drop-in для не-Tailwind проектов) |
| `tailwind.config.js` | Tailwind v4 тема |
| `components.jsx` | React-стабы компонентов |
| `result.json` | сырые данные анализа, включая `motion` и `composition` (ground truth) |
| `screenshot.png` | полностраничный скриншот |
| `screenshot-overlay.png` | скриншот с рамками компонентов |

После запуска прочитай `DESIGN.md` и выдай выжимку пользователю.

### Передача дизайна в другой проект

Папка `analyses/<slug>/` — **самодостаточный handoff-пакет**. Чтобы перенести дизайн
в проект, где нужен конкретный визуал, отдай агенту-исполнителю всю папку и укажи
читать `APPLY_DESIGN.md` первым — там манифест и инструкция, как применить по стеку:
Tailwind (`tailwind.config.js`), CSS (`tokens.css`), любой стек (`design-tokens.json`),
композиция+анимации (`DESIGN.md`). Агент сам выберет канал и применит, плюс там
прописаны обязательные шаги: резолв шрифтов в OSS-замену и сверка primary-цвета по скриншоту.

## ВАЖНО — детекция эвристическая, не vision/ML

README приложения прямо предупреждает: компоненты и токены определяются эвристиками.
На практике стабильно врут:

- **Шрифты** — часто падают в CSS-fallback ("Times New Roman", "base", мусорные имена).
  Не верь полю типографики без проверки.
- **Роли цветов** — primary/background могут быть выдернуты из SVG/иллюстрации,
  а не из реального chrome страницы.
- **UX-паттерны** — переоценивают (pricing, FAQ, dark mode, search могут быть ложными).

Поэтому:
1. `result.json` и `screenshot.png` — надёжный ground truth.
2. `DESIGN.md` — черновик первого прохода, помечай артефакты честно.
3. Если нужна точность по шрифтам/цветам — сверь со `screenshot.png`
   через сабагент (по правилу обработки изображений), не тащи картинку в основной контекст.
