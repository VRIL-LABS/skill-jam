#!/usr/bin/env python3
"""
Stop-hook wrapper for session-metrics.py — from supraforge-mueller/.claude
Reads session_id from Claude Code hook stdin, scores the session,
and outputs Q100 to stderr (visible in Claude Code logs).
Deduplicates: only scores once per session by checking existing scores.
"""

import json
import sys
import os
from pathlib import Path

SCORES_FILE = Path.home() / ".claude" / "telemetry" / "quality_scores.jsonl"
METRICS_SCRIPT = Path.home() / ".claude" / "scripts" / "session-metrics.py"


def get_last_score_time(session_id: str) -> float:
    """Get timestamp of last score for this session. Returns 0 if not scored."""
    if not SCORES_FILE.exists():
        return 0
    last_ts = 0
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("session_id") == session_id:
                    ts = entry.get("timestamp", "")
                    if ts:
                        from datetime import datetime, timezone
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        last_ts = max(last_ts, dt.timestamp())
            except:
                continue
    return last_ts


def main():
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    session_id = hook_input.get("session_id", "")
    if not session_id:
        sys.exit(0)

    import time
    last_scored = get_last_score_time(session_id)
    if last_scored > 0 and (time.time() - last_scored) < 60:
        sys.exit(0)

    import subprocess
    result = subprocess.run(
        [sys.executable, str(METRICS_SCRIPT), "--session-id", session_id],
        capture_output=True,
        text=True,
        timeout=12,
        cwd=hook_input.get("cwd", str(Path.home())),
    )

    if result.stdout:
        for line in result.stdout.split("\n"):
            if "Q100" in line and "=" in line:
                print(line.strip(), file=sys.stderr)
                break

    sys.exit(0)


if __name__ == "__main__":
    main()
