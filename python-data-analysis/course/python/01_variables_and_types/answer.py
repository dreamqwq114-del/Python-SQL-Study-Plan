"""第一章四道练习的参考答案。"""


def convert_age(age_text: str) -> int:
    """把年龄文本转换为非负整数。"""
    age = int(age_text)
    if age < 0:
        raise ValueError("年龄不能小于 0")
    return age


def convert_price(price_text: str) -> float:
    """把价格文本转换为非负浮点数。"""
    price = float(price_text)
    if price < 0:
        raise ValueError("价格不能小于 0")
    return price


def calculate_order_amount(unit_price_text: str, quantity_text: str) -> float:
    """转换单价和数量，并计算订单总金额。"""
    unit_price = float(unit_price_text)
    quantity = int(quantity_text)
    if unit_price < 0:
        raise ValueError("单价不能小于 0")
    if quantity < 0:
        raise ValueError("数量不能小于 0")
    return unit_price * quantity


def build_order_summary(
    product_name: str,
    quantity_text: str,
    unit_price_text: str,
) -> str:
    """生成包含商品、数量、单价和总金额的订单摘要。"""
    quantity = int(quantity_text)
    unit_price = float(unit_price_text)
    if quantity < 0:
        raise ValueError("数量不能小于 0")
    if unit_price < 0:
        raise ValueError("单价不能小于 0")
    total_amount = unit_price * quantity
    return (
        f"商品：{product_name}，数量：{quantity}，"
        f"单价：{unit_price:.2f} 元，总金额：{total_amount:.2f} 元"
    )
