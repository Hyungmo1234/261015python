"""matplotlib 설치·동작 간단 검증용 예제 (3D)

실행 전에 필요하면:
    pip install matplotlib
"""

# pyplot: 그래프를 그릴 때 쓰는 matplotlib의 간단한 인터페이스
import matplotlib.pyplot as plt

# 3D 축을 쓰려면 이 모듈을 import 해야 함 (직접 안 써도 plt가 인식함)
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ----- 한글 설정 -----
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ----- 그릴 데이터 (x, y, z 세 축) -----
x = [1, 2, 3, 4, 5]
y = [2, 5, 3, 8, 6]
z = [15, 11, 2, 18, 1]

# ----- 3D 그래프 그리기 -----
fig = plt.figure(figsize=(7, 6))

# projection="3d" → 일반 2D 축이 아니라 3D 축으로 만들기
ax = fig.add_subplot(111, projection="3d")

# 3D 선 그래프 (점 + 선)
# xs, ys, zs 순서로 세 축 값을 넣음
ax.plot(x, y, z, marker="o", linestyle="-", color="steelblue", label="점수 경로")

# 산점도만 보려면: ax.scatter(x, y, z, c="tomato", s=50)

ax.set_title("Matplotlib 3D 테스트")
ax.set_xlabel("X (회차)")
ax.set_ylabel("Y (점수)")
ax.set_zlabel("Z (다른 값)")
ax.legend()

plt.tight_layout()
plt.show()  # 창에서 마우스로 돌려가며 볼 수 있음

print("matplotlib 3D 정상 동작 확인")
