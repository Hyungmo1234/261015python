#미니 프로젝트 2: 학생성적관리 및 통계처리

#• 목적: 학생별 과목 점수를 받아 총점, 평균, 합격 여부(Pass/Fail)를 판정하고 성적순 석차 정렬 및 과목별 평균을 출력하는 프로그램 작성

#1.람다 함수 (Lambda):  (과목은 subjectList에 맞춤 — 키 하드코딩 X)
#•총점 계산: lambda s: sum(s.values())  또는  sum(s[sub] for sub in subjectList)
#•평균 계산: lambda s: sum(s.values()) / len(subjectList)
#•합격 여부(삼항 연산자): lambda avg: "Pass" if avg >= 70 else "Fail"
#2.sorted() & lambda 정렬: sorted(students, key=lambda x: x["avg"], reverse=True)를 이용해 성적 내림차순으로 정렬하여 석차 산출.
#3.map() & lambda: 학생 데이터 리스트에서 특정 과목 점수만 추출하여 학급 전체 과목별 평균을 한 줄로 산출.

# ----- 전역 변수 -----
stdList = []       
scoreBoard = []    # 성적 목록. 원소 예: {"학번": 1, "이름": "김철수", "국어": 90, "영어": 80, "수학": 70}
passScore = 70

def setStudent(stdNo, stdName):
    global stdList
    std = {"학번": stdNo, "이름": stdName}  
    stdList.append(std)

subjectList = ["국어", "영어", "수학"]  # 입력받을 과목 이름들 (바꾸면 점수 키도 같이 바뀜)

while True:
    print("-----------------------------------------------------------------")
    print("학번과 이름을 입력해주세요. 학번에 0을 넣으면 입력완료로 간주합니다.")
    stdNo = int(input("학번 : "))
    if stdNo == 0:
        print("---------------------------------------")
        print("입력 종료합니다.")
        print("---------------------------------------")
        break
    else:
        stdName = input("이름 : ")  # 이름 입력
        setStudent(stdNo, stdName)  # stdList에 학생 추가

for std in stdList:
    print("-----------------------------------------------------------------")
    print(f"------------{std['이름']}의 성적을 입력합니다----------------------")
    # 학번·이름을 scoreBoard에도 넣음 (총점 계산은 subjectList만 합산)
    scoreDict = {"학번": std["학번"], "이름": std["이름"]}
    for subject in subjectList:
        score = int(input(f"{subject} 점수 입력 : "))
        scoreDict[subject] = score  # 키=과목명, 값=점수
    scoreBoard.append(scoreDict)

print("-----------------모든 입력이 끝났습니다--------------------")

# 학생별로 for문
for s in scoreBoard:
    # s 예: {"학번": 1, "이름": "김철수", "국어": 90, "영어": 80, "수학": 70}
    # 학번/이름이 섞여 있으므로 과목(subjectList)만 더함
    total = sum(s[sub] for sub in subjectList)
    avg = total / len(subjectList)
    pf = (lambda a: "Pass" if a >= passScore else "Fail")(avg)
    print(f"------------[{s['학번']}] {s['이름']} 총점: {total}, 평균: {avg:.1f}, 합격여부: {pf}------------")
