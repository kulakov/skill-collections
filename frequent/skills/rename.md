---
description: "Переименование сессии Claude Code. Используй когда пользователь говорит 'переименуй', 'rename', 'назови сессию', 'rename session'. НЕ используй для: сохранения контекста (l-x-save-context), TLDR (tldr)."
---

Rename current Claude Code session in VSCode.

Details: 10-CLAUDE/session-rename-howto.md

## Algorithm

1. **CRITICAL: Get session ID via $PPID** (NOT by searching cwd/entrypoint):
   ```bash
   cat ~/.claude/sessions/$PPID.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['sessionId'], d['cwd'].lstrip('/').replace('//','/').replace('//','/').replace('/','-'))"
   ```
   This returns: SESSION_ID PROJECT_DIR

   **WHY $PPID:** When multiple sessions are open for the same project, searching by cwd picks the WRONG one. $PPID is the Claude Code process that spawned this bash = always correct.

2. Name: $ARGUMENTS if provided, else ask user

3. JSONL path: ~/.claude/projects/-{PROJECT_DIR}/{sessionId}.jsonl

4. Append BOTH lines to end of JSONL via Bash:
   {"type":"custom-title","customTitle":"NAME","sessionId":"ID"}
   {"type":"ai-title","sessionId":"ID","aiTitle":"NAME"}

5. Confirm: Session renamed: NAME
   Add: Cmd+Shift+P -> Developer: Reload Window

## Rules
- **ALWAYS use $PPID** to find session -- NEVER search by cwd/entrypoint
- custom-title has priority over ai-title -- write both
- Do NOT touch sessions-index.json
- Name: 3-7 words in session's working language
