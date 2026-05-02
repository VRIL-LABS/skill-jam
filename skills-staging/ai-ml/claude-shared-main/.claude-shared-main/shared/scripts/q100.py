#!/usr/bin/env python3
"""One-liner Q100 display: latest score + mini-trend. From supraforge-mueller/.claude"""
import json, sys
from pathlib import Path

SCORES = Path.home() / ".claude" / "telemetry" / "quality_scores.jsonl"

if not SCORES.exists():
    print("No Q100 data yet.")
    sys.exit(0)

scores = []
with open(SCORES, "r", encoding="utf-8") as f:
    for line in f:
        try:
            scores.append(json.loads(line))
        except:
            pass

if not scores:
    print("No Q100 data yet.")
    sys.exit(0)

latest = scores[-1]
q = latest["q100"]
grade = "A+" if q >= 90 else "A" if q >= 80 else "B" if q >= 70 else "C" if q >= 60 else "D" if q >= 50 else "F"
sid = latest["session_id"][:8]
cfg = latest.get("config_hash", "?")[:8]

recent = [s["q100"] for s in scores[-5:]]
if len(recent) >= 2:
    delta = recent[-1] - recent[0]
    arrow = "^" if delta > 2 else "v" if delta < -2 else "="
    trend = f"  trend({len(recent)}): {' -> '.join(f'{s:.0f}' for s in recent)} {arrow}"
else:
    trend = ""

print(f"Q100={q:.1f} [{grade}]  cfg={cfg}  session={sid}{trend}")
