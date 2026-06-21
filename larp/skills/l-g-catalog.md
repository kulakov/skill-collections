---
description: "Каталог 365 механик: 185 метатехник LARP + 180 механик настольных игр (BGG). Используй когда пользователь говорит:
  - 'какие механики', 'mechanics catalog', 'справочник техник', 'покажи механики'
  - 'какая техника подходит для...', 'what technique for...', 'подбери механику'
  - 'расскажи про lookdown', 'что такое worker placement', 'meta-techniques'
  - 'техники безопасности в ларпе', 'safety mechanics', 'calibration'
  - 'механики настольных игр', 'board game mechanics', 'BGG mechanics'
  - 'придумай игру', 'game design', 'сконструируй игру', 'какие механики сочетаются'
  - 'фасеты', 'facets', фильтрация по category/timing/mode/interaction/tradition
  - Ссылка на library.lance.ru/public/mechanics
  НЕ используй для: проверки игры (l-g-check), документации (l-g-doc), LARP по методу Вая (l-g-vai)"
aliases:
  - l-g-meta
  - l-g-techniques
  - l-g-bgg
version: "2.0"
updated: "2026-03-31"
---

# Game Mechanics Catalog (365 mechanics)

## Data

The catalog contains **365 mechanics** from 3 traditions:
- **Nordic LARP** (47) -- metatechniques from the Nordic LARP tradition
- **Russian LARP** (138) -- techniques from Russian LARP games
- **Board Games / BGG** (180) -- board game mechanics from BoardGameGeek

### Loading data

1. If local file `10-CLAUDE/highlights-library/data/mechanics.json` exists -- read it (Read tool)
2. Otherwise -- fetch via WebFetch: `https://library.lance.ru/api/public/mechanics`

The data includes: name (ru + en), description, examples with game names, sources with URLs, facets.

## Facet system

| Facet | LARP Values | BGG Values |
|-------|------------|------------|
| **Tradition** | `nordic`, `russian` | `board-game` |
| **Category** | safety, narrative, communication, space, flow | bg-action-selection, bg-auction-economy, bg-card-management, bg-conflict-area-control, bg-movement-spatial, bg-pattern-puzzle, bg-social-communication, bg-game-structure |
| **Timing** | pre-game, in-game, inter-scene, post-game | in-game (default for BGG) |
| **Mode** | verbal, gestural, spatial, temporal | verbal (default for BGG) |
| **Interaction** | solo, player-player, facilitated | solo, player-player, facilitated |

## Response modes

Respond in the language the user writes in. Determine the mode from context:

### Mode 1: Lookup -- user asks about a specific mechanic

- Name (RU + EN)
- Tradition badge (Nordic / RU / BGG)
- Description (in user's language)
- Category + facets
- Examples of use in games (with names, links if available)
- Sources
- Link to card: `https://library.lance.ru/public/mechanics#MECHANIC_ID`

### Mode 2: Search -- user needs a mechanic for a task

- Suggest 3-7 mechanics from ANY tradition (mix LARP + BGG if relevant)
- For each: name, tradition, why it fits, link to card
- If the task is covered by several mechanics -- show a combination
- Prioritize mechanics that have examples (games that used them)

### Mode 3: Overview -- user wants to browse

- Group by tradition or category
- Brief table with key fields
- Mention total counts per group

### Mode 4: Game Design -- user wants to create a game

This is the key creative mode. When the user says "придумай игру", "game design", "сконструируй игру":

**Step 1: Understand the brief**
Ask (if not provided): genre, player count, session length, theme, tone (serious/playful).

**Step 2: Suggest a mechanics palette**
Select 4-8 mechanics that work together. Draw from ALL traditions:
- **Core loop** -- what players do on their turn / most of the time (1-2 mechanics)
- **Tension** -- what creates conflict or drama (1-2 mechanics)
- **Progression** -- how the game evolves over time (1-2 mechanics)
- **Social glue** -- how players interact with each other (1-2 mechanics)
- **Safety** (for LARP) -- if applicable (1 mechanic)

For each mechanic show:
- Name + tradition + link
- Role in the design (core/tension/progression/social/safety)
- Example game that uses it similarly

**Step 3: Synergies and conflicts**
- Flag which mechanics reinforce each other
- Warn about combinations that may clash (e.g., Real-Time + heavy Hand Management)
- Suggest variants if a mechanic is too complex for the target audience

**Step 4: Prototype sketch**
If the user wants, outline a 1-paragraph game concept using the selected palette.

### Mechanic combination patterns (reference)

Known good combinations for board games:
- **Engine builder**: Deck Building + Resource Management + End Game Bonuses
- **Area control**: Area Majority + Worker Placement + Variable Player Powers
- **Social deduction**: Hidden Roles + Voting + Player Elimination
- **Euro**: Worker Placement + Set Collection + End Game Bonuses + Income
- **Ameritrash**: Dice Rolling + Variable Player Powers + Modular Board + Stat Check

Known good combinations for LARP:
- **Safety stack**: OK Check-in + Lookdown + Lines and Veils + Debrief Circle
- **Narrative drive**: Monologue + Flashback + Blackbox + Epilogue
- **Immersion**: Ars Amandi + Slow Play + Soundtrack + Meta-room

Cross-tradition combinations (LARP + Board Game):
- **LARP with board game elements**: Hidden Roles (BGG) + Negotiation (BGG) + Monologue (LARP) + OK Check-in (LARP)
- **Board game with LARP elements**: Role Playing (BGG) + Storytelling (BGG) + Calibration (LARP) + Debrief (LARP)

### Mode 5: Deep Dive -- user wants details about a specific BGG mechanic

When the user asks to dig deeper into a mechanic ("подробнее про worker placement", "покажи примеры для deck building", "какие лучшие игры с этой механикой"):

1. Find the mechanic in the data, get its `sources[0].url` (BGG page URL)
2. Fetch the BGG page using WebFetch with the URL and prompt: "Extract: 1) full description of this mechanic, 2) list of top-rated games that use it (name + year + rating if shown), 3) any related mechanics mentioned"
3. Present the enriched info:
   - Full description (from BGG, more detailed than our cached version)
   - **Top games** table: Name | Year | BGG Rating
   - Related mechanics (with links to our catalog cards)
   - Link to the BGG page for further exploration

If WebFetch fails (BGG blocks it), fall back to the cached description from mechanics.json and note that live data is unavailable.

For LARP mechanics, the deep dive reads the source URLs from the `sources` array (nordiclarp.org wiki pages, etc.).

## Important rules

- Do not invent mechanics -- use only the 365 from the data
- If there is no mechanic for the task -- say so directly
- When recommending a mechanic ALWAYS provide a link to the card
- When mixing traditions, clearly label each mechanic's origin
- Mechanic IDs: LARP ids are plain (e.g., `monologue`), BGG ids are prefixed (e.g., `bgg-worker-placement`)

## Web interface

Full catalog with faceted filtering: https://library.lance.ru/public/mechanics
- Filter by tradition to see only LARP or only BGG mechanics
- Link to a specific card: `https://library.lance.ru/public/mechanics#MECHANIC_ID`
