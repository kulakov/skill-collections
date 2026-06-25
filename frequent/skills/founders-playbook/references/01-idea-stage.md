# Idea Stage

## Цель стадии

**Research-oriented validation:** собрать качественные доказательства, что реальная проблема существует и предложенное решение её эффективно адресует — ДО того как Claude Code напишет первую строчку production-кода.

Работа на этой стадии — research, customer discovery, конкурентный анализ, честная оценка disconfirming evidence. Не билд.

## Exit criteria

Готов к переходу на MVP когда можешь сказать «да» всем трём:

1. **Проблема реальная и конкретная.** Можешь назвать кто страдает, как часто, насколько остро, что делает сейчас.
2. **Решение адресует ту проблему, что выявил процесс валидации.** Не ту, что предположили на старте. Иногда совпадают, часто нет.
3. **Сигнала достаточно, чтобы оправдать билд.** Нет certainty (это own failure mode — ждать), но есть qualitative evidence, что MVP — обоснованное решение, а не акт веры.

---

## Ловушки этой стадии

### Перепутать билд с валидацией
Когда технические блокеры сняты, фаундер рискует пропустить самую важную работу: валидацию, что идея реально нужна людям.

**42% стартапов умирают потому что построили то, что никому не нужно.** Agentic coding сократил дистанцию между «у меня идея» и «у меня продукт» — эта статистика только ухудшится.

Прототип легко перепутать с конкретным доказательством. Это не доказательство — это **useful pressure-testing prop для разговоров с пользователями**. Сами разговоры — реальное доказательство.

### Преждевременный масштаб
Когда билд бесплатный, легко scale execution far ahead of business demand. Agentic coding бесконечно энтузиастичен — будет генерить, тестить, дебажить, рефакторить кодбейс вокруг fundamentally flawed premise с тем же энтузиазмом, что и вокруг great idea.

Prime directive этой стадии: **держи sense-making ahead of building**, особенно когда билд так быстр и feels effortless.

### Потеря объективности
Confirmation bias теперь приходит с research-движком. Попроси AI валидировать идею — он найдёт supporting evidence. Попроси оценить TAM — найдёт число, которое делает TAM fundable.

AI следует твоему направлению. Фаундер, не задающий hard questions, теперь может сконструировать elaborate well-researched-looking case за bad idea быстрее чем когда-либо, чувствуя что делает due diligence.

**Антидот — тот же инструмент, развёрнутый в обратную сторону.** AI pressure-test идеи так же тщательно, как и валидирует.

---

## Упражнения

### Упражнение 1 — Заточи гипотезу до testable

**Зачем:** problem statement, который не может ответить «кто, как часто, насколько остро» — не готов к валидации.

**Как:**
- Команда формулирует problem statement руками
- Просят Claude найти где формулировка слишком расплывчата
- Перепиши до уровня: «In-house legal teams at mid-market companies spend 3+ days per contract review cycle because redlines are managed across email threads rather than a single version-controlled document»
- Тест: есть конкретный сегмент, частота, причина, текущее поведение

**Anti-pattern:** «Contract review takes too long» — это observation, не testable hypothesis.

### Упражнение 2 — Devil's advocate против собственной идеи

**Зачем:** убить confirmation bias до того, как он убьёт стартап.

**Как:**
- Дай Claude свою гипотезу
- Промпт: «Найди disconfirming evidence: negative market signals, провалившиеся конкуренты, паттерны поведения пользователей и structural obstacles, которые поддерживающий синтез quietly deprioritized»
- Зафиксируй 5 сильнейших аргументов против
- Для каждого: что должно быть истиной, чтобы аргумент НЕ был валиден?

**Note:** Это core use case на каждой стадии playbook'а. Возвращайся к этому упражнению регулярно.

### Упражнение 3 — Карта конкурентов по тирам

**Зачем:** competitor neglect — startup-specific phenomenon недооценки того, что делают другие в той же области.

