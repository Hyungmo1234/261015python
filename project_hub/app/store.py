from __future__ import annotations

import json
import re
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_PORTAL = {
    "portal_title": "형모 프로젝트 포털",
    "portal_subtitle": "내 프로젝트 정보를 한곳에서 관리합니다.",
    "owner": "Hyungmo",
    "projects": [],
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slug_id(name: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9가-힣]+", "-", name.strip()).strip("-").lower()
    if not base:
        base = "project"
    return f"{base}-{uuid.uuid4().hex[:6]}"


def data_dir(root: Path) -> Path:
    import os

    raw = os.environ.get("PORTAL_DATA_DIR", "").strip()
    if raw:
        p = Path(raw)
    else:
        p = root / "data"
    p.mkdir(parents=True, exist_ok=True)
    return p


def portal_path(root: Path) -> Path:
    return data_dir(root) / "portal.json"


def seed_from_config(root: Path, config_path: Path) -> None:
    path = portal_path(root)
    if path.is_file():
        return
    seed = deepcopy(DEFAULT_PORTAL)
    if config_path.is_file():
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        for entry in cfg.get("projects", []):
            seed["projects"].append(
                {
                    "id": entry["id"],
                    "name": entry["name"],
                    "description": entry.get("description", ""),
                    "tags": list(entry.get("tags") or []),
                    "status": "active",
                    "site_url": None,
                    "repo_url": entry.get("repo"),
                    "notes": "",
                    "scan_dir": entry.get("dir"),
                    "status_doc": entry.get("status_doc"),
                    "links": list(entry.get("links") or []),
                    "dev_hint": entry.get("dev"),
                    "updated_at": _now_iso(),
                }
            )
    seed["seeded_at"] = _now_iso()
    path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")


def load_portal(root: Path) -> dict[str, Any]:
    path = portal_path(root)
    if not path.is_file():
        return deepcopy(DEFAULT_PORTAL)
    return json.loads(path.read_text(encoding="utf-8"))


def save_portal(root: Path, data: dict[str, Any]) -> None:
    data["updated_at"] = _now_iso()
    portal_path(root).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def upsert_project(root: Path, body: dict[str, Any]) -> dict[str, Any]:
    portal = load_portal(root)
    projects: list[dict[str, Any]] = portal.setdefault("projects", [])
    pid = body.get("id")
    if pid:
        idx = next((i for i, p in enumerate(projects) if p.get("id") == pid), None)
        if idx is None:
            raise KeyError(pid)
        merged = {**projects[idx], **body, "id": pid, "updated_at": _now_iso()}
        projects[idx] = merged
        save_portal(root, portal)
        return merged
    new_id = slug_id(str(body.get("name", "project")))
    item = {
        "id": new_id,
        "name": body.get("name", "새 프로젝트"),
        "description": body.get("description", ""),
        "tags": list(body.get("tags") or []),
        "status": body.get("status") or "active",
        "site_url": body.get("site_url"),
        "repo_url": body.get("repo_url"),
        "notes": body.get("notes", ""),
        "scan_dir": body.get("scan_dir"),
        "status_doc": body.get("status_doc"),
        "links": list(body.get("links") or []),
        "dev_hint": body.get("dev_hint"),
        "updated_at": _now_iso(),
    }
    projects.append(item)
    save_portal(root, portal)
    return item


def delete_project(root: Path, project_id: str) -> None:
    portal = load_portal(root)
    projects = portal.get("projects") or []
    portal["projects"] = [p for p in projects if p.get("id") != project_id]
    save_portal(root, portal)
