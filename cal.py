import calendar
import unicodedata


def _display_width(s: str) -> int:
    """터미널 표시 너비 (한글 등은 2칸)"""
    total = 0
    for ch in s:
        total += 2 if unicodedata.east_asian_width(ch) in ("F", "W") else 1
    return total

def _pad(s: str, width: int) -> str:
    """표시 너비 기준으로 가운데 정렬"""
    pad = width - _display_width(s)
    if pad <= 0:
        return s
    left = pad // 2
    right = pad - left
    return " " * left + s + " " * right


class KoreanCalendar(calendar.TextCalendar):
    """일요일 시작, 요일: 일 월 화 수 목 금 토"""

    def __init__(self):
        super().__init__(firstweekday=calendar.SUNDAY)

    def formatweekday(self, day, width):
        # day: 0=월 ... 6=일
        names = ["월", "화", "수", "목", "금", "토", "일"]
        return _pad(names[day], width)

    def formatday(self, day, weekday, width):
        if day == 0:
            s = ""
        else:
            s = str(day)
        return _pad(s, width)


def month(year, month_num, w=3):
    """calendar.month 대신 한글 요일 달력 반환 (w=칸 너비)"""
    return KoreanCalendar().formatmonth(year, month_num, w=w)


m24_6 = month(2024, 6)
m25_9 = month(2025, 9)
d26_12_11 = calendar.day_abbr[calendar.weekday(2026, 12, 11)]

"""
print(m24_6)
print(m25_9)
print(d26_12_11)
"""