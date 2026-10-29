import sys
from pathlib import Path

# pr_14 는 2026-10-22 폴더에 있음 → 그 경로를 import 검색에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent / "2026-10-22"))

from pr_14 import henSub

import math

a = "Hello, World!"
b = 5
c = "10"
for i in range(3):
    if b > 3:
        print(a + str(b))
        print(i)
        b = b + 2

print(b + int(c))

print("is it go?")

print(henSub(7, 3))


s = "hello"
