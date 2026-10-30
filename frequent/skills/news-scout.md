---
name: news-scout
description: "Daily delta-research digest. Triggers: 'news scout', 'дайджест новостей', 'scout run', 'запусти скаут', 'news digest'. Scheduled daily at 18:00 via /schedule."
---

# News Scout — Delta-Research Daily Digest

You are a delta-research agent. Your job: find NEW signals across the topics from sources.json, deduplicate, and deliver a concise digest to Telegram.

## Config

**Sources are defined in `10-CLAUDE/news-scout/data/sources.json`** — read this file first.

Structure:
- `topics` — each with name/OKR/keywords/cadence. `cadence: "daily"` — every run; `cadence: "weekly"` + `day` — include ONLY when today's weekday matches (Europe/Warsaw). Skip weekly topics on other days entirely (no sources fetched, no searches).
- `muted` — kicked sources. NEVER fetch a source listed here. Entries: {kind, id, name, muted_at}.
- `telegram` — TG channels, each tagged with a topic
- `rss` — RSS/Atom feeds, each tagged with a topic
- `youtube` — YouTube channels (fetched via t.me or youtube.com/@handle/videos), each with topic
- `web` — static web pages to monitor for changes (blogs, changelogs, listings)

FACTS_DIR: `10-CLAUDE/news-scout/data` — one facts-{topic}.md per topic.

## Pipeline (execute sequentially)

### Step 1: Load config + exclusion lists
1. Read `10-CLAUDE/news-scout/data/sources.json` — get topics, TG channels, RSS feeds, YouTube, web sources
2. Determine ACTIVE topics for today: all daily topics + weekly topics whose `day` matches today's weekday. Work only with active topics and their sources.
3. Filter out muted sources: any source whose channel/url appears in the `muted` array is skipped without fetching.
4. For each active topic, read the FIRST ~80 lines of `facts-{topic}.md` (create file if missing) — new facts are PREPENDED to the top (see Step 8), so the top of the file is the most recent history. Do NOT use `tail`/"last N lines" for this — that reads the OLDEST entries and will cause stale exclusion lists and duplicate signals.
5. If topic `platforms` is ACTIVE today: read `10-CLAUDE/news-scout/data/platform-flags-delta.md`. It is a pre-computed, deterministic diff of feature flags on selfpub platforms, produced by a probe that runs daily. Treat every ПОЯВИЛСЯ / УБРАН / ПЕРЕКЛЮЧЁН line as a first-class signal for the `platforms` topic — it is a decision already shipped into a product, which outranks any blog announcement. Ignore the file if it says «Изменений нет». Never treat an unreachable source noted in that file as a change.

Build internal exclusion list per topic — signals already known. Do NOT repeat them unless there is genuinely new data.

### Step 2: Parse Telegram channels
### Step 2a: Parse Telegram channels (from sources.json → telegram)
For each channel, fetch `https://t.me/s/{channel_name}` via WebFetch.
Use this prompt for WebFetch: "Extract posts from last 24 hours. For each post return VERBATIM: 1) post number/ID from URL, 2) exact first 2 sentences of post text word-for-word (do NOT paraphrase), 3) any links, 4) date/time"

For each post capture:
- Channel name
- Post ID (from URL: t.me/channel/POST_ID)
- VERBATIM first 2 sentences — this is the ONLY text you may put in quotation marks
- Links mentioned in the post
- Date

IMPORTANT: Always capture the post ID so you can construct the direct link https://t.me/{channel}/{post_id} for the digest.
IMPORTANT: If WebFetch returned a summary/paraphrase instead of verbatim text — mark it as "paraphrased" and do NOT use quotes in the digest.

Skip channels that return errors (closed/private).

### Step 2b: Parse RSS feeds (from sources.json → rss)
For each feed: WebFetch with prompt "Extract items from last 24 hours. Return: title (verbatim), link (direct URL), published date, first 200 chars of description (verbatim). Skip items older than 24h."

Tag each item with the feed's topic from sources.json.

### Step 2c: Parse YouTube channels (from sources.json → youtube)
For each channel: WebFetch `https://www.youtube.com/@{channel}/videos` with prompt "Extract videos from last 7 days. Return: title, link, publish date, duration, view count (if visible). Skip older videos."

Weekly cadence is fine for YouTube (daily is too frequent for video content).

### Step 2d: Parse web sources (from sources.json → web)
For each URL: WebFetch with prompt "Extract new items/posts/entries since last 24 hours. Return: title, link, date, first 200 chars. If no new content, return 'no updates'."

For changelog/blog pages, track what's new compared to previous runs.

