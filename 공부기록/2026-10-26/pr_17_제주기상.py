# 2026-10-26 - NumPy + 공공데이터(제주 일단위 기상) 예제
#
# 데이터: data/제주특별자치도_관측소별일단위기상정보_20211231.csv
# 출처: 공공데이터포털 (파일데이터, 로그인 없이 다운로드)
#
# 실행 (venv 활성 상태):
#   python 공부기록/2026-10-26/pr_17_제주기상.py

import csv
from pathlib import Path

import numpy as np

# ------------------------------------------------------------
# 0) 파일 위치 · 인코딩
#    한글 Windows CSV 는 종종 cp949 (utf-8 아님)
# ------------------------------------------------------------
DATA = Path(__file__).resolve().parent / "data" / "제주특별자치도_관측소별일단위기상정보_20211231.csv"

# 연습용으로 관측소·연도 하나만 고름 (전체가 6만 행이라 처음엔 좁히는 게 편함)
STATION = "대정"
YEAR = "2021"


def to_float(text: str):
    """빈 칸·이상한 값은 None 으로 (나중에 배열에서 제외)"""
    text = (text or "").strip()
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


# ------------------------------------------------------------
# 1) CSV 읽기 → 숫자 리스트 모으기 (아직 파이썬 list)
# ------------------------------------------------------------
dates = []
avg_list = []   # 평균기온
min_list = []   # 최저기온
max_list = []   # 최고기온
rain_list = []  # 일강수량

with open(DATA, encoding="cp949", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["관측소명"] != STATION:
            continue
        if not row["해당일자"].startswith(YEAR):
            continue

        avg = to_float(row["평균기온(섭씨)"])
        low = to_float(row["최저기온(섭씨)"])
        high = to_float(row["최고기온(섭씨)"])
        rain = to_float(row["일강수량(mm)"])
        # 기온이 비어 있으면 그 날은 건너뜀
        if avg is None or low is None or high is None:
            continue

        dates.append(row["해당일자"])
        avg_list.append(avg)
        min_list.append(low)
        max_list.append(high)
        rain_list.append(0.0 if rain is None else rain)  # 비 안 온 날 빈칸 → 0으로

print("=" * 55)
print(f"불러온 데이터: {STATION} / {YEAR}년  /  {len(dates)}일")
print(f"첫날 {dates[0]}  →  평균 {avg_list[0]}C")
print(f"마지막 {dates[-1]} →  평균 {avg_list[-1]}C")


print("\n" + "=" * 55)
print("예제 A) np.array - 리스트를 NumPy 배열로")
print("=" * 55)
# pr_17 의 a = np.array([1,2,3,4]) 와 같은 작업
avg = np.array(avg_list, dtype=float)
low = np.array(min_list, dtype=float)
high = np.array(max_list, dtype=float)
rain = np.array(rain_list, dtype=float)

print("avg[:5]  →", avg[:5], "  # 앞 5일 평균기온")
print("dtype    →", avg.dtype)
print("shape    →", avg.shape, "  # (일수,) 1차원")


print("\n" + "=" * 55)
print("예제 B) 연산 비교 - 리스트 vs NumPy")
print("=" * 55)

# ---------- B-1) 리스트로 같은 계산 (직접 하나씩 / 컴프리헨션) ----------
print("\n[리스트 방식]")

# 일교차: for 또는 컴프리헨션으로 짝지어 빼야 함
# (리스트끼리 high_list - min_list 는 TypeError - 자동으로 안 빼줌)
diff_list = [h - l for h, l in zip(max_list, min_list)]
print("일교차 앞 5일 →", diff_list[:5])

# 평균: 합 / 개수
avg_year_list = sum(avg_list) / len(avg_list)
print("연평균 기온   →", round(avg_year_list, 2), "C")

# 최고/최저 + 그날 날짜: max/min 후 index 찾기
high_year_list = max(max_list)
low_year_list = min(min_list)
print("연 최고기온   →", high_year_list, "C  (", dates[max_list.index(high_year_list)], ")")
print("연 최저기온   →", low_year_list, "C  (", dates[min_list.index(low_year_list)], ")")

print("총 강수량     →", round(sum(rain_list), 1), "mm")

# 화씨: 각 원소마다 공식 적용
f_list = [t * 1.8 + 32 for t in avg_list]
print("첫날 평균(화씨) →", round(f_list[0], 1), "F")

# 헷갈리기 쉬운 점: 리스트 * 2 는 "숫자 두 배"가 아니라 "목록 두 번"
print("리스트[:3] * 2 →", avg_list[:3] * 2, "  # 이어붙이기!")


# ---------- B-2) NumPy 로 같은 계산 (통째로) ----------
print("\n[NumPy 방식]  <- 결과가 위와 같아야 정상")

# 일교차 = 최고 - 최저  (날짜마다 자동으로 짝지어 빼기)
diff = high - low
print("일교차 앞 5일 →", diff[:5])
print("연평균 기온   →", round(float(avg.mean()), 2), "C")
print("연 최고기온   →", float(high.max()), "C  (", dates[int(high.argmax())], ")")
print("연 최저기온   →", float(low.min()), "C  (", dates[int(low.argmin())], ")")
print("총 강수량     →", round(float(rain.sum()), 1), "mm")
# 화씨: 배열 * 1.8 + 32 한 줄
print("첫날 평균(화씨) →", round(float(avg[0] * 1.8 + 32), 1), "F")
print("배열[:3] * 2   →", avg[:3] * 2, "  # 각 칸 x2")


print("\n" + "=" * 55)
print("예제 C) 인덱싱 / 슬라이싱 - 원하는 날·구간만 꺼내기")
print("=" * 55)
print("0번째 날 평균 →", avg[0], "C  (", dates[0], ")")
print("처음 7일(한 주) →", avg[:7])
print("마지막 7일      →", avg[-7:])

# 조건 인덱싱: 평균기온 25C 이상인 날만
hot = avg[avg >= 25]
print(f"평균 25C 이상인 날: {hot.size}일  /  그때 평균 {hot.mean():.1f}C" if hot.size else "25C 이상인 날 없음")


print("\n" + "=" * 55)
print("예제 D) 2차원 배열 - 표처럼 (행=날짜, 열=기온종류)")
print("=" * 55)
#        열0평균  열1최저  열2최고
# 행0일 [  ... ,   ... ,   ... ]
temps = np.column_stack([avg, low, high])  # shape: (일수, 3)
print("temps.shape →", temps.shape, "  # (날 수, 3열)")
print("temps[0]    →", temps[0], "  # 첫날 [평균, 최저, 최고]")
print("temps[:, 0] 앞5 →", temps[:5, 0], "  # 모든 행의 0열 = 평균만")
print("temps[:, 2] 앞5 →", temps[:5, 2], "  # 최고기온 열만")


print("\n" + "=" * 55)
print("예제 E) reshape - 같은 숫자, 모양만 바꾸기")
print("=" * 55)
# 앞 30일만 잘라서 10일 × 3주 비슷한 형태로 (연습용)
sample = avg[:30]  # 30칸
print("1차원 30일 →", sample.shape)
weekly = sample.reshape(3, 10)  # 3행 × 10열  (주차별 10일씩 가정한 연습)
print("reshape(3,10) →\n", weekly)
print("주차별 평균 →", weekly.mean(axis=1))  # 각 행(주)의 평균


print("\n" + "=" * 55)
print("끝. 관측소/연도는 파일 위쪽 STATION, YEAR 만 바꿔보세요.")
print("예: STATION = '외도'  /  YEAR = '2020'")
print("=" * 55)
