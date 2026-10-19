# ============================================================
# 리스트(list) vs 튜플(tuple)
# - 리스트: []  , 내용 변경 가능 (mutable)
# - 튜플  : ()  , 내용 변경 불가 (immutable)
# ============================================================

# --- 1) 만드는 방법 ------------------------------------------------
scores_list = [90, 85, 78]       # 리스트: 대괄호 []
scores_tuple = (90, 85, 78)      # 튜플  : 소괄호 ()
# 원소 1개짜리 튜플은 반드시 쉼표 필요
one_tuple = (90,)                # (90)만 쓰면 그냥 숫자 90

print(f"리스트 scores_list = {scores_list}")
print(f"튜플   scores_tuple = {scores_tuple}")
print(f"타입 확인 list  = {type(scores_list)}")
print(f"타입 확인 tuple = {type(scores_tuple)}")
print(f"원소 1개 튜플 one_tuple = {one_tuple}, type = {type(one_tuple)}")

# --- 2) 읽기는 둘 다 같음 ------------------------------------------
# 인덱스로 값을 읽는 방식은 동일
print(f"리스트[0] = {scores_list[0]}")
print(f"튜플[0]   = {scores_tuple[0]}")
print(f"리스트 길이 = {len(scores_list)}, 튜플 길이 = {len(scores_tuple)}")

# --- 3) 변경 가능 여부 (가장 큰 차이) -------------------------------
# 리스트: 값을 바꾸거나, 추가/삭제 가능
scores_list[0] = 100             # 수정 OK
scores_list.append(95)           # 맨 뒤에 추가 OK
scores_list.remove(78)           # 값 삭제 OK
print(f"변경 후 리스트 = {scores_list}")

# 튜플: 만들어진 뒤로는 수정/추가/삭제 불가
# scores_tuple[0] = 100          # TypeError: 'tuple' object does not support item assignment
# scores_tuple.append(95)        # AttributeError: 'tuple' object has no attribute 'append'
print(f"튜플은 그대로 = {scores_tuple}")

# --- 4) 언제 뭘 쓰나 -----------------------------------------------
# 리스트: 점수처럼 도중에 바뀌는 데이터 모음
# 튜플  : 좌표, RGB처럼 "한 묶음으로 고정"할 데이터
point = (10, 20)                 # (x, y) 좌표 — 바뀌면 안 되는 느낌
rgb = (255, 128, 0)              # 색상 코드
print(f"좌표 point = {point}")
print(f"색상 rgb   = {rgb}")

# --- 5) 서로 변환 --------------------------------------------------
as_tuple = tuple(scores_list)    # 리스트 → 튜플 (복사본, 원본 리스트는 그대로)
as_list = list(scores_tuple)     # 튜플 → 리스트 (이제 이 복사본은 수정 가능)
print(f"리스트→튜플 as_tuple = {as_tuple}")
print(f"튜플→리스트 as_list  = {as_list}")

# --- 6) 언패킹 (둘 다 가능) ----------------------------------------
x, y = point                     # 튜플을 변수 여러 개로 풀기
a, b, c = [1, 2, 3]              # 리스트도 동일
print(f"언패킹 x = {x}, y = {y}")
print(f"언패킹 a = {a}, b = {b}, c = {c}")

# --- 7) 정리 -------------------------------------------------------
# [] 리스트 = 가변(수정·추가·삭제 O)  → 자주 바뀌는 목록
# () 튜플   = 불변(수정·추가·삭제 X)  → 고정된 묶음, 실수 방지
