#!/usr/bin/env python3
"""
Session Quality Metrics (Part A) — from supraforge-mueller/.claude
Extracts 12 metrics from Claude Code session JSONL files and computes a Q100 quality score.

Usage:
    python3 ~/.claude/scripts/session-metrics.py                    # Latest session in current project
    python3 ~/.claude/scripts/session-metrics.py --session-id ID    # Specific session
    python3 ~/.claude/scripts/session-metrics.py --all              # All sessions in current project
    python3 ~/.claude/scripts/session-metrics.py --trend            # Show Q100 trend over time
    python3 ~/.claude/scripts/session-metrics.py --project-key KEY  # Specify project key
"""

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration -----------------------------------------------------------

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
TELEMETRY_DIR = CLAUDE_DIR / "telemetry"
SCORES_FILE = TELEMETRY_DIR / "quality_scores.jsonl"

# Metric weights (must sum to 1.0)
WEIGHTS = {
    "plan_rate": 0.10,
    "subagent_efficiency": 0.08,
    "tool_diversity": 0.07,
    "read_before_edit": 0.12,
    "error_rate": 0.10,
    "self_correction": 0.08,
    "cache_hit_rate": 0.05,
    "token_efficiency": 0.08,
    "dedicated_tool_usage": 0.07,
    "turn_duration": 0.05,
    "file_ops_success": 0.10,
    "completion_depth": 0.10,
}

# Normalization thresholds (metric_name: (worst, best) -> mapped to 0-100)
THRESHOLDS = {
    "plan_rate": (0.0, 0.5),
    "subagent_efficiency": (0, 5),
    "tool_diversity": (2, 12),
    "read_before_edit": (0.0, 1.0),
    "error_rate": (0.3, 0.0),
    "self_correction": (0.0, 0.5),
    "cache_hit_rate": (0.0, 0.8),
    "token_efficiency": (0, 1),
    "dedicated_tool_usage": (0.0, 1.0),
    "turn_duration": (60000, 3000),
    "file_ops_success": (0.5, 1.0),
    "completion_depth": (0.5, 4.0),
}


# --- JSONL Parser ------------------------------------------------------------

def parse_session(jsonl_path: Path) -> list[dict]:
    entries = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


# --- Metric Extractors -------------------------------------------------------

def extract_tool_calls(entries: list[dict]) -> list[dict]:
    tools = []
    for entry in entries:
        if entry.get("type") != "assistant":
            continue
        msg = entry.get("message", {})
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "tool_use":
                tools.append({
                    "name": block.get("name", ""),
                    "id": block.get("id", ""),
                    "input": block.get("input", {}),
                    "timestamp": entry.get("timestamp", ""),
                    "uuid": entry.get("uuid", ""),
                })
    return tools


def extract_tool_results(entries: list[dict]) -> dict[str, bool]:
    results = {}
    for entry in entries:
        if entry.get("type") != "user":
            continue
        msg = entry.get("message", {})
        if not isinstance(msg, dict):
            continue
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "tool_result":
                results[block.get("tool_use_id", "")] = block.get("is_error", False)
    return results


def extract_token_usage(entries: list[dict]) -> dict:
    totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read": 0,
        "cache_creation": 0,
        "turns": 0,
    }
    for entry in entries:
        if entry.get("type") != "assistant":
            continue
        msg = entry.get("message", {})
        usage = msg.get("usage", {})
        if not usage:
            continue
        totals["input_tokens"] += usage.get("input_tokens", 0)
        totals["output_tokens"] += usage.get("output_tokens", 0)
        totals["cache_read"] += usage.get("cache_read_input_tokens", 0)
        totals["cache_creation"] += usage.get("cache_creation_input_tokens", 0)
        totals["turns"] += 1
    return totals


