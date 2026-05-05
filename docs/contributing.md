<div align="center">
  <img src="contributing-header.svg" alt="Contributing to Skill Jam by VRIL LABS" width="100%"/>
</div>

<div align="center">

![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen?style=flat-square)
![Good First Issue](https://img.shields.io/badge/good%20first%20issue-available-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/license-open%20source-green?style=flat-square)
![Discord](https://img.shields.io/badge/community-discord-7289da?style=flat-square)

</div>

# 🤝 Contributing to Skill Jam

Thank you for your interest in contributing to **skill-jam** — the community hub for agent skills! Every contribution, whether a new skill, a bug fix, improved documentation, or a community submodule suggestion, helps make this resource better for developers and AI engineers worldwide.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Skill Structure & Format](#skill-structure--format)
- [Adding a New Skill (Step-by-Step)](#adding-a-new-skill-step-by-step)
- [Suggesting a Submodule / Popular Skill Repo](#suggesting-a-submodule--popular-skill-repo)
- [Improving Documentation](#improving-documentation)
- [Reporting Bugs or Issues](#reporting-bugs-or-issues)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Review Process](#review-process)
- [Community & Support](#community--support)

---

## Code of Conduct

This project is an open, welcoming community. By participating you agree to our standards:

- **Be respectful** — treat all contributors and maintainers with kindness and patience.
- **Be inclusive** — welcome newcomers; avoid gatekeeping or exclusionary language.
- **Be constructive** — give and receive feedback graciously; critique code, not people.
- **No spam or self-promotion** — skills should be genuinely useful; please do not submit promotional or low-quality content.

Violations may result in removal of contributions or banning from the community. Report issues to the maintainers via a private GitHub issue.

---

## How Can I Contribute?

| Contribution Type | Effort | Impact |
|---|---|---|
| 🆕 Add a new skill | Medium | ⭐⭐⭐ |
| 🐛 Fix a bug or broken skill | Low–Medium | ⭐⭐⭐ |
| 📖 Improve documentation | Low | ⭐⭐ |
| 🌐 Suggest a submodule / popular skill repo | Low | ⭐⭐⭐ |
| 🎨 Improve existing skill quality | Medium | ⭐⭐ |
| 💡 Propose a new category | Low | ⭐⭐ |

---

## Skill Structure & Format

Every skill in `skills/` must be a **directory** containing at minimum a `SKILL.md` file. Skills follow the [Agent Skills](https://agentskills.io/) open format and must be compatible with the `skills` CLI.

### Required file: `SKILL.md`

Your `SKILL.md` must include all of the following sections:

```markdown
# Skill Name

## Description
One paragraph explaining what this skill does and when to use it.

## Category
One of: Engineering | Data | Productivity | Research | Commerce | Creative

## Invocation
How the agent should call this skill (natural language trigger).

## Process
Step-by-step breakdown of how the skill executes.

## Inputs
| Parameter | Type | Required | Description |
|---|---|---|---|
| param_name | string | Yes | What this parameter does |

## Outputs
| Field | Type | Description |
|---|---|---|
| result_field | string | What this field contains |

## Example
### Input
\`\`\`json
{ "param_name": "example value" }
\`\`\`

### Output
\`\`\`json
{ "result_field": "example result" }
\`\`\`

## Dependencies
List any APIs, tools, libraries, or external services required (if none, write "None").

## Notes
Any additional context, limitations, or best practices.
```

### Optional files

You may also include in your skill directory:

| File | Purpose |
|---|---|
| `README.md` | Detailed skill documentation with full usage examples |
| `example.json` | A worked example input/output pair |
| `config.json` | Default configuration options |
| `CHANGELOG.md` | Version history for the skill |

### Naming conventions

- Directory name: `kebab-case`, descriptive, no version numbers (e.g., `code-reviewer`, `sql-optimizer`)
- `SKILL.md` — always uppercase
- Avoid abbreviations; prefer clarity over brevity

---

## Adding a New Skill (Step-by-Step)

### 1. Fork the repository

Click **Fork** on GitHub to create your personal copy of `skill-jam`.

```bash
git clone https://github.com/<your-username>/skill-jam.git
cd skill-jam
```

### 2. Create a feature branch

Name your branch descriptively:

```bash
git checkout -b skill/my-new-skill-name
```

### 3. Create your skill directory

Place your skill in the appropriate category subdirectory:

```
skills/
├── engineering/      ← Software development & DevOps
├── data/             ← Data analysis, ETL, ML
├── productivity/     ← Scheduling, email, file management
├── research/         ← Search, summarization, citations
├── commerce/         ← E-commerce, finance, business
└── creative/         ← Writing, media, content
```

```bash
mkdir skills/<category>/<your-skill-name>
touch skills/<category>/<your-skill-name>/SKILL.md
```

### 4. Write your `SKILL.md`

Use the template in [Skill Structure & Format](#skill-structure--format) above. Quality checklist:

- [ ] Clear, single responsibility (one skill = one purpose)
- [ ] Descriptive name that matches the directory name
- [ ] All required sections are present and filled in
- [ ] At least one complete example with realistic input/output
- [ ] Dependencies clearly listed
- [ ] Written in clear, concise English

### 5. Validate your skill (optional but recommended)

If you have the `skills` CLI installed, you can validate your skill format:

```bash
npx skills validate ./skills/<category>/<your-skill-name>
```

### 6. Commit and push

```bash
git add skills/<category>/<your-skill-name>/
git commit -m "feat: add <skill-name> skill"
git push origin skill/my-new-skill-name
```

### 7. Open a Pull Request

Go to your fork on GitHub and click **Compare & pull request**. Fill in the PR template (see [Pull Request Guidelines](#pull-request-guidelines)).

---

## Suggesting a Submodule / Popular Skill Repo

The `popular-skills/` directory contains curated Git submodules from leading organizations. To suggest adding a new submodule:

1. **Open a GitHub Issue** using the `[Submodule Request]` label.
2. Provide:
   - Repository URL
   - Organization / author
   - Brief description of the skills it contains
   - Approximate skill count
   - Why it belongs in skill-jam
3. Maintainers will review and add it if it meets quality standards.

### Criteria for submodule inclusion

- Repository must be publicly accessible
- Must contain valid Agent Skills–formatted skills (`SKILL.md` or equivalent)
- Must be actively maintained (last commit within 12 months)
- Must not duplicate an existing submodule
- Must be broadly useful, not narrowly promotional

---

## Improving Documentation

Documentation improvements are highly valued. This includes:

- Fixing typos, grammar, or broken links in any `.md` file
- Expanding examples or clarifying ambiguous instructions
- Adding translations (create `docs/contributing.<lang>.md`)
- Updating the skill table in `README.md` when new skills are added

For documentation-only changes:

```bash
git checkout -b docs/improve-contributing-guide
# make your changes
git commit -m "docs: fix typo in contributing.md"
git push origin docs/improve-contributing-guide
```

---

## Reporting Bugs or Issues

Use [GitHub Issues](https://github.com/VRIL-LABS/skill-jam/issues) to report:

- A broken or incorrect skill
- A submodule that is inaccessible or stale
- Incorrect information in `README.md` or other docs
- CI/CD pipeline failures

When filing an issue, please include:

- **Title**: Short, descriptive summary
- **Description**: What you expected vs. what happened
- **Steps to reproduce**: If applicable
- **Environment**: OS, Node version, CLI version (if relevant)
- **Skill / file path**: Which skill or file is affected

---

## Pull Request Guidelines

### PR title format

Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes:

| Prefix | Use for |
|---|---|
| `feat:` | Adding a new skill or feature |
| `fix:` | Bug fix in an existing skill or docs |
| `docs:` | Documentation-only changes |
| `chore:` | Maintenance tasks (submodule updates, CI tweaks) |
| `refactor:` | Skill rewrites that don't change behavior |

Examples:
- `feat: add sql-query-explainer skill`
- `docs: fix broken link in README`
- `fix: correct broken output example in sentiment-analyzer`

### PR description checklist

When you open a PR, please confirm:

- [ ] My skill follows the required `SKILL.md` format
- [ ] I have placed the skill in the correct category directory
- [ ] The skill has a clear, single responsibility
- [ ] I have included at least one complete example
- [ ] All dependencies are documented
- [ ] I have read the [Code of Conduct](#code-of-conduct)
- [ ] My branch is up to date with `main`

### Branch hygiene

- Branch off from and target `main`
- Keep PRs focused — one skill per PR where possible
- Rebase or merge `main` into your branch before submitting if it has diverged
- Do not include unrelated changes in a skill PR

---

## Review Process

1. **Automated checks** run on all PRs (format validation, link checking).
2. A maintainer will review your PR within **7 days**.
3. Feedback will be provided as review comments — please address all before requesting re-review.
4. Once approved, a maintainer will merge your PR using squash merge.

If your PR has not received a review after 7 days, feel free to leave a comment to ping the maintainers.

---

## Community & Support

- 💬 **GitHub Discussions** — ask questions, share ideas, and connect with contributors: [Discussions](https://github.com/VRIL-LABS/skill-jam/discussions)
- 🐛 **GitHub Issues** — report bugs and request features: [Issues](https://github.com/VRIL-LABS/skill-jam/issues)
- 🌐 **Agent Skills spec** — learn more about the format at [agentskills.io](https://agentskills.io/)
- 📦 **Skills CLI** — install and validate skills with `npx skills`

---

<p align="center">Made with 🎸 by the skill-jam community — <a href="https://github.com/VRIL-LABS/skill-jam">VRIL-LABS/skill-jam</a></p>
