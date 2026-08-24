---
name: skill-navigator
description: >
  Find the right agent skill for a task, decide when to use a skill vs. inline reasoning, and sequence
  skill calls efficiently. Use when the user asks which skill to use, when the workflow is uncertain,
  or when a task would benefit from a proven reusable process.
---

# Skill Navigator

Use this skill to find the best skill for the current task and choose the right invocation timing. The goal is to maximize quality and minimize wasted tokens.

This is a distilled synthesis of the strongest skill-discovery patterns across the agent-skills ecosystem, especially the skill-discovery guidance in VRIL LABS `skill-jam` and the broader industry practice of matching tasks to explicit `When to Use` sections.

## When to Use

- Agent is unsure which skill applies to a task
- User asks "what skills are available?" or "which skill should I use for X?"
- A task has a known structure and a skill could encode it cleanly
- The task would benefit from a repeatable process or reference workflow
- A session is starting and the agent should orient to available capabilities
- A phase is complete and the next skill in the chain needs to be chosen

## Process

### 1. Decide whether a skill is needed

Before searching, judge whether a skill is appropriate.

Use a skill when:
- the task has a well-defined structure
- the workflow is repetitive or domain-specific
- external APIs or platform operations are involved
- the process would take multiple steps to re-derive
- output needs a consistent format

Do not use a skill when:
- the task is a simple direct answer
- no known skill fits and the work is cheaper inline
- the skill would overcomplicate a small task
- the skill would duplicate work already done in the same session

### 2. Start from the obvious category

Check the likely skill families first:
- code review or debugging
- research and web search
- file and project analysis
- testing and validation
- deployment and operations
- documentation and writing
- domain-specific services or tools

Prefer the most likely matches before scanning a broad list.

### 3. Filter by description and trigger phrases

Look for the best matches using these signals:
- task verb and noun
- technology or domain keywords
- expected output type
- the skill's explicit `When to Use` or description

If multiple skills look plausible, narrow to the top 2–4 candidates by fit, not by volume.

### 4. Read the candidate `When to Use` sections

This is the authoritative decision gate. If the current task matches a bullet or trigger phrase, the skill is a valid fit. If not, do not recommend it.

Use the rule:
- one clear match is enough
- more than 4 recommendations is usually too broad
- avoid recommending the same skill twice in a session for the same purpose

### 5. Choose the right timing

Invoke at session start when:
- the task requires repo reconnaissance before implementation
- the work depends on external research or tooling context
- the skill sets up a reliable process for the whole session

Invoke mid-task when:
- the implementation or diagnosis has a clear stage boundary
- the user needs a focused specialist step
- a review or validation step is needed before finish

Invoke at the end when:
- documentation or release readiness is needed
- final validation or cleanup is required

### 6. Prefer chains when they add clarity

When a task has multiple stages, use a small chain rather than a single "do everything" skill.

A typical flow is:
- reconnaissance or research skill
- implementation or domain skill
- review, validation, or documentation

Keep chains minimal and purposeful.

### 7. Return a concise navigation recommendation

Recommend the best fit with:
- task summary
- recommended skill(s)
- invocation timing
- brief rationale
- optional chain sequence

## Output Format

```markdown
## Skill Navigation

**Task**: <brief, concrete task>
**Recommended skill(s)**: <skill name(s)>
**Invocation timing**: <now / after X / at task end>
**Rationale**: <1–2 sentence explanation>
**Chain**: <optional: skill A → skill B>
```

## Examples

### Example Input

```text
We need to set up database migrations for a Node.js app. Which skill should we use first, and when?
```

### Example Output

```markdown
## Skill Navigation

**Task**: Add PostgreSQL migration workflow to a Node.js project
**Recommended skill(s)**: `codebase-recon`, `database-migration`
**Invocation timing**: Start with `codebase-recon` now, then use `database-migration` before implementing
**Rationale**: `codebase-recon` finds reference patterns and existing conventions first, while `database-migration` encodes the actual migration process and common failure modes.
**Chain**: `codebase-recon` → `database-migration` → implement → validate
```

## Boundaries

- Do not recommend a skill unless its trigger conditions clearly match the task
- Do not recommend more than 4 skills for a single task
- Do not recommend a skill twice for the same work in one session
- Do not force a skill when inline reasoning is clearly cheaper and cleaner
- Always include invocation timing; "use skill X" by itself is incomplete
- If no skill fits, say so clearly and recommend inline reasoning

## Authoritative references

- VRIL LABS `skill-jam` `skill-navigator` and `skill-builder` guidance
- Anthropic `anthropics/skills` guidance on skill creation and metadata design
- `agentskills/agentskills` open standard for skills, descriptions, and discovery patterns
