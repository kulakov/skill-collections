---
name: news-scout
description: "Daily delta-research digest. Triggers: 'news scout', 'дайджест новостей', 'scout run', 'запусти скаут', 'news digest'. Scheduled daily at 18:00 via /schedule."
---

# News Scout — Delta-Research Daily Digest

You are a delta-research agent. Your job: find NEW signals across 3 topics, deduplicate, and deliver a concise digest to Telegram.

## Config

**Sources are defined in `10-CLAUDE/news-scout/data/sources.json`** — read this file first.

Structure:
- `topics` — 5 topics (dzun, jetstyle, attraction, funding, craft), each with name/OKR/keywords
- `telegram` — TG channels, each tagged with a topic
- `rss` — RSS/Atom feeds, each tagged with a topic
- `youtube` — YouTube channels (fetched via t.me or youtube.com/@handle/videos), each with topic
- `web` — static web pages to monitor for changes (blogs, changelogs)

FACTS_DIR: `10-CLAUDE/news-scout/data` — one facts-{topic}.md per topic.

## Pipeline (execute sequentially)

### Step 1: Load config + exclusion lists
1. Read `10-CLAUDE/news-scout/data/sources.json` — get topics, TG channels, RSS feeds, YouTube, web sources
2. For each topic in config, read the last 50 lines of `facts-{topic}.md` (create file if missing)

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
For each post, determine which topic(s) it relates to:
- **dzun**: AI, coding tools, vibe-coding, no-code, builders, LLM, startups building software
- **larp**: LARP, role-playing games, game design methodology, narrative design, Nordic larp
- **jetstyle**: Agency business, design services, marketing channels, DaaS, client acquisition, AI in agencies, XR/VR business
- **general**: Interesting but doesn't fit any topic — skip unless truly remarkable

Posts that don't match any topic → discard.

### Step 4: Cross-channel deduplication
If the same news/event appears in multiple channels:
- Keep ONE entry
- Note: "(@channel1 + N more channels)"

### Step 5: Web Research
For each topic, do 1-2 targeted WebSearch queries for the last 24 hours:

**dzun**: "vibe coding" OR "AI builder" OR "Lovable" OR "Bolt.new" OR "Replit" OR "Cursor" site:techcrunch.com OR site:producthunt.com
**larp**: "larp design" OR "nordic larp" OR "larp methodology" site:nordiclarp.org OR site:analoggamestudies.org
**jetstyle**: "design agency AI" OR "DaaS" OR "productized design" OR "agency business model 2026"

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

AI / DZUN  {N} новых

1. Suleyman: агенты на <b>месячные проекты к 2027</b>
Вычисления выросли в триллион раз с 2010
<i>"Semi-autonomous agents will manage month-long projects" — <a href="https://t.me/blognot/4521">@blognot</a></i>

2. Amazon <b>$200B capex</b> 2026, Trainium <b>$20B→$50B</b>
AI-инфраструктура AWS становится самостоятельным бизнесом
<i><a href="https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-2025-letter-to-shareholders">Andy Jassy shareholder letter</a></i>

LARP  {N} новых

3. <b>Knutpunkt AWIG</b> начинается завтра
Nordic Larp Talks live + ларпы до основной конференции 16-19 апр
<i><a href="https://knutpunkt.se/a-week-in-gothenburg/">knutpunkt.se</a></i>

AGENCY  {N} новых

4. Rec Room VR: <b>$3.5B</b> оценка, серверы закрываются 1 июня
<i>"Очередной стартап-юникорн — на этот раз $3.5B" — <a href="https://t.me/startupoftheday/4997">@startupoftheday</a></i>

Нет новых: {topics where empty}

Ответь номером — получишь подробности и действия
```

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
  "date": "2026-04-05",
  "signals": {
    "1": {
      "topic": "dzun",
      "title": "OpenAI $122B",
      "detail": "one-line for the digest message",
      "theses": "3-5 bullet points summarizing key implications:\n- thesis 1\n- thesis 2\n- thesis 3",
      "source": "...",
      "source_url": "..."
    }
  }
}
```

The `theses` field is CRITICAL — it powers the "Подробнее" button in Telegram.
For each signal, write 3-5 short theses answering: what happened, why it matters, what it means for the topic.
Do NOT repeat the `detail` text — theses should add context and interpretation.

IMPORTANT: End every theses block with a section "Для моих целей:" that maps the signal to Lance's OKR:
- O1: JetStyle самоуправляемый и прибыльный
- O3: Новый быстро растущий бизнес (Dzun/Hodman)
- O4: Масштабируемый канал привлечения клиентов
- O7: Произведения которыми горжусь (LARP, книги)
- O8: Схизма (книга)

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
