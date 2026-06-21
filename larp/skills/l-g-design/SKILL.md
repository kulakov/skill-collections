---
name: l-g-design
description: "Конструктор LARP-игры на базе каталога 159 метатехник из library.lance.ru (47 Nordic + 112 русских). Используй когда пользователь говорит 'создай игру из механик', 'собери игру из техник', 'подбери механики для игры', 'какие техники безопасности взять', 'хочу игру с блидом', 'подбери метатехники', 'что из нордика подойдёт', 'сравни Nordic и русские подходы', 'design LARP from mechanics', 'pick metatechniques', 'LARP mechanics toolkit', 'which safety mechanics', 'хочу сделать игру, какие механики', 'набор техник для камерки', 'у меня игра на 12 человек, помоги с механиками', 'как собрать игру из метатехник', 'воркшоп-план для игры'. Отличие от l-g-create: этот скилл подбирает конкретные техники из каталога, а l-g-create ведёт по 13 разделам без привязки к каталогу. НЕ используй для: просмотра каталога без создания игры (l-g-catalog), создания по методу Вая (l-g-vai), полного Nordic-процесса от идеи до дебрифа (l-g-nordic), алгоритмов Taning/Havskaya (l-g-algo), проверки целостности (l-g-check), продюсерского ревью сценария (l-g-neurolenoran), создания персонажей (l-g-char)."
aliases:
  - game-design
  - larp-design
  - mechanic-picker
---

# LARP Design from Metatechniques

Конструктор LARP на базе каталога из 159 метатехник: 47 Nordic + 112 русских экспериментальных.

## Источники

- **Каталог техник (API):** `https://library.lance.ru/api/public/mechanics`
- **Веб-каталог:** `https://library.lance.ru/public/mechanics`
- **Скиллы-предшественники:**
  - `/l-g-create` — общий процесс создания LARP
  - `/l-g-nordic` — Nordic-подход (Stenros, Koljonen)
  - `/l-g-algo` — русские алгоритмы (Taning, Havskaya, False Paths)
  - `/l-g-cats` — быстрый CATS-фреймворк

## Принцип

Этот скилл не заменяет методологические скиллы выше, а дополняет их. Его суперсила — **знание конкретных техник** и умение собирать из них рабочий набор под замысел.

## Процесс

### Фаза 1 — Замысел (3 вопроса)

**Первый вопрос — ТРАДИЦИЯ.** Спрашивай сразу, до остального. От выбора зависит весь набор техник.

1. **Традиция** (спрашивать первым!):
   - **Nordic LARP** — safety culture, workshops, bleed, metatechniques, 360° immersion. 47 техник в каталоге.
   - **Русские игры** — gamefocus, модели, алгоритмы, реквизит, scoring. 112 техник в каталоге.
   - **Гибрид** — обе традиции, подбираем лучшее из каждой.

   Если пользователь не уверен — кратко объяснить разницу и помочь выбрать.

2. **Идея:** Что за игра? Тема, источник вдохновения, целевой опыт
3. **Формат:** Камерка / полигон? Сколько людей? Сколько времени?

### Фаза 2 — Каркас (5 слоёв)

Для каждого слоя подобрать 2-4 техники из каталога с обоснованием:

**Слой 1: Safety & Calibration**
Обязательный. Какие техники безопасности подходят формату.
- Nordic: Stop/Go, Lookdown, Check-in, Scene Cut, Off-game Symbol, Freeze
- Russian: Stop Word, Debrief, Content Warnings, Safe Space, Warm Frame, Sensitive Role Marking, Simulated Physicality