def extract_turn_durations(entries: list[dict]) -> list[int]:
    durations = []
    for entry in entries:
        if entry.get("type") == "system" and entry.get("subtype") == "turn_duration":
            ms = entry.get("durationMs", 0)
            msg_count = entry.get("messageCount", 1)
            if ms > 0 and msg_count > 0:
                durations.append(ms // msg_count)
    return durations


def extract_user_messages(entries: list[dict]) -> list[int]:
    return [i for i, e in enumerate(entries) if e.get("type") == "user"]


def extract_assistant_messages(entries: list[dict]) -> list[int]:
    return [i for i, e in enumerate(entries) if e.get("type") == "assistant"]


# --- 12 Metrics --------------------------------------------------------------

def m01_plan_rate(tool_calls: list[dict], user_indices: list[int]) -> float:
    plan_calls = sum(1 for t in tool_calls if t["name"] in ("EnterPlanMode", "ExitPlanMode"))
    user_turns = max(1, len(user_indices))
    plan_cycles = plan_calls / 2
    return min(1.0, plan_cycles / user_turns)


def m02_subagent_efficiency(tool_calls: list[dict]) -> int:
    return sum(1 for t in tool_calls if t["name"] == "Agent")


def m03_tool_diversity(tool_calls: list[dict]) -> int:
    return len(set(t["name"] for t in tool_calls))


def m04_read_before_edit(tool_calls: list[dict]) -> float:
    files_read = set()
    edit_count = 0
    read_before_count = 0
    for t in tool_calls:
        if t["name"] == "Read":
            fp = t["input"].get("file_path", "")
            if fp:
                files_read.add(fp.replace("\\", "/").lower())
        elif t["name"] in ("Edit", "Write"):
            edit_count += 1
            fp = t["input"].get("file_path", "")
            if fp and fp.replace("\\", "/").lower() in files_read:
                read_before_count += 1
    return read_before_count / max(1, edit_count)


def m05_error_rate(tool_results: dict[str, bool], entries: list[dict]) -> float:
    tool_errors = sum(1 for is_err in tool_results.values() if is_err)
    api_errors = sum(
        1 for e in entries
        if e.get("type") == "assistant" and e.get("message", {}).get("isApiErrorMessage")
    )
    total_errors = tool_errors + api_errors
    assistant_turns = sum(1 for e in entries if e.get("type") == "assistant")
    return total_errors / max(1, assistant_turns)


def m06_self_correction(tool_calls: list[dict], tool_results: dict[str, bool]) -> float:
    sequence = []
    for t in tool_calls:
        fp = t["input"].get("file_path", t["input"].get("command", ""))
        is_err = tool_results.get(t["id"], False)
        sequence.append((t["name"], fp, is_err))
    if not sequence:
        return 0.0
    error_count = sum(1 for _, _, err in sequence if err)
    if error_count == 0:
        return 1.0
    corrections = 0
    for i, (name, fp, err) in enumerate(sequence):
        if err:
            for j in range(i + 1, min(i + 6, len(sequence))):
                if sequence[j][0] in ("Edit", "Write"):
                    corrections += 1
                    break
    return corrections / error_count


def m07_cache_hit_rate(token_usage: dict) -> float:
    total_input = token_usage["input_tokens"] + token_usage["cache_read"] + token_usage["cache_creation"]
    if total_input == 0:
        return 0.0
    return token_usage["cache_read"] / total_input


def m08_token_efficiency(token_usage: dict) -> float:
    if token_usage["turns"] == 0:
        return 0.0
    avg = token_usage["output_tokens"] / token_usage["turns"]
    if 200 <= avg <= 800:
        return 1.0
    elif avg < 200:
        return max(0, avg / 200)
    else:
        return max(0, 1.0 - (avg - 800) / 1200)


def m09_dedicated_tool_usage(tool_calls: list[dict]) -> float:
    dedicated = sum(1 for t in tool_calls if t["name"] in ("Glob", "Grep", "Read"))
    bash_search = 0
    for t in tool_calls:
        if t["name"] == "Bash":
            cmd = t["input"].get("command", "")
            if re.search(r'\b(grep|rg|find|cat|head|tail|sed|awk)\b', cmd):
                bash_search += 1
    total = dedicated + bash_search
    if total == 0:
        return 1.0
    return dedicated / total


def m10_turn_duration(durations: list[int]) -> float:
    if not durations:
        return 30000
    return statistics.median(durations)


def m11_file_ops_success(tool_calls: list[dict], tool_results: dict[str, bool]) -> float:
    file_ops = ["Read", "Edit", "Write", "Glob", "Grep"]
    total = 0
    success = 0
    for t in tool_calls:
        if t["name"] in file_ops:
            total += 1
            if not tool_results.get(t["id"], False):
                success += 1
    return success / max(1, total)


def m12_completion_depth(entries: list[dict], user_indices: list[int], assistant_indices: list[int]) -> float:
    if not user_indices or not assistant_indices:
        return 0
    depths = []
    for i, ui in enumerate(user_indices):
        next_ui = user_indices[i + 1] if i + 1 < len(user_indices) else len(entries)
        depth = sum(1 for ai in assistant_indices if ui < ai < next_ui)
        if depth > 0:
            depths.append(depth)
    return statistics.mean(depths) if depths else 0


# --- Normalization & Scoring -------------------------------------------------

def normalize(value: float, worst: float, best: float) -> float:
    if worst == best:
        return 100.0
    if worst > best:
        score = (worst - value) / (worst - best)
    else:
        score = (value - worst) / (best - worst)
    return max(0.0, min(100.0, score * 100))


def compute_q100(raw_metrics: dict[str, float]) -> tuple[float, dict[str, float]]:
    normalized = {}
    for name, raw in raw_metrics.items():
        if name == "token_efficiency":
            normalized[name] = raw * 100
        else:
            worst, best = THRESHOLDS[name]
            normalized[name] = normalize(raw, worst, best)
    q100 = sum(normalized[name] * WEIGHTS[name] for name in WEIGHTS)
    return round(q100, 1), {k: round(v, 1) for k, v in normalized.items()}


# --- Config Hash -------------------------------------------------------------

def compute_config_hash() -> str:
    hasher = hashlib.sha256()
    global_claude = CLAUDE_DIR / "CLAUDE.md"
    if global_claude.exists():
        hasher.update(global_claude.read_bytes())
    project_claude = Path.cwd() / "CLAUDE.md"
    if project_claude.exists():
        hasher.update(project_claude.read_bytes())
    settings = Path.home() / ".claude" / "settings.json"
    if settings.exists():
        hasher.update(settings.read_bytes())
    return hasher.hexdigest()[:12]


# --- Session Discovery -------------------------------------------------------

def get_project_key(project_key: str | None = None) -> str:
    if project_key:
        return project_key
    cwd = str(Path.cwd())
    key = cwd.replace(os.sep, "-").replace(":", "-").replace("/", "-")
    return key


def find_sessions(project_key: str, session_id: str | None = None) -> list[Path]:
    project_dir = PROJECTS_DIR / project_key
    if not project_dir.exists():
        for d in PROJECTS_DIR.iterdir():
            if d.is_dir() and project_key in d.name:
                project_dir = d
                break
        else:
            print(f"Error: No project directory found for '{project_key}'")
            print(f"Available: {[d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]}")
            sys.exit(1)

    if session_id:
        target = project_dir / f"{session_id}.jsonl"
        if target.exists():
            return [target]
        matches = list(project_dir.glob(f"{session_id}*.jsonl"))
        if matches:
            return matches
        print(f"Error: Session '{session_id}' not found in {project_dir}")
        sys.exit(1)

    sessions = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return sessions


# --- Session Metadata --------------------------------------------------------

def extract_metadata(entries: list[dict]) -> dict:
    meta = {"version": "unknown", "model": "unknown", "start": "", "end": ""}
    for entry in entries:
        if entry.get("type") == "system" and entry.get("subtype") == "turn_duration":
            meta["version"] = entry.get("version", meta["version"])
            break
    for entry in entries:
        if entry.get("type") == "assistant":
            model = entry.get("message", {}).get("model", "")
            if model:
                meta["model"] = model
                break
    timestamps = [e.get("timestamp", "") for e in entries if e.get("timestamp")]
    if timestamps:
        meta["start"] = timestamps[0]
        meta["end"] = timestamps[-1]
    return meta


# --- Main Analysis -----------------------------------------------------------

def analyze_session(jsonl_path: Path) -> dict:
    entries = parse_session(jsonl_path)
    if not entries:
        return {"error": "Empty session"}

    tool_calls = extract_tool_calls(entries)
    tool_results = extract_tool_results(entries)
    token_usage = extract_token_usage(entries)
    durations = extract_turn_durations(entries)
    user_indices = extract_user_messages(entries)
    assistant_indices = extract_assistant_messages(entries)
    metadata = extract_metadata(entries)

    raw = {
        "plan_rate": m01_plan_rate(tool_calls, user_indices),
        "subagent_efficiency": m02_subagent_efficiency(tool_calls),
        "tool_diversity": m03_tool_diversity(tool_calls),
        "read_before_edit": m04_read_before_edit(tool_calls),
        "error_rate": m05_error_rate(tool_results, entries),
        "self_correction": m06_self_correction(tool_calls, tool_results),
        "cache_hit_rate": m07_cache_hit_rate(token_usage),
        "token_efficiency": m08_token_efficiency(token_usage),
        "dedicated_tool_usage": m09_dedicated_tool_usage(tool_calls),
        "turn_duration": m10_turn_duration(durations),
        "file_ops_success": m11_file_ops_success(tool_calls, tool_results),
        "completion_depth": m12_completion_depth(entries, user_indices, assistant_indices),
    }

    q100, normalized = compute_q100(raw)

    session_id = jsonl_path.stem
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "q100": q100,
        "metrics": normalized,
        "raw_metrics": {k: round(v, 4) if isinstance(v, float) else v for k, v in raw.items()},
        "token_usage": token_usage,
        "cc_version": metadata["version"],
        "model": metadata["model"],
        "config_hash": compute_config_hash(),
        "session_start": metadata["start"],
        "session_end": metadata["end"],
        "total_entries": len(entries),
        "user_turns": len(user_indices),
        "assistant_turns": len(assistant_indices),
        "tool_calls": len(tool_calls),
    }


