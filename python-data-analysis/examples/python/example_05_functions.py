"""函数、参数与返回值示例。"""


def calculate_order_total(
    quantity: int,
    unit_price: float,
    discount: float = 0.0,
) -> float:
    """返回应用折扣后的订单金额。"""
    return quantity * unit_price * (1 - discount)


def calculate_growth_rate(old_value: float, new_value: float) -> float:
    """返回百分数形式的增长率。"""
    return (new_value - old_value) / old_value * 100


def main() -> None:
    regular_total = calculate_order_total(2, 15.0)
    discounted_total = calculate_order_total(3, 20.0, 0.1)
    growth_rate = calculate_growth_rate(100.0, 125.0)

    print(f"无折扣金额：{regular_total:.2f}")
    print(f"折扣后金额：{discounted_total:.2f}")
    print(f"销售增长率：{growth_rate:.1f}%")


if __name__ == "__main__":
    main()
