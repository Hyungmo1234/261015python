#!/usr/bin/env python3
"""전날 공부 활동을 확인해 노트 작성 후 git push (공부량 있을 때만)."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = REPO_ROOT / "notes"
STUDY_LOG = NOTES_DIR / "study-log.md"
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules"}
TRANSCRIPT_ROOTS = [
    Path.home() / ".cursor" / "projects" / "mnt-c-Users-LT-013-261015python" / "agent-transcripts",
    Path("/mnt/c/Users/LT-013/.cursor/projects"),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Publish previous-day study notes to git")
    p.add_argument(
        "--date",
        help="대상 날짜 YYYY-MM-DD (기본: 어제)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="파일/커밋/푸시 없이 동작만 확인",
    )
    p.add_argument(
        "--force-weekend",
        action="store_true",
        help="주말이어도 공부량이 있으면 강제 진행 (기본 동작과 동일하게 공부량 기준)",
    )
    return p.parse_args()


def target_day(args: argparse.Namespace) -> date:
    if args.date:
        return date.fromisoformat(args.date)
    return date.today() - timedelta(days=1)


def is_weekend(d: date) -> bool:
    return d.weekday() >= 5  # Sat=5, Sun=6


def day_bounds(d: date) -> tuple[datetime, datetime]:
    start = datetime.combine(d, datetime.min.time())
    end = datetime.combine(d + timedelta(days=1), datetime.min.time())
    return start, end


def in_day(ts: float, start: datetime, end: datetime) -> bool:
    t = datetime.fromtimestamp(ts)
    return start <= t < end


def collect_activity(d: date) -> list[tuple[Path, datetime]]:
    start, end = day_bounds(d)
    found: list[tuple[Path, datetime]] = []

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        root_path = Path(root)
        if root_path == NOTES_DIR:
            # 노트 자동 생성물 순환 참조 방지: 기존 수동 노트만 참고
            pass
        for name in files:
            path = root_path / name
            if path.suffix.lower() not in {".py", ".md", ".log", ".txt"}:
                continue
            if path.name.startswith("."):
                continue
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if in_day(mtime, start, end):
                found.append((path, datetime.fromtimestamp(mtime)))

    for base in TRANSCRIPT_ROOTS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".jsonl", ".txt", ".md", ".log"}:
                continue
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if in_day(mtime, start, end):
                found.append((path, datetime.fromtimestamp(mtime)))

    found.sort(key=lambda x: x[1])
    return found


def estimate_window(items: list[tuple[Path, datetime]]) -> tuple[str, str, str]:
    if not items:
        return "-", "-", "-"
    first = items[0][1]
    last = items[-1][1]
    minutes = max(int((last - first).total_seconds() // 60), 1)
    hours, mins = divmod(minutes, 60)
    if hours:
        duration = f"약 {hours}시간 {mins}분" if mins else f"약 {hours}시간"
    else:
        duration = f"약 {mins}분"
    return first.strftime("%H:%M"), last.strftime("%H:%M"), duration


def note_path(d: date) -> Path:
    return NOTES_DIR / f"{d.isoformat()}-study.md"


def build_note(d: date, items: list[tuple[Path, datetime]]) -> str:
    start_s, end_s, duration = estimate_window(items)
    rel_files: list[str] = []
    for path, _ in items:
        try:
            rel = path.relative_to(REPO_ROOT)
            rel_files.append(str(rel))
        except ValueError:
            rel_files.append(str(path))

    # 중복 제거, 순서 유지
    seen: set[str] = set()
    unique_files: list[str] = []
    for f in rel_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    file_lines = "\n".join(f"- `{f}`" for f in unique_files[:40]) or "- (파일 목록 없음)"

    return f"""# {d.isoformat()} 공부 노트

> 날짜: {d.isoformat()} ({['월','화','수','목','금','토','일'][d.weekday()]})  
> 공부 시간: {start_s} ~ {end_s} ({duration})  
> 생성: 자동 (다음날 12:30 배치)

