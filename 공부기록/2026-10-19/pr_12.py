# ============================================================
# dict(딕셔너리) - 키(key) -> 값(value)
# - 인덱스가 아니라 키로 접근: d["이름"]
# - 키는 보통 문자열/숫자 (변경 불가능한 것만 키로 가능)
# - 같은 키는 하나 (넣으면 값이 덮어씌워짐)
# ============================================================

# --- 1) 만들기 ----------------------------------------------------
student = {
    "name": "Kim",
    "age": 20,
    "scores": [90, 85, 78],
}
empty = {}                 # 빈 dict
# empty = dict()           # 같은 뜻
print(f"student = {student}")
print(f"타입 = {type(student)}")

# --- 2) 읽기 / 쓰기 -----------------------------------------------
print(f"이름 = {student['name']}")
print(f"나이 = {student['age']}")

student["age"] = 21                    # 기존 키 수정
student["major"] = "CS"                # 새 키 추가
print(f"수정 후 = {student}")

# 없는 키를 []로 읽으면 KeyError
# print(student["phone"])
print(f"get 안전 조회 = {student.get('phone')}")           # None
print(f"get 기본값   = {student.get('phone', '없음')}")    # 없음

# --- 3) 키 / 값 / 쌍 ----------------------------------------------
print(f"keys   = {list(student.keys())}")
print(f"values = {list(student.values())}")
print(f"items  = {list(student.items())}")

# --- 4) 반복 ------------------------------------------------------
print("--- for key in dict ---")
for key in student:
    print(f"  {key} -> {student[key]}")

print("--- for key, value in items() ---")
for key, value in student.items():
    print(f"  {key} -> {value}")

# --- 5) 삭제 ------------------------------------------------------
grade = {"국어": 90, "영어": 80, "수학": 95}
print(f"삭제 전 = {grade}")
del grade["영어"]                 # 키 삭제
print(f"del 후  = {grade}")
math = grade.pop("수학")          # 꺼내면서 삭제
print(f"pop 수학 = {math}, 남은 grade = {grade}")
grade.clear()                     # 전부 비우기
print(f"clear 후 = {grade}")

# --- 6) 멤버십 (키 기준) ------------------------------------------
menu = {"아메리카노": 1500, "라떼": 2000}
print(f"'라떼' in menu   = {'라떼' in menu}")       # True (키)
print(f"1500 in menu     = {1500 in menu}")         # False (값은 안 봄)
print(f"1500 in values() = {1500 in menu.values()}")

# --- 7) 여러 방식의 생성 ------------------------------------------
d1 = dict(a=1, b=2)
d2 = dict([("x", 10), ("y", 20)])
d3 = dict.fromkeys(["id", "name", "age"], None)  # 키만 만들고 값은 None
print(f"dict(a=1,b=2)     = {d1}")
print(f"dict(쌍 리스트)   = {d2}")
print(f"fromkeys          = {d3}")

# --- 8) update / setdefault ---------------------------------------
profile = {"name": "Lee"}
profile.update({"age": 22, "city": "Seoul"})
print(f"update 후 = {profile}")

# 키 없으면 넣고, 있으면 기존 값 유지
profile.setdefault("name", "UNKNOWN")   # 이미 있으므로 Lee 유지
profile.setdefault("email", "n/a")      # 없어서 추가
print(f"setdefault 후 = {profile}")

# --- 9) 중첩 dict (값 안에 또 dict) --------------------------------
classroom = {
    "A반": {"인원": 30, "담임": "Park"},
    "B반": {"인원": 28, "담임": "Choi"},
}
print(f"A반 담임 = {classroom['A반']['담임']}")
print(f"B반 인원 = {classroom['B반']['인원']}")

# --- 10) 한눈에 정리 ----------------------------------------------
# d[key] / d.get(key)     읽기
# d[key] = value          쓰기(추가/수정)
# del d[key] / pop(key)   삭제
# keys(), values(), items()
# in 은 키 기준
#
# list/tuple : 순서로 접근 (0, 1, 2...)
# dict       : 이름으로 접근 ("name", "age"...)
