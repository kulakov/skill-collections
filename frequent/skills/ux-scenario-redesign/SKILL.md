---
name: ux-scenario-redesign
description: "UX+UI редизайн под целевой сценарий. Используй когда пользователь говорит 'редизайн по сценарию', 'scenario redesign', 'переделай UI под задачу', 'UX redesign', 'упрости интерфейс для'. НЕ используй для: UX-аудита (ux-audit-rethink), frontend-разработки (frontend-design), CRO (page-cro)."
---

# UX Scenario Redesign

Redesign an interface for a **specific user scenario** with minimum friction. Not a generic audit — a targeted rebuild where every pixel serves the scenario.

## When to Use

- "User grooms 130 tasks, needs max 2 clicks per task"
- "Admin reviews 50 applications, needs to approve/reject in <3 sec each"
- "Writer processes 10 meeting notes, needs to extract insights without switching tabs"

## Inputs

- **scenario**: Who does what, how often, what's the acceptable interaction cost (REQUIRED)
- **current_ui**: Screenshot, HTML file path, or code snippet (REQUIRED)
- **pain_points**: What specifically sucks right now (OPTIONAL, user feedback)

## Methodology Stack

This skill synthesizes 5 authorities into a single evaluation-then-redesign pipeline:

### 1. Nielsen's 10 Heuristics (filter: which are violated by THIS scenario)

Only evaluate heuristics relevant to the scenario. Skip irrelevant ones.

| # | Heuristic | Scenario relevance test |
|---|-----------|------------------------|
| H1 | Visibility of system status | Is user waiting or uncertain? |
| H2 | Match real world | Does terminology confuse this user? |
| H3 | User control & freedom | Can user undo/escape easily? |
| H4 | Consistency & standards | Are patterns broken within the flow? |
| H5 | Error prevention | What errors are likely in this scenario? |
| H6 | Recognition over recall | Does user need to remember anything? |
| H7 | Flexibility & efficiency | Are there shortcuts for repeat use? |
| H8 | Aesthetic & minimalist design | What can be REMOVED without loss? |
| H9 | Help users with errors | When it breaks, is recovery obvious? |
| H10 | Help & documentation | Does user need instructions? |

### 2. Norman's 7 Principles (The Design of Everyday Things)

| Principle | Question for scenario |
|-----------|---------------------|
| Discoverability | Can user find the action without scanning? |
| Feedback | Does every action produce visible result? |
| Conceptual model | Does the UI match user's mental model of the task? |
| Affordances | Do interactive elements look interactive? |
| Signifiers | Is it clear WHERE to click/tap? |
| Mapping | Do controls relate logically to their effects? |
| Constraints | Does the UI prevent wrong actions? |

### 3. Yablonski's Laws of UX (psychology-backed, quantifiable)

Apply the 5 most impactful laws to the scenario:

- **Fitts's Law**: Time to target = f(distance, size). Make primary actions LARGE and CLOSE to cursor starting position.
- **Hick's Law**: Decision time = f(number of choices). Fewer visible options = faster decisions. Progressive disclosure.
- **Miller's Law**: Working memory holds 7 +/- 2 chunks. Group related items, don't exceed 5-7 visible options.
- **Jakob's Law**: Users spend most time on OTHER sites. Match conventions they already know.
- **Doherty Threshold**: Productivity soars when system responds < 400ms. Perceived speed matters.

Secondary laws (apply when relevant):
- **Pareto Principle**: 80% of use comes from 20% of features. Optimize the 20%.
- **Peak-End Rule**: Users judge experience by its peak and end. Nail the last interaction.
- **Von Restorff Effect**: Visually distinct items are remembered. Make the primary CTA stand out.
- **Tesler's Law**: Complexity is conserved — move it from user to system.
- **Postel's Law**: Be liberal in what you accept, strict in what you produce.

### 4. Krug's "Don't Make Me Think" (practical ruthlessness)

- **Self-evident > self-explanatory > needs explanation**. If it needs a label, it's not obvious enough.
- **Eliminate happy talk** (text no one reads).
- **Reduce noise** by 50%, then reduce again.
- **Omit needless clicks**. Every click costs trust.
- **The trunk test**: Can user answer "where am I, what are my options, what's the main action?" in 3 seconds?

