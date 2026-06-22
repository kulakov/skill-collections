---
name: map-maker
description: "Генератор карт вымышленного мира. World-as-data: YAML источник истины + nano-banana растровый рендеринг + pycairo векторный рендеринг. Используй когда пользователь просит создать карту, обновить географию, сгенерировать фрагмент карты, или добавить HTML-подписи на карту."
aliases:
  - l-d-map
---

# Map Maker — Карты вымышленных миров (World-as-data)

## Архитектура

**Источник истины = YAML файл.** Все координаты, объекты и валидация читаются из него. Рендереры (растровый и векторный) — производные.

```
tallan_world.yaml (канон)
    ├── map_generator.py (pycairo, вектор)
    ├── nano-banana prompt (Gemini, растр)
    └── HTML overlay (подписи поверх растра)
```

### Почему не AI-extraction

**Провалившийся подход:** AI reference → OpenCV HSV-сегментация → pycairo.
**Проблема:** AI генерирует разную географию каждый раз. Города/горы привязаны к координатам v1, а контур моря из v2 — горы оказываются в воде.
**Решение:** YAML как единый источник. Все объекты валидируются при загрузке (point-in-polygon).

---

## Ключевые файлы

### Проект "Тал'Лан" (Дети глины)
```
03-CREATE/Писательство/Дети_глины/справочник/
├── tallan_world.yaml              # КАНОН — вся география
├── map_generator.py               # pycairo рендерер (читает YAML)
├── tallan_british_clean.png       # Растровая карта БЕЗ подписей
├── tallan_british_raster.png      # Растровая карта С подписями
├── tallan_archipelago_hires.png   # Детальный фрагмент (архипелаг)
└── MAP_HTML_CONTEXT.md            # Контекст для HTML-подписей
```

### Скилл
```
~/.claude/skills/map-maker/
├── SKILL.md                       # этот файл
├── extract.py                     # OpenCV extraction (legacy, для новых миров)
├── render.py                      # pycairo базовый рендерер
├── svg_viewer.py                  # SVG просмотрщик с pan/zoom
├── styles/                        # JSON пресеты стилей
└── templates/clear-colors-prompt.txt  # промпт для AI-референсов
```

---

## YAML — формат данных мира

Координаты нормализованы 0..1, (0,0) = top-left. Для CSS: `left: X*100%`, `top: Y*100%`.

```yaml
world:
  name: "Тал'Лан"

seas:           # полигоны морей
  clay_sea:
    name: "Глиняное море"
    label_pos: [0.50, 0.48]
    polygon: [[x,y], ...]        # замкнутый контур

islands:        # полигоны островов (holes в морях)
  clay_shore:
    name: "Глиняный Берег"
    label_pos: [0.56, 0.52]
    polygon: [[x,y], ...]

cities:         # точки с direction для подписей
  sharani:
    name: "Шарани"
    pos: [0.50, 0.09]
    size: large                   # large / medium / small
    direction: N                  # куда отступить подпись

mountains:      # spine — массив точек хребта
  isthmus:
    spine: [[x,y], ...]
    label: "Перешеек"
    label_pos: [0.24, 0.36]

roads:          # линии между городами
  sharani_artak:
    points: [[0.50, 0.09], [0.38, 0.10], [0.26, 0.13]]

rivers:         # аналогично roads
forests:        # pos + radius + stretch + rotation
ruins:          # pos (мелкий курсив)
melkar_colonies:  # pos + size: small

presets:        # viewport'ы для масштабов
  world:     { viewport: [0, 0, 1, 1] }
  archipelago: { viewport: [0.35, 0.35, 0.40, 0.40] }
```

### Валидация при загрузке

`map_generator.py` → `load_world(yaml_path)`:
- Ray casting (point-in-polygon) для каждого города/горы/леса
- Если объект в воде → WARNING (но не crash — вулкан на острове = ожидаемый false positive)

---

## Пайплайн: растровая карта (основной)

### 1. Генерация полной карты (nano-banana)

```python
from image_gen import generate, new_session
new_session()
result = generate(
    'Описание географии из YAML + стиль',
    resolution='2K'
)
```

