# Map Maker — Генератор векторных карт вымышленного мира

Автоматизированный пайплайн для создания точных векторных карт через комбинацию AI-генерации, OpenCV извлечения и pycairo рендеринга.

## Быстрый старт

### Использование через Claude Code

```bash
/map-maker
# или
/l-d-map
```

Claude проведёт тебя через весь процесс:
1. Запросит описание географии мира
2. Сгенерирует AI-референс с чистыми цветами (через nano-banana)
3. Извлечёт топологию через OpenCV HSV-сегментацию
4. Отрендерит векторные карты в заданном стиле
5. Создаст overlay для проверки точности

### Использование напрямую (Python)

```bash
# Шаг 1: Генерация reference
# (используй /nanobanana или промпт из templates/clear-colors-prompt.txt)

# Шаг 2: Извлечение топологии
python ~/.claude/skills/map-maker/extract.py reference.png topology.json

# Шаг 3: Рендеринг карты
python ~/.claude/skills/map-maker/render.py topology.json british-os-19c map_world.png
```

---

## Алгоритм (3 шага за ~2 минуты)

### 1. AI-генерация reference с чистыми цветами (~60 сек)

**Проблема:** Gemini по умолчанию генерирует монохромные карты (вода и суша неразличимы: BGR difference 12-16).

**Решение:** Промпт с ЯВНЫМ требованием цветов:
```
Deep blue (#2266AA) water, beige (#D4B896) land, sharp boundaries, NO GRADIENTS
```

Результат: PNG 1024×1024 с отличным контрастом.

### 2. OpenCV извлечение координат (~30 сек)

**Алгоритм:**
- HSV-сегментация: `H=90-130, S>80, V>80` → маска воды
- Морфология: `CLOSE → OPEN` (убрать шум, закрыть дыры)
- Контуры: `cv2.findContours(RETR_TREE)` → иерархия (море + острова как holes)
- Упрощение: Douglas-Peucker binary search → целевое количество точек
- Нормализация: координаты в 0..1

**Результат:** `topology.json` с нормализованными контурами.

### 3. pycairo векторный рендеринг (~30 сек)

**Алгоритм:**
- Загрузка координат + стилевой пресет
- Catmull-Rom spline → cubic Bezier (alpha=0.5)
- Рендеринг в заданном стиле (hachures, compass rose, cartouche, etc.)
- Экспорт PNG (или SVG)

**Результат:** Векторная карта в стиле British OS 19c / fantasy / modern / tolkien.

---

## Стили

### 1. British Ordnance Survey 19c (default)

Гравюра, сепия, штриховка, каллиграфия.

**Особенности:**
- Волнистая штриховка воды (hachures)
- Плотные хачуры гор
- Компасная роза + масштабная линейка
- Заголовок в картуше (двойная рамка)

**Использование:**
```bash
python render.py topology.json british-os-19c map_world.png
```

### 2. Fantasy

Castle icons, volumetric mountains, пергамент.

**Особенности:**
- Замки вместо кружков для городов
- Объёмные горы
- Sea monsters (опционально)
- Состаренная бумага

**Использование:**
```bash
python render.py topology.json fantasy map_world.png
```

### 3. Modern Minimalist

Минимализм, чистые линии, sans-serif.

**Особенности:**
- Белый фон
- Нет штриховки (solid fill)
- Простые треугольники для гор
- Без декоративных элементов

**Использование:**
```bash
python render.py topology.json modern map_world.png
```

### 4. Tolkien (Middle-earth Style)

Runic fonts, aged paper, темные хачуры.

**Особенности:**
- Runic decorations
- Темные хачуры гор
- Состаренная бумага
- Celtic border

**Использование:**
```bash
python render.py topology.json tolkien map_world.png
```

---

## Примеры

### Пример 1: Создание карты Тал'Лан с нуля

**Входные данные:**
```
Создай карту мира "Тал'Лан":
- Глиняное море в центре с глубокими бухтами на западе и острыми мысами на востоке
- Крупный вулканический остров "Глиняный Берег" в юго-центре моря
- Архипелаг из 7 мелких островов на севере моря
- Пепельное море на северо-западе (за горным Перешейком)
- Стиль: British Ordnance Survey 19 века
```

