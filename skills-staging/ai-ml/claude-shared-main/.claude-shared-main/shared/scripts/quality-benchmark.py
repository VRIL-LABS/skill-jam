#!/usr/bin/env python3
"""
Quality Benchmark System (Part B) — from supraforge-mueller/.claude
Scores Claude Code session JSONL files against 8 benchmark tasks.
Semi-manual: user runs tasks in a session, then this script scores the session.

Usage:
    python3 ~/.claude/scripts/quality-benchmark.py score [--session-id ID]   # Score a session
    python3 ~/.claude/scripts/quality-benchmark.py set-baseline              # Set current as baseline
    python3 ~/.claude/scripts/quality-benchmark.py trend                     # Show BQ100 trend
    python3 ~/.claude/scripts/quality-benchmark.py tasks                     # List benchmark tasks
    python3 ~/.claude/scripts/quality-benchmark.py compare                   # Compare latest vs baseline
"""

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

CLAUDE_DIR = Path.home() / ".claude"
TELEMETRY_DIR = CLAUDE_DIR / "telemetry"
TASKS_FILE = TELEMETRY_DIR / "benchmark_tasks.json"
RESULTS_FILE = TELEMETRY_DIR / "benchmark_results.jsonl"
BASELINE_FILE = TELEMETRY_DIR / "benchmark_baseline.json"
PROJECTS_DIR = CLAUDE_DIR / "projects"

REGRESSION_TOLERANCE = 2.0  # +/- points considered STABLE


# ── JSONL Parser ─────────────────────────────────────────────────────────────

def parse_session(jsonl_path: Path) -> list[dict]:
    """Parse a session JSONL file."""
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


def get_project_key() -> str:
    """Get project key from CWD."""
    cwd = str(Path.cwd())
    return cwd.replace(os.sep, "-").replace(":", "-").replace("/", "-")


def find_latest_session() -> Path | None:
    """Find the most recent session JSONL."""
    project_key = get_project_key()
    project_dir = PROJECTS_DIR / project_key
    if not project_dir.exists():
        for d in PROJECTS_DIR.iterdir():
            if d.is_dir() and project_key in d.name:
                project_dir = d
                break
        else:
            return None
    sessions = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return sessions[0] if sessions else None


def find_session(session_id: str) -> Path | None:
    """Find a specific session by ID."""
    project_key = get_project_key()
    project_dir = PROJECTS_DIR / project_key
    if not project_dir.exists():
        for d in PROJECTS_DIR.iterdir():
            if d.is_dir() and project_key in d.name:
                project_dir = d
                break
        else:
            return None
    target = project_dir / f"{session_id}.jsonl"
    if target.exists():
        return target
    matches = list(project_dir.glob(f"{session_id}*.jsonl"))
    return matches[0] if matches else None


# ── Task Detection ───────────────────────────────────────────────────────────

def extract_conversations(entries: list[dict]) -> list[dict]:
    """Extract user-prompt -> assistant-response pairs with tool calls."""
    conversations = []
    current = None

    for entry in entries:
        if entry.get("type") == "user":
            msg = entry.get("message", {})
            user_text = ""

            if isinstance(msg, dict):
                content = msg.get("content", "")
                if isinstance(content, str):
                    user_text = content.strip()
                elif isinstance(content, list):
                    text_parts = []
                    has_tool_result = False
                    for b in content:
                        if isinstance(b, dict):
                            if b.get("type") == "text":
                                text_parts.append(b.get("text", ""))
                            elif b.get("type") == "tool_result":
                                has_tool_result = True
                                if current:
                                    current["tool_results"][b.get("tool_use_id", "")] = {
                                        "is_error": b.get("is_error", False),
                                    }
                    user_text = " ".join(text_parts).strip()
                    if has_tool_result and not user_text:
                        continue
            else:
                user_text = str(msg).strip()

            if user_text.startswith("<task-notification>"):
                continue

            if user_text and len(user_text) > 5:
                if current:
                    conversations.append(current)
                current = {
                    "user_text": user_text,
                    "assistant_texts": [],
                    "tool_calls": [],
                    "tool_results": {},
                }

        elif entry.get("type") == "assistant" and current:
            msg = entry.get("message", {})
            for block in msg.get("content", []):
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        current["assistant_texts"].append(block.get("text", ""))
                    elif block.get("type") == "tool_use":
                        current["tool_calls"].append({
                            "name": block.get("name", ""),
                            "id": block.get("id", ""),
                            "input": block.get("input", {}),
                        })

    if current:
        conversations.append(current)

    return conversations


