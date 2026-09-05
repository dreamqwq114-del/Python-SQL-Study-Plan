"""变量、数据类型、类型转换与 f-string 示例。"""


def build_order_summary(
    product_name: str,
    quantity_text: str,
    unit_price_text: str,
) -> str:
    """转换订单字段并返回摘要。"""
    quantity = int(quantity_text)
    unit_price = float(unit_price_text)
    total_amount = quantity * unit_price
    return (
        f"商品：{product_name}，数量：{quantity}，"
        f"单价：{unit_price:.2f} 元，总金额：{total_amount:.2f} 元"
    )


def main() -> None:
    product_name = "Python 入门书"
    quantity_text = "2"
    unit_price_text = "39.90"
    is_member = True
    coupon = None

    print(build_order_summary(product_name, quantity_text, unit_price_text))
    print(type(int(quantity_text)).__name__)
    print(type(float(unit_price_text)).__name__)
    print(type(is_member).__name__)
    print(type(coupon).__name__)


if __name__ == "__main__":
    main()
