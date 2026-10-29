#콘솔기반 가계부
#수입과 지출 내역을 관리하고, 예외발생 없이  총수입, 총지출, 잔액 요약 보고서 출력하는 프로그램 작성

#카테고리 입력에 수입 또는 지출 이외의 값이 들어올 경우, valueError 발생 시켜서 프로그램이 비정상 종료 되지 않도록 예외 처리
# f-string 포맷팅 : 금액 표시 시 천 단위 쉼표 적용
# 딕셔너리 리스트를 사용하여 거래 내역 저장 및 리스트 컴프리핸션/sum() 기반 자동정산

#수입 및 지출 정리 함수

totalCash = 0
totalSpending = 0
totalIncome = 0
cashIndex = 0
cashHistory = {"차수":0, "타입":0, "금액":0}
cashHistoryList = []

def setHistory(calType, value, spendType) :
    global cashIndex, cashHistory
    cashIndex = cashIndex + 1
    cashHistory = {"차수" : cashIndex, "타입" : calType,"용도" : spendType, "금액" : value}
    cashHistoryList.append(cashHistory)


def cal(calType, value) :
    global totalIncome, totalSpending, totalCash
    if calType == 1:
        totalIncome = totalIncome + value
        totalCash = totalCash + value
    elif calType == 2:
        totalSpending = totalSpending + value
        totalCash = totalCash - value
    return totalCash


def useMethod(methodType):
    if methodType == 1:
        try:
            moneyType = int(input("수입은 1, 지출은 2 : "))
            if moneyType not in (1, 2):
                print("1,2 중에서 넣어주셔야죠")
                return
            if moneyType == 1:
                value = int(input("수입액을 넣어주세요 : "))
            else:
                value = int(input("지출액을 넣어주세요 : "))
            spendType = input("용도 : ")
            current = cal(moneyType, value)
            setHistory(moneyType, value, spendType)

        except ValueError:
            print("값을 잘못 입력하신것 같아요. 다시 입력해주세요. 자연수로 넣은것 맞나요?")
            return

    elif methodType == 2:
        print("---------------------------------------")
        print("------현재까지의 수입, 지출, 총액을 보고합니다.-----------")
        for i in cashHistoryList:
            print(f"{i['차수']}회차")
            if i['타입'] == 1 : print("수입")
            if i['타입'] == 2 : print("지출")
            print(f"용도 : {i['용도']}")
            print(f"{i['금액']:,}원")
        print(f"총수입 : {totalIncome:,}")
        print(f"총지출 : {totalSpending:,}")
        print(f"총액(잔액) : {totalCash:,}")

    return 0

while True:
    print("---------------------------------------")
    print("1 : 수입 및 지출 입력")
    print("2 : 보고서 조회")
    print("0 : 종료")
    try:
        buttonNum = int(input("사용자 입력(0,1,2) : "))
    except ValueError:
        print("---------------------------------------")
        print("0,1,2 중에서 입력해주세요.")
        continue
    if buttonNum == 0:
        print("---------------------------------------")
        print("종료합니다.")
        print("---------------------------------------")
        break
    if buttonNum not in (1, 2):
        print("---------------------------------------")
        print("0,1,2 중에서 입력해주세요.")
        continue
    useMethod(buttonNum)

