import pr_2
print(pr_2.s)
print("=== Python Log Analyzer ===")

def analyze_log(file_path):
    log_count = {
        "INFO": 0,
        "WARN": 0,
        "ERROR": 0
    }

    total_count = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            total_count += 1

            if "ERROR" in line:
                log_count["ERROR"] += 1
            elif "WARN" in line:
                log_count["WARN"] += 1
            elif "INFO" in line:
                log_count["INFO"] += 1

    return log_count, total_count

def main():
    result, total = analyze_log("logs/server.log")

    print("=== Python Log Analyzer ===")
    print(f"전체 로그: {total}줄")

    for level, count in result.items():
        print(f"{level}: {count}건")

    if total > 0:
        warn_rate = result["WARN"] / total * 100
        error_rate = result["ERROR"] / total * 100
        print(f"WARN 비율: {warn_rate:.1f}%")
        print(f"오류 비율: {error_rate:.1f}%")


if __name__ == "__main__":
    main()

