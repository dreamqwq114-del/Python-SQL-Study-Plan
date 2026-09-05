"""使用基础类封装客户数据和行为示例。"""


class Customer:
    """保存客户名称和月消费。"""

    def __init__(self, name: str, monthly_spending: float) -> None:
        self.name = name
        self.monthly_spending = monthly_spending

    def annual_spending(self) -> float:
        """返回十二个月的消费金额。"""
        return self.monthly_spending * 12

    def describe(self) -> str:
        """返回客户摘要。"""
        return f"{self.name}: {self.monthly_spending:.2f}"


def main() -> None:
    customers = [
        Customer("Alice", 188.5),
        Customer("Bob", 250.0),
    ]

    for customer in customers:
        print(customer.describe())
        print(f"年消费：{customer.annual_spending():.2f}")


if __name__ == "__main__":
    main()
