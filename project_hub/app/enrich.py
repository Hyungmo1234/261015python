from __future__ import annotations

from pathlib import Path
from typing import Any

from app.catalog import (
    _git_info,
    _package_info,
    _readme_excerpt,
    _simple_stats,
    _status_summary,
    resolve_project_root,
)


def portal_entry_to_catalog_entry(entry: dict[str, Any]) -> dict[str, Any]:
    scan = entry.get("scan_dir")
    links = entry.get("links") or []
    return {
        "id": entry["id"],
        "name": entry["name"],
        "description": entry.get("description", ""),
        "repo": entry.get("repo_url"),
        "tags": list(entry.get("tags") or []),
        "dir": scan,
        "status_doc": entry.get("status_doc"),
        "links": links,
        "dev": entry.get("dev_hint"),
        "local_only": False,
    }


def enrich_portal_project(
    entry: dict[str, Any], bases: list[Path]
) -> dict[str, Any]:
    cat_entry = portal_entry_to_catalog_entry(entry)
    root = resolve_project_root(cat_entry, bases) if cat_entry.get("dir") else None

    out: dict[str, Any] = {
        "id": entry["id"],
        "name": entry["name"],
        "description": entry.get("description", ""),
        "tags": list(entry.get("tags") or []),
        "status": entry.get("status") or "active",
        "site_url": entry.get("site_url"),
        "repo_url": entry.get("repo_url"),
        "notes": entry.get("notes") or "",
        "updated_at": entry.get("updated_at"),
        "scan_dir": entry.get("scan_dir"),
        "path": str(root) if root else None,
        "scan_available": root is not None,
    }

    links: list[dict[str, Any]] = []
    for link in entry.get("links") or []:
        item = {"label": link["label"], "path": link.get("path", "")}
        if root and link.get("path") and (root / link["path"]).is_file():
            item["exists"] = True
        links.append(item)
    out["links"] = links

    if entry.get("notes"):
        out["display_notes"] = entry["notes"]
    elif not root and entry.get("scan_dir"):
        out["display_notes"] = (
            "로컬/서버에 소스 폴더가 없어도 포털에 등록된 정보는 그대로 표시됩니다."
        )

    if root:
        out["readme_excerpt"] = _readme_excerpt(root)
        out["git"] = _git_info(root)
        out["package"] = _package_info(root)
        out["status_summary"] = _status_summary(root, entry.get("status_doc"))
        out["stats"] = _simple_stats(root)
        if entry.get("dev_hint") and isinstance(entry["dev_hint"], dict):
            out["dev"] = entry["dev_hint"]

    return out


def load_portal_catalog(
    portal: dict[str, Any], projects_base: Path | None, hub_root: Path
) -> dict[str, Any]:
    from datetime import datetime, timezone

    bases: list[Path] = []
    if projects_base and projects_base.is_dir():
        bases.append(projects_base.resolve())
    sibling = hub_root.parent.parent
    if sibling.is_dir() and sibling not in bases:
        bases.append(sibling.resolve())

    projects = [
        enrich_portal_project(p, bases) for p in portal.get("projects") or []
    ]
    return {
        "portal_title": portal.get("portal_title", DEFAULT_TITLE),
        "portal_subtitle": portal.get("portal_subtitle", ""),
        "owner": portal.get("owner", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "projects_base": str(bases[0]) if bases else None,
        "data_path": str(hub_root / "data" / "portal.json"),
        "projects": projects,
    }


DEFAULT_TITLE = "형모 프로젝트 포털"
