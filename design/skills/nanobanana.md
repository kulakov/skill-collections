---
description: "Генерация изображений через Gemini API. Используй когда пользователь просит нарисовать, сгенерировать картинку, сделать мокап, иконку, обложку, портрет, схему-как-картинку, инфографику, фон/подложку для карточки, иллюстрацию для презентации или лендинга. Также для доработки ранее сгенерированных изображений ('дорисуй', 'измени фон', 'добавь деталь'). Для карточек с большим количеством текста — генерируй только подложку/фон этим скиллом, текст делай отдельно в HTML. НЕ используй для: анализа существующих изображений, промптов Midjourney (/l-g-midjourney), апскейла (/l-d-enhance), генерации музыки, создания презентаций (/l-d-slides)."
aliases:
  - l-d-img
  - l-d-gen
---

# Nano-banana: Генерация изображений

Используй Python-модуль `image_gen.py` для генерации изображений через Gemini API.

## Расположение модуля

```
/Users/lance/lance-claude/09-REFERENCE/my-promts/claude/claude-artifacts/lesson-modules/3-nano-banana/image_gen.py
```

## Как использовать

### Базовая генерация

```bash
cd /Users/lance/lance-claude/09-REFERENCE/my-promts/claude/claude-artifacts/lesson-modules/3-nano-banana
python3 -c "
from image_gen import generate, new_session

new_session()
result = generate('Описание того, что нужно нарисовать')
print(f'Saved: {result}')
"
```

> Ключ загружается автоматически из `.env` файла рядом с модулем. Не хардкодь ключ в команде!

### Параметры generate()

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `prompt` | Текстовое описание | обязательный |
| `reference_images` | Список путей к референсам | None |
| `aspect_ratio` | "1:1", "3:4", "16:9" | "1:1" |
| `resolution` | "1K", "2K", "4K" | "1K" |
| `model` | gemini-2.5-flash-image / gemini-3-pro-image-preview | gemini-3-pro |

### Multi-turn (улучшение)

```python
# Первая генерация
result = generate("A cat sitting on a moon")

# Улучшение (сохраняет контекст)
result = generate("Make the cat orange and add stars")

# Ещё улучшение
result = generate("Add a spaceship in the background")
```

### Управление сессией

```python
new_session()      # Очистить сессию
session_info()     # Показать статус
revert(turns=1)    # Откатить последний turn
```

## Выходы

Изображения сохраняются в папку `outputs/` рядом с модулем.

## Ввод пользователя

$ARGUMENTS
