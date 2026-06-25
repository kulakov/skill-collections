---
name: ux-audit-rethink
description: "Комплексный UX-аудит по 7 факторам IxDF, 5 характеристикам юзабилити, 5 измерениям взаимодействия, 12 Laws of UX (Hick's, Fitts's, Miller's, Jakob's, Doherty, Peak-End, Von Restorff, Serial Position, Aesthetic-Usability, Tesler's, Postel's, Zeigarnik), Gestalt-принципам, и Liz Lerman Critical Response Process. С severity scoring. Используй когда пользователь говорит 'UX audit', 'UX аудит', 'проверь юзабилити', 'usability review', 'оцени UX', 'cognitive check', 'когнитивный аудит', 'Laws of UX', 'design critique', 'Liz Lerman'. НЕ используй для: CX по Руденко (l-cx-rudenko), редизайна по сценарию (ux-scenario-redesign), CRO лендинга (page-cro)."
---

# UX Audit and Rethink

This skill enables AI agents to perform a **comprehensive, holistic UX audit** based on the Interaction Design Foundation's methodology from "The Basics of User Experience Design". It evaluates products across multiple dimensions and proposes strategic redesign recommendations.

Unlike focused evaluations (Nielsen, WCAG, Don Norman), this skill provides a **360-degree UX assessment** combining factors, characteristics, dimensions, and research techniques into a unified framework.

## When to Use This Skill

Invoke this skill when:
- Conducting initial comprehensive UX assessment
- Evaluating overall product-market fit from UX perspective
- Making strategic product decisions
- Assessing all dimensions of user experience holistically
- Preparing for product redesign or pivot
- Benchmarking against UX best practices
- Creating UX improvement roadmap

## Inputs Required

- **app_description**: Detailed description (purpose, target users, key features, platform) [REQUIRED]
- **screenshots_or_links**: Screenshots, wireframes, prototypes, or live URLs [OPTIONAL but highly recommended]
- **user_feedback**: Existing reviews, complaints, support tickets [OPTIONAL]
- **target_goals**: Specific UX objectives [OPTIONAL]

## The IxDF UX Framework

### Framework 1: The 7 Factors Influencing UX (Peter Morville's Honeycomb)

1. **Useful** - Does it solve real user problems?
2. **Usable** - Is it easy to use and navigate?
3. **Findable** - Can users find content and features?
4. **Credible** - Does it inspire trust?
5. **Desirable** - Is it aesthetically appealing and emotionally engaging?
6. **Accessible** - Is it usable by people with disabilities?
7. **Valuable** - Does it deliver value to users and business?

### Framework 2: The 5 Usability Characteristics (ISO 9241-11)

1. **Effectiveness** - Can users achieve their goals accurately?
2. **Efficiency** - Can users complete tasks quickly with minimal effort?
3. **Engagement** - Is the interface pleasant and satisfying?
4. **Error Tolerance** - Can users prevent and recover from errors?
5. **Ease of Learning** - Can new users learn quickly?

**Formula**: Utility (right features) + Usability (easy to use) = **Usefulness**

### Framework 3: The 5 Dimensions of Interaction Design (Crampton Smith & Silver)

1. **Words** - Labels, instructions, microcopy
2. **Visual Representations** - Icons, images, typography, graphics
3. **Physical Objects/Space** - Input devices, touch, screen size
4. **Time** - Animations, transitions, loading, responsiveness
5. **Behavior** - Actions, reactions, feedback mechanisms

### Framework 4: Laws of UX (Cognitive Audit Layer — see `references/cognitive-check.md`)

Apply these when evaluating cognitive load and decision architecture. Each one is a check, not a rule — note where the interface aligns or deviates and why.

| Law | Check |
|-----|-------|
| **Hick's Law** | How many choices simultaneously? Progressive disclosure used? |
| **Fitts's Law** | Primary actions large + near focus? Destructive distant from constructive? Mobile targets ≥44pt? |
| **Miller's Law** | More than 4-7 items without chunking? |
| **Jakob's Law** | Follows platform/industry conventions? Are deviations justified? |
| **Doherty Threshold** | Interactions respond within 400ms? Delays masked with feedback? |
| **Peak-End Rule** | What is the emotional peak? The final moment? Both deliberately designed? |
| **Von Restorff Effect** | Most important element visually stands out? Distinctiveness used strategically? |
| **Serial Position** | Most important items first and last in lists/menus? |
| **Aesthetic-Usability** | Is visual polish masking usability problems? |
| **Tesler's Law** | Complexity reduced as far as possible without removing essential function? |
| **Postel's Law** | Liberal in what input is accepted? Forgiving formatting? |
| **Zeigarnik Effect** | Incomplete tasks creating productive engagement or anxiety? |

