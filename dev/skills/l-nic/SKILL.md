---
description: "NIC Method — структурированная фасилитация проекта (Brief -> Challenge -> Debrief -> Plan -> Spec). Используй когда пользователь говорит 'NIC', 'фасилитация проекта', 'давай по методу NIC', 'brief challenge debrief', 'structured facilitation'. НЕ используй для: трекинга стартап-команд (track), ретроспективы сессии (l-s-retro), диалогового мышления (thinking-partner)."
---

# NIC Method — Structured Project Facilitation

Brief → Challenge → Debrief → Plan → Spec

## When to Use

Complex projects that need structured thinking before coding. Invoke via `/l-nic` or when user says "давай по NIC", "пройдём по циклу", "brief для проекта".

## Modes

NIC works in **3 modes**. Ask user which mode at the start.

### Mode 1: Interview (Lance writes, NIC asks)

Claude is a strict facilitator. For each field:
1. **Name the field** and give the norm (what a good answer looks like, 1-2 sentences)
2. **Wait** for user to write
3. **Challenge** if the answer is vague, too broad, or missing the point
4. **Confirm** and move to the next field

Do NOT suggest content. Only ask questions and give norms.

Example:
```
## Concept — Норма высказывания

Опиши проблему которую решаешь в 1-2 предложениях.
Хороший ответ: "Предприниматели пробуют AI и бросают — внедряют не то"
Плохой ответ: "Хочу сделать полезный сервис"

Твой ответ:
```

### Mode 2: Guided (NIC suggests, Lance edits)

Claude предлагает содержание каждого поля на основе контекста разговора. User подтверждает, редактирует или отклоняет.

For each field:
1. **Name the field** and give the norm
2. **Propose** 1-2 варианта содержания
3. **Wait** for user: "да" / правка / "нет, вот так"
4. **Fix** and move on

### Mode 3: Auto-fill (NIC fills from context, asks only gaps)

Claude берёт весь доступный контекст (текущий разговор, CLAUDE.md, предыдущие сессии, vault) и:
1. **Auto-fills** every field where data is already clear
2. **Presents** the pre-filled document
3. **Marks gaps** with `[?]` — asks only about those
4. User reviews, corrects, fills gaps
5. Claude finalizes

Best for: projects where context is already rich (discussions happened, research done).

---

## Process

### Stage 1: BRIEF

Output file: `BRIEF.md` in project directory.

Fields to fill (in order):

| # | Field | Norm |
|---|-------|------|
| 1 | **Concept** | Проблема + корневая причина + позиционирование. 2-3 абзаца. Не "хочу сделать X", а "люди страдают от Y потому что Z" |
| 2 | **Persona** | Кто пользователь. Одно ключевое свойство (полномочия, боль, контекст) |
| 3 | **Pain** | Что именно болит. Конкретно, не абстрактно. "Тратит 10 часов" > "неэффективно" |
| 4 | **"After"** | Как выглядит мир после. Одно предложение |
| 5 | **Current alternatives** | 3-6 вариантов что делают сейчас. Для каждого — почему не работает |
| 6 | **Ecosystem** | В какую систему встраивается. Кому выгодно кроме пользователя |
| 7 | **Scope** | Что делаем |
| 8 | **Anti-scope** | Что точно НЕ делаем (3-5 пунктов) |
| 9 | **Related artifacts** | Существующие артефакты (скиллы, файлы, research) |
| 10 | **Validation** | Метрики успеха: ядро (2-3), воронка (таблица), репутация |
| 11 | **MVP** | Минимальный продукт — что входит в первую версию |

### Stage 2: CHALLENGE

Stress-test Brief. Check **5 connections**:

| # | Connection | Question |
|---|-----------|----------|
| 1 | Problem → Solution | Механизм действительно решает проблему? Какой evidence? |
| 2 | Who → Problem | У этих людей действительно есть эта боль? Данные? |
| 3 | MVP → Validation | MVP реально измерит метрики? Не wishful thinking? |
| 4 | Anti-scope → Solution | Что будет когда упрёмся в границы? Это провал или осознанное ограничение? |
| 5 | Current → New | Чем конкретно лучше существующих решений? Не "лучше", а "в чём"? |

For each connection:
- State the connection
- Evaluate: strong / weak / needs work
- If weak → ask user to strengthen or consciously accept limitation
- Log result in Challenge Log

