#!/bin/bash
# repair-plugin-cache.sh — from supraforge-mueller/.claude
# Fixes broken plugin cache by syncing hooks/core from marketplace sources
# Bug: Claude Code plugin caching only creates __pycache__ but never copies source scripts
# This script runs on UserPromptSubmit to ensure caches stay healthy.

PLUGINS_DIR="$HOME/.claude/plugins"
CACHE_DIR="$PLUGINS_DIR/cache"
MARKET_DIR="$PLUGINS_DIR/marketplaces"

repaired=0

for cache_entry in "$CACHE_DIR"/*/*/; do
    [ -d "$cache_entry" ] || continue
    marketplace=$(basename "$(dirname "$cache_entry")")
    plugin=$(basename "$cache_entry")

    for version_dir in "$cache_entry"*/; do
        [ -d "$version_dir" ] || continue

        src_dir=""
        if [ -d "$MARKET_DIR/$marketplace/plugins/$plugin/hooks" ]; then
            src_dir="$MARKET_DIR/$marketplace/plugins/$plugin"
        else
            for mp in "$MARKET_DIR"/*/plugins/"$plugin"/; do
                if [ -d "${mp}hooks" ]; then
                    src_dir="$mp"
                    break
                fi
            done
        fi

        [ -z "$src_dir" ] && continue

        if [ -d "${src_dir}/hooks" ]; then
            needs_repair=false
            if [ ! -d "${version_dir}hooks" ]; then
                needs_repair=true
            else
                for src_file in "${src_dir}/hooks/"*; do
                    [ -f "$src_file" ] || continue
                    cached_file="${version_dir}hooks/$(basename "$src_file")"
                    if [ ! -f "$cached_file" ] || [ "$src_file" -nt "$cached_file" ]; then
                        needs_repair=true
                        break
                    fi
                done
            fi

            if $needs_repair; then
                mkdir -p "${version_dir}hooks"
                cp -r "${src_dir}/hooks/"* "${version_dir}hooks/" 2>/dev/null
                repaired=$((repaired + 1))
            fi
        fi

        if [ -d "${src_dir}/core" ]; then
            needs_repair=false
            if [ ! -d "${version_dir}core" ]; then
                needs_repair=true
            else
                for src_file in "${src_dir}/core/"*; do
                    [ -f "$src_file" ] || continue
                    cached_file="${version_dir}core/$(basename "$src_file")"
                    if [ ! -f "$cached_file" ] || [ "$src_file" -nt "$cached_file" ]; then
                        needs_repair=true
                        break
                    fi
                done
            fi

            if $needs_repair; then
                mkdir -p "${version_dir}core"
                cp -r "${src_dir}/core/"* "${version_dir}core/" 2>/dev/null
                repaired=$((repaired + 1))
            fi
        fi
    done
done

if [ $repaired -gt 0 ]; then
    echo "Plugin cache: repaired $repaired entries" >&2
fi
exit 0
