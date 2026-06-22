---
description: "Добавление нового стиля в библиотеку стилей изображений. Используй когда пользователь говорит 'добавь стиль', 'add style', 'сохрани стиль', 'новый стиль в библиотеку', 'запомни этот стиль'. Из картинки или описания. НЕ используй для: стилей слайдов (l-s-slide-add), просмотра библиотеки (browse-styles, l-b-s), применения стиля (l-s-use)."
---

# Add Style to Library

Add a new style to the global style library.

## Arguments
- `$ARGUMENTS` - Can be:
  - Path to an image file (to extract style from)
  - A prompt/style description
  - Empty (to save the most recently used prompt)

## Instructions

The style library is located at:
`~/.claude/style-library.html`

Thumbnails go to:
`~/.claude/style-library-thumbnails/`

### Workflow:

1. **Determine input type:**
   - If `$ARGUMENTS` is a file path → extract style using `style_extract.py`
   - If `$ARGUMENTS` is a prompt → use it directly
   - If empty → ask user what to add

2. **If extracting from image:**
   ```python
   import sys
   sys.path.insert(0, '/Users/lance/Documents/claude-code-course/lesson-modules/3-nano-banana')
   from style_extract import extract_style
   style_description = extract_style('IMAGE_PATH')
   ```

3. **Read current library** to find:
   - Next available ID number
   - CATEGORIES array
   - CANONICAL_TAGS object

4. **Ask user for:**
   - Style name (suggest one based on the prompt)
   - Category (from CATEGORIES)
   - Tags (from CANONICAL_TAGS for that category, 2-4 tags)

5. **Generate a sample image** using the style to create a thumbnail:
   ```python
   import sys
   sys.path.insert(0, '/Users/lance/Documents/claude-code-course/lesson-modules/3-nano-banana')
   from image_gen import generate
   # Generate a sample that showcases the style
   ```

6. **Copy thumbnail** to the thumbnails folder with kebab-case name

7. **Add entry to styles array** in the HTML file:
   ```javascript
   {
     id: NUMBER,
     name: "Style Name",
     category: "Category",
     tags: ["tag1", "tag2"],
     thumbnail: "thumbnails/filename.png",
     prompt: `The style prompt here`,
     exampleUse: "When to use this style"
   }
   ```

8. **Confirm** and tell user to refresh browser

### Important Rules:
- Only use tags from CANONICAL_TAGS
- Only use categories from CATEGORIES
- Style prompts should describe VISUAL style, not specific content
- Keep prompts reusable with [subject] placeholders
