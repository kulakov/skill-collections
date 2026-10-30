#!/bin/bash
# Integrity check for Granola ROUTING.md — verifies every handler resolves on disk.
# Usage: bash check.sh   (reads the canonical ROUTING.md)
set -uo pipefail

VAULT="~"
ROUTING="$VAULT/00-INBOX/_granola/ROUTING.md"
TEAMS="$VAULT/11-TRACKER/teams"
RECIPES="$VAULT/09-REFERENCE/my-promts/granola-recipes"
SKILLS="$HOME/.claude/skills"
CMDS="$HOME/.claude/commands"
PROJ_CMDS="$VAULT/.claude/commands"
PROJ_SKILLS="$VAULT/.claude/skills"

ok=0; warn=0
say()  { printf "%s\n" "$1"; }
pass() { printf "  ok  %s\n" "$1"; ok=$((ok+1)); }
fail() { printf "  ×   %s\n" "$1"; warn=$((warn+1)); }

[ -f "$ROUTING" ] || { echo "× ROUTING.md not found at $ROUTING"; exit 1; }

# Only scan the rules table rows (lines beginning with "| <digit>")
RULES=$(grep -E '^\| *[0-9]+ *\|' "$ROUTING")

say "== track debrief → команды =="
echo "$RULES" | grep -oE 'track debrief [a-zA-Z0-9_-]+' | sort -u | while read -r _ _ team; do
  if [ -f "$TEAMS/$team/STATE.md" ]; then pass "team '$team' (STATE.md есть)"; else fail "team '$team' — нет $TEAMS/$team/STATE.md"; fi
done

say "== рецепты =="
echo "$RULES" | grep -oE 'рецепт `[0-9]{2}-[a-zA-Z-]+`' | tr -d '`' | sed 's/рецепт //' | sort -u | while read -r r; do
  if [ -f "$RECIPES/$r.md" ]; then pass "recipe '$r'"; else fail "recipe '$r' — нет $RECIPES/$r.md"; fi
done

say "== скил-обработчики =="
for s in l-w-redaktor l-g-call insight-distill; do
  if echo "$RULES" | grep -q "$s"; then
    if [ -d "$SKILLS/$s" ] || [ -f "$SKILLS/$s/SKILL.md" ] || [ -d "$PROJ_SKILLS/$s" ] || [ -f "$CMDS/$s.md" ] || [ -f "$PROJ_CMDS/$s.md" ]; then
      pass "skill '$s'"
    else
      fail "skill '$s' — не найден в skills/commands"
    fi
  fi
done

say "== режимы =="
bad_modes=$(echo "$RULES" | awk -F'|' '{m=$6; gsub(/[* ]/,"",m); if (m!="" && m!="AUTO" && m!="AUTO·safe" && m!="ASK" && m!="SKIP") print m}')
if [ -z "$bad_modes" ]; then pass "все режимы валидны"; else fail "неизвестные режимы: $bad_modes"; fi

say "== дубли паттернов =="
dups=$(echo "$RULES" | awk -F'|' '{print $3}' | sed 's/^ *//;s/ *$//' | sort | uniq -d)
if [ -z "$dups" ]; then pass "дублей нет"; else fail "дублирующиеся паттерны: $dups"; fi

say ""
say "ИТОГО: ok=$ok  проблем=$warn"
[ "$warn" -eq 0 ] && exit 0 || exit 2
