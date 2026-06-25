# MVP Stage

## Цель стадии

**Перевести валидированную проблему в работающий продукт**, который реальные пользователи будут использовать. Не full version с каждой фичей roadmap'а — самая focused итерация идеи, которая ставит solution перед real users и генерит real evidence of product-market fit.

Параллельно — **moving fast without accruing the kind of technical debt that will compound** когда придут реальные пользователи в meaningful numbers.

И с **investing in persistent context from day one** — что превращает AI из source of entropy в force multiplier.

## Exit criteria

Стадия закрыта когда есть **genuine evidence of product-market fit**:
- Конкретная identifiable группа пользователей
- Found product valuable enough to:
  - Return to it (retention), OR
  - Pay for it (revenue), OR
  - Tell others about it (referral)

---

## Ловушки этой стадии

### Agentic technical debt

AI essentially снимает каждое естественное bottleneck, которое раньше controlled what reaches production. Скорость гарантирована. Но если speed — единственная переменная, которую фаундер factors в MVP build, он рискует accruing технический долг, который потом не выплатит.

Без specs и architectural constraints written down somewhere AI can read, **каждая сессия re-derives foundational decisions from scratch, и те decisions drift**. Получаешь кодбейс, который не имеет coherent mental model behind it — не потому что какой-то single piece плох, а потому что pieces were never designed to fit together.

Фаундеры, которые **skip specs, architectural decisions, и context files (like CLAUDE.md)** упираются в predictable wall: каждая новая сессия требует re-explaining кодбейс, а AI-generated changes дрейфуют от исходного vision.

### Falling for false product-market fit

AI tools могут сгенерировать impressive early numbers — но это **не гарантия, что рынок нужен в твоём продукте**.

Early momentum — психологически мощное переживание. После недель/месяцев валидации и careful disciplined building, shipping a product feels like confirmation, что ты был прав all along.

Agentic coding делает этот момент быстрее чем когда-либо, но **early traction ≠ product-market fit**. Launch energy генерируется из ephemeral forces:
- Друзья фаундера
- Prospective buyers из portfolio companies инвестора
- Hacker News headline driving spike

Ни один из этих сигналов **надёжно не предсказывает что произойдёт на 6-й или 12-й неделе**.

### Zero-friction scope creep

Когда билд feels effortless и почти бесплатный, всегда есть «ещё одна cool feature» или «ещё один edge case». Scope creep может do more harm than good.

Раньше scope creep тормозила real cost of engineering time. Теперь, когда добавление фичи — afternoon вместо sprint, **traditional forcing function gone**.

Каждое individual addition defensible:
- Конечно продукт должен handle тот edge case
- Конечно пользователи захотят тот workflow

Но продукт sprawls beyond его original boundaries → теряешь direction и momentum.

**Antidote:** written scope definition created before building begins, описывающий:
- Что продукт делает
- Что он **deliberately not делает**
- Specific evidence from real users, который оправдал бы добавление чего-то нового

Moves decision point с «should we build this?» → «a critical mass of users told us they can't get value without this?»

### Insecure by inexperience

Фаундеры, использующие AI tools чтобы rush applications to market без понимания fundamental security principles, exposing users to preventable risks.

**Hard truth:** agentic coding tools генерят код, который работает, не код, который inherently secure.
- Functional code легко — feature либо работает, либо нет
- Security vulnerabilities **invisible** пока не exploited

Нет natural feedback loop, который alert first-time founder, что что-то wrong. Shipping a live MVP to real users means **real data, real exposure, real consequences**.

Bootstrapped стартапы in every era often delayed security considerations until late в билде. **Security review before any user touches your app — minimum responsible threshold для releasing MVP в мир.**

---

## Упражнения

### Упражнение 1 — Architecture before code

**Перед** Claude Code пишет первую строчку production-кода:

- Open Claude и describe what you're building: core problem, users, scale realistically expected в следующие 6 месяцев
- Define:
  - Architectural principles, которые должны govern MVP build
  - Dependencies to avoid given constraints
  - Tradeoffs, которые consciously accepting на этой стадии
- **Save this output как CLAUDE.md** в корне проекта

Это **первый артефакт билда** и тот, на который depends каждая subsequent сессия Claude Code. CLAUDE.md = persistent "memory" проекта, читается Agent SDK автоматически.

### Упражнение 2 — Scope definition

Прежде чем первая фича построена:

