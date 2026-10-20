from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.enrich import load_portal_catalog
from app.store import delete_project, load_portal, save_portal, seed_from_config, upsert_project

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "projects.json"
STATIC = ROOT / "static"

app = FastAPI(title="형모 프로젝트 포털", version="2.0.0")


class PortalMeta(BaseModel):
    portal_title: str | None = None
    portal_subtitle: str | None = None
    owner: str | None = None


class ProjectBody(BaseModel):
    id: str | None = None
    name: str = Field(min_length=1, max_length=120)
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    status: str = "active"
    site_url: str | None = None
    repo_url: str | None = None
    notes: str = ""
    scan_dir: str | None = None
    status_doc: str | None = None


def projects_base() -> Path | None:
    raw = os.environ.get("PROJECTS_BASE", "").strip()
    if raw:
        p = Path(raw)
        return p if p.is_dir() else None
    default = ROOT.parent.parent
    return default if default.is_dir() else None


def require_edit_token(x_portal_token: str | None) -> None:
    expected = os.environ.get("PORTAL_EDIT_TOKEN", "").strip()
    if not expected:
        return
    if x_portal_token != expected:
        raise HTTPException(status_code=403, detail="편집 토큰이 올바르지 않습니다.")


@app.on_event("startup")
def on_startup() -> None:
    seed_from_config(ROOT, CONFIG)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "hyungmo-project-portal"}


def _portal_response() -> dict[str, Any]:
    portal = load_portal(ROOT)
    return load_portal_catalog(portal, projects_base(), ROOT)


@app.get("/api/portal")
def api_portal() -> dict[str, Any]:
    return _portal_response()


@app.get("/api/projects")
def api_projects_legacy() -> dict[str, Any]:
    return _portal_response()


@app.put("/api/portal/meta")
def api_portal_meta(
    body: PortalMeta,
    x_portal_token: str | None = Header(default=None, alias="X-Portal-Token"),
) -> dict[str, Any]:
    require_edit_token(x_portal_token)
    portal = load_portal(ROOT)
    if body.portal_title is not None:
        portal["portal_title"] = body.portal_title
    if body.portal_subtitle is not None:
        portal["portal_subtitle"] = body.portal_subtitle
    if body.owner is not None:
        portal["owner"] = body.owner
    save_portal(ROOT, portal)
    return _portal_response()


@app.post("/api/portal/projects")
def api_create_project(
    body: ProjectBody,
    x_portal_token: str | None = Header(default=None, alias="X-Portal-Token"),
) -> dict[str, Any]:
    require_edit_token(x_portal_token)
    upsert_project(ROOT, body.model_dump())
    return _portal_response()


@app.put("/api/portal/projects/{project_id}")
def api_update_project(
    project_id: str,
    body: ProjectBody,
    x_portal_token: str | None = Header(default=None, alias="X-Portal-Token"),
) -> dict[str, Any]:
    require_edit_token(x_portal_token)
    payload = body.model_dump()
    payload["id"] = project_id
    try:
        upsert_project(ROOT, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.") from exc
    return _portal_response()


@app.delete("/api/portal/projects/{project_id}")
def api_delete_project(
    project_id: str,
    x_portal_token: str | None = Header(default=None, alias="X-Portal-Token"),
) -> dict[str, Any]:
    require_edit_token(x_portal_token)
    delete_project(ROOT, project_id)
    return _portal_response()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
