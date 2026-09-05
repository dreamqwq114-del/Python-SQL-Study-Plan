"""第四章四道练习的参考答案。"""


def classify_spending(amount: float) -> str:
    """根据月消费金额划分客户等级。"""
    if amount < 0:
        raise ValueError("消费金额不能小于 0")
    if amount < 100:
        return "low"
    if amount < 500:
        return "medium"
    return "high"


def count_churned(statuses: list[str]) -> int:
    """统计流失状态为 Yes 的数量。"""
    count = 0
    for status in statuses:
        if status not in ("Yes", "No"):
            raise ValueError("状态只能是 Yes 或 No")
        if status == "Yes":
            count += 1
    return count


def calculate_valid_average(values: list[float | None]) -> float:
    """忽略 None 并计算平均值。"""
    total = 0.0
    count = 0
    for value in values:
        if value is not None:
            total += value
            count += 1
    if count == 0:
        raise ValueError("没有可用于计算的数值")
    return total / count


def find_first_large_order(
    amounts: list[float],
    threshold: float,
) -> int | None:
    """返回第一笔超过阈值的订单索引。"""
    if threshold < 0:
        raise ValueError("阈值不能小于 0")
    for amount in amounts:
        if amount < 0:
            raise ValueError("订单金额不能小于 0")

    for index, amount in enumerate(amounts):
        if amount > threshold:
            return index
    return None