- Claude помогает создать scope-документ описывающий:
  - Что MVP product делает
  - Что он deliberately не делает
  - Feature amendment criteria: какие specific evidence from real users оправдали бы добавление чего-то на этой точке

Когда новые feature-идеи всплывают (а они всплывут) — Claude pressure-test: это genuine signal from users или founder enthusiasm dressed up как product thinking?

### Упражнение 3 — Session template

Каждая сессия Claude Code:
1. **Revisit scope-документ** — что строим, что нет
2. **Provide model с CLAUDE.md** — архитектурный контекст
3. **В конце сессии** — лог-запись в CLAUDE.md: что построено, какие decisions surfaced, какие assumptions session introduced

**5 минут документирования на сессию = cheap insurance против architectural drift, который compounds в unmanageable codebase.**

### Упражнение 4 — Security review до первого user

**Не substitute for security tooling, но baseline check:**

- Перед deploy to any real users — Claude review core application code
- Specific brief: review authentication и session handling, data exposure в API responses, input validation и injection risks, dependencies with known vulnerabilities
- Каждый finding: treat seriously, human review для всего что touches authentication / secrets / data handling

**Claude Code Security** (limited beta на момент publication) идёт дальше: сканирует кодбейсы и suggests targeted patches.

### Упражнение 5 — Measurement framework ДО запуска

**Фаундеры, которые mis-identify early traction как PMF — обычно те же, кто начинает tracking данные после launch**, выбирая метрики чтобы assess what was working, а не surface what wasn't.

**Установи measurement framework перед первым пользователем:**

- Какие метрики matter для вашего specific продукта
- Benchmarks
- Какие data patterns indicate **genuine PMF vs flattering noise**
- Retention benchmarks, activation criteria, Day 7 / Day 30 targets

**Define what a false positive looks like:**
- Signups без активации
- Revenue без retention
- Initial enthusiasm без repeat usage

Когда данные приходят — Claude builds adversarial case против собственной traction: «что бы skeptic сказал про эти числа?»

### Упражнение 6 — Sean Ellis test

**Sean Ellis test:** Спроси active users:
> «How would you feel if you could no longer use this product?»

Если **больше 40% ответят "very disappointed"** — meaningful PMF indicator.

### Упражнение 7 — The effort test

**Pre-PMF retention требует constant intervention:** frequent outreach, incentives, personal follow-up, heroic founder energy expended just keeping users engaged.

**Post-PMF продукт starts doing that on its own.** Когда вещи begin **pulling** instead of **pushing** — shift в effort — один из clearest signals, что что-то реальное changed.

**Note:** Single data point не confirms PMF. Это pattern, который должен hold через multiple iteration cycles прежде чем можно definitively call it.

### Упражнение 8 — Discovery & feedback logistics

Раз real users в продукте, operational layer expands fast:

- Claude Cowork handles важные но tedious work:
  - Building и maintaining user contact lists
  - Running outreach sequences
  - Scheduling feedback sessions
  - Triaging bug reports
  - Tracking iteration cycles

- **Keep human в collection loop для nuanced exploration** user feedback:
  - User говорит «this is great but I wish it could also...» → требует интерпретации
  - Core need или nice-to-have?
  - Specific to этому customer или representative segment'у?
  - Missing feature reveals real problem или это onboarding upstream?

### Упражнение 9 — Pivot when evidence demands

После 3+ iteration cycles без meaningful движения к PMF:

- Run diagnostic с Claude
- Feed retention data, user feedback, original problem hypothesis
- Three questions:
  1. **Есть ли сегмент в данных, реагирующий по-другому?** Возможно правильная аудитория уже в данных, просто underweighted
  2. **Gap между designed value и experienced value — positioning или product problem?** Adjustment в onboarding/messaging/feature emphasis может fix без changing what built
  3. **Что должно быть true, чтобы current product найти genuine PMF, и realistic ли этот сценарий?**

Stay open к possibility, что disconnect runs deep enough чтобы require more fundamental change.

**Answers determine: adjust, pivot, или return to Idea stage.**

---

## Сквозной принцип MVP stage

Стадия заканчивается когда у тебя **genuine evidence of PMF**, no matter how «finished» продукт feels.

Decllaring PMF — это **judgment exercise combining founder intuition with collected evidence**. Useful litmus tests есть (Sean Ellis, effort test), но окончательно — pattern that holds across multiple cycles.

Когда подтверждено — переход в Launch stage. Фокус shifts с «can we prove the product deserves to exist?» на «can we prove the business deserves to grow?»
