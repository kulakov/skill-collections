# Launch Stage

## Цель стадии

Если MVP stage был про **proving your product deserves to exist**, Launch stage — про **proving your business deserves to grow**.

**Turn early traction into repeatable, sustainable growth engine.** Beyond making продукт production-ready — harden infrastructure underneath, и одновременно build an actual company around your product.

Стартапы естественно founder-centric во время Idea и MVP — нужна full situational awareness и tight feedback loops. Сейчас фаундер, который ещё пытается лично hold каждую нить — становится Launch stage bottleneck.

**Цель не в том, чтобы remove себя из компании, а build operational systems that free your attention для decisions, которые only фаундер может make.**

## Exit criteria

Три элемента:

1. **Growth is repeatable and channel-driven.** Не просто retaining users — acquiring them predictably через specific channels с understood unit economics: **CAC, LTV, payback period** — numbers you know и can defend.

2. **Product can handle production workloads.** Infrastructure hardened, security и compliance в порядке, reliability holds под real production conditions (не только conditions, под которые tested).

3. **Operations run without founder bottlenecks.** Processes exist и automation in place. Ты уже не the person personally handling support, triage, sprint planning, или reporting.

---

## Ловушки этой стадии

### Technical debt comes due

MVP codebase built для скорости и валидации работал хорошо enough чтобы prove продукт worked, **но production traffic, new features, и growing complexity now exposing the shortcuts**.

На MVP, accumulating некоторый tech debt — reasonable tradeoff для velocity. В Launch phase, тот debt **starts accruing interest**, и чем дольше unaddressed — тем дороже to fix.

**Решение:** systematic architectural audit — identify structural weaknesses, targeted refactoring чтобы address worst of them, и meaningful expansion test coverage, чтобы next round feature work не reintroduce same problems.

### The founder becomes the bottleneck

На MVP, founder being в every loop — asset. На Launch, as support volume grows, product decisions stack up, и operational complexity multiplies — same instinct becomes constraint.

Transition с **doing the work** на **designing the systems that do the work** — один из hardest shifts в startup lifecycle. Rarely clear moment когда happens; risk — miss it entirely и stay в builder mode пока organization stalls around you.

**Telltale signs:**
- Decisions, которые должны take час, теперь take неделю — пока тебя обходят
- Support requests pile up, потому что только ты знаешь answer
- Operational tasks happen только когда ты personally remember to do them

**Remedy:** all-out audit всего, что лично handle, от tiniest задачи до highest-stakes decisions. Что systematized, что delegated, что genuinely still merits founder time и attention.

### Security и compliance больше нельзя откладывать

Keeping security и compliance simple было OK для MVP. Сейчас, с real users, real data, и потенциально enterprise contracts на столе — становится liability.

На MVP, с handful of beta users и no sensitive data в production, security vulnerabilities были theoretical risks. **Hypothetical, однако, становится very real exposure risk** the moment product enters production with real users depending on it.

Furthermore, compliance requirements, которые не applied to prototype, **definitely apply** the moment handling customer data, processing payments, или selling в regulated industries.

**Remedy:** systematic security и compliance review **до того, как production scale arrives**, не после. Treat everything that surfaces как required remediation — не suggestion — перед next wave users.

### Expansion before you're ready

New markets и funding opportunities выглядят как growth opportunities. Они также **могут быть где PMF goes to die**.

Initial traction real — но **specific to your early audience**. Expanding too early в market, который meaningfully different от original, introduces new user behaviors, compliance requirements, payment infrastructure, и baseline expectations, **под которые продукт не был designed around**.

Suddenly too many new variables — теряешь ability интерпретировать собственные данные clearly. Также run risk neglecting original user base chasing new и unproven audience.

---

## Упражнения

### Упражнение 1 — Technical debt remediation

**Цель:** systematic pass через codebase в search of any technical debt, который мог become structural liability.

**Как:**
- Direct Claude Code run full architectural audit:
  - Identify где codebase brittle
  - Shortcuts, которые станут expensive to maintain
  - Test coverage thin enough, что next round feature work will reintroduce same problems