def save_score(result: dict):
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")


def print_report(result: dict):
    if "error" in result:
        print(f"  Error: {result['error']}")
        return

    print(f"\n{'='*60}")
    print(f"  Session Quality Report (Q100)")
    print(f"{'='*60}")
    print(f"  Session:  {result['session_id'][:12]}...")
    print(f"  Model:    {result['model']}")
    print(f"  Version:  {result['cc_version']}")
    print(f"  Config:   {result['config_hash']}")
    print(f"  Period:   {result.get('session_start', '?')[:19]} -> {result.get('session_end', '?')[:19]}")
    print(f"  Entries:  {result['total_entries']} ({result['user_turns']} user, {result['assistant_turns']} assistant, {result['tool_calls']} tool calls)")
    print()

    tu = result["token_usage"]
    total_input = tu["input_tokens"] + tu["cache_read"] + tu["cache_creation"]
    print(f"  Tokens:   {total_input:,} input ({tu['cache_read']:,} cached) + {tu['output_tokens']:,} output")
    print()

    q = result["q100"]
    bar_len = int(q / 2)
    bar = "#" * bar_len + "." * (50 - bar_len)
    grade = "A+" if q >= 90 else "A" if q >= 80 else "B" if q >= 70 else "C" if q >= 60 else "D" if q >= 50 else "F"
    print(f"  Q100 = {q:5.1f}  [{bar}]  Grade: {grade}")
    print()

    print(f"  {'Metric':<24} {'Score':>6}  {'Weight':>6}  {'Raw':>10}")
    print(f"  {'-'*24} {'-'*6}  {'-'*6}  {'-'*10}")
    metrics = result["metrics"]
    raw = result["raw_metrics"]
    for name in WEIGHTS:
        score = metrics.get(name, 0)
        weight = WEIGHTS[name]
        raw_val = raw.get(name, 0)
        if isinstance(raw_val, float):
            raw_str = f"{raw_val:.3f}"
        else:
            raw_str = str(raw_val)

        if score >= 80:
            indicator = "+"
        elif score >= 50:
            indicator = "~"
        else:
            indicator = "-"

        print(f"  {indicator} {name:<22} {score:5.1f}  {weight*100:5.0f}%  {raw_str:>10}")

    print(f"\n{'='*60}\n")