**Слой 2: Narrative & Dramatic**
Как рассказываем историю. Техники движения сюжета.
- Nordic (15): Monologue, Voiceover, Flashback, Blind Play, Montage, Retcon, Time Jump, Silent Scenes, Symbolic Objects, Cinematic Sequences, Emotion Condensation, Relationship Map, Dream/Hallucination Scenes, Symbolic Death, Narrative Voting
- Russian (18): Flashback Scene, Inner Monologue, Moral Dilemma, Interconnected Backstories, Secret as Driver, External Escalation, Progressive Loss, Ideological Conflict, NPC Letters/Messages, Unreliable Narrator, Public Confession, Moral Court, Parallel Stories, Secret Alliance, Choice Under Pressure, Generational Shift, Final Speech, Symbolic Transformation

**Слой 3: Communication**
Как игроки взаимодействуют и обмениваются информацией.
- Nordic (15): Meta-reflection, Role Exit Symbols, Ping the Glass, Intent Declaration, Internal State Sharing, Open Future Discussion, Emotion Description, Alternative Actions Discussion, Emotional Calibration, Inner Circle Sharing, Transparency Mechanic, Negotiation Escalation, Role Delegation, Meta-commentary, Status Play
- Russian (8): Restricted Communication, Formal Address, Formal Documents, Push Sign, Wall-Posted Information, Ritual Phrase, Participant Directory, Pass System

**Слой 4: Space & Environment**
Как используем пространство, реквизит, физический мир.
- Nordic (4): Meta-Room, Special Meta-rooms, Fear Meta-rooms, Meta-time
- Russian (17): Tape Zoning, Location Labels, Light and Sound Design, Character Props, Costume Elements, Character Diary, Bureaucratic Forms, Parallel Spaces, Locked Spaces, Secret Rooms, Mobile Locations, Status Markers, Visual Information Board, Projection/Screens, Food as Mechanic, Music Playlist, Spatial Restrictions

**Слой 5: Game Flow & Scoring**
Как течёт игра, структура, механики подсчёта.
- Nordic (6): Conflict Analysis, Oblivion, Game Filters, Inner Monologue Play, Scene Voting, Stone-Pouch Combat
- Russian (62): Act Structure, Countdown Timer, Sound Signal, Daily Routine, Respawn, Council/Parliament, Voting Mechanics, Quest Chain, Economy, Crafting, Investigation, Character Progression, Ritual Mechanics, Auction, Random Events, Limited Resource, Visible Status, Consequence Accumulation, Territorial Mechanics, Exam Mechanic, ...и ещё 40+

### Фаза 3 — Сборка

Собрать выбранные техники в таблицу:

```markdown
| Техника | Слой | Традиция | Когда | Как именно в нашей игре |
|---------|------|----------|-------|------------------------|
| Stop Word | Safety | RU | Always | "Стоп" замораживает сцену |
| Flashback | Narrative | Nordic | Mid-game | Ведущий объявляет "Flashback — год назад" |
| ... | ... | ... | ... | ... |
```

### Фаза 4 — Воркшоп-план

Какие техники надо отработать на воркшопе перед игрой.
Приоритет: Safety > Narrative > Communication > Space > Flow.

### Фаза 5 — Проверка

Прогнать через чеклист l-g-check:
- Все техники служат целевому опыту?
- Safety покрывает все опасные зоны?
- Нет ли конфликтующих техник?
- Воркшоп учит всем техникам?

## Дополнительные режимы

### "Подбери техники"
Если пользователь уже знает замысел и хочет только подбор техник — перейти сразу к Фазе 2.

### "Покажи технику"
Описать конкретную технику подробно: что, когда, примеры из игр.
Данные: `https://library.lance.ru/api/public/mechanics`

### "Сравни традиции"
Показать как одну и ту же задачу решают Nordic и русская школа.
Пример: "как передать внутренний конфликт" → Nordic: Monologue + Emotional Calibration vs Russian: Inner Monologue + Moral Dilemma + Public Confession.

## Использование

```
/l-g-design
/l-g-design камерка на 15 человек про советский космос
/l-g-design подбери техники для детектива
/l-g-design сравни подходы для темы "потеря памяти"
```

$ARGUMENTS
