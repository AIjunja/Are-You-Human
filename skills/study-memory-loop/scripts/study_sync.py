#!/usr/bin/env python3
"""Append a minimal study packet, commit only the study ledger, and optionally push."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=check
    )


def slugify(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z가-힣]+", "-", value.strip().lower()).strip("-")
    return value[:70] or "untitled"


def repo_root(candidate: str | None) -> Path:
    path = Path(
        candidate
        or os.environ.get("STUDY_MEMORY_REPO")
        or os.environ.get("CODEX_STUDY_REPO")
        or Path.cwd()
    ).expanduser().resolve()
    result = run_git(path, "rev-parse", "--show-toplevel")
    return Path(result.stdout.strip()).resolve()


def load_packet(path: str | None, raw: str | None) -> dict:
    if path:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    elif raw:
        data = json.loads(raw)
    else:
        data = json.load(os.sys.stdin)
    required = ("topic", "title", "summary", "facts", "recall_prompt", "recall_result")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError("missing fields: " + ", ".join(missing))
    if not isinstance(data["facts"], list) or not data["facts"]:
        raise ValueError("facts must be a non-empty list")
    data.setdefault("misconceptions", [])
    data.setdefault("tags", [])
    data.setdefault("next_review", (dt.date.today() + dt.timedelta(days=1)).isoformat())
    data["recorded_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    return data


def append_unique(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="study Git repository")
    parser.add_argument("--packet", help="JSON packet file; stdin if omitted")
    parser.add_argument("--packet-json", help="inline JSON packet")
    parser.add_argument("--push", action="store_true", help="push after commit")
    args = parser.parse_args()

    repo = repo_root(args.repo)
    packet = load_packet(args.packet, args.packet_json)
    ledger = repo / "study-ledger"
    topic_slug = slugify(str(packet["topic"]))
    title = str(packet["title"]).strip()
    date = str(packet["recorded_at"])[:10]
    packet_id = f"{date}-{topic_slug}-{slugify(title)[:40]}"

    (ledger / "packets").mkdir(parents=True, exist_ok=True)
    packet_path = ledger / "packets" / f"{packet_id}.json"
    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    topic_path = ledger / "topics" / f"{topic_slug}.md"
    facts = "\n".join(f"- {item}" for item in packet["facts"])
    misconceptions = "\n".join(f"- {item}" for item in packet["misconceptions"]) or "- 없음"
    entry = (
        f"## {date} · {title}\n\n"
        f"**요약**: {packet['summary']}\n\n"
        f"**핵심**\n{facts}\n\n"
        f"**회상 질문**: {packet['recall_prompt']}\n\n"
        f"**회상 결과**: {packet['recall_result']}\n\n"
        f"**혼동**\n{misconceptions}\n\n"
        f"**다음 복습**: {packet['next_review']}\n"
    )
    if not topic_path.exists():
        topic_path.parent.mkdir(parents=True, exist_ok=True)
        topic_path.write_text(f"# {packet['topic']}\n\n", encoding="utf-8")
    append_unique(topic_path, entry)

    queue_path = ledger / "review-queue.jsonl"
    append_unique(queue_path, json.dumps({
        "id": packet_id,
        "topic": packet["topic"],
        "title": title,
        "due": packet["next_review"],
        "result": packet["recall_result"],
        "tags": packet["tags"],
    }, ensure_ascii=False))

    index = ledger / "index.md"
    if not index.exists():
        index.write_text("# Study Ledger\n\n학습 주제별 최소 기억 패킷과 복습 큐.\n\n## Topics\n", encoding="utf-8")
    existing = index.read_text(encoding="utf-8")
    marker = f"- [{packet['topic']}](topics/{topic_slug}.md)"
    if marker not in existing:
        index.write_text(existing.rstrip() + "\n" + marker + "\n", encoding="utf-8")

    run_git(repo, "add", "--", "study-ledger")
    staged = run_git(repo, "diff", "--cached", "--name-only").stdout.strip()
    if not staged:
        print(json.dumps({"status": "unchanged", "repo": str(repo)}, ensure_ascii=False))
        return 0
    message = f"study: {packet['topic']} - {title}"[:120]
    run_git(repo, "commit", "-m", message)

    config_path = ledger / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    pushed = False
    if args.push or config.get("auto_push") is True:
        remotes = run_git(repo, "remote", check=False).stdout.splitlines()
        if remotes:
            branch = run_git(repo, "branch", "--show-current").stdout.strip()
            if branch:
                remote = "origin" if "origin" in remotes else remotes[0]
                run_git(repo, "push", remote, branch)
                pushed = True
    print(json.dumps({"status": "synced", "repo": str(repo), "commit": message, "pushed": pushed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
