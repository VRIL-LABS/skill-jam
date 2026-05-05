---
name: skill-navigator
description: >
  Skill discovery and invocation guidance skill exclusively by VRIL LABS. Teaches agents the
  optimal strategy for finding the right skill in the skill-jam repository, determining when
  skills should be used during a development session, and sequencing skill invocations to
  maximize output quality while minimizing token expenditure. Invoke when an agent is uncertain
  which skill to use, when to use a skill at all, or how to discover available skills for a task.
---

# Skill Navigator

*Exclusively by VRIL LABS*

Mastery guide for finding the right skill, at the right moment, in the right sequence. Agents that use skills well produce dramatically higher-quality outputs while consuming far fewer tokens — because they offload structured reasoning to proven skill frameworks rather than re-deriving it from scratch every session. This skill teaches the full discipline of skill-aware development.

## When to Use

- Agent is uncertain which skill in the repository applies to a current task
- Agent needs to decide whether to use a skill or proceed with inline reasoning
- A new development session is beginning and the agent should orient to available capabilities
- User explicitly asks "what skills are available?" or "which skill should I use for X?"
- Agent has completed one phase of a task and needs to choose the next skill to chain
- Task quality is suffering and the agent needs to reset and re-approach with structured skill usage

## Process

### Phase 1 — Orient to the Repository

Before searching for skills, understand the skill-jam layout:

```
skill-jam/
├── skills/                ← 50 core general skills (flat kebab-case dirs)
├── featured-skills/       ← 10 VRIL LABS 3D visualizer skills
├── skills/vercel-services/  ← Vercel platform skill files
├── skills/cloudflare-services/ ← Cloudflare edge skill files
├── skills/browser-automation/  ← Browser automation skills
├── skills/dev-tools/      ← Developer tool skills
├── skills/search-research/  ← Web & research search skills
├── skills/document-processing/ ← PDF, DOCX, XLSX, PPTX skills
├── skills/security/       ← Security/safety skills
├── skills/blockchain-crypto/ ← Blockchain/crypto skills
├── skills/codebase-recon/ ← VRIL LABS: codebase reconnaissance
├── skills/skill-builder/  ← VRIL LABS: SKILL.md authoring
├── skills/skill-navigator/ ← VRIL LABS: this skill
└── .claude-plugin/marketplace.json ← Full index of all 103+ skills
```

**Fastest orientation**: read `README.md` skills table or scan `marketplace.json` for the full flat list of skill names and descriptions.

### Phase 2 — Determine Whether a Skill Is Needed

Apply this decision filter before searching for skills:

#### Use a skill when:
- The task has a **known structure** that a skill encodes (e.g., "review code" → code-reviewer, "research topic" → research-assistant)
- The task is **repetitive** across sessions and consistency matters
- The task involves **external integrations** (APIs, platforms, services) — skills encode the right endpoints, auth patterns, and rate-limit handling
- The process would take **>5 agent steps** to derive from scratch — skills compress this into a proven sequence
- The output needs a **specific format** that must be consistent across turns or agents
- The task is in a **specialized domain** (security, blockchain, 3D visualization, browser automation) where background knowledge is dense

#### Do NOT use a skill when:
- The task is a **one-liner** the agent can answer directly (e.g., "what's the capital of France?")
- **No relevant skill exists** and creating one would take more tokens than doing the work inline
- The skill's **process is overkill** for the scale of the task (e.g., running the full research-assistant process for a single factual lookup)
- The user has **explicitly scoped** the task to a simple, direct answer
- A skill would **duplicate work already done** in the current session context

### Phase 3 — Discovery: Find the Right Skill

Use this hierarchy, stopping as soon as you have a confident match:

#### Step 1 — Check the obvious categories first

| Task type | First skill to check |
|-----------|---------------------|
| Writing/reviewing code | `code-reviewer`, `code-refactorer`, `bug-diagnoser` |
| Generating tests | `test-generator` |
| Documentation | `documentation-writer` |
| CI/CD setup | `cicd-pipeline-builder` |
| Dependencies/packages | `dependency-updater` |
| Security vulnerabilities | `security-scanner`, `skills/security/prompt-guard` |
| Research a topic | `research-assistant` |
| Codebase reconnaissance | `skills/codebase-recon` |
| Web search | `skills/search-research/tavily-search` or `skills/search-research/exa-*` |
| Data analysis | `data-analyst`, `data-validator` |
| API specification | `openapi-generator`, `api-scaffolder` |
| Docker/containers | `docker-composer` |
| Git operations | `git-workflow-automator` |
| Performance | `performance-profiler`, `cache-advisor` |
| Writing a new skill | `skills/skill-builder` |
| Cloudflare deployment | `skills/cloudflare-services/*` |
| Vercel deployment | `skills/vercel-services/*` |
| Browser automation | `skills/browser-automation/*` |
| Document processing | `skills/document-processing/*` |
| Blockchain/crypto | `skills/blockchain-crypto/*` |

#### Step 2 — Scan marketplace.json descriptions

If Step 1 yields no match, read the `description` field of each skill in `.claude-plugin/marketplace.json`. The description is written to enable this exact lookup. Filter by:
- Keywords from the task (verb + noun: "generate tests", "analyze logs")
- Technology/platform: language, framework, service name
- Output type: the user's desired deliverable

#### Step 3 — Read the candidate skill's "When to Use" section

Open the `SKILL.md` of each candidate. The "When to Use" bullets are the authoritative filter. If the current task matches ≥1 bullet, the skill is applicable.

