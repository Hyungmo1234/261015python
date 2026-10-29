# 1) 기본: 인자 → 식
add = lambda a, b: a + b
print(add(3, 5))  # 8

add3 = lambda a, b, c : a + b + c
print(add3(4,5,6))

# 2) 자주 쓰는 곳: sorted 정렬 키
names = ["qd1", "lee2", "kim3", "park4"]
print(sorted(names))
names.sort(key=lambda s : s[-1], reverse=True)
print(names)

print(sorted(names, key=lambda s: len(s)))  # ['kim', 'lee', 'park']

# 3) map: 각 원소에 같은 연산 적용
nums = [1, 2, 3, 4]
print(list(map(lambda x: x * 2, nums)))  # [2, 4, 6, 8]

mapISGoing = map(lambda t: t[1] + (t[0] * 2), enumerate(nums));

# 인덱스(i)가 필요하면 enumerate 사용 (람다 안에서 i += 1 불가)
print(list(map(lambda t: t[1] + t[0], enumerate(nums))))  # [1, 3, 5, 7]
print(f"mapISGoing is { list(mapISGoing)}")


# 같은 뜻, 더 읽기 쉬운 방식
print([x + i for i, x in enumerate(nums)])  # [1, 3, 5, 7]


# 4) filter: 조건 맞는 것만 남김
print(list(filter(lambda x: x % 2 == 0, nums)))  # [2, 4]

# 5) max / min: 비교 기준 바꾸기
people = [("kim", 30), ("lee", 25), ("park", 35)]
print(max(people, key=lambda p: p[1]))  # ('park', 35) 나이 최대
print(min(people, key=lambda p: p[1]))  # ('lee', 25)  나이 최소
