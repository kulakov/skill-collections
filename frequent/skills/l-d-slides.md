---
description: "Генератор HTML-презентаций из markdown. Используй когда пользователь просит сделать презентацию, слайды, доклад в HTML, говорит 'сделай слайды', 'create slides', 'HTML presentation', 'l-d-slides'. НЕ используй для: PPTX (pptx), сториз (l-k-stories), старого генератора (l-d-slides-old)."---. Выход: один HTML-файл с навигацией (стрелки, клик, свайп). НЕ используй для: генерации картинок (/nanobanana), PowerPoint файлов (/pptx), проверки композиции слайдов (/l-s-slide-check), подгонки контента (/l-s-slide-fit), добавления нового стиля (/l-s-slide-add)."
aliases:
  - l-slides
---

# Generate HTML Presentation from Markdown (v2)

Generate beautiful HTML slide presentations using the extended Slide Style Library with full template support.

## Arguments
- `$ARGUMENTS` - Can be:
  - A markdown file path
  - A style number (e.g., `#3` or `3`)
  - A style number + file path (e.g., `3 /path/to/content.md`)
  - "compare" or "10 styles" to generate comparison page
  - Empty (interactive mode)

## Key Locations

**Template Library:** `/Users/lance/lance-claude/slide-templates-full.json`
**Style Browser:** `~/.claude/style-library.html` (open → Slides tab)

## Workflow

### 1. Read Template Library

Read `/Users/lance/lance-claude/slide-templates-full.json` which contains:
- 15 complete slide styles
- Multiple template types per style: `title`, `content`, `quote`, `section`, `closing`, `data`, `twoColumn`, `code`, `terminal`, `cta`
- Full CSS for each style (embedded in templates)

### 2. Parse Arguments

- Extract style number if provided (with or without #)
- Extract file path if provided
- Detect "compare" / "10 styles" mode

### 3. Get Content

- If file path provided: read markdown file
- If no file: ask user for content or markdown file path
- Parse markdown into slides using `---` as separator

### 4. Choose Mode

**Mode A: "Compare 10 styles"** (when user says "compare", "10 styles", "show styles")
- Pick 10 diverse styles (at least one from each category)
- Take the first slide's content (title slide)
- Generate a single `style-comparison.html` file with a 2x5 grid
- Each cell: style's title template with the content
- Label each cell with `#ID - Style Name (Category)`
- Open in browser
- Ask user: "Which style? Tell me the number."

**Mode B: "Specific style"** (when user provides a style number)
- Read the style from library by ID
- Generate the full presentation using mode 5

**Mode C: "Recommend"** (default when no style specified and not comparing)
- Analyze the markdown content
- Suggest top 3 styles with reasoning
- Ask user to pick one

### 5. Generate Full Presentation

When style is selected:

#### Step 1: Parse Markdown into Slides

Split by `---` separator. For each slide, analyze content to determine type:

```
FIRST SLIDE → type: "title"
  Extract: title (# heading), subtitle (first paragraph)

SLIDE starting with > → type: "quote"
  Extract: quote text, author (from — attribution)

SLIDE with only ## heading + short text → type: "section"
  Extract: heading, optional label

SLIDE with numbers/metrics (%, $, x faster) → type: "data"
  Extract: heading, metrics array

SLIDE with ## heading + bullet list → type: "content"
  Extract: heading, bullets array

SLIDE with code block ``` → type: "code"
  Extract: heading, code content

LAST SLIDE (if has CTA words: contact, reach, thank) → type: "closing"
  Extract: heading, text, contact info

DEFAULT → type: "content"
```

#### Step 1b: Content Sizing (fit content to viewport)

The slide is a **fixed 100vw x 100vh viewport**. Content must fill it (80-95%), not cluster in the center.

**Classify each slide by density:**

| Density | Content signals | Action |
|---------|-----------------|--------|
| **Sparse** | 1 heading + 0-1 short lines | Scale heading UP (60-72px), add vertical centering |
| **Normal** | 1 heading + 3-5 bullets OR 1 heading + 1 paragraph + 1 blockquote | Use template defaults (heading 38-44px, body 17-20px) |
| **Dense** | 1 heading + 6+ bullets OR table + blockquote OR code block + explanation | Scale body DOWN (15-16px), tighten line-height to 1.5, consider splitting |
| **Overflow** | Content height estimate > 95% viewport | MUST split into 2 slides |

**Font size ranges by slide type:**

| Slide type | Heading | Body/Bullets | Blockquote | Footer |
|------------|---------|-------------|------------|--------|
| title | 48-72px | 20-28px | — | 14-16px |
| content | 36-48px | 16-20px | 18-22px italic | 14-16px |
| quote | — | — | 28-40px | 14-16px |
| section | 48-68px | 14-18px label | — | 14-16px |
| closing | 40-56px | 17-22px | — | 14-16px |

**Heading-to-body ratio:** always >= 1.5x. If heading is 42px, body must be <= 28px.

**Quick height estimate** (assuming 1080px viewport, 70px padding top + 70px bottom = 940px usable):
- Each text line ≈ font-size x line-height (default 1.5-1.7)
- Bullet item ≈ font-size x line-height + margin-bottom (12-16px)
- Heading ≈ font-size x 1.2 + margin-bottom (20-28px)
- Blockquote ≈ lines x font-size x line-height + padding (20px)
- If total > 940px → split. If total < 560px (< 60%) → scale up.

**Content limits per slide:**
- Max 7 bullet points (prefer 5)
- Max 20 words per bullet
- Max 2 content blocks per slide (e.g., bullets + blockquote, OR table + note)
- Tables: max 4 rows + header, max 4 columns
- Code blocks: max 12 lines at 15px

#### Step 2: Apply Templates

For each slide:
1. Get slide type (from Step 1)
2. Get template HTML from `style.templates[type]`
3. If template doesn't exist for this type, fall back to `content` template
4. Substitute variables using simple string replace:
   - `{{title}}` → extracted title
   - `{{subtitle}}` → extracted subtitle
   - `{{heading}}` → extracted heading
   - `{{#bullets}}...{{/bullets}}` → loop over bullets array
   - `{{quote}}` → quote text
   - `{{author}}` → author name
   - etc.

#### Step 3: Build Final HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{presentationTitle}}</title>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Instrument+Serif&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* Reset + presentation engine */
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 100%; height: 100%; overflow: hidden; }
    .deck { width: 100%; height: 100%; }
    .slide {
      width: 100vw; height: 100vh;
      display: none;
      overflow: hidden;
    }
    .slide.active { display: flex; }
    .nav-counter {
      position: fixed; bottom: 20px; right: 20px;
      font-size: 0.75rem; z-index: 100;
      opacity: 0.5; font-family: 'JetBrains Mono', monospace;
    }
    @media print {
      .slide { display: block !important; page-break-after: always;
               width: 100%; height: auto; min-height: 100vh; }
      .nav-counter { display: none; }
    }

    /* Style-specific CSS from templates */
    {{styleCssClass}} {
      /* Insert base styles from style.cssClass */
    }
  </style>
</head>
<body>
  <div class="deck">
    {{#slides}}
    <div class="slide {{cssClass}}">
      {{slideHtml}}
    </div>
    {{/slides}}
  </div>
  <div class="nav-counter">
    <span id="current">1</span> / <span id="total">{{totalSlides}}</span>
  </div>
  <script>
    const slides = document.querySelectorAll('.slide');
    let current = 0;
    function go(n) {
      slides[current].classList.remove('active');
      current = Math.max(0, Math.min(slides.length - 1, n));
      slides[current].classList.add('active');
      document.getElementById('current').textContent = current + 1;
    }
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(current + 1); }
      if (e.key === 'ArrowLeft') go(current - 1);
      if (e.key === 'Home') go(0);
      if (e.key === 'End') go(slides.length - 1);
    });
    document.addEventListener('click', e => {
      if (e.clientX > window.innerWidth / 2) go(current + 1);
      else go(current - 1);
    });
    // Touch swipe
    let touchX = 0;
    document.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; });
    document.addEventListener('touchend', e => {
      const diff = e.changedTouches[0].clientX - touchX;
      if (Math.abs(diff) > 50) {
        if (diff < 0) go(current + 1); else go(current - 1);
      }
    });
    go(0);
  </script>
