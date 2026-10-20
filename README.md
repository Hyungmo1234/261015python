# 261015python

Python 기초 연습 저장소입니다.

## 형모 프로젝트 포털 (나만의 웹)

`project_hub/` — GitHub가 아닌 **브라우저용 개인 포털**. `data/portal.json`에 프로젝트를 저장하고 웹에서 등록·수정합니다.

```bash
cd project_hub
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PROJECTS_BASE=/path/to/parent-of-repos
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

자세한 내용: [project_hub/README.md](project_hub/README.md)

## 구성

| 파일 | 설명 |
|------|------|
| `pr_1.py` | 로그 분석기 (INFO/WARN/ERROR 건수·비율) |
| `pr_2.py` | 타입·연산·반복 연습 |
| `pr_3.py` | `print` 옵션 (`sep`, `end`) |
| `pr_4input.py` | `input()` 연습 |
| `logs/server.log` | 샘플 로그 |
| `notes/` | 학습 정리 글 · 공부 시간 기록 |
| `scripts/daily_study_publish.py` | 전날 공부 노트 자동 작성 + push |
| `scripts/run_daily_study.sh` | 스케줄러용 실행 래퍼 |

## 실행

```bash
# Windows
python pr_1.py

# WSL
python3 pr_1.py
```

학습 노트: [notes/2026-10-16-cursor-python.md](notes/2026-10-16-cursor-python.md)

## 매일 자동 노트 (12:30, Agent 불필요)

Cursor Agent를 켜지 않아도 **Windows 작업 스케줄러**가 백그라운드에서 활동을 모아 `notes/YYYY-MM-DD-day.md` 를 쓰고, 공부량이 있으면 git push 합니다.

- **대상:** `C:\Users\LT-013`(및 Desktop) 아래 **프로그램 소스로 판별된 작업 폴더** + Cursor agent-transcripts  
  - 새 폴더가 생기면 `.py`/`.js`/`package.json` 등으로 소스 프로젝트인지 구분 → 맞으면 `notes/tracked-projects.json`에 편입 후 기존과 같이 추적·기록·요약  
  - 요약/기록 포맷은 그대로 (`YYYY-MM-DD-day.md`, study-log)
- **시간:** 매일 12:30 (`261015python-DailyStudyNote`)
- **날짜 규칙:**
  - **평일(화~금):** 전날(어제) 1일
  - **월요일:** **금·토·일** 3일을 한 번에 보고, 공부량 있는 날만 노트 + 한 번에 push
  - 주말에 공부했으면 월요일에 반영 (토·일 단독 스케줄은 없음 — 월요일이 주말분 담당)
- **규칙:** 공부량이 있을 때만 노트 + push. 이미 수동으로 쓴 day 노트는 기본적으로 덮어쓰지 않음 (`--force` 시 덮어씀)
- **절전:** `StartWhenAvailable` — 잠들어 12:30을 놓치면 깨어난 뒤 실행
- **로그:** `logs/daily_study_*.log`

스케줄 등록/갱신 (최초 1회 또는 설정 변경 시):

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\LT-013\261015python\scripts\install_daily_study_task.ps1
```

수동 실행:

```bat
REM Windows
C:\Users\LT-013\261015python\scripts\run_daily_study.cmd
C:\Users\LT-013\261015python\scripts\run_daily_study.cmd --dry-run
```

```bash
# WSL
./scripts/run_daily_study.sh
python3 scripts/daily_study_publish.py --date 2026-10-16 --dry-run
```
