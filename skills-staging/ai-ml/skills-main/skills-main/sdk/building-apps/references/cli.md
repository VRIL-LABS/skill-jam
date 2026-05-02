# CLI Command Reference

## Prerequisites

### Python Apps — uv (Required)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Node.js Apps — Node.js v20+ (Required)

```bash
# macOS / Linux (via fnm)
curl -fsSL https://fnm.vercel.app/install | bash
fnm install 22

# Or via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 22
```

### Hardware

| App Type | Development |
|----------|-------------|
| CPU apps | Any machine |
| GPU apps | NVIDIA CUDA GPU required |

## Installation

```bash
curl -fsSL https://cli.inference.sh | sh
infsh login
infsh me  # Check current user
```

## App Commands

### Development

```bash
# Create
infsh app init my-app              # Non-interactive (Python default)
infsh app init my-app --lang node  # Non-interactive (Node.js)
infsh app init                     # Interactive

# Test locally
infsh app test                     # Test with input.json
infsh app test --input '{"k":"v"}' # Test with inline JSON
infsh app test --input in.json     # Test with input file
infsh app test --save-example      # Generate sample input.json

# Deploy
infsh app deploy                   # Deploy from current directory
infsh app deploy --dry-run         # Validate without deploying
```

### Running Apps (Cloud)

```bash
infsh app run user/app --input input.json
infsh app run user/app@version --input '{"prompt": "hello"}'

# Generate sample input for an app
infsh app sample user/app
infsh app sample user/app --save input.json
```

### Managing Apps

```bash
# Your apps
infsh app my                       # List your deployed apps
infsh app my -l                    # Detailed list

# Browse store
infsh app list                     # List available apps
infsh app list --featured          # Featured apps
infsh app list --category image    # Filter by category

# Get app details
infsh app get user/app             # View app info and schemas
infsh app get user/app --json      # Output as JSON

# Pull apps
infsh app pull [id]                # Pull an app
infsh app pull --all               # Pull all apps
infsh app pull --all --force       # Overwrite existing
```

## Integration Commands

```bash
infsh app integrations list        # List available integrations
```

## General Commands

```bash
infsh help                         # Get help
infsh [command] --help             # Command help
infsh version                      # View version
infsh update                       # Update CLI
infsh completion bash              # Shell completions (bash/zsh/fish)
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `INFSH_API_KEY` | API key (overrides config file) |