def show_trend():
    if not SCORES_FILE.exists():
        print("No historical scores found. Run analysis first.")
        return

    scores = []
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                scores.append(json.loads(line))
            except:
                continue

    if not scores:
        print("No scores found.")
        return

    print(f"\n{'='*60}")
    print(f"  Q100 Trend ({len(scores)} sessions)")
    print(f"{'='*60}\n")

    by_config = {}
    for s in scores:
        ch = s.get("config_hash", "?")
        if ch not in by_config:
            by_config[ch] = []
        by_config[ch].append(s)

    for config_hash, group in by_config.items():
        avg_q = statistics.mean(s["q100"] for s in group)
        print(f"  Config {config_hash}: {len(group)} sessions, avg Q100 = {avg_q:.1f}")

    print()
    print(f"  {'Date':<20} {'Q100':>5} {'Config':>8} {'Model':<30} {'Version':<10}")
    print(f"  {'-'*20} {'-'*5} {'-'*8} {'-'*30} {'-'*10}")

    for s in scores[-20:]:
        ts = s.get("timestamp", "?")[:19]
        q = s["q100"]
        ch = s.get("config_hash", "?")[:8]
        model = s.get("model", "?")[:30]
        ver = s.get("cc_version", "?")[:10]
        bar = "#" * int(q / 5) + "." * (20 - int(q / 5))
        print(f"  {ts} {q:5.1f} {ch:>8} {model:<30} {ver:<10}  {bar}")

    print(f"\n{'='*60}\n")