**Как:**
- Direct Claude построить карту конкурентов:
  - Прямые
  - Косвенные
  - Потенциальные acquirers
  - Соседние игроки, которые могут зайти в твою область
- Для каждого тира: попроси Claude **доказать почему каждый — genuine threat**, не easy-to-dismiss версия угрозы
- Зафиксируй: почему их подход actually лучше, почему пользователи могут выбрать их, почему твои differentiators могут быть слабее, чем кажется

### Упражнение 4 — TAM/SAM/SOM с pressure-test допущений

**Как:**
- Claude Cowork извлекает данные из industry-отчётов, analyst filings, market research docs
- Строит TAM/SAM/SOM модели
- Pressure-test допущений: рынок expanding/consolidating/mature? Это влияет на timing и differentiation
- Карта buyer landscape: у кого бюджет, кто influences решения, это же люди?

### Упражнение 5 — Trend analysis

**Зачем:** заходишь ли в right moment?

**Как:**
- Track subreddits и LinkedIn groups где уже происходят разговоры о проблеме
- Точная лексика, которой пользуются люди описывая issues
- Analogous markets где similar problem был решён — что сработало, что нет
- Спроси Claude: 3 external trends (regulatory / technological / demographic), которые могут significantly affect рынок в следующие 2 года — попутный ветер или встречный?

### Упражнение 6 — Customer discovery: кому звонить, что спрашивать

**Кому звонить:**
- Precise target profile (specific job titles, company types, team structures, seniority levels) — infinitely valuable чем длинный contact list
- Где эти люди actually reachable — communities, events, LinkedIn groups, Slack workspaces
- Prioritization framework: кому первым по близости к проблеме

**Что спрашивать:**
- Claude строит interview framework
- Anti-rookie-mistake: НЕ задавай generic future-facing вопросы («would you use something like this?») — генерит noise, не signal
- Задавай specifically про recent past: «tell me about the last time you dealt with this problem»
- Claude flags leading questions, too broad, future-facing, socially desirable answer-prone
- Claude дизайнит follow-up probes для deflections и vague answers

### Упражнение 7 — Post-interview analysis (после каждых 5)

**Зачем:** ловить confirmation bias на лету.

**Как:**
- Feed Claude Cowork notes из 5 интервью
- Two lists:
  1. Evidence supporting гипотезу
  2. Evidence challenging гипотезу
- Если первый significantly длиннее второго — спроси Claude: эта асимметрия отражает данные или то, что ты надеялся найти?

### Упражнение 8 — Customer outreach automation

**Как:**
- Claude Cowork получает validated target profile
- Researches и compiles structured prospect list (с verified contacts)
- Drafts personalized outreach emails at scale (под job/role/context)
- Подключается к Gmail + Calendar через MCP — manages threads, scheduling, follow-ups
- Drafts day-7 follow-up cadence для non-respondents
- Updates tracking sheet по каждому этапу

### Упражнение 9 — Final solution concept

**Зачем:** проверить, что предложенное решение работает именно под ту проблему, которую выявила валидация.

**Как:**
- Present solution concept Claude
- Claude identifies 3 главных допущения, на которых концепт держится
- Для каждого: что должно быть истиной, какие consequences если нет?
- Reality checkpoint: твой design адресует проблему, что revealed валидация — или проблему, что ты assumed going in?

### Упражнение 10 — Lightweight prototype с Claude Code

**Только после прохождения предыдущих упражнений.**

- Не строй real-world product (yet). Строй functional sample для customer/investor conversations
- Define single core interaction, на которой держится решение
- Claude Code строит только это
- Покажи 5 людям из validated target profile, попроси try out
- Что выяснил в этих 5 разговорах determines: продолжаешь билд или идёшь обратно к drawing board

---

## Сквозной принцип Idea stage

Все упражнения служат одной финальной проверке: **Is this worth building?**

Когда ответ — обоснованный «да» (не act of faith, а reasoned decision) — переходим в MVP. AI role shifts с research partner на construction crew.

Если в процессе появилось disconfirming evidence — это **сигнал к pivot**, не к bypassing.
