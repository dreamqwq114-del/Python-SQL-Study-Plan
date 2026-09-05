"""使用异常保护数据转换示例。"""


def parse_positive_amount(text: str) -> float:
    """把文本转换成严格大于 0 的金额。"""
    amount = float(text)
    if amount <= 0:
        raise ValueError("金额必须大于 0")
    return amount


def main() -> None:
    values = ["12.5", "0", "unknown"]

    for value in values:
        try:
            amount = parse_positive_amount(value)
            print(f"{value} -> {amount:.2f}")
        except ValueError as error:
            print(f"{value} -> 错误：{error}")


if __name__ == "__main__":
    main()
