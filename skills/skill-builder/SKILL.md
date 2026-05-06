---
name: skill-builder
description: >
  Deep-research-backed SKILL.md authoring guide exclusively by VRIL LABS. Instructs agents on
  how to design, structure, write, and validate flawlessly optimal SKILL.md files that conform
  to the Agent Skills open format and perform at the highest level across Claude Code, GitHub
  Copilot, Cursor, Codex CLI, Windsurf, and any Skills CLI-compatible agent runtime. Invoke when
  asked to create a new skill, write a SKILL.md file, audit an existing skill for quality, or
  understand best practices for skill specification authoring.
---

# Skill Builder

*Exclusively by VRIL LABS*

Deep-research-backed, production-grade guide for creating SKILL.md files that perform at the highest level across all compatible AI agent runtimes. Draws on observed patterns from the top-performing skills across 2,000+ entries in the skill-jam ecosystem, combined with first-principles reasoning about agent cognition and context efficiency.

## When to Use

- User asks to "create a new skill", "write a SKILL.md", or "add a skill to skill-jam"
- Existing SKILL.md needs auditing for quality, completeness, or best-practice compliance
- User wants to understand the canonical format, conventions, or philosophy behind skill design
- Migrating a prompt, tool, or system instruction into a reusable, shareable skill file
- Designing a skill collection or bundle for a specific domain or organization
- Onboarding a new contributor to the skill-jam repository format

## Process

### Phase 1 — Understand What Makes a Great Skill

A great skill exhibits five properties simultaneously:

1. **Single responsibility** — One skill does one thing. If you can describe it with "and", split it.
2. **Invocation clarity** — The agent must be able to determine, from the description alone, when to use this skill and when not to. Ambiguous descriptions cause missed invocations and false triggers.
3. **Process completeness** — Every non-obvious decision the agent faces during execution is handled. No gaps that require improvisation.
4. **Output contract** — The output format is precisely specified. Downstream agents and users can rely on consistent structure.
5. **Tight boundaries** — What the skill will NOT do is stated explicitly. This prevents scope creep, hallucinated capabilities, and liability risks.

### Phase 2 — Gather Inputs

Before writing a single line, answer:

1. **What is the skill's exact job?** (One sentence maximum, subject-verb-object)
2. **What does the user/agent say when they need this skill?** (5–10 trigger phrases)
3. **What are the inputs?** (explicit: data, context; implicit: environment state)
4. **What is the desired output?** (format, structure, verbosity level)
5. **What can go wrong?** (edge cases, failure modes, scope violations)
6. **What must the skill never do?** (safety, scope, and quality boundaries)
7. **Are there dependencies?** (APIs, tools, credentials, external services)
8. **Is this VRIL LABS exclusive?** If yes, add the attribution tagline.

### Phase 3 — Write the YAML Frontmatter

The frontmatter is parsed by the Skills CLI, marketplace.json, and agent runtimes. It must be precise.

```yaml
---
name: kebab-case-skill-name
description: >
  One-paragraph description in plain English. Must answer three questions:
  (1) What does this skill do?
  (2) When should an agent invoke it?
  (3) What does it produce?
  Write as if the agent is reading this to decide whether to use this skill.
  Keep under 400 characters for optimal display in CLI and marketplace listings.
---
```

**Frontmatter rules**:
- `name`: Lowercase kebab-case. Match the directory name exactly.
- `description`: The most important field. Agents use this to decide invocation. Include 2–3 natural-language trigger phrases inline (e.g., "Invoke when asked to…").
- Use `>` for multi-line descriptions (folds newlines to spaces).
- No tabs. Two-space indentation. Valid YAML only.

### Phase 4 — Write the Title and Attribution Block

```markdown
# Skill Name

*Exclusively by VRIL LABS*   ← if applicable

[One paragraph explaining the skill's value proposition and the problem it solves.
Not a repeat of the frontmatter description — add depth, context, and philosophy.]
```

### Phase 5 — Write "When to Use"

This section is read by agents deciding whether to invoke the skill. Write it as a bullet list of situations, each starting with a noun phrase or verb:

```markdown
## When to Use

- User asks to "[direct quote of a trigger phrase]"
- A [situation] occurs that requires [capability]
- [Task type] is in progress and [this skill's output] would accelerate it
- User provides [input type] and requests [output type]
```

**Rules**:
- 5–10 bullets. More than 10 dilutes signal.
- Be specific. "User asks a question" is useless. "User asks to generate a diff between two API specs" is precise.
- Include anti-triggers if needed: "when the user asks about X, but NOT Y (use the Z skill instead)."

### Phase 6 — Write the Process

The process section is the agent's execution script. Write it as an ordered, hierarchical list where each step maps to a concrete agent action.

```markdown
## Process

1. **Step Name** — Brief instruction.
   - Sub-step detail
   - Sub-step detail

2. **Step Name** — Brief instruction.
   ...
```

