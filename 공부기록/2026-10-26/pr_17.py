# 2026-10-26 — NumPy 공부
# pip install numpy  (venv 안에서)
#
# 실행: python 공부기록/2026-10-26/pr_17.py
# 리스트 vs NumPy 개념: 같은 폴더의 리스트_vs_NumPy.md

import numpy as np

print("=" * 50)
print("1) 배열 만들기 — 리스트를 NumPy 형태로 바꾸는 것")
print("=" * 50)
# np.array(...) : 파이썬 리스트를 NumPy 배열(ndarray)로 변환
# 한 번 배열이 되면, 아래처럼 통째로 계산할 수 있음
a = np.array([1, 2, 3, 4])
print("a =", a)
print("  dtype:", a.dtype, "  ← 원소 타입 (여기선 정수)")
print("  shape:", a.shape, "  ← 모양. (4,) 는 원소 4개인 1차원")

# np.arange(시작, 끝, 간격) : range() 랑 비슷하지만 결과가 배열
# 끝 숫자는 포함 안 됨 (range와 동일)
b = np.arange(0, 10, 2)  # 0부터 10 미만까지 2씩 → [0, 2, 4, 6, 8]
print("b = arange(0,10,2) →", b)

# np.zeros((행, 열)) : 전부 0으로 채운 표(2차원 배열)
# 괄호가 두 겹인 이유: 모양을 "하나의 튜플"로 넘기기 때문
c = np.zeros((2, 3))  # 2행 3열
print("c = zeros(2행3열) →\n", c)

# np.ones : zeros와 같은데 1로 채움
d = np.ones((2, 3))
print("d = ones(2행3열) →\n", d)

# np.linspace(시작, 끝, 개수) : 시작~끝 "포함"해서 개수만큼 균등 분할
# arange는 "간격" 지정, linspace는 "몇 개" 지정 → 용도가 다름
e = np.linspace(0, 1, 5)  # 0, 0.25, 0.5, 0.75, 1.0
print("e = linspace(0,1,5) →", e)


print("\n" + "=" * 50)
print("2) 연산 — 리스트와 제일 다른 부분 (원소마다 자동 계산)")
print("=" * 50)
# 리스트: [1,2,3] * 2  → [1,2,3,1,2,3]  (이어 붙이기)
# NumPy : array * 2    → [2,4,6]         (각 칸에 ×2)
print("a * 2  →", a * 2, "   # 각 원소 × 2")
print("a + a  →", a + a, "   # 같은 위치끼리 더함")
print("a.sum()  →", a.sum(), "     # 전부 합")
print("a.mean() →", a.mean(), "   # 평균")


print("\n" + "=" * 50)
print("3) 인덱싱 / 슬라이싱 — 표에서 칸·행·열 꺼내기")
print("=" * 50)
# 2행 3열 표라고 생각하면 편함
#        열0  열1  열2
# 행0  [  1,   2,   3 ]
# 행1  [  4,   5,   6 ]
m = np.array([[1, 2, 3], [4, 5, 6]])
print("m =\n", m)

# m[행, 열]  ← 리스트는 m[행][열] 두 번, NumPy는 콤마로 한 번에
print("m[0, 1] →", m[0, 1], "  # 0행 1열 = 2")

# : 는 "전부" 라는 뜻 (슬라이싱)
print("m[:, 1] →", m[:, 1], "  # 모든 행의 1열 = [2, 5]")
print("m[1, :] →", m[1, :], "  # 1행의 모든 열 = [4, 5, 6]")


print("\n" + "=" * 50)
print("4) reshape — 같은 숫자인데 모양만 바꾸기")
print("=" * 50)
# a 는 [1,2,3,4] (1차원 4칸)
# reshape(2, 2) → 2행 2열로 "다시 배치"
# 주의: 칸 수(4)가 맞아야 함. reshape(2,3)은 6칸 필요해서 에러
print("원래 a:", a)
print("reshape(2,2) →\n", a.reshape(2, 2))
print("  ※ a 자체는 그대로. reshape는 '보이는 모양'을 바꾼 새 뷰/배열")


# 아래에 오늘 수업/실습 이어서 작성
