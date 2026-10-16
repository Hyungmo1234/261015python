# Python·Cursor CLI로 하루 배운 것 정리

> 작성일: 2026-10-16  
> 환경: Windows + WSL2, Cursor CLI

오늘은 Cursor CLI로 Python을 만지면서, **실행 환경**과 **언어 문법**을 같이 짚어봤다.

---

## 1. Cursor CLI는 PC 전권이 아니다

에이전트는 워크스페이스·허용된 도구 범위에서 일한다.  
원하면 `approvalMode: unrestricted`로 승인을 최소화할 수 있지만, OS 관리자 권한과는 다르다.

화면 아래 퍼센트(5% → 6%…)는 **요금 토큰 잔액이 아니라 대화 컨텍스트 사용량**이다.  
거의 차면 예전 대화가 잘리거나 요약될 수 있다.

Auto는 매 요청마다 백엔드 모델을 고르지만, 기본적으로 **어떤 모델인지 숨긴다.**  
(팀 설정의 Underlying model = Displayed가 아니면 확인이 어렵다.)

---

## 2. 로그 분석기 (`pr_1.py`)

로그를 읽어 INFO / WARN / ERROR 건수를 세고, **WARN 비율·오류 비율**을 각각 출력한다.

```python
warn_rate = result["WARN"] / total * 100
error_rate = result["ERROR"] / total * 100
print(f"WARN 비율: {warn_rate:.1f}%")
print(f"오류 비율: {error_rate:.1f}%")
```

여러 가상환경에서 돌리고 싶다면 tox(설정 파일형) / nox(스크립트형)를 쓸 수 있다.  
연습용 스크립트 하나면 셸로 venv만 순회해도 충분하다.

---

## 3. 타입·연산 (`pr_2.py`)

### bool과 0, 1

- `0`, `1`은 **int**, `True` / `False`는 **bool**
- 다만 Python에서 `True == 1`, `False == 0`은 참이다
- `False == 1.1`은 타입 에러가 아니라 **그냥 거짓**이다

### 문자열 + 숫자

Java와 다르게 `"문자열" + 숫자`는 `TypeError`가 난다.

```python
print(a + str(b))  # 숫자를 문자열로 변환 후 연결
```

### `for i in range(3)`

`i`는 **0, 1, 2** (3은 미포함). Java의 `for (int i = 0; i < 3; i++)`와 같다.

---

## 4. import의 함정

`import`는 변수만 가져오는 게 아니라 **파일을 위에서부터 실행**한다.  
그래서 최상단 `print` / `for`가 import 시점에 바로 출력된다.

파일명에 하이픈이 있으면 (`pr-2.py`) `import pr-2`는 문법 오류다.  
`pr_2.py`로 바꾸거나 `importlib.import_module("pr-2")`를 쓴다.

실행 코드는 아래처럼 감싸면, import 때는 안 돌고 직접 실행할 때만 돈다.

```python
if __name__ == "__main__":
    main()
```

---

## 5. 들여쓰기

Python에서 들여쓰기는 문법이다.  
블록 밖에서의 무의미한 들여쓰기 → `IndentationError`.

---

## 6. WSL vs Windows Python

같은 PC라도 설치가 분리된다.

| 환경 | 명령 | 예 |
|------|------|-----|
| Windows | `python`, `py` | 3.11 |
| WSL | `python3` | 3.14 (배포판과 함께 설치) |

Windows에 깐 Python을 WSL이 그대로 쓰지는 않는다.

---

## 7. Cursor 업데이트 실패 (보너스)

업데이트 중 `resources` 폴더 이동이 실패하며 **액세스 거부 (os error 5)** 가 났다.  
VS Code가 Cursor 설치 폴더를 잠근 채 업데이트가 돈 전형적인 케이스다.  
VS Code까지 완전히 끈 뒤 Retry 하면 된다.

---

## 한 줄 정리

오늘은 **Python이 어떻게 실행·타입·import 되는지**와  
**Cursor / WSL이 Windows와 어떻게 다른 환경인지**를 같이 익힌 날이다.
