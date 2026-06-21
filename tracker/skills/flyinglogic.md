---
description: "Генератор диаграмм Flying Logic (нативный формат .xlogic через JSON+генератор) и деревьев ТОС. Используй когда пользователь говорит 'флаинглоджик', 'flyinglogic', 'flying logic', 'сделай в flying logic', 'экспорт в flying logic', '.xlogic', 'дерево текущей реальности', 'CRT', 'current reality tree', 'дерево будущей реальности', 'FRT', 'дерево ТОС', 'TOC tree', 'дерево конфликтов', 'грозовая туча', 'evaporating cloud', 'логическое дерево', 'дерево НЖЯ'. Строит промежуточный JSON (nodes/edges/groups) → .xlogic; опционально Mermaid/псевдографика. Алиас: l-d-flyinglogic. НЕ используй для: извлечения тезисов из транскрипта (thesis-extraction), графа знаний (graphify), картинок (nanobanana), презентаций (l-d-slides)."
---

# Скилл: Flying Logic / деревья ТОС

Строит диаграммы Theory of Constraints для **Flying Logic**. Поддерживает CRT (дерево текущей
реальности), FRT (дерево будущей реальности), Conflict/Evaporating Cloud, Prerequisite Tree.

## ⚠️ ЕДИНСТВЕННЫЙ способ (не отклоняться)

Алексей пользуется **Flying Logic 3.0.1**. Формат и шаблон уже решены. Делать ровно так:

**ВСЕГДА:** собрать `graph.json` → прогнать готовый генератор → отдать `.xlogic`. Одна команда:
```bash
python3 "09-REFERENCE/my-promts/ TOC diagram/flyinglogic_generator.py" \
  --in crt-<slug>.flyinglogic.json --out crt-<slug>.xlogic
```
Генератор по умолчанию берёт вшитый canonical-шаблон `templates/toc-crt.xlogic` (настоящая обвязка
домена из реального файла Алексея), строит vertices/edges по точной схеме 3.0.1, валидирует XML.
Координат не нужно — FL раскладывает сам. Файл открывается двойным кликом. **Проверено, открывается.**

**НИКОГДА:**
- ❌ не запрашивать шаблон у пользователя — он уже вшит;
- ❌ не писать `.xlogic`/XML руками и не выдавать `<flyinglogic version="3">` за формат — FL это не откроет;
- ❌ не подгонять под другую версию FL и не менять `--template` (по умолчанию = canonical, этого достаточно);
- ❌ не отдавать вместо `.xlogic` другой формат (Mermaid/HTML — только как доп. визуал по запросу).

Факты формата (для справки, руками НЕ собирать): plain XML, корень `<flyingLogic majorVersion="4" minorVersion="0">`,
`decisionGraph → logicGraph → graph → vertices/edges`; узел `<vertex eid>` с `<attribute key="type">entity</attribute>`,
`entityClass`(ref), `title`, `note`; ребро `<edge eid source target>`. Всё это уже умеет генератор.

> Исключение (редко): если пользователь явно сообщит, что файл НЕ открывается в его FL — тогда попросить
> один его `.xlogic`, положить в `templates/`, передать `--template`. Без этого сигнала — не трогать.

## Источник истины (что реально работает)

- **Генератор:** `09-REFERENCE/my-promts/ TOC diagram/flyinglogic_generator.py` — он и есть спека формата.
- **Canonical-шаблон:** `09-REFERENCE/my-promts/ TOC diagram/templates/toc-crt.xlogic` (донор обвязки 3.0.1).
- **Эталонный вход:** `11-TRACKER/teams/kindred/research/crt-communities.flyinglogic.json`.
- Старый `thesis-extraction-module-flyinglogic.md` — НЕ читать как спеку формата (там устаревшее описание).
- **Mermaid/GraphViz модули:** рядом в `09-REFERENCE/my-promts/ TOC diagram/` (доп. визуал, не `.xlogic`).

## Промежуточный JSON (вход генератора)

```json
{
  "title": "...",
  "nodes": [
    { "id": "RC", "title": "...", "class": "root", "annotation": "КОРНЕВАЯ ПРИЧИНА" },
    { "id": "C1", "title": "...", "class": "intermediate" },
    { "id": "U1", "title": "...", "class": "ude" }
  ],
  "edges": [
    { "source": "RC", "target": "C1" },
    { "source": "U1", "target": "RC", "type": "feedback", "annotation": "петля" }
  ]
}
```
Эталон входа — рядом: `11-TRACKER/teams/kindred/research/crt-communities.flyinglogic.json` (CRT) и
`frt-communities.flyinglogic.json` (FRT).

**Классы узлов (домен ТОС, цвета вшиты в canonical-шаблон):**
`root` (корень, розовый) · `intermediate` (следствие, жёлтый) · `context` (условие среды, серый) ·
`multiplier` (мультипликатор, синий) · `ude` (боль/НЖЯ, красный) ·
FRT: `inject` (инъекция, зелёный) · `good` (желаемое) · `goal` (цель).
Старые синонимы (`problem`→ude, `claim`→intermediate, `fact`→context) тоже поддержаны.

## Сборка .xlogic

```bash
python3 "09-REFERENCE/my-promts/ TOC diagram/flyinglogic_generator.py" \
  --in crt-<slug>.flyinglogic.json \
  --out crt-<slug>.xlogic
```
Без `--template` берётся вшитый canonical `templates/toc-crt.xlogic` (FL 3.0.1). Генератор строит
`vertex`/`edge` по точной схеме формата, вставляет в `<graph>`, проставляет eid/noteNumber, валидирует XML.
`class` → цвет (см. список выше), `annotation` → заметка узла. Координаты не нужны — FL раскладывает сам.
`--template my.xlogic` — только если у пользователя другая версия FL и canonical не открывается.

## Правила построения

1. **Рёбра:** `source`=причина → `target`=следствие (sufficient cause: «ЕСЛИ source, ТО target»).
2. **Логика И:** несколько причин в один `target` — генератор подключает их прямо к узлу (forwardOperator
   узла), отдельные junctor-узлы не создаются. Для FL это валидно и читаемо.
3. **Петли:** `type="feedback"` + annotation с именем петли. Возражение — `type="negative"`.
4. **Корень:** ровно один; в annotation — «КОРНЕВАЯ ПРИЧИНА».
5. **Формулировки L4:** компактные (15–20 слов).

## Алгоритм

1. Прочитай канонический модуль (путь выше).
2. Из входа собери `nodes` + `edges` + `groups`, сохрани `crt-<slug>.flyinglogic.json` в папку проекта.
3. Если просили визуал прямо сейчас — добавь **Mermaid** (`graph BT`) и/или HTML-дерево (не путать с .xlogic).
4. Прогони генератор (одна команда, БЕЗ `--template`) → отдай `.xlogic`. Шаблон не запрашивать,
   XML руками не писать, под другую версию не подгонять.
5. Дай полный абсолютный путь `/Users/lance/...`.

## Связанное
- `/thesis-extraction` — извлечь тезисы из транскрипта (вход для этого скилла)
- `/graphify` — граф знаний (не ТОС)
