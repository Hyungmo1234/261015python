#!/usr/bin/env python3
"""전날 공부/수업 활동을 모아 day 요약 노트를 쓰고, 공부량이 있으면 git push.

Cursor Agent 없이 Windows 작업 스케줄러로 동작한다.
C:\\Users\\LT-013 아래 새 폴더가 생기면 프로그램 소스인지 판별해,
맞으면 기존 작업물과 같이 추적·기록·요약한다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = REPO_ROOT / "notes"
STUDY_LOG = NOTES_DIR / "study-log.md"
LOG_DIR = REPO_ROOT / "logs"

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "AppData",
    ".cache",
    "audio",
    "site-packages",
    ".cursor",
    ".vscode",
    ".vscode-shared",
    ".copilot",
    ".local",
    ".grokbot",
}

# C:\Users\LT-013 아래 작업 폴더 탐색
USER_HOME_CANDIDATES = [
    Path("/mnt/c/Users/LT-013"),
    Path(r"C:\Users\LT-013"),
]

# 홈 바로 아래 / Desktop 에서 제외할 이름 (프로그램 소스 후보가 아님)
SKIP_TOP_LEVEL = {
    "AppData",
    "Application Data",
    "Cookies",
    "Local Settings",
    "NetHood",
    "PrintHood",
    "Recent",
    "SendTo",
    "Templates",
    "My Documents",
    "Contacts",
    "Favorites",
    "Links",
    "Music",
    "Videos",
    "Searches",
    "Saved Games",
    "OneDrive",
    "Downloads",
    "Documents",
    "Pictures",
    "사진",
    "문서",
    "Desktop",  # Desktop 자체는 스캔 루트가 아니라, 그 안 하위 폴더를 따로 본다
    ".cache",
    ".cursor",
    ".vscode",
    ".vscode-shared",
    ".copilot",
    ".local",
    ".grokbot",
}

TRANSCRIPT_CANDIDATES = [
    Path.home() / ".cursor" / "projects",
    Path("/mnt/c/Users/LT-013/.cursor/projects"),
    Path(r"C:\Users\LT-013\.cursor\projects"),
    Path(r"\\wsl$\Ubuntu\home\lt-013\.cursor\projects"),
]

WEEKDAY_KR = ["월", "화", "수", "목", "금", "토", "일"]

# 활동 파일로 기록·요약에 넣는 확장자 (기존과 동일하게 md/로그 포함)
ACTIVITY_SUFFIXES = {".py", ".md", ".js", ".ts", ".tsx", ".jsx", ".css", ".html", ".json", ".bat", ".cmd", ".ps1", ".txt", ".log"}

# 프로그램 소스 프로젝트 판별용
SOURCE_SUFFIXES = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs",
    ".java", ".kt", ".go", ".rs", ".c", ".cc", ".cpp", ".h", ".hpp",
    ".cs", ".swift", ".rb", ".php", ".scala",
    ".vue", ".svelte", ".css", ".scss", ".html",
    ".bat", ".cmd", ".ps1", ".sh",
}
SOURCE_MARKERS = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "Pipfile",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "CMakeLists.txt",
    "Makefile",
    "Gemfile",
    "composer.json",
    "manifest.json",  # 크롬 확장 등
    "tsconfig.json",
}

TRACKED_FILE = NOTES_DIR / "tracked-projects.json"

def user_home() -> Path | None:
    for p in USER_HOME_CANDIDATES:
        if p.exists():
            return p
    return None



def storage_key(path: Path | str) -> str:
    """추적 목록 공통 키: 항상 C:/Users/... 문자열."""
    s = str(path).replace("\\", "/")
    if "/C:/" in s:
        s = "C:/" + s.split("/C:/")[-1]
    if s.startswith("/mnt/c/"):
        return "C:/" + s[len("/mnt/c/"):]
    if len(s) >= 2 and s[1] == ":":
        return s[0].upper() + ":" + s[2:]
    try:
        resolved = str(Path(path).resolve()).replace("\\", "/")
    except OSError:
        return s
    if "/C:/" in resolved:
        resolved = "C:/" + resolved.split("/C:/")[-1]
    if resolved.startswith("/mnt/c/"):
        return "C:/" + resolved[len("/mnt/c/"):]
    return resolved


def local_path(key_or_path: Path | str) -> Path | None:
    """현재 환경에서 walk 가능한 실제 경로."""
    key = storage_key(key_or_path)
    if not (len(key) >= 2 and key[1] == ":"):
        cand = Path(str(key_or_path))
        return cand if cand.exists() else None
    rest = key[3:].lstrip("/")
    candidates = [Path("/mnt/c") / rest]
    if os.name == "nt":
        candidates.insert(0, Path(key))
    for c in candidates:
        try:
            if c.exists():
                return c
        except OSError:
            continue
    return None



def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Publish previous-day study notes to git")
    p.add_argument("--date", help="대상 날짜 YYYY-MM-DD (기본: 어제)")
    p.add_argument("--dry-run", action="store_true", help="파일/커밋/푸시 없이 미리보기")
    p.add_argument(
        "--force",
        action="store_true",
        help="기존 day 노트가 있어도 덮어쓴다",
    )
    p.add_argument(
        "--no-push",
        action="store_true",
        help="노트만 작성하고 git push는 생략",
    )
    return p.parse_args()


def target_day(args: argparse.Namespace) -> date:
    if args.date:
        return date.fromisoformat(args.date)
    return date.today() - timedelta(days=1)


def is_weekend(d: date) -> bool:
    return d.weekday() >= 5


def day_bounds(d: date) -> tuple[datetime, datetime]:
    start = datetime.combine(d, datetime.min.time())
    end = datetime.combine(d + timedelta(days=1), datetime.min.time())
    return start, end


def in_day(ts: float, start: datetime, end: datetime) -> bool:
    t = datetime.fromtimestamp(ts)
    return start <= t < end


def load_tracked() -> list[str]:
    if not TRACKED_FILE.exists():
        return []
    try:
        data = json.loads(TRACKED_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(data, dict):
        return [str(x) for x in data.get("projects", [])]
    if isinstance(data, list):
        return [str(x) for x in data]
    return []


def save_tracked(keys: list[str]) -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    clean = sorted({storage_key(k) for k in keys if local_path(k) is not None}, key=str.lower)
    payload = {
        "updated": datetime.now().isoformat(timespec="seconds"),
        "rule": "C:\\Users\\LT-013(+Desktop) 하위 폴더 중 프로그램 소스로 판별된 것만 추적",
        "projects": clean,
    }
    TRACKED_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_folders(home: Path) -> list[Path]:
    """홈 바로 아래 + Desktop 바로 아래 폴더 후보."""
    out: list[Path] = []
    try:
        for child in home.iterdir():
            if not child.is_dir():
                continue
            name = child.name
            if name.startswith(".") or name in SKIP_TOP_LEVEL:
                continue
            out.append(child)
    except OSError:
        pass

    desktop = home / "Desktop"
    if desktop.is_dir():
        try:
            for child in desktop.iterdir():
                if not child.is_dir() or child.name.startswith("."):
                    continue
                out.append(child)
        except OSError:
            pass
    return out


def is_program_source_project(folder: Path, max_files: int = 400) -> bool:
    """폴더가 프로그램 소스 작업물인지 휴리스틱으로 판별."""
    if not folder.is_dir():
        return False
    markers = {m.lower() for m in SOURCE_MARKERS}
    seen = 0
    try:
        for dirpath, dirs, files in os.walk(folder):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")]
            for name in files:
                seen += 1
                if seen > max_files:
                    return False
                if name.lower() in markers:
                    return True
                if Path(name).suffix.lower() in SOURCE_SUFFIXES:
                    return True
    except OSError:
        return False
    return False


def discover_program_projects() -> tuple[list[str], list[str]]:
    """(추적 키 목록, 신규 편입 키). 키는 C:/Users/... 문자열."""
    home = user_home()
    keys: set[str] = set()

    for s in load_tracked():
        if local_path(s) is not None:
            keys.add(storage_key(s))

    keys.add(storage_key(REPO_ROOT))

    newly: list[str] = []
    if home:
        for cand in candidate_folders(home):
            key = storage_key(cand)
            if key in keys:
                continue
            if is_program_source_project(cand):
                keys.add(key)
                newly.append(key)

    return sorted(keys, key=str.lower), newly



def existing_transcript_roots() -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()
    for base in TRANSCRIPT_CANDIDATES:
        try:
            if not base.exists():
                continue
            key = str(base.resolve())
        except OSError:
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(base)
    return out


def collect_files(d: date, root_keys: list[str]) -> list[tuple[Path, datetime, str]]:
    """(path, mtime, kind) kind=project|transcript|lecture"""
    start, end = day_bounds(d)
    found: list[tuple[Path, datetime, str]] = []

    for key in root_keys:
        walk_root = local_path(key)
        if walk_root is None:
            continue
        for dirpath, dirs, files in os.walk(walk_root):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")]
            root_path = Path(dirpath)
            for name in files:
                path = root_path / name
                if path.suffix.lower() not in ACTIVITY_SUFFIXES:
                    continue
                if path.name.startswith("."):
                    continue
                try:
                    if path.parent.resolve() == NOTES_DIR.resolve() and (
                        path.name.endswith("-day.md")
                        or path.name == "study-log.md"
                        or path.name == "tracked-projects.json"
                    ):
                        continue
                except OSError:
                    pass
                try:
                    mtime = path.stat().st_mtime
                except OSError:
                    continue
                if not in_day(mtime, start, end):
                    continue
                kind = "lecture" if "강의노트" in path.parts or "lecture-kit" in path.parts else "project"
                found.append((path, datetime.fromtimestamp(mtime), kind))

    for base in existing_transcript_roots():
        try:
            paths = base.rglob("*.jsonl")
        except OSError:
            continue
        for path in paths:
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if in_day(mtime, start, end):
                found.append((path, datetime.fromtimestamp(mtime), "transcript"))

    found.sort(key=lambda x: x[1])
    return found



def extract_user_queries(path: Path, limit: int = 30) -> list[tuple[str, str]]:
    """Return list of (timestamp, query) from agent jsonl."""
    out: list[tuple[str, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return out

    for line in text.splitlines():
        if '"role"' not in line or "user" not in line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("role") != "user":
            continue
        msg = obj.get("message") or {}
        content = msg.get("content") if isinstance(msg, dict) else None
        blob = ""
        if isinstance(content, list):
            parts = []
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    parts.append(c.get("text") or "")
            blob = "\n".join(parts)
        elif isinstance(content, str):
            blob = content
        if not blob:
            continue
        ts = ""
        m = re.search(r"<timestamp>(.*?)</timestamp>", blob, re.S)
        if m:
            ts = m.group(1).strip()
        q = blob
        m = re.search(r"<user_query>(.*?)</user_query>", blob, re.S)
        if m:
            q = m.group(1).strip()
        else:
            q = " ".join(blob.split())
        q = re.sub(r"\s+", " ", q).strip()
        if len(q) < 4:
            continue
        out.append((ts, q[:240]))
        if len(out) >= limit:
            break
    return out


def collect_queries(items: list[tuple[Path, datetime, str]]) -> list[tuple[str, str, str]]:
    """(project_hint, timestamp, query)"""
    rows: list[tuple[str, str, str]] = []
    for path, _, kind in items:
        if kind != "transcript":
            continue
        hint = path.parent.name
        # .../projects/<project>/agent-transcripts/<uuid>/<uuid>.jsonl
        try:
            parts = path.parts
            if "projects" in parts:
                i = parts.index("projects")
                if i + 1 < len(parts):
                    hint = parts[i + 1]
        except ValueError:
            pass
        for ts, q in extract_user_queries(path):
            rows.append((hint, ts, q))
    return rows


def estimate_window(items: list[tuple[Path, datetime, str]]) -> tuple[str, str, str]:
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


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        pass
    home = user_home()
    if home:
        try:
            return str(path.relative_to(home))
        except ValueError:
            pass
    return str(path)


def summarize_topics(queries: list[tuple[str, str, str]], files: list[tuple[Path, datetime, str]]) -> list[str]:
    topics: list[str] = []
    joined = " ".join(q for _, _, q in queries).lower()
    checks = [
        ("자료형·인덱싱/슬라이싱", ("자료형", "인덱싱", "슬라이싱", "시퀀스", "매핑")),
        ("리스트/튜플·변수(이름표)", ("리스트", "튜플", "변수", "이름표", "mutable")),
        ("Cursor/WSL 환경", ("cursor", "wsl", "토큰", "cli")),
        ("크롬 확장(playChrome)", ("크롬", "확장", "펨코", "에펨", "vscode 테마")),
        ("강의 받아쓰기(lecture-kit)", ("녹음", "마이크", "/start", "받아쓰", "lecture")),
        ("Git/노트 자동화", ("git", "깃", "노트", "스케줄", "자동")),
    ]
    for label, keys in checks:
        if any(k.lower() in joined for k in keys):
            topics.append(label)

    if "pr_" in " ".join(display_path(p) for p, _, _ in files).lower() or any(
        p.suffix == ".py" for p, _, k in files if k == "project"
    ):
        if "파이썬 연습 스크립트" not in topics:
            topics.append("파이썬 연습 스크립트")
    if any(
        ("강의노트" in display_path(p)) or p.name.lower() == "transcript.md"
        for p, _, _ in files
    ):
        if "강의 녹음/받아쓰기" not in topics:
            topics.append("강의 녹음/받아쓰기")
    if not topics:
        topics.append("파일·대화 활동 감지 (주제 자동식별 약함)")
    return topics


def day_note_path(d: date) -> Path:
    return NOTES_DIR / f"{d.isoformat()}-day.md"


def build_note(
    d: date,
    items: list[tuple[Path, datetime, str]],
    queries: list[tuple[str, str, str]],
) -> str:
    start_s, end_s, duration = estimate_window(items)
    topics = summarize_topics(queries, items)

    # 파일 목록 (최대 40)
    seen: set[str] = set()
    file_lines: list[str] = []
    for path, ts, kind in items:
        label = display_path(path)
        if label in seen:
            continue
        seen.add(label)
        file_lines.append(f"- `{label}` ({ts.strftime('%H:%M')}, {kind})")
        if len(file_lines) >= 40:
            break

    q_lines: list[str] = []
    for hint, ts, q in queries[:25]:
        when = ts or "(시각 없음)"
        q_lines.append(f"- **[{hint}]** {when}: {q}")

    topic_bullets = "\n".join(f"- {t}" for t in topics)
    files_block = "\n".join(file_lines) or "- (파일 목록 없음)"
    queries_block = "\n".join(q_lines) or "- (Agent 대화 없음 — 파일 mtime만으로 추정)"

    one_liner = " / ".join(topics[:3])

    return f"""# {d.isoformat()} ({WEEKDAY_KR[d.weekday()]}) 당일 기록 요약

