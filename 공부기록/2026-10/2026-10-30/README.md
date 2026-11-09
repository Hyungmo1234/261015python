# 2026-10-30 — 산업 센서 이상탐지 시각화 (`project1`)

원본 작업 경로: `C:\Users\LT-013\project1`  
데이터: Hugging Face [Petsteb/industrial-sensor-anomaly-data](https://huggingface.co/datasets/Petsteb/industrial-sensor-anomaly-data) (`data.csv`, 약 5만 행 · 저장소에는 미포함)

## 오늘 한 일

1. `equipment_id` 기준 장비별 이상(`is_anomaly=1`) 추출·시각화
2. 정상 구간을 **검정 점**으로 함께 표시
3. 주요 센서 결측 행 **제외** (평균 대치 없음)
4. `operating_mode != normal` 구간을 **배경색**으로 표시  
   (`high_load` / `startup` / `cooldown` / `idle`)
5. `sensor_malfunction` 이상 건은 그래프에서 **제외**

## 실행

```bash
# project1 폴더에서 (data.csv 필요)
python split_by_equipment.py
# → anomaly_plots/EQ-00x_anomalies.png
```

## 파일

| 파일 | 설명 |
|------|------|
| `split_by_equipment.py` | 장비별 정상+이상 산점도 / 모드 배경 / 결측·센서고장 제외 |
| `데이터셋_가이드.md` | AI Insight Campus용 데이터셋 매핑 메모 |
| `anomaly_plots/` | EQ-001~005 결과 PNG |
