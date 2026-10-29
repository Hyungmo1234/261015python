#파일 호출 시 인자로 받은값은 어디로 들어가는가?
import sys
args = sys.argv[1:] 

for x in args:
    print (x, end=" ")
else:
    print()

# ============================================================
# int도 객체다 — id()로 메모리(객체 정체) 확인
# - 변수 = 이름표, 값 = 객체
# - int는 불변(immutable) → e += 5 는 같은 칸 수정이 아니라 새 객체 + 이름 이동
# - list는 가변(mutable) → append 하면 같은 객체가 바뀌어 a,b 둘 다 보임
# ============================================================

# --- 1) 작은 int는 같은 객체를 재사용하기도 함 --------------------
a = 10
b = 10
print("=== 1) a=10, b=10 ===")
print(f"id(a)={id(a)}, id(b)={id(b)}")
print(f"a is b → {a is b}")   # True인 경우가 많음 (인터프리터 캐시)

# --- 2) e = d 후 e += 5 → e만 새 객체를 가리킴 --------------------
print("\n=== 2) int += 는 새 객체 ===")
d = 10
e = d
print(f"이전: d={d}, e={e}")
print(f"이전 id: d={id(d)}, e={id(e)}, 같은가? {d is e}")

e += 5   # e = e + 5 와 같음 → 새 int 15 생성, e만 이동
print(f"이후: d={d}, e={e}")
print(f"이후 id: d={id(d)}, e={id(e)}, 같은가? {d is e}")

# --- 3) list와 나란히 비교 (핵심) ---------------------------------
print("\n=== 3) int(불변) vs list(가변) ===")

x = 1
y = x
y += 1
print(f"int : x={x}, y={y}, x is y → {x is y}")   # 1, 2, False

p = [1]
q = p
q.append(2)
print(f"list: p={p}, q={q}, p is q → {p is q}")   # [1,2], [1,2], True

# --- 4) int도 객체라서 타입/메서드가 있다 --------------------------
print("\n=== 4) int 객체 확인 ===")
n = 7
print(f"type(n) = {type(n)}")
print(f"n.bit_length() = {n.bit_length()}")  # 7을 비트로 표현하는 데 필요한 자리수
print(f"n.real = {n.real}")

# --- 5) 한눈에 ----------------------------------------------------
# d = 10; e = d     → 둘 다 같은 int 객체를 가리킬 수 있음
# e += 5            → 새 15를 만들고 e만 거기로 이동 (d는 10 유지)
# b = a; b.append() → 같은 list를 수정 → a로 봐도 바뀜
#
# 정리: "복사가 됐다"기보다 "불변 객체라 수정 대신 새 객체 + 재할당"


c = "안녕하세요"
d = c
c = c + "대성입니다"
print(f"c={c}, d={d}, c is d → {c is d}")   # False

a = {"a": 1}

b = a
b["b"] = 2
print(f"a={a}, b={b}, a is b → {a is b}")   # True


#파이썬은 모든것이 객체이다. int도 객체이다.
print((7).__add__(3))  # 10

print ("a".__len__())


def add(x, y):
    return x + y



def henSub(c,v) :
    c = c + 4
    v = v + 5
    return c - v

print (henSub(add(8,15),3))