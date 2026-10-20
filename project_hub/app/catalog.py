from __future__ import annotations

import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class ProjectInfo:
    id: str
    name: str
    description: str
    repo: str | None
    tags: list[str]
    available: bool
    path: str | None
    readme_excerpt: str | None = None
    git: dict[str, Any] | None = None
    package: dict[str, Any] | None = None
    status_summary: list[str] | None = None
    links: list[dict[str, str]] = field(default_factory=list)
    dev: dict[str, str] | None = None
    stats: dict[str, int] | None = None
    local_only: bool = False
    notes: str | None = None


def _run_git(cwd: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if out.returncode != 0:
            return None
        return out.stdout.strip() or None
    except (OSError, subprocess.TimeoutExpired):
        return None


def _git_info(root: Path) -> dict[str, Any] | None:
    if not (root / ".git").exists():
        return None
    branch = _run_git(root, "rev-parse", "--abbrev-ref", "HEAD")
    commit = _run_git(root, "rev-parse", "--short", "HEAD")
    subject = _run_git(root, "log", "-1", "--pretty=%s")
    date = _run_git(root, "log", "-1", "--pretty=%ci")
    dirty = _run_git(root, "status", "--porcelain")
    return {
        "branch": branch,
        "commit": commit,
        "last_subject": subject,
        "last_commit_at": date,
        "dirty": bool(dirty and dirty.strip()),
    }


def _readme_excerpt(root: Path, max_len: int = 480) -> str | None:
    readme = root / "README.md"
    if not readme.is_file():
        return None
    try:
        text = readme.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            if lines:
                break
            continue
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
        if sum(len(x) + 1 for x in lines) > max_len:
            break
    excerpt = " ".join(lines).strip()
    if len(excerpt) > max_len:
        excerpt = excerpt[: max_len - 1].rstrip() + "…"
    return excerpt or None


def _package_info(root: Path) -> dict[str, Any] | None:
    for rel in ("package.json", "frontend/web/package.json"):
        pkg_path = root / rel
        if not pkg_path.is_file():
            continue
        try:
            data = json.loads(pkg_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        scripts = data.get("scripts") or {}
        return {
            "path": rel,
            "name": data.get("name"),
            "version": data.get("version"),
            "scripts": {k: scripts[k] for k in ("dev", "build", "start") if k in scripts},
        }
    return None


def _status_summary(root: Path, rel: str | None, limit: int = 8) -> list[str] | None:
    if not rel:
        return None
    path = root / rel
    if not path.is_file():
        return None
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    bullets: list[str] = []
    in_current = False
    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip().lower()
            in_current = title in ("current", "현재", "work status", "진행")
            continue
        if not in_current:
            continue
        m = re.match(r"^-\s+\[[ xX]\]\s+(.+)$", line.strip())
        if m:
            bullets.append(m.group(1).strip())
        elif line.strip().startswith("- ") and not bullets:
            bullets.append(line.strip()[2:].strip())
        if len(bullets) >= limit:
            break
    return bullets or None


def _simple_stats(root: Path) -> dict[str, int]:
    counts = {"py": 0, "ts_tsx": 0, "md": 0}
    try:
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if ".git" in p.parts or "node_modules" in p.parts or "__pycache__" in p.parts:
                continue
            if p.suffix == ".py":
                counts["py"] += 1
            elif p.suffix in (".ts", ".tsx"):
                counts["ts_tsx"] += 1
            elif p.suffix == ".md":
                counts["md"] += 1
    except OSError:
        pass
    return counts


def resolve_project_root(entry: dict[str, Any], bases: list[Path]) -> Path | None:
    if entry.get("local_only"):
        for raw in entry.get("local_paths") or []:
            p = Path(raw)
            if p.is_dir():
                return p.resolve()
        for base in bases:
            candidate = base / entry.get("dir", "")
            if candidate.is_dir():
                return candidate.resolve()
        return None
    dir_name = entry.get("dir")
    if not dir_name:
        return None
    for base in bases:
        candidate = base / dir_name
        if candidate.is_dir():
            return candidate.resolve()
    return None


def load_catalog(config_path: Path, projects_base: Path | None) -> dict[str, Any]:
    bases: list[Path] = []
    if projects_base and projects_base.is_dir():
        bases.append(projects_base.resolve())
    hub_parent = config_path.resolve().parents[2]
    sibling = hub_parent.parent
    if sibling.is_dir() and sibling not in bases:
        bases.append(sibling.resolve())

    raw = json.loads(config_path.read_text(encoding="utf-8"))
    projects: list[ProjectInfo] = []
    for entry in raw.get("projects", []):
        root = resolve_project_root(entry, bases)
        available = root is not None
        links: list[dict[str, str]] = []
        for link in entry.get("links") or []:
            item = {"label": link["label"], "path": link["path"]}
            if root and (root / link["path"]).is_file():
                item["exists"] = True
            links.append(item)

        info = ProjectInfo(
            id=entry["id"],
            name=entry["name"],
            description=entry.get("description", ""),
            repo=entry.get("repo"),
            tags=list(entry.get("tags") or []),
            available=available,
            path=str(root) if root else None,
            links=links,
            dev=entry.get("dev"),
            local_only=bool(entry.get("local_only")),
            notes=None,
        )
        if not available:
            if entry.get("local_only"):
                info.notes = "로컬 PC 경로에만 존재합니다. Cloud에서는 메타데이터만 표시됩니다."
            else:
                info.notes = f"경로를 찾지 못했습니다. PROJECTS_BASE 아래 `{entry.get('dir')}` 폴더를 확인하세요."
        elif root:
            info.readme_excerpt = _readme_excerpt(root)
            info.git = _git_info(root)
            info.package = _package_info(root)
            info.status_summary = _status_summary(root, entry.get("status_doc"))
            info.stats = _simple_stats(root)

        projects.append(info)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "projects_base": str(bases[0]) if bases else None,
        "projects": [asdict(p) for p in projects],
    }
