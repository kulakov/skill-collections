---
description: "Проверка композиции HTML-презентации. Используй когда пользователь говорит 'проверь слайды', 'check slides', 'композиция слайдов', 'slide review', 'аудит презентации', 'проверь типографику слайдов', 'slide composition', 'что не так со слайдами', 'почему слайд выглядит плохо', 'slide audit'. Скоркард по 6 критериям: content fill, hierarchy, CRAP, signal/chrome, typography, layout. Pipeline: l-d-slides → l-s-slide-check. НЕ используй для: подгонки контента до генерации (l-s-slide-fit), генерации презентации (l-d-slides), проверки визуализации данных (l-s-dataviz-check), извлечения шаблонов из презентации (l-s-slide-extract)."
---

# Slide Composition Check

Review an HTML presentation for composition, sizing, and typography quality. Outputs a per-slide scorecard with specific fixes.

## Arguments
- `$ARGUMENTS` - Path to HTML presentation file. If empty, ask for the path.

## Instructions

### Phase 1: Read and parse

1. Read the HTML presentation file
2. Extract all slides (elements with `data-slide` attribute or `.slide` class)
3. Read the global CSS to determine: base font-sizes, padding values, line-heights, layout classes
4. For each slide, extract: heading text, body text, images, inline style overrides, layout structure

### Phase 2: Run checks per slide

For each slide, evaluate these criteria. Score each as PASS / WARN / FAIL.

#### A. Content-to-canvas ratio (the core principle)

The slide is a fixed viewport. Content must be sized to fill it, not cluster in the center.

- **Estimate fill ratio**: calculate total content height (text lines x font-size x line-height + image heights + margins + gaps) vs available height (viewport minus padding top/bottom)
- PASS: 80-95% fill
- WARN: 60-80% (too much empty space) or 95-100% (tight, might overflow)
- FAIL: <60% (content clusters in center) or >100% (overflows)
- **Fix suggestion**: recommend specific font-size and/or line-height adjustments

#### B. Visual hierarchy (squint test)

- Check heading vs body font-size ratio. PASS if >= 1.5x. WARN if 1.2-1.5x. FAIL if <1.2x (looks like a mistake, not a hierarchy)
- Check that heading uses a different weight or color from body
- Check that there is exactly one dominant element per slide (one h1 or one large image or one statement)

#### C. CRAP principles

- **Contrast**: heading/body size ratio (see above), accent colors vs background contrast
- **Repetition**: are heading sizes consistent across slides? Are bullet styles consistent?
- **Alignment**: check for mixed alignment (some elements centered, some left-aligned on the same slide = FAIL)
- **Proximity**: check spacing between heading and its body vs spacing between sections

#### D. Signal vs chrome

- **Slide number font-size**: should be <= 16px. WARN if scaled up with content
- **Nav hint**: same check
- **Decorative elements**: flag any positioned absolute elements that aren't content (tape, ribbons, ornaments) as candidates for removal

#### E. Typography

- **Hanging prepositions** (Russian text): scan for single-char prepositions (в, с, к, о, а, и) followed by a regular space instead of `&nbsp;`. Count violations
- **Quotes**: check for straight quotes `"` in Russian text (should be `&laquo;/&raquo;`)
- **Dashes**: check for ` - ` (should be ` -- ` or em-dash `&mdash;`)
- **Trailing periods**: check for `.` at the end of the last `<p>` or `<li>` in each slide
- **Widows**: check for short last lines (single word) in paragraphs

#### F. Layout patterns

- **Flex centering on dense slides**: flag `justify-content: center` (or `.v-center` class) on slides where estimated content > 70% of available height. These should distribute content, not cluster it
- **Flex on ul**: flag any `<ul style="...display: flex...">` as a bug (breaks ::before bullets)
- **Image sizing**: flag images without explicit max-width/max-height constraints

### Phase 3: Output scorecard

Format output as:

```
SLIDE COMPOSITION CHECK: [filename]
Deck-wide: [base font-size] / [padding] / [line-height] / [slides count]

--- Slide 1: [first heading text, truncated to 40 chars] ---
  Content fill:     [PASS 87%] | [WARN 55% -- increase font-size to 32px]
  Visual hierarchy: [PASS h1:63px / p:27px = 2.3x]
  CRAP:             [PASS]
  Signal/chrome:    [PASS]
  Typography:       [WARN 3 hanging prepositions]
  Layout:           [PASS]

--- Slide 2: ... ---
  ...

SUMMARY
  Total slides: 20
  PASS: 14 | WARN: 4 | FAIL: 2
  Top issues:
    1. Slides 14, 16: content fill <60% -- need smaller font or denser line-height
    2. Slides 5, 8: no clear focal point
    3. 12 hanging prepositions across deck
```

### Phase 4: Offer to fix

After the scorecard, ask:

> Found N issues. Want me to fix them?
> - Fix all automatically
> - Fix only FAIL items
> - Show me the fixes first

If the user chooses to fix, apply changes directly to the HTML file using Edit tool. For each fix, explain what changed.

### Reference

The full production principles are documented in the Slide Style Library:
`/Users/lance/Documents/claude-code-course/lesson-modules/3-nano-banana/3.1-intro-to-image-gen/3.1.4-style-database/slide-style-library.html`
(see "Production principles for all styles" section in the header)
