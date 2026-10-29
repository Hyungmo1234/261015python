# ============================================================
# for / while 반복문
# - for   : "이 묶음을 순서대로 하나씩" 돌 때 (횟수·시퀀스가 정해진 경우)
# - while : "조건이 참인 동안" 돌 때 (언제 끝날지 조건으로 정할 때)
# - break : 반복 즉시 종료 / continue : 이번만 건너뛰고 다음 회차로
# ============================================================

# --- 1) for + range ------------------------------------------------
# range(n)      -> 0 ~ n-1
# range(a, b)   -> a ~ b-1
# range(a, b, s)-> a부터 s씩 증가, b 직전까지
print("=== for + range ===")
for i in range(5):
    print(f"i = {i}")

print("1부터 5까지:")
for n in range(1, 6):
    print(n, end=" ")
print()

print("짝수만 (2, 4, 6, 8, 10):")
for n in range(2, 11, 2):
    print(n, end=" ")
print()

# --- 2) for + 리스트 / 문자열 / 딕셔너리 ---------------------------
print("\n=== for + 시퀀스 ===")
fruits = ["사과", "바나나", "포도"]
for f in fruits:
    print(f"과일: {f}")

for ch in "hi":
    print(f"글자: {ch}")

scores = {"국어": 90, "영어": 85, "수학": 95}
for subject, score in scores.items():
    print(f"{subject} = {score}")

# 인덱스도 같이 필요할 때
for idx, f in enumerate(fruits):
    print(f"[{idx}] {f}")

# --- 3) while -----------------------------------------------------
print("\n=== while ===")
count = 0
while count < 3:
    print(f"count = {count}")
    count += 1                 # 없으면 무한 루프!

# 합계 구하기
total = 0
n = 1
while n <= 5:
    total += n
    n += 1
print(f"1~5 합 = {total}")

# --- 4) break / continue ------------------------------------------
print("\n=== break / continue ===")
for i in range(10):
    if i == 3:
        continue               # 3만 건너뜀
    if i == 7:
        break                  # 7에서 종료
    print(i, end=" ")
print()

# while + break (입력 흉내)
nums = [2, 5, 0, 8]            # 0이 나오면 중단한다고 가정
i = 0
while i < len(nums):
    if nums[i] == 0:
        print("0 만남 -> 중단")
        break
    print(f"처리: {nums[i]}")
    i += 1

# --- 5) 중첩 반복 -------------------------------------------------
print("\n=== 중첩 for (구구단 2단) ===")
for dan in range(2, 3):
    for mul in range(1, 10):
        print(f"{dan} x {mul} = {dan * mul}")

# --- 6) for vs while 언제? ----------------------------------------
# for   : 리스트/range처럼 "돌릴 대상"이 분명할 때
# while : "이 조건일 때까지"처럼 끝 조건이 중요할 때
#
# 같은 일을 둘 다로:
print("\n=== 같은 일 비교 ===")
for i in range(3):
    print("for:", i)

i = 0
while i < 3:
    print("while:", i)
    i += 1

# --- 7) 한눈에 정리 -----------------------------------------------
# for x in 묶음:     묶음의 원소를 순서대로
# for i in range(n): 0..n-1 숫자 반복
# while 조건:        조건이 True인 동안
# break / continue