**Gestalt principles** (also in cognitive audit): Proximity, Similarity, Closure, Continuity, Figure-Ground, Common Region.

### Framework 5: Liz Lerman Critical Response Process (Design Critique Layer — see `references/design-critique.md`)

When user asks for a **design critique** (vs. pure audit), use Lerman's 4-step process:
1. **Statements of Meaning** — what works well, what stands out positively (protect during iteration)
2. **Designer's Questions** — address designer's specific concerns first
3. **Neutral Questions** — clarify design intent before judgment ("I notice X — what informed that?")
4. **Permissioned Opinions** — observations tied to evidence and heuristics, not preference

Score critique across 10 dimensions (1-10 each): Clarity, Consistency, Hierarchy, Efficiency, Accessibility, Emotional Design, Error Resilience, Cognitive Load, Aesthetic Quality, Innovation.

## Severity Scoring (replaces flat P0-P3 priorities)

For each finding, calculate Severity = Impact × Frequency × Persistence (1-5 each, max 125):

| Score | Severity | Action |
|-------|----------|--------|
| 75-125 | **Critical** | Block ship until fixed |
| 50-74 | **High** | Fix in current sprint |
| 25-49 | **Medium** | Fix in next release |
| 10-24 | **Low** | Backlog |
| 1-9 | **Cosmetic** | Polish pass |

Then check **fixability**: easy/medium/hard. A medium-severity easy fix beats a high-severity hard fix in next-sprint prioritization.

## Audit Procedure

### Step 1: Context Analysis
- Review app_description, identify primary purpose, target users, key journeys
- Create 2-3 provisional personas if not provided
- Document assumptions and constraints

### Step 2: Evaluate 7 UX Factors (rate each 1-5)
For each: Strengths, Gaps, Evidence, Rating with criteria

### Step 3: Assess 5 Usability Characteristics (rate each 1-5)
For each: Metrics, Issues Found, Specific examples

### Step 4: Review 5 Interaction Design Dimensions
For each: Evaluate specific elements, document issues

### Step 5: Apply UX Research Techniques
- Expert Review (heuristic evaluation)
- Recommend user interviews, usability testing, card sorting, A/B tests

### Step 6: Identify Issues and Prioritize
Create prioritized issue list:
- **P0 (Critical)**: Blocks users, fix immediately
- **P1 (High)**: Major friction, fix in current sprint
- **P2 (Medium)**: Annoyance, fix in next release
- **P3 (Low)**: Nice-to-have, backlog

Each issue: Frameworks Violated, User Impact, Business Impact, Severity, Effort, Recommendation

### Step 7: Propose Rethink and Redesign
Using Design Thinking: Empathize -> Define -> Ideate -> Prototype -> Test
For each proposal: Current Issues, Proposed Solution, Expected Impact, Effort

## Scoring

- 7 UX Factors: 35 points max
- 5 Usability Characteristics: 25 points max
- 5 Interaction Dimensions: 25 points max
- **Total**: 85 points

**Grading:**
- 85-75: A (Excellent)
- 74-65: B (Good)
- 64-55: C (Acceptable)
- 54-45: D (Poor)
- 44-0: F (Critical)

## Output Format

```markdown
# UX Audit Report
**Product**: [Name]
**Score**: [X/85] ([Grade])

## Executive Summary
[3-5 key findings + top 3 priorities]

## Scores
| Framework | Score | Grade |
|-----------|-------|-------|
| 7 UX Factors | X/35 | |
| 5 Usability | X/25 | |
| 5 Interaction | X/25 | |
| **Total** | **X/85** | **[Grade]** |

## Critical Issues (P0)
[Issue, Impact, Fix]

## High Priority (P1)
[Issue, Impact, Fix]

## Redesign Proposals
[Proposal with wireframe description, expected impact, effort]

## Next Steps
[Phased implementation roadmap]
```

## Best Practices

1. Be Evidence-Based: Support ratings with observations
2. Think Holistically: Consider all frameworks together
3. Prioritize Ruthlessly: High-impact, feasible improvements first
4. Be Actionable: Specific recommendations, not vague suggestions
5. Consider Context: Mobile vs desktop, user types, constraints
6. Measure Impact: Define success metrics before implementing

**References**: IxDF, Peter Morville (Honeycomb), ISO 9241-11, Crampton Smith & Silver, Jakob Nielsen
