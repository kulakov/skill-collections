# Когда какой Claude — Chat / Cowork / Code

Три поверхности — один Claude underneath. Что меняется: workspace вокруг.

## Таблица выбора

| Если задача… | Поверхность | Почему |
|--------------|-------------|--------|
| Вопрос, переписать, быстрый brainstorm | **Chat** | Быстро, conversational, no setup |
| Research, analysis, finished document built from files | **Claude Cowork** | Folder access, connectors, skills, scheduled runs |
| Writing, testing, shipping software | **Claude Code** | Codebase access, diffs, git, dev environments |

---

## Claude (Chat)

**Для quick exchanges без leaving приложение, в котором уже.**

Use для constant small tasks of running a company:
- Pulling one-sentence takeaway из dense investor memo
- Sanity-checking claim перед board meeting
- Making sense long Slack thread с командой

**Не для:** долгие projects, работа с files, шипить код.

---

## Claude Cowork

**Для knowledge work, который actually takes time, оперирует at scale, и producing something finished.**

Use для:
- Turning папку customer call transcripts в themed findings doc для next product review
- Building competitive landscape из десятка vendor sites перед fundraise
- Standing Monday-morning task — pulls weekly KPI brief из connected tools, drops в shared folder
- Customer outreach automation: prospect list + personalized outreach + scheduling через Gmail/Calendar MCP
- Operating layer ops: scheduling sprint ceremonies, routing bug reports, compiling weekly metrics, maintaining feedback loop

**Ключевая способность Scale stage:** running operational layer enterprise support — ticket routing, escalation workflows, documentation updates triggered product changes, renewal tracking, reporting cadences.

---

## Claude Code

**Agentic coding environment для engineers твоей команды.**
- Direct codebase access
- Plan Mode
- Git integration
- Local IDE или sandboxed cloud environments

Use для:
- Lean team shipping features через growing codebase
- Migrating legacy code с MVP days
- Moving с prototype to production без waiting for more headcount
- Architectural audit (Launch stage)
- Security review (MVP/Launch stages)
- Native integrations + APIs/webhooks/SDKs (Scale stage)

**CLAUDE.md** — persistent memory проекта, читается Agent SDK автоматически когда runs в директории.

---

## Композиция на стадиях

| Стадия | Главный фокус | Mix |
|--------|----------------|-----|
| Idea | Research, validation | Chat (быстро) + Cowork (research, customer discovery, outreach automation) + Code (только lightweight prototype в конце) |
| MVP | Build с дисциплиной | Chat (sanity checks, devil's advocate) + Cowork (feedback logistics, scheduling) + Code (билд по scope + CLAUDE.md) |
| Launch | Hardening + operations | **All three в full use** — каждый produces inputs для других двух |
| Scale | Org infrastructure + moat | **All three** + Skills (codified workflows) — fully integrated operational layer |

**Compounding logic:** outputs одного becomes inputs других. Фаундер, использующий все три vместе, получает **больше суммы частей**.

Это **structurally возможный ultra-lean startup model**:
- **Claude Code** builds the product
- **Claude Cowork** builds the company around it
- **Claude (Chat)** operationalizes product и organizational knowledge

Small team может run like company **N× its size**.
