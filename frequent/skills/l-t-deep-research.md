---
name: deep-research
aliases:
  - l-t-deep-research
description: "Глубокий ресёрч через OpenAI Deep Research API (o4-mini). Используй когда пользователь говорит 'deep research', 'глубокий ресёрч', 'исследуй тему глубоко', 'comprehensive research', 'полное исследование', 'найди всё по теме'. Веб-поиск + синтез через OpenAI o4-mini-deep-research. НЕ используй для: научного ресёрча (/l-c-research, /l-rnd), добавления статьи в библиотеку (/l-t-paper), конспекта одного текста (/l-c-big-summary), VOC-майнинга (/l-t-voice-mine)."
---

# Deep Research (Lance Edition)

Глубокий ресёрч с веб-поиском через OpenAI Deep Research API (o4-mini-deep-research).

## Требования
- OPENAI_API_KEY в .env или environment
- Python 3.7+
- Скрипт: `10-CLAUDE/research-skills/deep-research/scripts/run_deep_research.py`

## Процесс

### 1. Принять запрос на ресёрч
Запрос может быть кратким или детальным.

### 2. Усилить промпт (если < 15 слов)
Спроси:
- Какой scope? (Open-source only? Определённый период?)
- Какая глубина? (Обзор / Техдетали / Сравнение / Имплементация)
- Фокус? (Перформанс / Стоимость / Безопасность / UX)

### 3. Запустить ресёрч

```bash
cd ~/10-CLAUDE/research-skills/deep-research/scripts && python3 run_deep_research.py "ПРОМПТ" --output-dir ~/10-CLAUDE/research-skills-test/results/
```

**ВАЖНО:** Ресёрч занимает 10-20 минут. Скрипт блокирующий — не нужен polling.

### 4. Представить результаты
- Markdown-отчёт с источниками
- Сохранить в `10-CLAUDE/research-skills-test/results/YYYYMMDD-research-[slug].md`

## Lance-специфика

### Связь с существующими скиллами
- `/l-t-res` — собственный ресёрч-скилл Lance (без API, через Claude)
- `/l-rnd` — автономный исследователь (через субагентов)
- `/l-t-deep-research` — этот скилл (через OpenAI API, с веб-поиском)

**Когда какой:**
- Быстрый вопрос → `/l-t-res`
- Автономное исследование → `/l-rnd`
- Глубокий ресёрч с актуальными данными из интернета → `/l-t-deep-research`
