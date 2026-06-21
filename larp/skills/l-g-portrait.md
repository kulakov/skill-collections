---
description: "Промпт для генерации портретов в Midjourney/DALL-E. Используй когда пользователь говорит 'сгенерируй портрет', 'portrait prompt', 'промпт для портрета', 'нарисуй персонажа', 'character portrait', 'аватар персонажа'. Создаёт детальный промпт с параметрами стиля, освещения, ракурса. НЕ используй для: генерации картинок напрямую (nanobanana), справочника MJ (l-g-midjourney), фото-апскейла (l-d-enhance)."
---

# Генератор промптов для портретов

Создай промпт для генерации портрета.

## Параметры для уточнения:

### Субъект
- Пол, возраст
- Этническая принадлежность
- Выражение лица
- Поза

### Стиль
- Фотореализм / иллюстрация / живопись
- Референсный художник/фотограф
- Эпоха/эстетика

### Освещение
- Natural light / studio / dramatic
- Направление света
- Цветовая температура

### Фон
- Solid color / gradient / environment
- Боке / резкость
- Настроение

### Технические параметры
- Камера/объектив (для фото-стиля)
- Соотношение сторон
- Детализация

## Формат промпта для Midjourney:

```
[subject description], [pose/expression], [style reference], [lighting], [background], [camera/lens], [additional details] --ar [ratio] --v 6
```

## Примеры:

**Корпоративный портрет:**
```
professional headshot of a confident 35-year-old businessman, slight smile, wearing navy suit, studio lighting with soft shadows, clean white background, shot on Canon 5D with 85mm lens, 8k, highly detailed --ar 3:4 --v 6
```

**Художественный портрет:**
```
oil painting portrait of a thoughtful woman in her 40s, inspired by John Singer Sargent, dramatic Rembrandt lighting, rich earth tones, visible brushstrokes, museum quality --ar 4:5 --v 6
```

Опиши, какой портрет нужен:
$ARGUMENTS
