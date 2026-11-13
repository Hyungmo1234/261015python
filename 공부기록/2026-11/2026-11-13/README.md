# AICE 모의고사 1회 — 학생 최종 성적 예측

출처: [Hyungmo1234/aice-mock1-student-score](https://github.com/Hyungmo1234/aice-mock1-student-score)  
올린 시각: 2026-11-13 19:44 (한국시간)

집에서도 이어서 풀 수 있도록 문제 노트북, 정답 노트북, CSV/JSON을 이 날짜 폴더로 가져왔습니다.

| 파일 | 설명 |
|------|------|
| `AICE_모의고사_1회_학생성적예측_문제.ipynb` | 시험형 문제. 2번 셀에 작성 중이던 읽기 코드가 들어 있습니다. |
| `AICE_모의고사_1회_학생성적예측_정답.ipynb` | 학습용 정답지 |
| `student_demographics.csv` | 학생 인구통계·최종 성적 300명 |
| `course_grades.json` | 중간·퀴즈·프로젝트 점수 300명 |

문제 노트북 2번의 파일 경로는, 깃에 있던 로컬 폴더 경로 대신 이 폴더의 `student_demographics.csv`와 `course_grades.json`을 읽도록 바꿔 두었습니다. 변수 이름 `df_demopraghics`는 작성 중이던 그대로입니다. 문항이 요구하는 이름은 `df_demographics`입니다.