#### Step 4 — If multiple skills match, chain them

Skills are composable. Common high-performance chains:

| Goal | Chain |
|------|-------|
| Build a feature with confidence | `codebase-recon` → implement → `code-reviewer` |
| Research and document | `research-assistant` → `documentation-writer` |
| New API endpoint | `openapi-generator` → `api-scaffolder` → `test-generator` |
| Audit a codebase | `code-reviewer` → `security-scanner` → `bug-diagnoser` |
| Deploy new service | `docker-composer` → `cicd-pipeline-builder` |
| Create a new skill | `skill-navigator` → `skill-builder` |

### Phase 4 — Optimal Invocation Timing

Skills are not always most effective at the first available moment. Apply these timing rules:

#### Invoke at session start when:
- `codebase-recon` — before writing any new code; recon first saves the most tokens and rework
- `research-assistant` — when a decision requires external information before design
- `dev-environment-setup` — at the very start of a new project or onboarding session

#### Invoke mid-task when:
- `code-reviewer` — after completing a coherent chunk (function, module, PR diff), not line-by-line
- `bug-diagnoser` — when a specific error or unexpected behavior surfaces
- `security-scanner` — after the feature is functionally complete, before final review
- `test-generator` — after implementation is stable, not during early iteration

#### Invoke at task end when:
- `documentation-writer` — after the implementation is finalized
- `git-workflow-automator` — when preparing to commit, tag, or release
- `dependency-updater` — as a final sweep before shipping

#### Invoke on-demand (any time) when:
- `data-analyst`, `data-validator` — whenever structured data appears
- `text-summarizer` — whenever a long document needs to be distilled
- `language-translator` — whenever translation is needed in context

### Phase 5 — Token Efficiency Rules

Skills save tokens when used correctly. They waste tokens when misapplied.

**Token-saving patterns**:
- Invoke `research-assistant` or `codebase-recon` **once** at the start, then use the output throughout the session without re-searching
- Use `text-summarizer` on long documents **before** passing them to other skills
- Chain `openapi-generator` before `api-scaffolder` to avoid having the scaffolder re-derive the spec
- Read only the **"When to Use" and "Process" sections** of a skill for invocation decisions; read the full skill only if implementing it for the first time

**Token-wasting anti-patterns**:
- Invoking `research-assistant` multiple times on the same topic within a session
- Running `code-reviewer` on every individual file rather than the complete diff
- Using `documentation-writer` mid-task before code is stable (will need to re-run)
- Reading the full `SKILL.md` of 10 candidates before narrowing to 2–3

### Phase 6 — Output the Navigation Decision

Return a clear, concise recommendation:

```
## Skill Navigation

**Task**: [brief task description]
**Recommended skill(s)**: [skill name(s)]
**Invocation timing**: [now / after X / at task end]
**Rationale**: [1–2 sentence explanation]
**Chain**: [optional: skill A → skill B if chaining applies]
```

## Output Format

```
## Skill Navigation

**Task**: Implement a JWT authentication middleware for an Express API
**Recommended skills**:
  1. `codebase-recon` (now) — find reference implementations before coding
  2. `auth-integrator` (now) — provides the JWT/OAuth process scaffold
  3. `security-scanner` (after implementation) — validate no auth bypass patterns
  4. `test-generator` (after implementation) — generate auth edge-case tests

**Invocation timing**: Start with codebase-recon + auth-integrator in parallel;
  run security-scanner and test-generator after the feature is functionally complete.

**Chain**: codebase-recon → auth-integrator → [implement] → security-scanner → test-generator

**Rationale**: auth-integrator encodes the full OAuth/JWT process and common pitfalls.
  codebase-recon surfaces battle-tested reference implementations (passport.js, jose, etc.)
  before a single line is written. Security review and test generation at the end ensures
  the implementation matches both the reference patterns and security standards.
```

## Examples

### Example Input
```
I need to set up automated database migrations for a PostgreSQL database in our Node.js
project. Which skill(s) should I use, and when?
```

### Example Output
```
## Skill Navigation

**Task**: Automated PostgreSQL database migrations (Node.js)
**Recommended skills**:
  1. `codebase-recon` (now) — scout Flyway, golang-migrate, node-pg-migrate, Prisma Migrate patterns
  2. `backend-database` (now) — provides PostgreSQL migration process scaffold
  3. `cicd-pipeline-builder` (after migration scripts are ready) — wire migrations into the deployment pipeline
  4. `test-generator` (after) — generate migration rollback tests

**Chain**: codebase-recon → backend-database → [implement migrations] → cicd-pipeline-builder → test-generator

**Rationale**: database migrations are an area where subtle ordering and rollback bugs are
  common; studying reference implementations first (codebase-recon) and using the backend-database
  skill's structured process prevents the most frequent failure modes.
```

## Boundaries

- Do NOT recommend a skill unless its "When to Use" section explicitly covers the current task type.
- Do NOT recommend more than 4 skills for a single task — diminishing returns set in quickly.
- Do NOT recommend invoking the same skill twice in a session for the same query — use cached output.
- Do NOT use this skill to evaluate whether a skill is high quality — use the `skill-builder` skill's self-review checklist instead.
- Always include invocation timing in the recommendation — "use skill X" without timing is incomplete.
- If no skill matches the task, say so explicitly and recommend inline reasoning rather than forcing a poor fit.
- Always consider the token cost of skill discovery itself — for simple tasks, spend no more than 5 lines of reasoning on navigation before defaulting to inline.