### Step 3: Classify channel posts by topic
For each post, determine which topic(s) it relates to. Use each topic's `keywords` from sources.json as the classification guide. Orientation for the trickier ones:
- **jerian**: любые упоминания игры The Life and Suffering of Prince Jerian / «Принц Джериан» + релизы/запуски игр-конкурентов (choices matter, interactive fiction, CRPG класса Бранте)
- **steamdev**: Steam/Valve как платформа и геймдев-индустрия — правила Steam, фесты, дискавери, маркетинг игр, wishlists, продажи, инди-рынок
- **selfpub**: рынок и платформы, НЕ промо отдельных книг (промо-посты конкурентов — сигнал только если видна платформенная механика или цифры)
- **xrvr**: бизнес-сторона XR; игровые обзоры и моды — discard
- **tracking**: новый приём/кейс с разбором; анонсы курсов — discard
- **stages**: сигнал обязан содержать дедлайн подачи или дату события
- **mentions**: только упоминания, требующие действия или заметные охватом
- **vitality**: только исследования с эффектами; лайфстайл-советы — discard
- **general**: Interesting but doesn't fit any topic — skip unless truly remarkable

Classify only into ACTIVE topics today (Step 1). IMPORTANT: новости про AI-модели, AI-кодинг, вайб-кодинг, LLM-вендоров (OpenAI, Anthropic, Cursor и т.п.) — НЕ тема дайджеста, discard. Исключение: AI-политики Steam/Valve и AI-скандалы в геймдеве → steamdev.

Posts that don't match any active topic → discard.

### Step 4: Deduplication — one story = one entry, GLOBALLY
Two levels, both mandatory:

**4a. Cross-channel:** the same news/event in multiple channels → keep ONE entry, note "(@channel1 + N ещё)". The link goes to the best source (original > repost).

**4b. Cross-topic:** the same story matching several topics (e.g. Valve AI-policy → steamdev + jerian; VR-контракт агентства → xrvr + jetstyle) → include it ONCE, in the single most relevant section. If the secondary angle matters, add one trailing line "также: {тема} — {полфразы почему}". NEVER describe the same event in two sections.

### Step 5: Web Research
For each ACTIVE topic, do 1-2 targeted WebSearch queries for the last 24 hours (weekly topics: last 7 days). Four topics are SEARCH-DRIVEN — for them this step is the primary source, do 2-3 queries:

**jerian**: "Prince Jerian" OR "Принц Джериан" OR "The Life and Suffering of Prince Jerian" — ищи упоминания где угодно (Reddit, DTF, StopGame, YouTube, кураторы Steam, форумы); вторая выборка — по-русски «Джериан» отзыв OR обзор OR стрим
**steamdev**: Steam sales OR wishlists OR "Next Fest" OR Valve policy OR indie game marketing site:gamediscover.co OR site:howtomarketagame.com OR site:gamedeveloper.com OR site:steamdb.info
**selfpub**: самиздат OR издательская платформа OR "Author.Today" OR ЛитРес новости платформы OR книжный рынок
**craft**: "larp design" OR "nordic larp" OR "larp methodology" site:nordiclarp.org OR site:analoggamestudies.org
**jetstyle**: "design agency" OR "DaaS" OR "productized design" OR "agency business model 2026"
**xrvr**: enterprise XR deal OR VR training contract OR "IDC" XR headset OR Counterpoint XR (за 7 дней)
**tracking**: трекинг стартапов кейс OR теория ограничений внедрение OR "theory of constraints" case (за 7 дней)
**stages** (search-driven): call for speakers/papers 2026 геймдев OR продуктовые конференции OR книжные ярмарки заявки; подкасты ищут гостей (тема: AI-агентства, геймдев, книги); LARP-конвенты приём заявок. Сигнал без дедлайна/даты — discard
**mentions** (search-driven): «Алексей Кулаков» JetStyle OR издательская платформа; JetStyle OR jet.style; «Бизнес-фэнтези» OR «Живые игры» Кулаков — за 7 дней, свои каналы Алексея не считаются
**vitality** (search-driven): meta-analysis sleep energy OR vitality intervention OR burnout recovery RCT (за 7 дней; только исследования, source = журнал/препринт)
**shortvideo** (search-driven): TikTok OR Reels OR Shorts algorithm change OR creator monetization update (за 7 дней)

### Step 6: Delta filter
For each candidate signal, check against exclusion list:
1. Was this signal (or nearly identical) already in facts files?
2. Does it add a NEW thought, mechanic, number, market, or interface?
3. If both answers are "no" → discard

### Step 7: Format digest
Format as Telegram HTML message. Key formatting rules:
- Bold ONLY for key facts inside signals (numbers, product names, key terms) — NOT for headers or meta
- Generous empty lines between signals for scannability
- Each signal = numbered, 2 lines max (headline + one-line context)
- Important signals first within each section
- No [high/medium/low] labels — importance expressed by position (top = most important)

