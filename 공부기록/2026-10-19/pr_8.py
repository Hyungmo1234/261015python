
s= """ 나는 띄어쓰기가 가능한지 확인하고 싶은 문자열입니다
들여쓰기는 어떻게 해야하지?
    이게 맞나요?"""


print(s)

print(len(s))

print(s[4])

print(f"{s!r}")

from collections import deque
q = deque([1,2,3])

print(q.popleft())

print(q)

print(q.pop())
print(q)

q.append(4)
q.appendleft(0)

print(q)