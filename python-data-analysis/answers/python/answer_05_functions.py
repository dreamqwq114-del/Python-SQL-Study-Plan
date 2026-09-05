"""第五章四道练习的参考答案。"""


def calculate_order_total(
    quantity: int,
    unit_price: float,
    discount: float = 0.0,
) -> float:
    """计算应用折扣后的订单金额。"""
    if quantity < 0:
        raise ValueError("数量不能小于 0")
    if unit_price < 0:
        raise ValueError("单价不能小于 0")
    if discount < 0 or discount > 1:
        raise ValueError("折扣必须在 0 到 1 之间")
    return quantity * unit_price * (1 - discount)


def calculate_growth_rate(old_value: float, new_value: float) -> float:
    """计算百分数形式的增长率。"""
    if old_value <= 0:
        raise ValueError("旧值必须大于 0")
    if new_value < 0:
        raise ValueError("新值不能小于 0")
    return (new_value - old_value) / old_value * 100


def summarize_scores(scores: list[float]) -> tuple[float, float, float]:
    """返回最低分、最高分和平均分。"""
    if len(scores) == 0:
        raise ValueError("成绩列表不能为空")
    for score in scores:
        if score < 0 or score > 100:
            raise ValueError("成绩必须在 0 到 100 之间")
    average = sum(scores) / len(scores)
    return min(scores), max(scores), average


def format_customer_label(customer_id: str, city: str = "Unknown") -> str:
    """生成格式统一的客户标签。"""
    cleaned_id = customer_id.strip()
    cleaned_city = city.strip()
    if cleaned_id == "":
        raise ValueError("客户编号不能为空")
    if cleaned_city == "":
        cleaned_city = "Unknown"
    return f"{cleaned_id} - {cleaned_city}"