def match_task(user_text: str, task: dict) -> float:
    """Score how well a user message matches a benchmark task prompt (0-1)."""
    prompt_lower = task["prompt"].lower()
    user_lower = user_text.lower()

    key_words = set(re.findall(r'\b\w{4,}\b', prompt_lower))
    user_words = set(re.findall(r'\b\w{4,}\b', user_lower))

    if not key_words:
        return 0.0

    overlap = len(key_words & user_words)
    return overlap / len(key_words)


# ── Scoring Functions ────────────────────────────────────────────────────────

def score_keyword_presence(test_config: dict, full_text: str) -> float:
    keywords = test_config.get("required_keywords", [])
    min_needed = test_config.get("min_keywords", len(keywords))
    if not keywords:
        return 100.0
    found = sum(1 for kw in keywords if kw.lower() in full_text.lower())
    return min(100.0, (found / max(1, min_needed)) * 100)


def score_tool_usage(test_config: dict, conv: dict) -> float:
    tool_names = [t["name"] for t in conv["tool_calls"]]
    tool_set = set(tool_names)
    score = 0.0
    total_checks = 0

    required = test_config.get("required_tools", [])
    if required:
        total_checks += 1
        found = sum(1 for t in required if t in tool_set)
        score += (found / len(required)) * 100

    preferred = test_config.get("preferred_tools", [])
    if preferred:
        total_checks += 1
        found = sum(1 for t in preferred if t in tool_set)
        score += (found / len(preferred)) * 100

    required_seq = test_config.get("required_sequence", [])
    if required_seq:
        total_checks += 1
        seq_idx = 0
        for t in tool_names:
            if seq_idx < len(required_seq) and t == required_seq[seq_idx]:
                seq_idx += 1
        score += (seq_idx / len(required_seq)) * 100

    anti = test_config.get("anti_patterns", [])
    if anti:
        total_checks += 1
        violations = 0
        for pattern in anti:
            if ":" in pattern:
                tool, cmd_pattern = pattern.split(":", 1)
                for t in conv["tool_calls"]:
                    if t["name"] == tool:
                        cmd = t["input"].get("command", "")
                        if cmd_pattern.lower() in cmd.lower():
                            violations += 1
            elif pattern in tool_set:
                violations += 1
        score += max(0, 100 - violations * 50)

    min_tools = test_config.get("min_tools")
    if min_tools:
        total_checks += 1
        score += min(100, (len(tool_set) / min_tools) * 100)

    return score / max(1, total_checks)


def score_response_quality(test_config: dict, full_text: str) -> float:
    score = 100.0
    min_len = test_config.get("min_length", 0)
    max_len = test_config.get("max_length", float("inf"))
    text_len = len(full_text)

    if text_len < min_len:
        score *= text_len / max(1, min_len)
    if text_len > max_len:
        score *= max(0, 1 - (text_len - max_len) / max_len)

    markers = test_config.get("structure_markers", [])
    if markers:
        found = sum(1 for m in markers if m in full_text)
        structure_score = (found / len(markers)) * 100
        score = (score + structure_score) / 2

    return min(100.0, score)


def score_completeness(test_config: dict, full_text: str) -> float:
    gt_count = test_config.get("ground_truth_count", 1)
    paths = re.findall(r'[\w/\\_]+\.py', full_text)
    unique_paths = len(set(paths))
    return min(100.0, (unique_paths / gt_count) * 100)


