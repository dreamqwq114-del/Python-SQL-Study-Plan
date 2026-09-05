"""使用字典表示记录并统计类别示例。"""


def count_contracts(contracts: list[str]) -> dict[str, int]:
    """统计每种合同类型的客户数。"""
    counts: dict[str, int] = {}
    for contract in contracts:
        counts[contract] = counts.get(contract, 0) + 1
    return counts


def main() -> None:
    customer = {
        "customer_id": "C001",
        "city": "Suzhou",
        "monthly_spending": 188.5,
    }
    contracts = ["Monthly", "Yearly", "Monthly", "Two-year"]

    print("客户编号：", customer["customer_id"])
    print("城市：", customer.get("city"))
    print("合同统计：", count_contracts(contracts))
    print("字段：", list(customer.keys()))


if __name__ == "__main__":
    main()