Output: append to `BRIEF.md` or separate `CHALLENGE_LOG.md`.

Result: "Brief solid" → proceed to Debrief. Or "Needs rework" → back to specific fields.

### Stage 3: DEBRIEF

Full system model, NO implementation details. Output file: `DEBRIEF.md`

| # | Section | What |
|---|---------|------|
| 1 | **Entities** | All objects in the system (table) |
| 2 | **Relationships** | Graph of connections (has_many, contains, starts, etc.) |
| 3 | **Verbs** | Who does what — system actions (table: verb, who, what, context) |
| 4 | **Lifecycles** | State machines for each entity (arrows notation) |
| 5 | **Business rules** | Constraints and invariants (numbered list) |
| 6 | **User scenarios** | 2-3 main user journeys (narrative) |
| 7 | **Screens / touchpoints** | All UI points (table) |
| 8 | **Data model** | What's stored vs computed |
| 9 | **Integrations** | External systems (table: system, why, mode) |
| 10 | **Metrics** | How we measure success (table: metric, target, calculation) |
| 11 | **Risks & tradeoffs** | With probability, impact, mitigation (table) |
| 12 | **MVP priorities** | v1 / v2 / v3 breakdown |

### Stage 4: PLAN

Roadmap with phases. Output file: `PLAN.md`

| # | Section | What |
|---|---------|------|
| 1 | **Strategy** | Overall approach, critical dependencies, key decisions |
| 2 | **Phase 0..N** | Each phase: goal, tasks table (task, owner, duration, dependencies), output, readiness criteria |
| 3 | **Timeline** | Summary table of phases with durations |
| 4 | **Critical dependencies & risks** | With mitigation |
| 5 | **Transition to Spec** | Readiness conditions |

Task table format:
```markdown
| Task | Owner | Duration | Dependencies |
|------|-------|----------|-------------|
| 0.1 Description | Who | X hours | — |
```

### Stage 5: SPEC

Detailed implementation requirements. Output file: `SPEC.md`

- API contracts (endpoints, payloads, responses)
- Wireframes / screen descriptions (from prototype)
- JSON Schema / data models (from Debrief section 8)
- User stories with acceptance criteria
- Technical architecture decisions
- Stack choices with rationale

---

## Status Tracking

Maintain status line in each output file footer:

```
NIC Status: Brief ✅ | Challenge ✅ | Debrief ⏸️ | Plan ⏸️ | Spec ⏸️
```

Also create/update `STATUS.md` in project directory with:
- Current NIC stage
- What's done
- Key artifacts (links to files)
- Next steps
- Open questions

---

## File Structure

NIC creates this structure in project directory:

```
project-name/
├── BRIEF.md
├── DEBRIEF.md
├── PLAN.md
├── SPEC.md
├── STATUS.md
└── (other project files)
```

---

## Key Principles

1. **Sequential with gates** — each stage unlocks the next. Can't Plan without Debrief
2. **Files are source of truth** — not chat. Decisions live in documents
3. **Challenge is mandatory** — no skipping the stress-test
4. **Prevents AI drift** — documented decisions, explicit changes
5. **Facilitator role** — Claude structures, asks, challenges. Not just executes
6. **One field at a time** (Mode 1 & 2) — don't dump everything at once
7. **Norms for every field** — user always knows what "good" looks like

## Anti-patterns

- Don't skip Challenge ("let's just move to Debrief")
- Don't fill Brief with vague statements ("make a useful thing")
- Don't merge stages (Brief+Debrief in one pass)
- Don't start coding before Plan is done
- Don't treat SPEC as optional — it prevents scope creep during implementation

## Integration

- Works with `/dev-workflow` — after SPEC, switch to dev-workflow for implementation
- Works with `/spec-driven` — SPEC.md becomes the spec for spec-driven development
- Works with `/l-t-crit` — can run critical analysis as an extended Challenge
- Works with `/l-t-deep-research` — can trigger research during Challenge (connection 2)

## Learnings

### 2026-02-11
- First full run on AI Injection Point Finder project
- Challenge with deep research (connection 2) significantly strengthened Brief
- "First domino" reframe came from Challenge, not initial Brief
- Phase 0 (data/intelligence base) emerged as critical blocker during Plan

### 2026-02-15
- Three modes formalized: Interview, Guided, Auto-fill
- Auto-fill mode best for projects with rich existing context
