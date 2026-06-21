---
description: "Синтаксис и параметры Midjourney. Используй когда пользователь говорит 'промпт для Midjourney', 'MJ prompt', 'Midjourney параметры', 'как написать для миджорни', 'midjourney syntax', '--ar --v --style'. Справочник по командам и параметрам. НЕ используй для: генерации картинок напрямую (nanobanana), промптов для портретов (l-g-portrait), генерации музыки (l-g-suno, l-d-suno)."
---

# Справочник Midjourney

## Базовый синтаксис
```
/imagine [prompt] --[parameters]
```

## Основные параметры

### Соотношение сторон
- `--ar 1:1` — квадрат
- `--ar 16:9` — широкий
- `--ar 9:16` — вертикальный (сториз)
- `--ar 4:3` — стандартное фото
- `--ar 3:2` — классическое фото

### Версии модели
- `--v 6` — последняя версия
- `--v 5.2` — предыдущая
- `--niji 6` — аниме-стиль

### Стилизация
- `--stylize [0-1000]` или `--s` — уровень стилизации (default 100)
- Низкие значения = ближе к промпту
- Высокие = больше художественной интерпретации

### Качество
- `--quality 0.25` — быстро, низкое качество
- `--quality 0.5` — быстро
- `--quality 1` — стандарт (default)

### Хаос
- `--chaos [0-100]` или `--c` — вариативность результатов

### Стоп
- `--stop [10-100]` — остановить генерацию на X%

### Seed
- `--seed [number]` — для воспроизводимости

### Tile
- `--tile` — бесшовный паттерн

### Negative prompts
- `--no [element]` — исключить элемент

## Веса в промпте
- `element::2` — увеличить вес
- `element::0.5` — уменьшить вес
- `element1:: element2::` — разделить концепции

## Полезные модификаторы

**Стиль:**
- cinematic, editorial, documentary
- hyper-realistic, photorealistic
- oil painting, watercolor, digital art
- minimalist, maximalist

**Освещение:**
- golden hour, blue hour
- studio lighting, natural light
- dramatic lighting, soft lighting
- rim light, backlit

**Камера:**
- shot on [camera name]
- 35mm, 50mm, 85mm lens
- shallow depth of field
- wide angle, telephoto

**Качество:**
- 8k, highly detailed
- intricate details
- professional photography

## Примеры промптов

**Продуктовое фото:**
```
minimal product photography of [product], clean white background, soft studio lighting, 8k --ar 1:1 --v 6
```

**Интерьер:**
```
modern scandinavian living room, natural light, plants, wooden furniture, architectural photography --ar 16:9 --v 6
```

**Портрет:**
```
editorial portrait of [description], shot on Hasselblad, 85mm lens, soft natural light --ar 3:4 --v 6
```

Что хочешь сгенерировать?
$ARGUMENTS
