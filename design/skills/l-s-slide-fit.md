---
description: "Подгонка контента под слайды до генерации HTML. Используй когда пользователь говорит 'подгони контент', 'slide fit', 'влезет ли на слайд', 'content density', 'проверь плотность слайдов', 'fit content to slides'. Анализирует markdown, оценивает fill ratio, рекомендует размеры шрифтов и split/merge. НЕ используй для: проверки готового HTML (l-s-slide-check), генерации презентации (l-d-slides), просмотра стилей (l-s-slide-browse)."
aliases:
  - l-s-slide-fit
  - slide-fit
---

# Slide Content Fit

Proactively fit markdown content to slides BEFORE generating HTML. Analyzes each slide's content density and outputs sizing recommendations + split/merge decisions.

Use this skill between writing markdown slides and generating HTML with `/l-d-slides`.

## Aliases
- `l-s-slide-fit`
- `slide-fit`

## Arguments
- `$ARGUMENTS` - Path to markdown file with slides (separated by `---`). If empty, ask for the path.

## Instructions

### Phase 1: Parse slides

1. Read the markdown file
2. Split by `---` separator
3. For each slide, extract content elements:
   - Headings (count, level)
   - Paragraphs (count, word count per paragraph)
   - Bullet lists (count of items, max words per item)
   - Blockquotes (count, word count)
   - Tables (rows x columns)
   - Code blocks (line count)
   - ASCII diagrams / pre-formatted blocks (line count)

### Phase 2: Estimate height per slide

Use this model (assuming 1080px viewport, 70px padding top + bottom = **940px usable**):

```
ELEMENT                          HEIGHT FORMULA
──────────────────────────────────────────────────
# Heading (h1)                   font-size x 1.2 + 28px margin
## Heading (h2)                  font-size x 1.2 + 24px margin
Paragraph (per line)             font-size x line-height
  - wrap: ceil(word_count / words_per_line) lines
  - words_per_line ≈ 600px / (font-size x 0.5)
Bullet item                      font-size x line-height + 14px margin
  - wrap: same as paragraph
Blockquote                       lines x font-size x line-height + 40px padding
Table row                        font-size x line-height + 16px padding
Table header                     same + 4px border
Code block line                  15px x 1.6 = 24px
Gap between sections             20-32px
```

### Phase 3: Classify density

For each slide, calculate **fill ratio** = estimated_height / 940px:

| Fill ratio | Density | Action |
|-----------|---------|--------|
| < 40% | **Empty** | Merge with adjacent slide OR scale heading to 60-72px |
| 40-60% | **Sparse** | Scale heading to 52-64px, body to 22-24px |
| 60-80% | **Light** | Scale heading to 44-52px, body to 19-21px |
| 80-95% | **Optimal** | Use template defaults (heading 38-44px, body 17-19px) |
| 95-110% | **Tight** | Reduce body to 16px, line-height to 1.45, tighten gaps |
| > 110% | **Overflow** | MUST split into 2 slides |

### Phase 4: Produce recommendations

For each slide, output one line:

```
SLIDE CONTENT FIT: [filename]
Viewport: 940px usable (1080 - 140px padding)

Slide  1 [title]   "Проблемы LARP как жан..."  SPARSE  42% → scale h1 to 64px
Slide  2 [content]  "Искусство — не артефа..."  OPTIMAL 83%
Slide  3 [content]  "Два органа художника"      LIGHT   68% → scale h1 to 48px, body to 20px
Slide  4 [content]  "Субъект ≠ Автор"           TIGHT   97% → reduce body to 16px, line-height 1.45
Slide  5 [content]  "Автор оперирует тремя..."  OVERFLOW 118% → SPLIT: move blockquote to new slide

SUMMARY
  Optimal: 8 | Light: 3 | Sparse: 2 | Tight: 1 | Overflow: 1
  Splits needed: 1 (slide 5)

INLINE SIZE HINTS (paste into markdown):
  <!-- slide-fit: h1=64px --> after slide 1 heading
  <!-- slide-fit: h1=48px body=20px --> after slide 3 heading
  <!-- slide-fit: body=16px lh=1.45 --> after slide 4 heading
  <!-- slide-fit: SPLIT --> between slide 5 content blocks
```

