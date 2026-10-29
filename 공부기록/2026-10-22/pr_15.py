import random

strarg = ["abc0", "cde1", "efg2"]

shflStr = random.shuffle(strarg)

print(strarg)

shflStr = strarg
print(shflStr)


class MyString:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def printMySelf(self):
        print(f"안녕하세요 제 이름은 {self.name} 이고, 나이는 {self.age}살 입니다")

s= MyString("양형모","35")
print(type(s))
print(MyString.__base__)
s.printMySelf()


import datetime

current = datetime.datetime.now()

print(current)