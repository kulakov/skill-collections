---
name: style-profile
aliases:
  - l-d-style-profile
  - brand-style-profile
  - style-json
description: "ОСНОВНОЙ скилл для клонирования визуального стиля. Извлекает JSON brand-style-profile из 1–N изображений или со страниц сайта — чтобы AI мог сгенерировать НОВЫЙ контент в том же стиле для любой темы. Используй когда пользователь говорит 'клонировать стиль', 'clone style', 'повтори стиль', 'сделай в этом стиле', 'in this style', 'возьми стиль с', 'стиль как у', 'извлеки стиль', 'extract style', 'style profile', 'стайл профиль', 'brand style profile', 'json стиля', 'опиши стиль для AI', 'разбери визуальный стиль', 'style guide из картинок', 'analyze visual style', 'distill style', 'переноси стиль на другой контент', 'переверстай в стиле', 'remake in style', 'restyle'. Вход: одно/несколько изображений или URL сайта (сделай скриншоты через Playwright). Выход: структурированный JSON (палитра, типографика, свет, композиция, пост-обработка, теги, правила переноса, anti-patterns). По окончании — предложи сохранить в библиотеку стилей через /add-style. НЕ используй для: добавления готового стиля в библиотеку (add-style), применения сохранённого стиля #N (l-s-use), генерации картинок (nanobanana), декомпозиции лендинга на 7 слоёв дизайн-системы (l-d-decompose), извлечения шаблонов слайдов (l-s-slide-extract), синтаксиса Midjourney (l-g-midjourney)."
---

# Style Profile Extractor

Извлекает **JSON brand style profile** из изображений — структурированное описание визуального языка, которое AI может использовать для генерации нового контента в том же стиле.

## Принцип

**Стиль ≠ контент.** Профиль описывает КАК выглядит, а не ЧТО изображено.

- НЕ упоминай конкретные субъекты, логотипы, продукты, людей, тексты, бренды с картинок
- ОПИСЫВАЙ только визуальный язык, правила композиции, дизайн-систему
- Цель: AI должен суметь применить профиль к ЛЮБОМУ контенту, сохранив визуальный язык

## Вход: $ARGUMENTS

- Один или несколько путей к изображениям
- ИЛИ URL сайта — тогда сделай 5–8 скриншотов разных типов страниц (главная, услуга, кейс, about, listing) через Playwright, сохрани в `.playwright-mcp/<slug>-style/` под allowed roots
- Если ничего не указано — спроси у пользователя

## Workflow

### 1. Чтение изображений — ОБЯЗАТЕЛЬНО через субагент

По глобальному правилу (CLAUDE.md): изображения читать ТОЛЬКО через `Task(subagent_type="general-purpose")`. Изображения съедают 1000–6000 токенов каждое.

Промпт для субагента:

```
Прочитай изображения по путям: [список путей].

Для КАЖДОЙ картинки извлеки наблюдения по 10 категориям:
1. Color usage — доминирующие тона, градиенты, палитра (hex-приближения), температура, контраст
2. Typography style — настроение шрифта (bold/modern/playful/clean/serif/grotesk/display), расположение, иерархия, weight
3. Lighting & vibe — energetic/moody/clean/vibrant/soft/harsh/diffused, направление света
4. Subject placement — centered/floating/grouped/perspective/rotated/cropped/rule-of-thirds
5. Background style — abstract/gradient/textured/scenic/solid/blurred/patterned
6. Composition layout — symmetrical/rule-of-thirds/collage/exploded-view/grid/diagonal
7. Branding elements — overlays, strokes, glows, shapes, burst effects, badges, frames
8. Visual tone — bold/casual/premium/loud/minimal/playful/editorial/corporate
9. Post-processing — contrast level, saturation, shadows, glow, noise/grain, vignette, film look
10. General style tags — жанр/feel (e.g. "sports aesthetic", "editorial", "clean tech", "pop art", "y2k", "brutalist")

Верни сводку по каждой категории. НЕ описывай конкретные субъекты/тексты/логотипы/бренды — только визуальный язык.
```

### 2. Синтез JSON-профиля

На основе ответа субагента собери JSON. Формат:

