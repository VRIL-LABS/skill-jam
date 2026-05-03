# Claude Code — AaaS Team Workflow

Shared team configuration. Personal overrides go in your own `~/.claude/CLAUDE.md`.

## Core Philosophy

**Bias toward action.** Execute first, report after. Do not ask for permission on anything that is recoverable. Only stop for operations that are irreversible and high-impact.

---

## Hard Stops (Require Explicit Approval)

1. **Deleting 15+ files outside the project directory**
2. **Destructive SQL on non-local databases** — DROP, TRUNCATE, DELETE without WHERE on staging/production
3. **Publishing to public registries** — npm publish, cargo publish, pushing release tags
4. **Accessing or transmitting financial/credential/identity data**
5. **Creating new external accounts or OAuth app authorizations**

Everything else: execute and report.

---

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction: update `tasks/lessons.md` with the pattern
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Run tests, check logs, demonstrate correctness
- Ask yourself: "Would a staff engineer approve this?"

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: implement the elegant solution
- Skip this for simple, obvious fixes

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

---

## Decision Matrix (60/30/10)

Not everything needs an LLM. Route work to the cheapest effective handler.

| Category | Examples | Handler |
|----------|----------|---------|
| **60% Traditional** | File I/O, git ops, linting, formatting, builds | CLI tools, scripts, shell |
| **30% Rule-Based** | Task routing, token budgeting, QA gating | Hooks, scripts |
| **10% LLM-Required** | Architecture decisions, code review, debugging | Claude (subagents/direct) |

**Principle:** If a deterministic tool can do it, don't spend LLM tokens on it.

---

## Self-Critical Validation (NO FALSE POSITIVES)

- **Validate every test result:** Before reporting "green", ask: "Does this actually prove what I claim?"
- **HTTP status semantics are non-negotiable:**
  - 401/403 = auth reached, correctly rejected → TESTED
  - 200 on unauthenticated write = AUTH BYPASS → CRITICAL
  - 404 = route not found → auth NEVER REACHED → NOT TESTED
  - 500/timeout/exception = NOT a valid test result → NOT TESTED
- **False positive checklist:**
  1. "Am I testing what I think I'm testing?"
  2. "Could this pass for the wrong reason?"
  3. "If I remove the feature under test, would this still pass?"
- **When in doubt, be pessimistic.** Report unknowns as NOT TESTED, never as passed.

---

## Context Management

- **Use `/clear` between unrelated tasks** — full context reset prevents bleed-over
- **Use `/compact` within long tasks** — preserves key decisions while freeing tokens
- **When compacting, ALWAYS preserve:** modified files list, current task state, architectural decisions with rationale, active branch, unresolved blockers
- **Subagents for heavy research** — offload exploration to keep main context clean

---

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Review Before Resolve**: Final review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

---

## Engineering Laws

These three laws override all other rules:

| # | Law | Rule |
|---|-----|------|
| 1 | **Search Before Create** | Before ANY change: exhaustive search first. Glob + Grep across affected AND related modules. Extend existing code > create new files. |
| 2 | **Verify Before Claiming** | Never claim knowledge without evidence. Mark uncertain info as `[ASSUMPTION: ...]`. Research internally (codebase, docs) before external search. |
| 3 | **Triple-Verify Before Done** | After implementation: (1) COMPLETENESS — all requirements met? (2) QUALITY — patterns followed, tests green? (3) WORLD-CLASS — would a staff engineer approve this as the simplest correct solution? |

---

## Quality Mode (Session-Level)

Override per-session by saying the mode name.

| Mode | Mocks | Tests | Auth/Security | Errors |
|------|-------|-------|---------------|--------|
| `prototype` | OK | None required | No | console.log |
| `mvp` | Stubs OK | >= 40% | Auth only | Generic |
| `development` | tests/ only | >= 60% | Auth + validation | Typed errors |
| `production` | Forbidden | >= 80% | Full OWASP | Structured |

---

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

---

## Error Recovery

- Test/build/lint failures: auto-fix and retry up to **3 times**
- Flaky failures (network, non-deterministic): retry **once**, then report
- Rebase conflicts: attempt auto-resolution, report only if stuck