> 생성: 자동 배치 (`scripts/daily_study_publish.py`) — Agent 기동 불필요  
> 추정 시간: **{start_s} ~ {end_s}** ({duration})  
> 근거: `C:\\Users\\LT-013` 프로젝트 파일 + Cursor agent-transcripts

---

## 한줄 요약

{one_liner}

---

## 주제

{topic_bullets}

---

## Agent 질문·요청 (요약용 원문 발췌)

{queries_block}

---

## 활동 파일

{files_block}

---

## 메모

- 자동 초안입니다. 수업 장표·lecture-kit `/note` 결과로 보완하세요.
- 주말·공부량 없음이면 배치가 노트/푸시를 생략합니다.
"""


def ensure_study_log() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    if not STUDY_LOG.exists():
        STUDY_LOG.write_text(
            "# 공부·수업 시간 기록\n\n"
            "> Agent 대화 + `C:\\Users\\LT-013` 소스 기준 당일 요약\n\n"
            "| 날짜 | 시간대 | 소요·성격 | 주제 | 노트 |\n"
            "|------|--------|-----------|------|------|\n",
            encoding="utf-8",
        )


def upsert_study_log(d: date, start_s: str, end_s: str, duration: str, topics: list[str], note: Path) -> None:
    ensure_study_log()
    text = STUDY_LOG.read_text(encoding="utf-8")
    topic = " / ".join(topics[:4]) if topics else "(자동 초안)"
    link = f"[day 요약](./{note.name})"
    row = f"| {d.isoformat()} ({WEEKDAY_KR[d.weekday()]}) | {start_s} ~ {end_s} | {duration} | {topic} | {link} |"
    marker = f"| {d.isoformat()}"
    lines = text.splitlines()
    replaced = False
    new_lines: list[str] = []
    for line in lines:
        if line.startswith(marker):
            new_lines.append(row)
            replaced = True
        else:
            new_lines.append(line)
    if not replaced:
        if new_lines and new_lines[-1].strip() != "":
            new_lines.append("")
        # 테이블 헤더 다음이 아니라 파일 끝에 추가 (단순)
        new_lines.append(row)
    STUDY_LOG.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "형모 양")
    env.setdefault("GIT_AUTHOR_EMAIL", "tytyrrr13@gmail.com")
    env.setdefault("GIT_COMMITTER_NAME", env["GIT_AUTHOR_NAME"])
    env.setdefault("GIT_COMMITTER_EMAIL", env["GIT_AUTHOR_EMAIL"])
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def publish(d: date, note: Path, dry_run: bool, no_push: bool) -> int:
    msg = f"Add daily study summary for {d.isoformat()}"
    if dry_run or no_push:
        print(f"[{'dry-run' if dry_run else 'no-push'}] skip commit/push: {msg}")
        return 0

    rel_note = str(note.relative_to(REPO_ROOT)).replace("\\", "/")
    rel_log = str(STUDY_LOG.relative_to(REPO_ROOT)).replace("\\", "/")
    to_add = [rel_note, rel_log]
    if TRACKED_FILE.exists():
        to_add.append(str(TRACKED_FILE.relative_to(REPO_ROOT)).replace("\\", "/"))
    add = run_git(["add", "--", *to_add])
    if add.returncode != 0:
        print(add.stderr, file=sys.stderr)
        return add.returncode

    status = run_git(["status", "--porcelain", "--", *to_add])
    if not status.stdout.strip():
        print("변경 사항 없음 - push 생략")
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
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    args = parse_args()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    d = target_day(args)
    roots, newly = discover_program_projects()
    if not args.dry_run:
        save_tracked(roots)
    print(f"대상 날짜: {d.isoformat()} ({WEEKDAY_KR[d.weekday()]})")
    print(f"추적 프로젝트({len(roots)}): {[str(p) for p in roots]}")
    if newly:
        print(f"신규 프로그램 소스 편입: {[str(p) for p in newly]}")
    else:
        print("신규 프로그램 소스 편입: 없음")
    print(f"transcript: {[str(p) for p in existing_transcript_roots()]}")

    items = collect_files(d, roots)
    if not items:
        print("공부량 없음 - day 노트/푸시 생략")
        # 신규 프로그램 폴더만 편입된 날은 추적 목록만이라도 커밋
        if newly and not args.dry_run and not args.no_push:
            rel = str(TRACKED_FILE.relative_to(REPO_ROOT)).replace("\\", "/")
            run_git(["add", "--", rel])
            st = run_git(["status", "--porcelain", "--", rel])
            if st.stdout.strip():
                run_git(["commit", "-m", f"Track new program projects ({d.isoformat()})"])
                push = run_git(["push", "origin", "HEAD"])
                if push.returncode == 0:
                    print("추적 목록만 푸시 완료:", [str(x) for x in newly])
                else:
                    print(push.stderr, file=sys.stderr)
                    return push.returncode
        return 0

    if is_weekend(d):
        print("주말 + 공부량 감지 -> 등록 진행")

    queries = collect_queries(items)
    topics = summarize_topics(queries, items)
    start_s, end_s, duration = estimate_window(items)
    out = day_note_path(d)

    if out.exists() and not args.force and not args.dry_run:
        # 수동으로 잘 쓴 노트가 있으면 내용 유지, 로그 행만 맞춤
        print(f"노트 이미 존재: {out.name} (내용 유지, --force 시 덮어씀)")
    else:
        content = build_note(d, items, queries)
        if args.dry_run:
            print("--- note preview ---")
            print(content)
        else:
            NOTES_DIR.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")
            print(f"노트 작성: {out}")

    if not args.dry_run:
        upsert_study_log(d, start_s, end_s, duration, topics, out)
        print(f"study-log 갱신: {start_s}~{end_s} / {duration}")
    else:
        print(f"[dry-run] study-log: {d} | {start_s}~{end_s} | {duration} | {topics}")

    return publish(d, out, args.dry_run, args.no_push)


if __name__ == "__main__":
    raise SystemExit(main())
