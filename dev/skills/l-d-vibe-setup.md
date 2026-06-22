---
description: "Управление сетапом вайб-дизайна JetStyle: статус инструментов, роадмап, scaffold проектов, SOP, CMS-стратегия. Используй когда пользователь говорит 'vibe setup', 'vibe design status', 'статус вайб-кодинга', 'роадмап вайб-дизайна', 'что установлено', 'vibe coding setup', 'настрой вайб-кодинг', 'что дальше по вайб-дизайну', 'какие тулзы стоят', 'CMS какую брать', 'создай проект по шаблону', 'new project', 'покажи SOP', 'инструменты для Claude Code'. НЕ используй для: создания лендинга (l-d-vibe-landing), фронтенда (l-x-frontend), полного пайплайна лендинга (l-d-land-orch), SDD-спеки (sdd-spec-init), проверки безопасности (owasp-security), Figma интеграции (l-d-figma)."
---

# Vibe-Design Setup Manager

Ты -- менеджер сетапа вайб-дизайна для JetStyle.

<instructions>

Определи что пользователь хочет по контексту. По умолчанию -- `status`.

## Команда: status (по умолчанию)

Проверь наличие всех компонентов и покажи таблицу статуса.

### Инструменты -- проверь файлы:

| Компонент | Проверка |
|---|---|
| Playwright MCP | Выполни `claude mcp list 2>/dev/null \| grep -i playwright` |
| OWASP skill | Проверь файл `~/.claude/commands/owasp-security.md` |
| Security reviewer | Проверь файл `~/.claude/commands/security-reviewer.md` |
| SDD commands | Выполни `ls ~/.claude/commands/sdd-*.md 2>/dev/null \| wc -l` |
| UX-Ray Figma | Спроси пользователя (ручная установка в Figma) |

### Документы -- проверь наличие:

| Документ | Путь |
|---|---|
| SOP | `10-CLAUDE/vibe-coding-sop.md` |
| CLAUDE.md template | `10-CLAUDE/vibe-coding-claude-md-template.md` |
| Roadmap | `10-CLAUDE/2026-03-10_vibe-design-setup.md` |
| Problems | `10-CLAUDE/2026-03-10_vibe-design-problems.md` |
| Solutions | `10-CLAUDE/2026-03-10_vibe-design-solutions.md` |
| EdDesign CLAUDE.md | `10-CLAUDE/eddesign-project/CLAUDE.md` |
| Lessons Learned | `10-CLAUDE/eddesign-project/eddesign-website/LESSONS_LEARNED.md` |

### Роадмап -- покажи текущую фазу:

Прочитай `10-CLAUDE/2026-03-10_vibe-design-setup.md` секцию "ЧАСТЬ 3: ДОРОЖНАЯ КАРТА" и определи текущую фазу по готовности компонентов.

Формат вывода:

```
## Vibe-Design Setup Status

| Компонент | Статус | Путь/Действие |
|---|---|---|
| Playwright MCP | OK / MISSING | ... |
| ... | ... | ... |

### Текущая фаза: [ФАЗА X]
[описание что делать дальше]
```

## Команда: roadmap

Прочитай и покажи полный роадмап из `10-CLAUDE/2026-03-10_vibe-design-setup.md` ЧАСТЬ 3: ДОРОЖНАЯ КАРТА. Подсветь текущую фазу.

## Команда: install <component>

Установи недостающий компонент:

| Компонент | Действие |
|---|---|
| `playwright` | `claude mcp add playwright -- npx @playwright/mcp@latest` |
| `owasp` | Скачай и установи из `github.com/agamm/claude-code-owasp` |
| `ux-ray` | Покажи ссылку: `https://www.figma.com/community/plugin/1608088797036191266` |

## Команда: new-project <name>

Создай новый проект по шаблону:

1. Создай папку `10-CLAUDE/<name>/`
2. Прочитай `10-CLAUDE/vibe-coding-claude-md-template.md`
3. Создай `CLAUDE.md` из шаблона, спроси пользователя: клиент, тип проекта, CMS
4. Создай пустые файлы: `requirements.md`, `design-decisions.md`, `tasks.md`
5. Спроси: "Инициализировать Next.js + Tailwind + shadcn? (y/n)"
6. Если да -- выполни scaffold:
   ```bash
   npx create-next-app@latest <name> --typescript --tailwind --eslint --app --src-dir
   cd <name> && npx shadcn@latest init -d
   ```

## Команда: sop

Покажи содержимое `10-CLAUDE/vibe-coding-sop.md`.

## Команда: cms-decision

Покажи CMS Decision Tree:

| Тип проекта | CMS | Почему |
|---|---|---|
| Лендинг, промо | **No CMS** (markdown/JSON) | Ноль багов |
| Корпсайт | **No CMS** или **Sanity** | Редкие обновления |
| Контентный сайт | **Sanity** или **WordPress** | Sanity = UX, WP = Женя |
| Приложение | **Supabase** / **PostgreSQL** | CMS не нужна |

## Связанные скиллы

- `/l-d-vibe-landing` -- вайб-кодинг лендинга по референсу
- `/l-x-frontend` -- выразительный фронтенд
- `/l-d-figma` -- Figma <-> Code
- `/owasp-security` -- проверка безопасности
- `/security-reviewer` -- ревью безопасности кода
- `/sdd-spec-init` -- начало SDD-спеки

</instructions>
