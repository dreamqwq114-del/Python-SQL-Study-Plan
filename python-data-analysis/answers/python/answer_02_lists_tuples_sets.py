"""第二章四道练习的参考答案。"""


def unique_recent_items(items: list[str], start: int) -> set[str]:
    """截取指定位置之后的数据并去重。"""
    return set(items[start:])


def calculate_average_score(scores: list[float]) -> float:
    """计算非空成绩列表的平均值。"""
    if len(scores) == 0:
        raise ValueError("成绩列表不能为空")
    return sum(scores) / len(scores)


def unpack_order(order: tuple[str, int, float]) -> str:
    """解包订单并生成摘要。"""
    product, quantity, price = order
    if quantity < 0:
        raise ValueError("数量不能小于 0")
    if price < 0:
        raise ValueError("单价不能小于 0")
    return f"{product}：{quantity} × {price:.2f}"


def find_common_customers(
    first_group: set[str],
    second_group: set[str],
) -> set[str]:
    """返回两个客户组的交集。"""
    return first_group & second_group