전날 활동 로그·파일 변경을 기준으로 초안을 만들었습니다.  
필요하면 주제/핵심 내용을 이어서 보완하세요.

## 활동 파일

{file_lines}

## 메모

- (자동 초안) Cursor/프로젝트 파일 변경 시각으로 시간대를 추정했습니다.
- 대화 요약이 필요하면 해당일 agent transcript를 추가로 정리하면 됩니다.
"""


def ensure_study_log_header() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    if not STUDY_LOG.exists():
        STUDY_LOG.write_text(
            "# 공부 시간 기록\n\n"
            "| 날짜 | 시간대 | 소요 | 주제 | 노트 |\n"
            "|------|--------|------|------|------|\n",
            encoding="utf-8",
        )


def append_study_log(d: date, start_s: str, end_s: str, duration: str, note: Path) -> None:
    ensure_study_log_header()
    text = STUDY_LOG.read_text(encoding="utf-8")
    marker = f"| {d.isoformat()} |"
    if marker in text:
        return
    link = f"[{note.name}](./{note.name})"
    row = f"| {d.isoformat()} | {start_s} ~ {end_s} | {duration} | (자동 초안) | {link} |\n"
    if not text.endswith("\n"):
        text += "\n"
    STUDY_LOG.write_text(text + row, encoding="utf-8")


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", env.get("GIT_AUTHOR_NAME", "study-bot"))
    env.setdefault("GIT_AUTHOR_EMAIL", env.get("GIT_AUTHOR_EMAIL", "study-bot@local"))
    env.setdefault("GIT_COMMITTER_NAME", env["GIT_AUTHOR_NAME"])
    env.setdefault("GIT_COMMITTER_EMAIL", env["GIT_AUTHOR_EMAIL"])
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def publish(d: date, note: Path, dry_run: bool) -> int:
    msg = f"Add study note for {d.isoformat()}"
    if dry_run:
        print(f"[dry-run] would commit/push: {msg}")
        return 0

    add = run_git(["add", str(note.relative_to(REPO_ROOT)), str(STUDY_LOG.relative_to(REPO_ROOT))])
    if add.returncode != 0:
        print(add.stderr, file=sys.stderr)
        return add.returncode

    status = run_git(["status", "--porcelain"])
    if not status.stdout.strip():
        print("변경 사항 없음 — push 생략")
        return 0

    commit = run_git(["commit", "-m", msg])
    if commit.returncode != 0:
        print(commit.stdout)
        print(commit.stderr, file=sys.stderr)
        return commit.returncode

    push = run_git(["push", "origin", "HEAD"])
    if push.returncode != 0:
        print(push.stdout)
        print(push.stderr, file=sys.stderr)
        return push.returncode

    print(f"푸시 완료: {d.isoformat()} → {note.name}")
    return 0


def main() -> int:
    args = parse_args()
    d = target_day(args)
    print(f"대상 날짜: {d.isoformat()} ({'주말' if is_weekend(d) else '평일'})")

    items = collect_activity(d)
    if not items:
        print("공부량 없음 — 노트/깃 작업 생략")
        return 0

    # 주말이어도 공부량이 있으면 등록 (요청사항)
    if is_weekend(d):
        print("주말 + 공부량 감지 → 등록 진행")

    start_s, end_s, duration = estimate_window(items)
    out = note_path(d)

    if out.exists() and not args.dry_run:
        # 이미 있으면 로그 행만 보완 시도 후, 내용 변경 없으면 push 스킵될 수 있음
        print(f"노트 이미 존재: {out.name} (내용 유지, 로그/푸시만 확인)")
    else:
        content = build_note(d, items)
        if args.dry_run:
            print("--- note preview ---")
            print(content)
        else:
            NOTES_DIR.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")
            print(f"노트 작성: {out}")

    if not args.dry_run:
        append_study_log(d, start_s, end_s, duration, out)
    else:
        print(f"[dry-run] study-log row: {d} | {start_s}~{end_s} | {duration}")

    return publish(d, out, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