### 5. Weinschenk's "100 Things Every Designer Needs to Know About People"

Key applicable principles:
- People scan, they don't read. Design for F-pattern scanning.
- People can only remember 3-4 items at a time (not Miller's 7 — updated research).
- People are motivated by autonomy, mastery, purpose (Deci & Ryan SDT).
- The brain processes visuals 60,000x faster than text. Replace labels with icons where unambiguous.
- People expect things to be close together if they're related (Gestalt proximity).

---

## Procedure

### Step 1: Scenario decomposition (2 min)

Parse the scenario into:
```
WHO: [user type, expertise level, frequency of use]
TASK: [what they need to accomplish]
VOLUME: [how many items/repetitions per session]
BUDGET: [max acceptable clicks/seconds per item]
FREQUENCY: [daily/weekly/monthly — affects learnability vs discoverability tradeoff]
```

If user is a **power user doing repetitive task** (daily + high volume):
- Optimize for EFFICIENCY over DISCOVERABILITY
- Keyboard shortcuts > mouse
- Progressive disclosure aggressive
- Learn curve acceptable

If user is **occasional user** (monthly + low volume):
- Optimize for DISCOVERABILITY over EFFICIENCY
- Labels > icons
- Everything visible
- Zero learning curve

### Step 2: Measure current interaction cost (3 min)

Count for the target scenario:
- **Clicks** to complete one cycle
- **Eye movements** (how many areas user must scan)
- **Decisions** (Hick's Law: how many choices at each step)
- **Memory load** (what must user remember between steps)
- **Context switches** (scrolling, tab changes, modal opens)

Output: `Current cost: X clicks, Y decisions, Z eye-scan zones`

### Step 3: Apply methodology stack (5 min)

For each law/principle violated, note:
```
[LAW]: [violation] → [fix] → [clicks saved]
```

Only list violations that affect THIS scenario. Skip irrelevant ones.

### Step 4: Generate redesign (output)

Output a concrete redesign with:

1. **Interaction budget**: `Target: N clicks, M decisions per cycle`
2. **Layout wireframe** (ASCII or description)
3. **What was REMOVED** (Krug: reduce by 50%)
4. **What was MOVED** to progressive disclosure
5. **What was ADDED** (keyboard shortcuts, auto-save, smart defaults)
6. **Code changes** — actual HTML/CSS/JS edits to implement

### Step 5: Before/After scorecard

```
| Metric              | Before | After | Improvement |
|---------------------|--------|-------|-------------|
| Clicks per cycle    |        |       |             |
| Decisions per cycle |        |       |             |
| Visible elements    |        |       |             |
| Eye-scan zones      |        |       |             |
| Time per cycle (est)|        |       |             |
```

---

## Output Format

```markdown
## Scenario
[parsed scenario]

## Current Cost
[clicks, decisions, scan zones]

## Violations Found
- [LAW]: [violation] → [fix] → [saving]

## Redesign
[wireframe + explanation]

## Code Changes
[actual edits]

## Scorecard
[before/after table]
```

## Key Principles

1. **Scenario-first**: Every decision justified by the scenario, not aesthetics
2. **Measure before/after**: No vague "improved UX" — count clicks
3. **Subtract before adding**: Remove > hide > rearrange > add
4. **Power users get shortcuts**: Don't dumb down for imaginary beginners
5. **Ship the 80%**: Perfect is the enemy of usable

## References

- Jakob Nielsen — 10 Usability Heuristics (1994, refined 2020)
- Don Norman — The Design of Everyday Things (1988, revised 2013)
- Jon Yablonski — Laws of UX (2020, 2nd ed 2024) — lawsofux.com
- Steve Krug — Don't Make Me Think (2000, revisited 2014)
- Susan Weinschenk — 100 Things Every Designer Needs to Know About People (2011, 2nd ed 2020)
- Steve Portigal — Interviewing Users (2013, 2nd ed 2023)
- Raluca Budiu / NN/g — The UX Reckoning 2025