</body>
</html>
```

#### Step 4: Save and Open

- Save as `presentation.html` (or custom name based on title)
- Open in browser: `open presentation.html`

### 6. Show User

Tell user:
- Style name and ID used
- Number of slides generated
- Path to the HTML file (both markdown link and plain path)
- Navigation instructions: arrow keys, click left/right, swipe, Home/End

## Template Variable Reference

### Title Slide
- `{{title}}` - Main title
- `{{subtitle}}` - Subtitle/description
- `{{footer}}` - Footer text (optional)

### Content Slide
- `{{heading}}` - Slide heading
- `{{#bullets}}{{.}}{{/bullets}}` - Bullet points
- `{{footer}}` - Footer text (optional)

### Quote Slide
- `{{quote}}` - Quote text
- `{{author}}` - Attribution

### Section Slide
- `{{label}}` - Section label (e.g., "Part 1")
- `{{heading}}` - Section heading

### Data Slide
- `{{heading}}` - Slide heading
- `{{date}}` - Date/timestamp
- `{{#metrics}}{{label}}, {{value}}, {{delta}}, {{color}}{{/metrics}}` - Metrics array

### Code Slide
- `{{heading}}` - Code heading
- `{{code}}` - Code content
- `{{#codeLines}}{{lineNum}}, {{codeLine}}{{/codeLines}}` - Formatted code

### Terminal Slide
- `{{command}}` - Terminal command
- `{{output}}` - Command output
- `{{description}}` - Description

### Two-Column Slide
- `{{leftHeading}}` - Left column heading
- `{{leftText}}` - Left column text
- `{{rightText}}` - Right column text

### CTA/Closing Slide
- `{{heading}}` - Closing heading
- `{{text}}` - Closing text
- `{{contact}}` - Contact info
- `{{ctaText}}` - CTA button text

## Important Rules

- Output is a SINGLE self-contained HTML file
- NO external dependencies (except Google Fonts)
- Navigation: keyboard (arrows, space), mouse click, touch swipe
- Print-friendly: Cmd+P produces one slide per page
- Design must match the selected style precisely
- Adapt content intelligently to slide types
- **Content sizing: every slide must fill 80-95% of viewport** (see Step 1b)
- **Heading-to-body ratio >= 1.5x** (visual hierarchy is non-negotiable)
- Max 5-7 bullet points per content slide (prefer 5)
- Max 20 words per bullet point
- **Split overflowing slides** rather than shrinking font below minimums
- If a template type doesn't exist for a style, fall back to `content` template
- Always use the cssClass from the style for consistency

## Examples

**Generate with style #4:**
```
/l-d-slides 4 presentation.md
```

**Compare 10 styles:**
```
/l-d-slides compare presentation.md
```

**Interactive mode:**
```
/l-d-slides
```