**Промпт строится из YAML:** перечислить все моря, города, хребты, дороги с позициями (north, south, center и т.д.).

**Стиль:** 19th century British Ordnance Survey copper-plate engraving, monochrome sepia.

### 2. Убрать надписи (multi-turn)

```python
result = generate('Remove ALL text labels — no city names, no sea names, no title...')
```

Gemini упорно оставляет 2-3 надписи. Нужен второй turn: "Remove CLAY SEA, ASH SEA, scale text."

**Результат:** `tallan_british_clean.png` — чистая карта для HTML-подписей.

### 3. Зум-фрагменты

**Метод:** полная карта как reference_image + описание зоны.

```python
new_session()
result = generate(
    'Zoomed-in nautical chart of the central sea area...',
    reference_images=['tallan_british_clean.png'],
    resolution='2K'
)
```

**КРИТИЧНО:** Использовать полную карту как референс, НЕ кроп. Кроп 410px → шакальные линии.

**Что добавлять в zoom:**
- Береговые хачуры (штриховка ТОЛЬКО у берегов, чистая вода в центре)
- Глубины (serif числа: 5, 8, 12, 15, 20, 35)
- Румбовые линии (тонкие прямые через море)
- Стипплинг на суше

**Чего НЕ добавлять (если нет на основной карте):**
- Не изобретать новые элементы — zoom должен выглядеть как увеличенная версия той же карты

### 4. HTML-подписи поверх

Контейнер `position: relative`, подписи `position: absolute` с `left/top` в процентах из YAML.
Шрифты: serif (Playfair Display / EB Garamond).
Подробности: `MAP_HTML_CONTEXT.md`.

---

## Пайплайн: векторная карта (legacy)

```bash
cd 03-CREATE/Писательство/Дети_глины/справочник/
python3 map_generator.py all --world tallan_world.yaml
```

Рендерит pycairo: береговые линии, хачуры гор, иконки городов, леса, дороги, компас, картуш.

---

## Уроки и антипаттерны

### Работающие приёмы
1. **YAML как канон** — горы не в море, города на местах, всё валидируется
2. **Полная карта как референс для zoom** — высокое качество линий
3. **Multi-turn для удаления надписей** — Gemini не убирает всё с первого раза
4. **Береговые хачуры "only near coastlines"** — явно указывать в промпте, Gemini умеет (проверено на v3)
5. **Карта без текста + HTML overlay** — полный контроль над подписями

### Антипаттерны
1. **НЕ доверяй AI-extraction для стабильной географии** — каждая генерация = новый мир
2. **НЕ используй маленький кроп как reference** — кроп 410px → пиксельные артефакты
3. **НЕ добавляй в zoom элементы отсутствующие на основной карте** — это создаёт противоречие
4. **НЕ доверяй субагенту-аналитику безоговорочно** — перепроверяй критичные выводы (v3 water hatching был правильный, а субагент сказал "всё залито")
5. **НЕ используй фэнтези-стиль** — для Тал'Лан стиль = British OS 19c (гравюра)

### Ограничения Gemini
- Не умеет pixel-accurate upscale — zoom всегда re-imagination с drift береговых линий
- Штриховку моря "только у берегов" делает, но может потребоваться явная формулировка
- Надписи убирает за 2 прохода, не за 1

---

## Стилевые пресеты

`~/.claude/skills/map-maker/styles/`:
- `british-os-19c.json` — гравюра, сепия, хачуры (default для Тал'Лан)
- `british-military-1850.json` — военная карта
- `fantasy.json` — castle icons, volumetric mountains
- `modern.json` — минимализм, sans-serif
- `tolkien.json` — Middle-earth, runic, aged paper

---

## Интеграция

- `/nanobanana` — генерация растровых карт и zoom-фрагментов
- `/l-d-enhance` — апскейл готовых карт (AuraSR 4x, без галлюцинаций)
- `/l-x-frontend` — HTML-страница с картой и подписями
- `MAP_HTML_CONTEXT.md` — полный контекст для HTML-подписей (координаты всех объектов)

---

$ARGUMENTS
