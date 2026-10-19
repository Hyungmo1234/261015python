# ============================================================
# set(집합) - 합집합 / 교집합 / 차집합
# - 중복 없음, 순서(인덱스) 없음 -> "들어 있나?" / 묶음 비교에 사용
# - 기호: | & - ^   또는 메서드: union, intersection, difference, ...
# ============================================================

# --- 1) 세트 만들기 ------------------------------------------------
a = {"김", "이", "박"}
b = {"이", "최", "박"}
print(f"a = {a}")
print(f"b = {b}")
print(f"타입 = {type(a)}")

# 리스트에서 세트로 (중복 제거)
nums = [1, 2, 2, 3, 1]
print(f"list -> set : {nums} -> {set(nums)}")

# --- 2) 합집합 (union) - 둘 중 하나라도 있으면 -------------------
# a | b  또는  a.union(b)
print(f"합집합 a | b        = {a | b}")
print(f"합집합 a.union(b)   = {a.union(b)}")

# --- 3) 교집합 (intersection) - 둘 다 있는 것만 -------------------
# a & b  또는  a.intersection(b)
print(f"교집합 a & b              = {a & b}")
print(f"교집합 a.intersection(b)  = {a.intersection(b)}")

# --- 4) 차집합 (difference) - a에만 있고 b에는 없는 것 ------------
# a - b  또는  a.difference(b)
print(f"차집합 a - b             = {a - b}")   # 김
print(f"차집합 b - a             = {b - a}")   # 최
print(f"차집합 a.difference(b)   = {a.difference(b)}")

# --- 5) 대칭차집합 (symmetric difference) - 한쪽에만 있는 것 ------
# a ^ b  또는  a.symmetric_difference(b)
# (합집합에서 교집합을 뺀 것과 같음)
print(f"대칭차 a ^ b                      = {a ^ b}")
print(f"대칭차 a.symmetric_difference(b)  = {a.symmetric_difference(b)}")
print(f"확인 (a|b) - (a&b)                = {(a | b) - (a & b)}")

# --- 6) 포함 관계 -------------------------------------------------
# issubset / issuperset / isdisjoint
small = {"이", "박"}
print(f"small이 a의 부분집합? small.issubset(a)   = {small.issubset(a)}")   # True
print(f"a가 small을 포함?     a.issuperset(small) = {a.issuperset(small)}") # True
print(f"a 와 {{'홍'}} 공통 없음? a.isdisjoint({{'홍'}}) = {a.isdisjoint({'홍'})}")

# --- 7) 원소 추가 / 삭제 (세트 자체는 mutable) --------------------
c = {"사과", "바나나"}
c.add("포도")              # 하나 추가
c.update(["수박", "사과"])  # 여러 개 (이미 있는 사과는 그대로)
print(f"add/update 후 c = {c}")
c.discard("바나나")        # 없으면 에러 안 남
# c.remove("없는것")       # 없으면 KeyError
print(f"discard 후 c    = {c}")

# --- 8) 한눈에 정리 -----------------------------------------------
# |  합집합      a.union(b)
# &  교집합      a.intersection(b)
# -  차집합      a.difference(b)
# ^  대칭차집합  a.symmetric_difference(b)
#
# 실무 예: 수강생 A반/B반 명단 비교, 태그 공통점, 이미 처리한 ID 제외
