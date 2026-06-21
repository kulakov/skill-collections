---
description: "Синтаксис и параметры Suno для генерации музыки. Используй когда пользователь говорит 'промпт для Suno', 'Suno синтаксис', 'как написать для суно', 'музыкальный промпт', 'suno tags', 'metatags suno'. Справочник по режимам, мета-тегам, стилям. НЕ используй для: генерации музыки через API (l-d-suno), локальной генерации музыки (ace-step), видео (l-d-kling, l-d-remotion)."
---

# Справочник Suno

## Базовые режимы

### Simple Mode
Просто опиши, что хочешь:
```
Upbeat pop song about summer love
```

### Custom Mode
Больше контроля:
- **Style of Music** — жанр и настроение
- **Title** — название трека
- **Lyrics** — текст песни

## Теги стиля

### Жанры
- pop, rock, indie, alternative
- hip-hop, rap, r&b, soul
- electronic, edm, house, techno
- jazz, blues, funk
- folk, country, acoustic
- classical, orchestral
- metal, punk, grunge

### Настроение
- upbeat, energetic, happy
- sad, melancholic, emotional
- chill, relaxed, ambient
- dark, intense, aggressive
- romantic, dreamy, nostalgic

### Эпоха
- 80s, 90s, 2000s
- vintage, retro, modern
- classic, contemporary

### Вокал
- male vocals, female vocals
- deep voice, high voice
- whispered, spoken word
- choir, harmonies

### Инструменты
- acoustic guitar, electric guitar
- piano, synth, strings
- drums, bass, percussion

## Структура лирики

### Metatags
```
[Intro]
[Verse]
[Pre-Chorus]
[Chorus]
[Bridge]
[Outro]
[Instrumental]
[Break]
```

### Вокальные теги
```
[Whispered]
[Spoken]
[Harmonized]
[Ad-lib]
```

### Пример структуры
```
[Intro]
[Verse 1]
First verse lyrics here
More lyrics

[Chorus]
Catchy chorus lyrics
Repeat this part

[Verse 2]
Second verse lyrics

[Chorus]

[Bridge]
Something different here

[Chorus]

[Outro]
```

## Советы

**Для лучших результатов:**
- Будь конкретным в стиле
- Используй референсные артисты: "in the style of [artist]"
- Комбинируй жанры: "indie folk with electronic elements"
- Указывай темп: "slow ballad", "fast-paced"
- Указывай инструментальные особенности

**Для текста:**
- Используй структурные теги
- Пиши рифмованные строки
- Учитывай ритм и слоги
- Добавляй повторения в припеве

## Примеры промптов

**Поп-баллада:**
```
Style: Emotional pop ballad, piano-driven, female vocals, in the style of Adele

[Verse 1]
Walking through the memories we made
Every photograph now starts to fade
...
```

**Инди-рок:**
```
Style: Indie rock, energetic, 2000s alternative, male vocals, driving guitars

[Verse 1]
...
```

Опиши, какую музыку хочешь создать:
$ARGUMENTS