def score_diff_check(test_config: dict, conv: dict) -> float:
    score = 100.0
    target = test_config.get("target_file", "")
    if target:
        edited = any(
            t["name"] == "Edit" and target.replace("/", "\\") in t["input"].get("file_path", "").replace("/", "\\")
            or t["name"] == "Edit" and target in t["input"].get("file_path", "")
            for t in conv["tool_calls"]
        )
        if not edited:
            score *= 0.3

    must_contain = test_config.get("must_contain", "")
    if must_contain:
        found = any(
            must_contain in t["input"].get("new_string", "")
            for t in conv["tool_calls"]
            if t["name"] == "Edit"
        )
        if not found:
            score *= 0.5

    return score


def score_diff_minimal(test_config: dict, conv: dict) -> float:
    max_added = test_config.get("max_added_lines", 10)
    max_removed = test_config.get("max_removed_lines", 5)

    total_added = 0
    total_removed = 0
    for t in conv["tool_calls"]:
        if t["name"] == "Edit":
            new = t["input"].get("new_string", "")
            old = t["input"].get("old_string", "")
            total_added += len(new.split("\n"))
            total_removed += len(old.split("\n"))

    score = 100.0
    if total_added > max_added:
        score *= max_added / total_added
    if total_removed > max_removed and max_removed > 0:
        score *= max_removed / total_removed

    return min(100.0, score)


# ── Score a Test ─────────────────────────────────────────────────────────────

def score_test(test_config: dict, conv: dict) -> float:
    full_text = " ".join(conv["assistant_texts"])
    test_type = test_config.get("type", "")

    if test_type == "keyword_presence":
        return score_keyword_presence(test_config, full_text)
    elif test_type == "tool_usage":
        return score_tool_usage(test_config, conv)
    elif test_type == "response_quality":
        return score_response_quality(test_config, full_text)
    elif test_type == "grep_ground_truth":
        return score_keyword_presence(test_config, full_text)
    elif test_type == "completeness":
        return score_completeness(test_config, full_text)
    elif test_type == "diff_check":
        return score_diff_check(test_config, conv)
    elif test_type == "diff_minimal":
        return score_diff_minimal(test_config, conv)
    else:
        return 50.0


# ── Main Scoring ─────────────────────────────────────────────────────────────

def score_session(session_path: Path) -> dict:
    tasks_data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    tasks = tasks_data["tasks"]
    entries = parse_session(session_path)
    conversations = extract_conversations(entries)

    if not conversations:
        return {"error": "No conversations found in session"}

    results = []
    for task in tasks:
        best_match = 0.0
        best_conv = None
        for conv in conversations:
            sim = match_task(conv["user_text"], task)
            if sim > best_match:
                best_match = sim
                best_conv = conv

        if best_match < 0.15 or not best_conv:
            results.append({
                "task_id": task["id"],
                "task_name": task["name"],
                "matched": False,
                "match_score": 0,
                "correctness": 0,
                "methodology": 0,
                "quality": 0,
                "avg": 0,
            })
            continue

        correctness = score_test(task["tests"]["correctness"], best_conv)
        methodology = score_test(task["tests"]["methodology"], best_conv)
        quality = score_test(task["tests"]["quality"], best_conv)
        avg = (correctness + methodology + quality) / 3

        results.append({
            "task_id": task["id"],
            "task_name": task["name"],
            "matched": True,
            "match_score": round(best_match, 3),
            "correctness": round(correctness, 1),
            "methodology": round(methodology, 1),
            "quality": round(quality, 1),
            "avg": round(avg, 1),
        })

    matched_tasks = [r for r in results if r["matched"]]
    bq100 = statistics.mean(r["avg"] for r in matched_tasks) if matched_tasks else 0

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_path.stem,
        "bq100": round(bq100, 1),
        "tasks_matched": len(matched_tasks),
        "tasks_total": len(tasks),
        "task_results": results,
    }