```json
{
  "style_name": "короткое описание стиля 2-4 слова",
  "tags": ["жанровые теги", "напр. sports-aesthetic", "bold-editorial"],
  "color": {
    "palette": ["#hex1", "#hex2", "#hex3"],
    "dominant": "#hex",
    "accent": "#hex",
    "temperature": "warm | cool | neutral",
    "contrast": "high | medium | low",
    "gradients": "описание градиентов или null",
    "notes": "напр. 'дуотон magenta+cyan', 'pastel washes'"
  },
  "typography": {
    "mood": "bold | modern | playful | clean | editorial | display",
    "families_implied": ["sans-serif", "grotesk", "serif", ...],
    "weight_range": "light | regular | bold | black",
    "case": "uppercase | lowercase | mixed | small-caps",
    "placement": "overlay-center | corner | banner | integrated",
    "hierarchy": "single-statement | hero+sub | multi-tier"
  },
  "lighting": {
    "mood": "energetic | moody | clean | vibrant | soft | harsh",
    "direction": "front | side | back | top | rim | diffused",
    "shadows": "deep | soft | none | hard-edged",
    "highlights": "blown | controlled | glow-bloom"
  },
  "subject_placement": {
    "framing": "centered | floating | grouped | perspective | rotated | cropped",
    "scale": "macro | medium | wide | tiny-in-vast",
    "orientation": "frontal | profile | three-quarter | top-down",
    "interaction_with_frame": "bleeding | contained | overflowing"
  },
  "background": {
    "type": "abstract | gradient | textured | scenic | solid | blurred | patterned",
    "depth": "flat | shallow | deep | infinite",
    "description": "напр. 'soft gradient blue→pink с лёгкой зернистостью'"
  },
  "composition": {
    "layout": "symmetrical | rule-of-thirds | collage | exploded-view | grid | diagonal | radial",
    "balance": "balanced | asymmetric | tension",
    "negative_space": "minimal | generous | extreme",
    "focal_strategy": "single-hero | distributed | guided-eye-path"
  },
  "branding_elements": {
    "overlays": ["strokes", "glows", "burst-rays", "frames", "badges", "tape", "stickers"],
    "motifs": "повторяющиеся графические элементы",
    "use_of_text_blocks": "большие плашки | inline | стикеры | none"
  },
  "visual_tone": ["bold", "premium", "playful", ...],
  "post_processing": {
    "contrast": "high | medium | low",
    "saturation": "muted | natural | boosted | hyper",
    "shadow_treatment": "crushed | lifted | natural",
    "glow_bloom": "none | subtle | heavy",
    "noise_grain": "none | fine | film-grain | heavy",
    "vignette": "none | subtle | strong",
    "film_emulation": "none | 35mm | polaroid | VHS | digital-clean"
  },
  "reapplication_rules": [
    "Конкретные правила, которые AI должен соблюдать при генерации нового контента в этом стиле.",
    "Напр.: 'Любой subject располагать по центру, увеличенным до 80% кадра'",
    "Напр.: 'Использовать только палитру из 3 цветов выше; accent — только на одном элементе'",
    "Напр.: 'Фон ВСЕГДА должен быть размытым градиентом без сцены'"
  ],
  "anti_patterns": [
    "Что НЕ делать при генерации в этом стиле.",
    "Напр.: 'не использовать реалистичные фотобэкграунды'",
    "Напр.: 'не добавлять серый — палитра строго насыщенная'"
  ]
}
```

### 3. Если изображений несколько

- Если стили ОДИНАКОВЫ → один общий JSON-профиль
- Если стили РАЗНЫЕ → попроси пользователя выбрать: общий профиль (усреднённый) или отдельные профили на каждую картинку

### 4. Сохранение

По умолчанию вывести JSON в чат. Затем предложи **две опции**:

1. **Сохранить в файл** — `style-profile_YYYY-MM-DD_HHMM.json` в текущей рабочей директории или другой указанный путь
2. **Добавить в библиотеку стилей** через `/add-style` — категория обычно `Branding` (теги: branding, studio, tech, system, creative и т.п.) для сайтов/брендов, или `Marketing` для рекламных/баннерных стилей. Thumbnail — первый исходный скриншот. Файл библиотеки: `~/.claude/style-library.html`, thumbnails: `~/.claude/style-library-thumbnails/`.

Если пользователь подтверждает (2), сделай запись напрямую (читай существующую структуру в `~/.claude/style-library.html`, найди next id, добавь запись перед `];` в конце массива `styles`).

## Правила вывода

- **Только JSON** (после короткого вступления в 1 строку). Никакого markdown вокруг JSON-блока, кроме ``` обёртки.
- Все поля заполнены. Если поле неприменимо → `null` или `"none"`, не пропускай.
- hex-цвета — приближения, не пиксель-перфектные.
- Никаких упоминаний реальных брендов/людей/продуктов/текстов с картинок.
- Профиль должен быть **переиспользуемым**: если подставить любую тему, AI должен выдать узнаваемо тот же стиль.

## Anti-checklist (что НЕ должно попасть в JSON)

- НЕ: "Фото Найка с кроссовкой Air Max" → ДА: "крупный объект по центру, контрастный к фону"
- НЕ: "Текст 'JUST DO IT'" → ДА: "крупная типографика-плашка, uppercase, bold"
- НЕ: "Спортсмен в прыжке" → ДА: "субъект в динамической позе, перспектива снизу"
