"""使用条件判断和循环分析客户消费示例。"""


def classify_spending(amount: float) -> str:
    """根据月消费金额返回客户等级。"""
    if amount < 100:
        return "low"
    if amount < 500:
        return "medium"
    return "high"


def main() -> None:
    customers = [("C001", 80.0), ("C002", 220.0), ("C003", 560.0)]
    high_value_count = 0

    for customer_id, spending in customers:
        level = classify_spending(spending)
        print(f"{customer_id}: {level}")
        if level == "high":
            high_value_count += 1

    print("高消费客户数：", high_value_count)


if __name__ == "__main__":
    main()
