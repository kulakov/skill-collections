---
description: "Создание выразительных фронтенд-интерфейсов с высоким качеством дизайна. Используй когда пользователь говорит 'сделай красивый UI', 'distinctive frontend', 'не generic AI слоп', 'полированный интерфейс', 'premium web component'. Прокси к frontend-design. НЕ используй для: лендингов (l-d-landing, l-d-vibe-landing), презентаций (l-d-slides), генерации картинок (nanobanana)."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
---

Use the frontend-design skill to create this interface.

**User request**: $ARGUMENTS

Apply the frontend-design skill principles:
1. Choose a BOLD aesthetic direction (not generic AI aesthetics)
2. Use distinctive typography (avoid Inter, Roboto, Arial)
3. Create cohesive color schemes with dominant colors and sharp accents
4. Add meaningful animations and micro-interactions
5. Design with intentionality - every choice should be deliberate

Before coding, briefly describe your design concept and aesthetic direction.

---

## Компонентная база — не выдумывать примитивы

Перед генерацией интерфейса подними shadcn MCP в папке проекта, чтобы брать компоненты
из реестра, а не сочинять их (первая итерация иначе выглядит нейросетевой):

```bash
npx shadcn@latest mcp init --client claude   # затем перезапуск и /mcp для проверки
```

Поверх базы — библиотеки-референсы. Порядок: shadcn/ui (база) → Unlumen UI
(https://ui.unlumen.com/ — плавность и микровзаимодействия, ставится тем же shadcn CLI:
`npx shadcn@latest add @unlumen-ui/[name]`) → Magic UI / Aceternity (вау-эффекты)
→ Page UI (готовые секции).

Полный справочник с составом и ценами:
`~/10-CLAUDE/ui-component-library.md`, секции «Стартер-пак» и 14.

Библиотека — источник блоков, а не замена дизайну: типографика, палитра и композиция
по-прежнему на тебе.
