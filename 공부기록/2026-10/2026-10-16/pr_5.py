import calendar
import cal

print(calendar.month(2025, 9))
print(cal.month(2025, 9))
print(len(calendar.month(2025, 9)))
print(len(cal.month(2025, 9)))


def add(x, y):
    return x + y   

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def div(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y


def floordiv(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x // y

def mod(x, y):
    if y == 0:
        raise ValueError("Cannot perform modulo by zero.")
    return x % y

def power(x, y):
    return x ** y

def sqrt(x):
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    return x ** 0.5

def factorial(n):
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number.")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def gcd(a, b):  
    while b:
        a, b = b, a % b
    return a


b = add(6, 7)  # 덧셈
print(f"덧셈 b = {b}")
c = sub(10, 3)  # 뺄셈
print(f"뺄셈 c = {c}")
d = mul(4, 5)  # 곱셈
print(f"곱셈 d = {d}")
e = div(4, 3)  # 실수 나눗셈
print(f"나눗셈 e = {e}")
f = floordiv(4, 3)  # 몫
print(f"몫 f = {f}")
g = mod(20, 3)  # 나머지
print(f"나머지 g = {g}")
h = power(2, 3)  # 거듭제곱
print(f"거듭제곱 h = {h}")
i = sqrt(16)  # 제곱근
print(f"제곱근 i = {i}")
j = factorial(5)  # 팩토리얼
print(f"팩토리얼 j = {j}")
k = gcd(48, 18)  # 최대공약수
print(f"최대공약수 k = {k}")

m = div(4.0, 3.0)
print(f"실수 나눗셈 m = {m}")

# --- 복소수 예제 (비슷하게 사칙 함수 사용) ---
print("=== 복소수 ===")
z1 = 1 + 2j
z2 = 3 - 4j
print(f"z1 = {z1}")
print(f"z2 = {z2}")

a = add(z1, z2)  # 덧셈
print(f"덧셈 a = {a}")
b = sub(z1, z2)  # 뺄셈
print(f"뺄셈 b = {b}")
c = mul(z1, z2)  # 곱셈
print(f"곱셈 c = {c}")
d = div(z1, z2)  # 나눗셈
print(f"나눗셈 d = {d}")
e = power(z1, 2)  # 거듭제곱
print(f"거듭제곱 e = {e}")

# 실수부 / 허수부 / 절댓값 / 켤레
print(f"실수부 z1.real = {z1.real}")
print(f"허수부 z1.imag = {z1.imag}")
print(f"절댓값 abs(z1) = {abs(z1)}")
print(f"켤레복소수 z1.conjugate() = {z1.conjugate()}")