# ── Output ───────────────────────────────────────────────────────────────────

def print_score_report(result: dict):
    if "error" in result:
        print(f"  Error: {result['error']}")
        return

    print(f"\n{'='*65}")
    print(f"  Benchmark Quality Report (BQ100)")
    print(f"{'='*65}")
    print(f"  Session:  {result['session_id'][:12]}...")
    print(f"  Tasks:    {result['tasks_matched']}/{result['tasks_total']} matched")
    print()

    bq = result["bq100"]
    bar_len = int(bq / 2)
    bar = "#" * bar_len + "." * (50 - bar_len)
    grade = "A+" if bq >= 90 else "A" if bq >= 80 else "B" if bq >= 70 else "C" if bq >= 60 else "D" if bq >= 50 else "F"
    print(f"  BQ100 = {bq:5.1f}  [{bar}]  Grade: {grade}")
    print()

    print(f"  {'ID':<4} {'Task':<24} {'Match':>5} {'Correct':>7} {'Method':>7} {'Quality':>7} {'Avg':>6}")
    print(f"  {'--':<4} {'-'*24} {'-----':>5} {'-------':>7} {'-------':>7} {'-------':>7} {'------':>6}")

    for t in result["task_results"]:
        if t["matched"]:
            ind = "+" if t["avg"] >= 80 else "~" if t["avg"] >= 50 else "-"
            ms = f"{t['match_score']:.1%}"
        else:
            ind = "x"
            ms = "  -- "
        print(f"  {ind} {t['task_id']:<2} {t['task_name']:<22} {ms:>5} {t['correctness']:6.1f} {t['methodology']:6.1f} {t['quality']:6.1f} {t['avg']:6.1f}")

    print(f"\n{'='*65}")

    if BASELINE_FILE.exists():
        baseline = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
        base_bq = baseline.get("bq100", 0)
        delta = bq - base_bq

        if abs(delta) <= REGRESSION_TOLERANCE:
            status = "STABLE"
        elif delta > 0:
            status = "IMPROVEMENT"
        else:
            status = "REGRESSION"

        delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"
        print(f"\n  vs Baseline: {base_bq:.1f} -> {bq:.1f} ({delta_str}) = {status}")
        print()


def save_result(result: dict):
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")


def set_baseline():
    if not RESULTS_FILE.exists():
        print("No benchmark results found. Run 'score' first.")
        return

    last_line = ""
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last_line = line

    if not last_line:
        print("No results found.")
        return

    result = json.loads(last_line)
    BASELINE_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"  Baseline set: BQ100 = {result['bq100']}")
    print(f"  Session: {result['session_id']}")
    print(f"  Tasks matched: {result['tasks_matched']}/{result['tasks_total']}")


def show_trend():
    if not RESULTS_FILE.exists():
        print("No benchmark results found.")
        return

    results = []
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                results.append(json.loads(line))
            except:
                continue

    print(f"\n{'='*65}")
    print(f"  BQ100 Trend ({len(results)} runs)")
    print(f"{'='*65}\n")

    print(f"  {'Date':<20} {'BQ100':>5} {'Matched':>7} {'Session':<14}")
    print(f"  {'-'*20} {'-'*5} {'-'*7} {'-'*14}")

    for r in results[-20:]:
        ts = r.get("timestamp", "?")[:19]
        bq = r["bq100"]
        matched = f"{r['tasks_matched']}/{r['tasks_total']}"
        sid = r["session_id"][:12]
        bar = "#" * int(bq / 5) + "." * (20 - int(bq / 5))
        print(f"  {ts} {bq:5.1f} {matched:>7} {sid}  {bar}")

    if len(results) >= 2:
        first = results[0]["bq100"]
        last = results[-1]["bq100"]
        delta = last - first
        print(f"\n  Overall trend: {first:.1f} -> {last:.1f} ({'+' if delta > 0 else ''}{delta:.1f})")

    print(f"\n{'='*65}\n")