### Phase 5: Offer to apply

After the report, ask:

> Found N slides that need adjustment. What to do?
> - Apply inline `<!-- slide-fit -->` hints to markdown
> - Split overflow slides automatically
> - Show me the splits first
> - Do nothing (I'll use the numbers manually)

If applying hints: insert `<!-- slide-fit: key=value -->` comments after the slide's `###` heading line. These hints are consumed by `/l-d-slides` during generation (Step 1b).

If splitting: insert `---` separator at the recommended split point and create a continuation heading.

### Key Principles

1. **The slide is a fixed canvas.** Content must be sized to fill it, not the other way around.
2. **80-95% fill is the sweet spot.** Below 60% looks empty. Above 95% risks overflow.
3. **Heading-to-body ratio >= 1.5x always.** This is the visual hierarchy contract.
4. **Split > shrink.** If content overflows, splitting into 2 readable slides is better than cramming into 1 unreadable slide.
5. **Sparse is as bad as overflow.** A slide with one sentence floating in a sea of whitespace fails just as hard as an overflowing wall of text.

### Phase 6: Runtime auto-fit JS (optional)

If the user wants RUNTIME auto-scaling (content adapts to viewport dynamically), offer to inject this JS snippet into the generated HTML. This is complementary to pre-generation sizing -- it handles edge cases at render time.

```javascript
// Auto-fit: wraps slide content in .slide-inner, binary-searches max scale
(function() {
  document.querySelectorAll('.slide').forEach(function(s) {
    var inner = document.createElement('div');
    inner.className = 'slide-inner';
    Array.from(s.childNodes).forEach(function(c) {
      if (c.nodeType === 1 && c.classList.contains('s-footer')) return;
      inner.appendChild(c);
    });
    s.appendChild(inner);
  });
  function fit() {
    var all = document.querySelectorAll('.slide');
    all.forEach(function(s) { s.style.display = 'flex'; s.style.visibility = 'hidden'; });
    all.forEach(function(s) {
      var inner = s.querySelector('.slide-inner');
      if (!inner) return;
      var availH = s.clientHeight - 160; // top+bottom padding
      var availW = s.clientWidth - 200;  // left+right padding
      if (availH <= 0 || availW <= 0) return;
      var lo = 0.5, hi = 1.0; // cap at 1.0: only scale DOWN, never UP
      for (var i = 0; i < 10; i++) {
        var mid = (lo + hi) / 2;
        inner.style.width = (availW / mid) + 'px';
        inner.style.transform = 'translate(-50%,-50%)';
        if (inner.offsetHeight * mid <= availH + 1) lo = mid;
        else hi = mid;
      }
      inner.style.width = (availW / lo) + 'px';
      inner.style.transform = 'translate(-50%,-50%) scale(' + lo + ')';
    });
    all.forEach(function(s) { s.style.display = ''; s.style.visibility = ''; });
  }
  fit();
  window.addEventListener('resize', fit);
  document.fonts.ready.then(fit);
})();
```

**Required CSS** for `.slide-inner`:
```css
.slide-inner {
  position: absolute;
  top: 50%;
  left: 50%;
}
```

**When to use runtime auto-fit:**
- Presentations shown on unknown screen sizes
- Slides with dense tables or two-column layouts
- When manual sizing would take too long

**When NOT to use:**
- Print-only presentations (CSS transform breaks page layout)
- Slides with absolute-positioned overlays

### Relation to other skills

- **`/l-d-slides`** -- reads `<!-- slide-fit -->` hints during generation (Step 1b: Content Sizing)
- **`/l-s-slide-check`** -- checks the GENERATED HTML after the fact (post-hoc). This skill is PRE-generation.
- Pipeline: write markdown -> `/l-s-slide-fit` -> fix -> `/l-d-slides` -> `/l-s-slide-check` -> polish