- Feed audit findings обратно в Claude (Chat/Cowork) — triage и sequence:
  - Что fix до next release
  - Что can wait sprint
  - Что represents acceptable ongoing debt given current stage

**Documentation moment:** decisions, которые жили в head во время MVP (потому что не было времени write them down) — теперь в CLAUDE.md, чтобы каждая future Claude Code сессия starts с shared understanding системы.

### Упражнение 2 — Founder attention audit

**Цель:** identify exactly где attention going, чтобы build systems, которые it free.

**Как:**
- Claude Cowork runs structured audit current operational load:
  - Document every recurring task
  - Every decision что lands на твоём столе
  - Каждый workflow, который happens только потому что ты personally remember
- Claude Cowork categorizes inventory:
  - Что can be **automated entirely**
  - Что needs **human но not necessarily you**
  - Что genuinely **requires founder judgment**

- Для automation candidates: design workflow logic — что triggers, decision rules, output, куда goes when done
- Claude Cowork builds и runs the operational layer:
  - Scheduling sprint ceremonies
  - Routing incoming bug reports
  - Compiling weekly metrics
  - Maintaining feedback loop user signals → product decisions

### Упражнение 3 — Security & compliance как product workstream

**Не one-time project — continuous workstream.**

**Как:**
- Claude Code surfaces code-level issues, которые frequently come up в SOC 2 / GDPR / HIPAA audits (применимых стандартах для target market)
- Surface vulnerabilities AND compliance gaps
- Claude помогает prioritize remediation и design:
  - Controls
  - Audit logging
  - Access management
- **Note:** AI scans — aid, не substitute для qualified compliance review

- Build compliance workstream в development cycle:
  - Documentation needs continuous maintenance
  - Не just one-time
- Для approaching enterprise contracts / international markets: Claude Code security scan + independent security assessment prep

**Exercise:** code-level security review с Claude Code oriented под frameworks, которые target market requires. Output → Claude → sequence:
- Prioritized security remediation sequence
- Documentation и controls list для compliance review prospective enterprise buyer

### Упражнение 4 — Build product management OS

Launch требует **lightweight repeatable processes**, которые run без founder intervention to trigger.

**Как:**
- Claude designs:
  - Product timeline и work cycle structure
  - Spec template (что spec needs to include)
  - Bug report triage и routing
  - Weekly metrics report (what covers, how distributed)

- Claude Cowork implements и runs operational elements:
  - Scheduling
  - Routing
  - Report compilation
  - Не дожидаясь founder triggering

**Exercise:** Claude designs lightweight product management OS — defined sprint cadence, minimum spec template, bug triage decision tree, weekly metrics brief that pulls from actual data sources. Затем set up Claude Cowork to implement и run system's recurring operational elements.

### Упражнение 5 — Channel-driven growth (если ещё не репликабельно)

**Если рост organic / founder-driven:** время структурировать.

**Как:**
- Claude Cowork:
  - Market segmentation analysis
  - Messaging architecture для each segment
  - Tactical execution layer: content pipelines, outbound sequences, analyst briefings, newsroom + PR cadences, CRM hygiene, pipeline reporting
- Claude Code строит product marketing infrastructure:
  - Interactive demo environments
  - Integration documentation
  - Sandbox tenants
  - API references
  - Technical one-pagers

**Цель:** GTM motion runs asynchronously — well-built demo environment closes deals пока ты в board meetings.

---

## Сквозной принцип Launch stage

**All three forms of Claude are in full use** на этой стадии, supporting друг друга: каждый tool produces outputs, которые become inputs для других двух. Результаты compound organically — фаундер using all three получает **more than the sum of their parts**.

Это что makes ultra-lean startup model **structurally possible**:
- **Claude Code** builds the product
- **Claude Cowork** builds the company around it
- **Claude** operationalizes product и organizational knowledge

Small team может run like company **N× its size**.

Когда exit criteria все выполнены — переход в Scale.
