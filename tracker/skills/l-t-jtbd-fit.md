---
description: "JTBD Fit Check — проверка product-market fit спеки по Jobs-to-be-Done (Christensen, Ulwick). Используй когда пользователь говорит 'JTBD check', 'проверка fit', 'jobs to be done review', 'попадание в работу пользователя', 'spec review JTBD'. Часть набора Spec Review. НЕ используй для: JTBD-анализа интервью (l-t-jtbd), cognitive walkthrough (l-t-cognitive-walkthrough), Kano (l-t-kano-analysis)."
---

# JTBD Fit Check — Spec Review

Проверка product-market fit по Jobs-to-be-Done (Christensen, Ulwick, Moesta). Для каждой ключевой фичи — проверить попадание в "работу" пользователя.

## Входные данные

Прочитай BRIEF.md (Pain, Persona, Killer Feature, Scope) и SPEC.md.

## Процедура

### Шаг 1: Сформулировать JTBD

Для целевого пользователя сформулируй 3-5 ключевых Jobs:
```
When [situation], I want to [motivation], so I can [expected outcome].
```

### Шаг 2: Анализ 4 сил для каждого Job

| Сила | Описание | Вопрос |
|------|----------|--------|
| **Push** | Боль в текущей ситуации | Насколько сильна боль? (1-5) |
| **Pull** | Притяжение нового решения | Насколько привлекателен результат? (1-5) |
| **Anxiety** | Страх переключения | Что пугает в переходе? (1-5, где 5 = максимальный страх) |
| **Inertia** | Привычка к текущему | Насколько привычно текущее решение? (1-5) |

**Формула:** Если Push + Pull > Anxiety + Inertia → переключение вероятно.

### Шаг 3: Проверка фич

Для каждой фичи из SPEC:
- К какому Job она относится?
- В какую силу бьёт? (снижает Anxiety? усиливает Pull? давит на Push?)
- Есть ли фичи которые НЕ бьют ни в один Job?

## Формат вывода

### Jobs Map

| # | Job | Push | Pull | Anxiety | Inertia | Sum | Verdict |
|---|-----|------|------|---------|---------|-----|---------|

### Feature-to-Job Matrix

| Фича | Job 1 | Job 2 | Job 3 | Job 4 | Job 5 | Orphan? |
|------|-------|-------|-------|-------|-------|---------|

### Findings

1. **Сильные связи** — фичи которые точно бьют в Job
2. **Слабые связи** — фичи где связь натянута
3. **Orphan фичи** — не привязаны ни к одному Job → кандидаты на вырезание
4. **Незакрытые Jobs** — важные Jobs без фич → gap в спеке
5. **Anxiety blockers** — что мешает переключению и как спека это адресует