# --- CLI ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Session Quality Metrics (Q100)")
    parser.add_argument("--session-id", "-s", help="Specific session ID")
    parser.add_argument("--all", "-a", action="store_true", help="Analyze all sessions")
    parser.add_argument("--trend", "-t", action="store_true", help="Show Q100 trend")
    parser.add_argument("--project-key", "-p", help="Project key (default: from CWD)")
    parser.add_argument("--no-save", action="store_true", help="Don't save to telemetry")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    if args.trend:
        show_trend()
        return

    project_key = get_project_key(args.project_key)

    if args.all:
        sessions = find_sessions(project_key)
    elif args.session_id:
        sessions = find_sessions(project_key, args.session_id)
    else:
        sessions = find_sessions(project_key)
        sessions = sessions[:1]

    if not sessions:
        print("No sessions found.")
        sys.exit(1)

    results = []
    for session_path in sessions:
        result = analyze_session(session_path)
        results.append(result)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_report(result)

        if not args.no_save and "error" not in result:
            save_score(result)

    if args.all and len(results) > 1:
        valid = [r for r in results if "error" not in r]
        if valid:
            avg_q = statistics.mean(r["q100"] for r in valid)
            print(f"\n  Average Q100 across {len(valid)} sessions: {avg_q:.1f}")
            print()


if __name__ == "__main__":
    main()
