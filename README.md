# 261015python

Python 기초 연습 저장소입니다.

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

## 매일 자동 노트 (12:30)

- **대상:** 전날 공부 (파일 변경·Cursor transcript 기준)
- **시간:** 매일 12:30 (Windows 작업 스케줄러 → WSL)
- **규칙:** 공부량이 있을 때만 노트 작성 + GitHub push  
  주말도 공부량이 있을 때만 등록 (없으면 생략)
- **절전 모드:** PC가 잠자면 해당 시각에는 실행되지 않음 (깨어난 뒤 수동 실행 가능)

수동 실행:

```bash
# 어제분
./scripts/run_daily_study.sh

# 특정 날짜 / 미리보기
python3 scripts/daily_study_publish.py --date 2026-10-16 --dry-run
```