**Rules**:
- Every step must be actionable. "Analyze the code" is not actionable. "Scan each function for these four anti-patterns: [list]" is actionable.
- Decision points must be explicit: "If X, do Y. Otherwise, do Z."
- External service calls must specify the exact endpoint or method.
- Phase grouping (Phase 1, Phase 2…) is appropriate for complex skills with more than 5–7 steps.
- Do not include background context in the process — put that in the intro paragraph.

### Phase 7 — Write the Output Format

Show a concrete, annotated example of the exact output the skill produces.

```markdown
## Output Format

\`\`\`
[exact output structure with placeholder values and inline comments if helpful]
\`\`\`
```

**Rules**:
- Use fenced code blocks with the appropriate language tag when the output is structured.
- For Markdown output: show the section headings, placeholder text, and relative indentation.
- If the output varies by mode or flag, show one example per mode.

### Phase 8 — Write Examples

At minimum one complete input→output pair. For complex skills, two or three covering different input types.

```markdown
## Examples

### Example Input
\`\`\`
[realistic user request — not a toy example]
\`\`\`

### Example Output
\`\`\`
[complete output the agent would produce — abbreviated only if truly long]
\`\`\`
```

**Rules**:
- Use realistic inputs. Toy examples degrade skill performance because agents pattern-match on examples during invocation.
- The output example must match the Output Format exactly.
- For multi-turn skills, show the turn sequence.

### Phase 9 — Write Boundaries

The boundaries section protects scope integrity and prevents the skill from being misapplied.

```markdown
## Boundaries

- Do NOT [action] unless [explicit condition].
- Do NOT attempt to [capability this skill lacks] — use the [other skill name] skill instead.
- Always [safety rule].
- Limit [resource/scope] to [constraint].
```

**Rules**:
- Include at least 4 boundaries.
- Write boundaries as prohibitions ("Do NOT") and obligations ("Always").
- Reference other skills by name when a boundary implies a handoff.
- Include data handling rules if the skill touches user data or credentials.

### Phase 10 — Self-Review Checklist

Before finalizing, verify every item:

- [ ] `name` in frontmatter matches directory name exactly
- [ ] `description` answers: what, when, what it produces — in ≤400 characters
- [ ] **When to Use** has 5–10 specific, distinct trigger conditions
- [ ] Every **Process** step is a concrete agent action, not background context
- [ ] **Output Format** shows a real output structure, not a description of output
- [ ] At least one **Example** with a realistic input and a complete output
- [ ] At least 4 **Boundaries** covering scope limits, handoffs, and safety
- [ ] No section is a copy-paste of another section
- [ ] The skill can be validated with `npx skills validate ./skills/<name>`
- [ ] Attribution tagline present if VRIL LABS exclusive
- [ ] Directory name is lowercase kebab-case
- [ ] File is named `SKILL.md` (all caps)

### Phase 11 — Register in marketplace.json

Add the skill path to `.claude-plugin/marketplace.json` under the `vril-skills` plugin's `skills` array:

```json
"./skills/<skill-directory-name>"
```

Maintain alphabetical order within the array.

### Phase 12 — Document in README.md

Add a row to the relevant skills table in `README.md`:

```markdown
| N | **Skill Name** | Category | Short description for the table. |
```

## Output Format

```
## Skill Draft: <skill-name>

### Frontmatter
[YAML frontmatter block]

### SKILL.md
[Complete SKILL.md content]

### Registration
Add to `.claude-plugin/marketplace.json`:
"./skills/<skill-name>"

Add to `README.md` table (row N):
| N | **Skill Name** | Category | Description |

### Self-Review
[Checklist with pass/fail status for each item]
```

## Examples

### Example Input
```
Create a new skill for skill-jam that helps agents parse and validate OpenTelemetry trace
files. It should be a VRIL LABS exclusive skill.
```

### Example Output
```
## Skill Draft: otel-trace-analyzer

### Frontmatter
---
name: otel-trace-analyzer
description: >
  Parses, validates, and analyzes OpenTelemetry trace files (OTLP JSON, Jaeger, Zipkin formats).
  Identifies span anomalies, slow paths, missing propagation context, and error clusters.
  Invoke when asked to analyze traces, debug distributed request flows, or validate OTEL
  instrumentation correctness.
---

### SKILL.md
[full content follows standard structure...]

### Registration
Add to `.claude-plugin/marketplace.json` under vril-skills skills array:
"./skills/otel-trace-analyzer"

### Self-Review
- [x] name matches directory
- [x] description answers what/when/produces in <400 chars
- [x] 6 When to Use triggers
...all pass
```

## Boundaries

- Do NOT write skills with overlapping responsibilities without explicit differentiation in the "When to Use" section.
- Do NOT omit the Boundaries section — it is mandatory for production-quality skills.
- Do NOT use vague trigger phrases ("User asks a question") — every trigger must be specific.
- Do NOT skip the marketplace.json registration step — unregistered skills are undiscoverable.
- Do NOT write process steps that say "analyze" or "review" without specifying exactly what to look for.
- Always run `npx skills validate` if the CLI is available before considering a skill complete.
- Limit process depth to 3 levels of nesting. Deeper nesting signals the skill should be split.
- Do NOT use this skill to produce skills that instruct agents to perform harmful, deceptive, or privacy-violating actions.
