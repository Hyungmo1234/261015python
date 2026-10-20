from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.catalog import load_catalog

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "projects.json"
STATIC = ROOT / "static"

app = FastAPI(title="Project Hub", version="1.0.0")


def projects_base() -> Path | None:
    raw = os.environ.get("PROJECTS_BASE", "").strip()
    if raw:
        p = Path(raw)
        return p if p.is_dir() else None
    default = ROOT.parent.parent
    return default if default.is_dir() else None


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/projects")
def api_projects() -> dict:
    return load_catalog(CONFIG, projects_base())


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