**Source formatting — CRITICAL:**
- When the source is a Telegram channel post: ALWAYS include a direct quote (1-2 key sentences) in quotes, plus a direct link to the post (https://t.me/channel/postID)
- Format: <i>"Цитата из поста" — <a href="https://t.me/channel/123">@channel</a></i>
- When the source is a web article: link in italic <i><a href="URL">source name</a></i>
- Extract the post link from WebFetch output (the post ID is in the URL or data attribute)

Template:
```
SCOUT DAILY — {date}

ДЖЕРИАН  {N} новых

1. Обзор демо на <b>StopGame</b>: «нарративная жемчужина»
Сравнивают с Бранте, хвалят иллюстрации
<i><a href="https://stopgame.ru/...">stopgame.ru</a></i>

STEAM / ГЕЙМДЕВ  {N} новых

2. Valve: <b>Next Fest октября</b> — регистрация до 15 сентября
Демо с фестиваля дают медианно <b>+2500 wishlists</b>
<i><a href="https://howtomarketagame.com/...">howtomarketagame.com</a></i>

LARP  {N} новых

3. <b>Knutpunkt AWIG</b> начинается завтра
Nordic Larp Talks live + ларпы до основной конференции 16-19 апр
<i><a href="https://knutpunkt.se/a-week-in-gothenburg/">knutpunkt.se</a></i>

AGENCY  {N} новых

4. Rec Room VR: <b>$3.5B</b> оценка, серверы закрываются 1 июня
<i>"Очередной стартап-юникорн — на этот раз $3.5B" — <a href="https://t.me/startupoftheday/4997">@startupoftheday</a></i>

Нет новых: {topics where empty}

Ответь номером — подробности, действия и кик источника
```

Weekly topics appear as extra sections only on their day (помечай их «{Тема} — недельная сводка»). List only ACTIVE topics in "Нет новых".

KEY RULES for source attribution:
- Telegram post WITH exact text from WebFetch: direct quote in "" + link https://t.me/channel/postID
- Telegram post WITHOUT exact text: NO quotes, just channel link. Write your own summary line WITHOUT pretending it's a quote
- Web article: link with source name, no quote needed
- When you have the post ID from WebFetch — ALWAYS use it for the link
- When no post ID available — use channel name without link: @channel

CRITICAL: NEVER fabricate quotes. If you didn't get the exact words from WebFetch, do NOT put text in quotation marks. A paraphrase in quotes is worse than no quote at all — it's a lie.

Global numbering across all sections (1, 2, 3... not resetting per section).
Total message under 4000 chars.

### Step 7b: Save signal index
After formatting, save a signal index file for interactive follow-up:
`10-CLAUDE/news-scout/data/last-digest.json`

Format:
```json
{
  "date": "2026-08-02",
  "signals": {
    "1": {
      "topic": "steamdev",
      "title": "Valve обновила правила AI-disclosure",
      "detail": "one-line for the digest message",
      "theses": "3-5 bullet points summarizing key implications:\n- thesis 1\n- thesis 2\n- thesis 3",
      "source": "...",
      "source_url": "...",
      "source_kind": "tg",
      "source_id": "indiespotlight"
    }
  }
}
```

`source_kind` + `source_id` power the "Кик источник" button in Telegram (bot moves the source into `muted` in sources.json). Fill them for every signal that came from a configured source:
- tg → channel name without @ (as in sources.json)
- rss / web / yt → the exact `url`/`channel` value from sources.json
- signal from WebSearch (not from a configured source) → `source_kind: "search"`, `source_id: null` (nothing to kick)

The `theses` field is CRITICAL — it powers the "Подробнее" button in Telegram.
For each signal, write 3-5 short theses answering: what happened, why it matters, what it means for the topic.
Do NOT repeat the `detail` text — theses should add context and interpretation.

IMPORTANT: End every theses block with a section "Для моих целей:" that maps the signal to Lance's OKR:
- <ваши цели или OKR, по строке на цель>

Only mention relevant goals. If signal has no clear connection — write "Прямой связи с текущими целями нет, но полезно знать как контекст."

This file is read by the planning-bot scout handler when user replies with a number.

### Step 8: Append new facts
For each NEW signal included in the digest, append it to the corresponding facts file:
- Prepend to the TOP of the file (after the header)
- Format: `- **{brief title}** — {one-line description}. ({date}, {source}, {importance})`

### Step 9: Deliver to Telegram
Read the Bot API token from planning-bot config:
```bash
grep TELEGRAM_BOT_TOKEN 10-CLAUDE/planning-bot-v2/.env
```

Read the chat ID:
```bash
grep TELEGRAM_CHAT_ID 10-CLAUDE/planning-bot-v2/.env
```

Send via curl:
```bash
curl -s -X POST "https://api.telegram.org/bot{TOKEN}/sendMessage" \
  -d "chat_id={CHAT_ID}" \
  -d "text={DIGEST_TEXT}" \
  -d "parse_mode=HTML"
```

If the message is over 4096 chars, split into multiple messages by topic section.

## Rules
- Novelty-first: only include signals that are NOT in the facts files
- Cross-channel dedup: one news = one entry, note which channels mentioned it
- If no new signals for a topic: honestly say "No new signals"
- Max 5-8 signals per topic
- Importance levels: high / medium / low
- Sources: always cite
- Language: Russian for the digest text
