#!/bin/bash
# install.sh — Install shared Claude Code team config into ~/.claude/
# Safe: does NOT touch settings.json, plugins/, projects/, memory/
# Run: git clone https://github.com/ibossyNr1/.claude-shared.git && cd .claude-shared && ./install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SHARED_DIR="$SCRIPT_DIR/shared"
CLAUDE_DIR="$HOME/.claude"

if [ ! -d "$CLAUDE_DIR" ]; then
    echo "Error: ~/.claude does not exist. Install Claude Code first."
    exit 1
fi

echo "Installing shared Claude Code config into $CLAUDE_DIR..."
echo ""

# ── Rules (symlink entire directories) ──────────────────────────────────────
echo "[1/7] Rules..."
mkdir -p "$CLAUDE_DIR/rules"
for ruledir in "$SHARED_DIR/rules/"*/; do
    dirname=$(basename "$ruledir")
    if [ -L "$CLAUDE_DIR/rules/$dirname" ]; then
        rm "$CLAUDE_DIR/rules/$dirname"
    fi
    if [ -d "$CLAUDE_DIR/rules/$dirname" ] && [ ! -L "$CLAUDE_DIR/rules/$dirname" ]; then
        echo "  SKIP rules/$dirname (local dir exists, not overwriting)"
    else
        ln -sfn "$ruledir" "$CLAUDE_DIR/rules/$dirname"
        echo "  OK   rules/$dirname -> shared"
    fi
done

# ── Agents (symlink individual files, preserve local additions) ─────────────
echo "[2/7] Agents..."
mkdir -p "$CLAUDE_DIR/agents"
for agent in "$SHARED_DIR/agents/"*.md; do
    name=$(basename "$agent")
    ln -sf "$agent" "$CLAUDE_DIR/agents/$name"
done
echo "  OK   $(ls "$SHARED_DIR/agents/"*.md 2>/dev/null | wc -l | tr -d ' ') agents linked"

# ── Skills (copy, don't symlink — allows personal additions) ───────────────
echo "[3/7] Skills..."
mkdir -p "$CLAUDE_DIR/skills"
for skilldir in "$SHARED_DIR/skills/"*/; do
    name=$(basename "$skilldir")
    if [ ! -d "$CLAUDE_DIR/skills/$name" ]; then
        cp -r "$skilldir" "$CLAUDE_DIR/skills/$name"
        echo "  NEW  skills/$name"
    else
        echo "  SKIP skills/$name (already exists)"
    fi
done

# ── Scripts (symlink, allows shared updates) ────────────────────────────────
echo "[4/7] Scripts..."
mkdir -p "$CLAUDE_DIR/scripts"
for script in "$SHARED_DIR/scripts/"*; do
    name=$(basename "$script")
    ln -sf "$script" "$CLAUDE_DIR/scripts/$name"
done
echo "  OK   $(ls "$SHARED_DIR/scripts/"* 2>/dev/null | wc -l | tr -d ' ') scripts linked"

# ── Hooks (merge: shared hooks.json as base, warn if local exists) ──────────
echo "[5/7] Hooks..."
mkdir -p "$CLAUDE_DIR/hooks"
if [ -f "$CLAUDE_DIR/hooks/hooks.json" ]; then
    echo "  WARN hooks/hooks.json already exists — not overwriting"
    echo "       Compare with: diff $CLAUDE_DIR/hooks/hooks.json $SHARED_DIR/hooks/hooks.json"
else
    cp "$SHARED_DIR/hooks/hooks.json" "$CLAUDE_DIR/hooks/hooks.json"
    echo "  OK   hooks/hooks.json installed"
fi

# ── Hookify rules (copy if not present) ─────────────────────────────────────
echo "[6/7] Hookify rules..."
for rule in "$SHARED_DIR/hookify/"*.local.md; do
    name=$(basename "$rule")
    target="$CLAUDE_DIR/$name"
    if [ ! -f "$target" ]; then
        cp "$rule" "$target"
        echo "  NEW  $name"
    else
        echo "  SKIP $name (already exists)"
    fi
done

# ── Shared CLAUDE.md (install as reference, don't overwrite personal) ───────
echo "[7/7] CLAUDE.md..."
if [ -f "$CLAUDE_DIR/CLAUDE.md" ]; then
    echo "  SKIP CLAUDE.md (personal version exists)"
    echo "       Shared version at: $SHARED_DIR/CLAUDE.md"
    echo "       Diff:  diff $CLAUDE_DIR/CLAUDE.md $SHARED_DIR/CLAUDE.md"
else
    cp "$SHARED_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
    echo "  OK   CLAUDE.md installed"
fi

echo ""
echo "Done. Shared config installed."
echo ""
echo "NOT touched: settings.json, plugins/, projects/, memory/"
echo "To update later: cd $(basename "$SCRIPT_DIR") && git pull && ./install.sh"
