# 형모 프로젝트 포털

**GitHub PR/저장소가 아니라, 브라우저에서 여는 나만의 프로젝트 정보 웹**입니다.

- 프로젝트 이름·설명·서비스 URL·메모를 **웹 화면에서 직접 등록/수정**
- 데이터는 서버의 `data/portal.json`에 저장 (Docker volume / Fly volume)
- (선택) `PROJECTS_BASE` 아래 소스 폴더가 있으면 Git·README·STATUS 자동 보강

## 가장 빠른 실행 (Docker)

```bash
cd project_hub
docker compose up --build
```

→ http://localhost:8080

## Python으로 실행

```bash
cd project_hub
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

로컬에서 다른 repo 폴더까지 스캔하려면:

```bash
export PROJECTS_BASE=/path/to/parent-of-repos
```

## 편집 보호 (운영 배포 시)

```bash
export PORTAL_EDIT_TOKEN=긴_랜덤_문자열
```

웹 「프로젝트 관리」에서 같은 값을 「편집 토큰」에 입력 후 저장합니다.  
토큰을 설정하지 않으면 누구나 API로 수정할 수 있으므로 **공개 인터넷에는 토큰 필수**입니다.

## Fly.io

```bash
cd project_hub
fly volumes create portal_data --region nrt --size 1
fly deploy
```

Fly API 토큰은 `fly auth login` 또는 `FLY_API_TOKEN` 환경 변수로 설정합니다.

## API

- `GET /api/portal` — 포털 전체 (UI가 사용)
- `POST /api/portal/projects` — 추가
- `PUT /api/portal/projects/{id}` — 수정
- `DELETE /api/portal/projects/{id}` — 삭제
