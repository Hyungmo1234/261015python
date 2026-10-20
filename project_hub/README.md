# Project Hub

연결된 GitHub 저장소(및 선택적 로컬 프로젝트)의 README, Git 상태, STATUS 문서 요약을 보여 주는 웹 대시보드입니다.

## 로컬 실행 (Cloud Agent / WSL)

```bash
cd project_hub
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PROJECTS_BASE=/agent/repos   # 형모 PC: 형제 폴더가 모인 상위 경로
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

브라우저: http://localhost:8080

## 프로젝트 추가

`config/projects.json`에 항목을 추가합니다. `dir`은 `PROJECTS_BASE` 아래 폴더 이름입니다.

## Fly.io 배포

이 디렉터리만으로는 **다른 저장소 파일이 이미지에 포함되지 않습니다.** Fly에서 전체 포트폴리오를 보려면:

1. 멀ti-repo 빌드(각 repo clone) 또는
2. GitHub API 연동(추후) 또는
3. Cloud Agent가 돌아가는 환경처럼 `PROJECTS_BASE`에 clone된 경로를 마운트

로컬 PC에서 허브만 배포할 경우, README·GitHub 링크 중심 메타만 표시됩니다.

```bash
cd project_hub
fly launch --no-deploy   # 최초 1회
fly deploy
```

## API

- `GET /api/health`
- `GET /api/projects` — 전체 카탈로그 JSON
