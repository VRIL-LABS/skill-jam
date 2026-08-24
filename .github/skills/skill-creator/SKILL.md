---
name: skill-creator
description: >
  Create new agent skills, improve existing ones, and evaluate their performance with test cases.
  Use when a user wants to turn a workflow into a reusable skill, refine a SKILL.md, optimize
  triggering and output contracts, or benchmark a skill against a baseline.
---

# Skill Creator

A meta-skill for turning workflows into durable, testable agent skills and for iterating on them until they are reliable.

This is a distilled synthesis of the most authoritative patterns in the agent-skills ecosystem, especially the Anthropic `skill-creator` guidance and the broader agent-skills spec used across the community.

## When to Use

- User wants to "turn this workflow into a skill" or "create a skill for X"
- Existing `SKILL.md` needs editing, restructuring, or quality improvement
- The skill description needs better triggering behavior
- The task benefits from evals, benchmark comparisons, or iterative tuning
- User wants to formalize a repeatable process into a reusable capability

## Process

### 1. Capture intent

Start by defining the skill's job in one sentence: what it should enable the agent to do, when it should trigger, and what the expected output is.

Ask clarifying questions if needed about:
- the core workflow to turn into a skill
- likely user prompts that should trigger it
- required inputs and expected output format
- edge cases, dependencies, and scope boundaries

### 2. Research and interview

Before writing the final skill, gather enough context to make it general and robust:
- inspect similar skills or patterns in relevant repos
- check the exact workflow and any existing examples
- identify common failure modes and edge cases
- decide whether this should be a deterministic workflow, a research workflow, or a subjective creative workflow

### 3. Draft the SKILL.md

Write a clear, usable skill file with:
- valid YAML frontmatter with `name` and `description`
- a concise but specific description that includes trigger contexts
- `## When to Use` bullet points with concrete situations
- an actionable `## Process` section with ordered steps
- explicit output format or example results
- explicit boundaries and scope limits

Prefer imperative language and focused responsibilities.

### 4. Structure for progressive disclosure

Keep the skill readable and token-efficient:
- metadata is the short description used for triggering
- the `SKILL.md` body contains the process and patterns
- supporting references or bundled scripts live in separate subpaths when they are large

Good skill design keeps the rapid path clear without burying the model in unnecessary context.

### 5. Add tests with realistic prompts

Create 2–5 realistic eval prompts that match how a user would actually request this skill.

For each prompt, define:
- the user request
- the expected behavior or output
- whether it is a deterministic or subjective evaluation

Use a baseline comparison when comparing skill performance is worthwhile.

### 6. Evaluate and iterate

Run the skill against realistic prompts and compare to a baseline or previous version.

Review:
- whether the skill triggered at the right times
- whether the outputs were usable and complete
- whether there were obvious failures or over-broad behavior
- whether the description should be more forceful or more precise

Then revise the skill based on the results.

### 7. Optimize for trigger quality

If the skill is under-triggering or over-triggering, improve the `description` and `When to Use` wording.

Best practice:
- include the task and trigger phrases explicitly
- mention the context where the skill is useful even if the user does not say the exact domain name
- keep the description crisp, but make it actionable enough that the agent will choose it when appropriate

### 8. Finalize and document

Before concluding, verify:
- the skill is narrow and purposeful
- boundaries are explicit
- outputs are concrete and consistent
- examples match the stated behavior
- the workflow is general enough to be reused

## Output Format

Use a clear skill brief like:

```markdown
## Skill plan

**Skill name**: <kebab-case-name>
**Purpose**: <one-sentence job>
**Primary trigger phrases**: <examples>
**Output**: <what the agent should produce>
**Key boundaries**: <what it must not do>
**Eval prompts**: <2-5 prompts to validate behavior>
```

## Examples

### Example Input

```text
Turn this checklist workflow into a reusable skill for my team. It should help agents review project setup, identify missing dependencies, and produce a concise remediation plan.
```

### Example Output

```markdown
## Skill plan

**Skill name**: project-setup-reviewer
**Purpose**: Check whether a repo or project is configured correctly and produce a short remediation plan.
**Primary trigger phrases**: review project setup, find missing dependencies, audit local environment, identify setup gaps
**Output**: a checklist of missing pieces and a prioritized fix plan
**Key boundaries**: do not rewrite the codebase; do not invent credentials; do not assume deployment targets without evidence
**Eval prompts**: 1) audit this project setup, 2) find missing environment files, 3) identify the next steps to make this repo runnable
```

## Boundaries

- Do not create a skill that is broader than a single, clear responsibility
- Do not leave ambiguous trigger conditions; the description should make selection obvious
- Do not write evals that are subjective unless the skill is inherently subjective
- Do not skip iteration; strong skills are refined against real prompts and feedback
- Do not hide dangerous or unauthorized actions inside a skill; keep scope safe and transparent

## Authoritative references

- Anthropic `anthropics/skills` — official `skill-creator` guidance and skill authoring patterns
- `agentskills/agentskills` — open standard for agent skill metadata and structure
- VRIL LABS `skill-jam` — strong examples of skill discovery and authoring discipline