**Выходные файлы:**
- `reference.png` — AI-референс с чистыми цветами
- `topology.json` — координаты (30 точек море, 15 точек остров, 7×7 точек архипелаг)
- `_debug_contours.png` — визуализация извлечённых контуров
- `comparison_overlay.png` — оверлей programmatic + reference (~95% совпадение)
- `map_world.png` — векторная карта в стиле гравюры

### Пример 2: Использование существующего референса

**Входные данные:**
```
У меня есть карта_banana_v1.png с чистыми цветами.
Извлеки топологию и отрендери в стиле fantasy.
```

**Команды:**
```bash
# Извлечение
python extract.py карта_banana_v1.png topology.json

# Рендеринг
python render.py topology.json fantasy map_world.png
```

### Пример 3: Изменение стиля существующей топологии

**Входные данные:**
```
У меня есть topology.json от предыдущей генерации.
Отрендери в стиле Tolkien.
```

**Команды:**
```bash
python render.py topology.json tolkien map_tolkien.png
```

---

## Troubleshooting

### Проблема: Монохромный Gemini

**Симптомы:**
- Gemini генерирует красивую карту, но вода и суша неразличимы (близкие цвета)

**Решение:**
Генерировать **новый** reference с ЯВНЫМ требованием цветов в промпте:
```
Deep blue (#2266AA) water, beige (#D4B896) land, sharp boundaries, NO GRADIENTS
```

Используй шаблон из `templates/clear-colors-prompt.txt`.

### Проблема: Обрезанные моря по краю референса

**Симптомы:**
- Пепельное море обрезано по краю (не полностью видно)

**Решение:**
Добавить в промпт:
```
Ensure all geographic features are fully inside the image (add padding around edges)
```

### Проблема: Города попадают в воду

**Симптомы:**
- После извлечения новой топологии координаты городов рассчитаны под старую географию

**Решение:**
1. **Вручную:** Переставить координаты городов в `map_generator.py`
2. **Автоматически:** Извлечь из banana-референса через YOLO/object detection

### Проблема: Слишком мало/много точек в контуре

**Симптомы:**
- Слишком грубая форма → потеря деталей бухт/мысов
- Слишком детальная → мелкие артефакты, шумные края

**Решение:**
Подстроить `target_points`:
```python
target_points = {
    "sea": 40,           # +10 точек для более сложной формы
    "large_island": 20,
    "small_island": 10
}
```

---

## Структура файлов

```
~/.claude/skills/map-maker/
├── SKILL.md                    # полное описание скилла для Claude
├── README.md                   # этот файл
├── extract.py                  # OpenCV extraction engine
├── render.py                   # pycairo rendering engine
├── styles/
│   ├── british-os-19c.json    # British Ordnance Survey 19c
│   ├── fantasy.json           # Fantasy map
│   ├── modern.json            # Modern minimalist
│   └── tolkien.json           # Middle-earth style
└── templates/
    └── clear-colors-prompt.txt # промпт-шаблоны для nano-banana
```

---

## Зависимости

```bash
# OpenCV для извлечения контуров
pip install opencv-python numpy

# pycairo для векторного рендеринга
pip install pycairo

# Optional: для генерации reference через nano-banana
# (установлено в Claude Code по умолчанию)
```

---

## Ключевой прорыв

**До:** Попытки извлечь береговую линию из монохромного Gemini-референса (все цветовые методы провалились).

**После:** Генерация **нового** reference с чистыми цветами → HSV-сегментация даёт ~95% точность топологии за 30 секунд.

**Производительность:**
- Генерация reference: ~60 сек
- Извлечение контуров: ~30 сек
- Рендеринг pycairo: ~30 сек
- **TOTAL: ~2 минуты** (vs часы ручного tweaking)

---

## Автор

Lance Kulakov
Проект: "Дети глины" (Тал'Лан)
Локация файлов: `~/03-CREATE/Писательство/Дети_глины/справочник/`

## Лицензия

MIT
