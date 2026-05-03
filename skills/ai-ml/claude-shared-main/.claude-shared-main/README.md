# .claude-shared — AaaS Team Configuration

Shared Claude Code configuration for the AaaS team (ibossyNr1 + supraforge-mueller).

## Three-Layer Architecture

```
Layer 1: This repo (.claude-shared)        ← Team baseline
Layer 2: Your personal ~/.claude repo       ← Personal overrides
Layer 3: settings.local.json (gitignored)   ← Machine-specific secrets
```

## What's Shared

| Component | Description |
|-----------|-------------|
| `shared/CLAUDE.md` | Team workflow: Hard Stops, Engineering Laws, Quality Modes, Decision Matrix |
| `shared/rules/` | 28 coding standard files (common + TypeScript, Python, Go, Perl) |
| `shared/agents/` | 18 agent definitions (architect, code-reviewer, security-reviewer, etc.) |
| `shared/skills/` | 5 team skills (check_billing, debug_test, test_api, testui, write_tests) |
| `shared/scripts/` | Q100 quality measurement system + plugin cache repair |
| `shared/hooks/` | 23 lifecycle hooks (hooks.json) |
| `shared/hookify/` | Safety rules (console-log, dangerous-rm, sensitive-files) |
| `templates/` | Starter settings.json and .gitignore templates |

## What's NOT Shared (stays personal)

- `settings.json` — permissions, plugins, MCP servers
- `plugins/` — which plugins you install
- `projects/` — session data, memory
- `settings.local.json` — secrets, local paths

## Quick Start

```bash
# 1. Clone this repo somewhere permanent
git clone https://github.com/ibossyNr1/.claude-shared.git ~/.claude-shared

# 2. Run the installer (symlinks shared config into ~/.claude/)
cd ~/.claude-shared
chmod +x install.sh
./install.sh

# 3. If you're new, copy the settings template
# cp templates/settings.json.template ~/.claude/settings.json
# cp templates/.gitignore.template ~/.claude/.gitignore
# Then customize with your personal plugins and permissions.
```

## Updating

```bash
cd ~/.claude-shared
git pull
./install.sh
```

The installer is safe to re-run. It won't overwrite personal files.

## Adding a Collaborator

```bash
gh repo edit ibossyNr1/.claude-shared --add-collaborator supraforge-mueller
```

## Q100 Quality Scoring

The shared scripts include a session quality measurement system:

```bash
# Score your latest session
python3 ~/.claude/scripts/session-metrics.py

# Quick one-liner score
python3 ~/.claude/scripts/q100.py

# Benchmark against standard tasks
python3 ~/.claude/scripts/quality-benchmark.py score

# Show trend over time
python3 ~/.claude/scripts/session-metrics.py --trend
```

## Contributing

Both team members can push to this repo. When making changes:
1. Edit files in `shared/`
2. Test by running `./install.sh` locally
3. Commit and push
4. Other team member runs `git pull && ./install.sh`