def show_tasks():
    tasks_data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))

    print(f"\n{'='*65}")
    print(f"  Benchmark Tasks ({len(tasks_data['tasks'])} tasks)")
    print(f"{'='*65}\n")

    for task in tasks_data["tasks"]:
        print(f"  {task['id']}: {task['name']}")
        prompt = task["prompt"]
        if len(prompt) > 80:
            prompt = prompt[:77] + "..."
        print(f"     {prompt}")
        print()

    print("  To run benchmark: execute these tasks in a Claude Code session,")
    print("  then score with: python3 ~/.claude/scripts/quality-benchmark.py score")
    print()


def compare():
    if not BASELINE_FILE.exists():
        print("No baseline set. Run 'set-baseline' first.")
        return

    if not RESULTS_FILE.exists():
        print("No results found. Run 'score' first.")
        return

    baseline = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    last_line = ""
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last_line = line
    latest = json.loads(last_line)

    print(f"\n{'='*65}")
    print(f"  Baseline vs Latest Comparison")
    print(f"{'='*65}\n")

    base_bq = baseline["bq100"]
    lat_bq = latest["bq100"]
    delta = lat_bq - base_bq

    if abs(delta) <= REGRESSION_TOLERANCE:
        status = "STABLE"
    elif delta > 0:
        status = "IMPROVEMENT"
    else:
        status = "REGRESSION"

    print(f"  Baseline BQ100:  {base_bq:5.1f}  (session: {baseline['session_id'][:12]})")
    print(f"  Latest BQ100:    {lat_bq:5.1f}  (session: {latest['session_id'][:12]})")
    print(f"  Delta:           {'+' if delta > 0 else ''}{delta:.1f}  = {status}")
    print()

    base_tasks = {t["task_id"]: t for t in baseline.get("task_results", [])}
    lat_tasks = {t["task_id"]: t for t in latest.get("task_results", [])}

    print(f"  {'Task':<26} {'Baseline':>8} {'Latest':>8} {'Delta':>8}")
    print(f"  {'-'*26} {'-'*8} {'-'*8} {'-'*8}")

    for tid in sorted(set(list(base_tasks.keys()) + list(lat_tasks.keys()))):
        bt = base_tasks.get(tid, {})
        lt = lat_tasks.get(tid, {})
        b_avg = bt.get("avg", 0) if bt.get("matched") else 0
        l_avg = lt.get("avg", 0) if lt.get("matched") else 0
        d = l_avg - b_avg
        name = bt.get("task_name", lt.get("task_name", tid))
        d_str = f"+{d:.1f}" if d > 0 else f"{d:.1f}"
        print(f"  {tid} {name:<22} {b_avg:7.1f} {l_avg:7.1f} {d_str:>8}")

    print(f"\n{'='*65}\n")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Quality Benchmark System (BQ100)")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    score_parser = subparsers.add_parser("score", help="Score a session")
    score_parser.add_argument("--session-id", "-s", help="Session ID")
    score_parser.add_argument("--no-save", action="store_true", help="Don't save result")
    score_parser.add_argument("--json", action="store_true", help="Output JSON")

    subparsers.add_parser("set-baseline", help="Set latest result as baseline")
    subparsers.add_parser("trend", help="Show BQ100 trend")
    subparsers.add_parser("tasks", help="List benchmark tasks")
    subparsers.add_parser("compare", help="Compare latest vs baseline")

    args = parser.parse_args()

    if args.command == "score":
        if args.session_id:
            session_path = find_session(args.session_id)
        else:
            session_path = find_latest_session()

        if not session_path:
            print("Session not found.")
            sys.exit(1)

        result = score_session(session_path)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_score_report(result)

        if not args.no_save and "error" not in result:
            save_result(result)

    elif args.command == "set-baseline":
        set_baseline()

    elif args.command == "trend":
        show_trend()

    elif args.command == "tasks":
        show_tasks()

    elif args.command == "compare":
        compare()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
