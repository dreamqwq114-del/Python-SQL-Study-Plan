"""第三章四道练习的参考答案。"""


def count_categories(values: list[str]) -> dict[str, int]:
    """统计每个类别出现的次数。"""
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def build_customer_record(
    customer_id: str,
    city: str,
    monthly_spending: float,
) -> dict[str, object]:
    """创建一条客户字典记录。"""
    if customer_id == "":
        raise ValueError("客户编号不能为空")
    if monthly_spending < 0:
        raise ValueError("月消费不能小于 0")
    return {
        "customer_id": customer_id,
        "city": city,
        "monthly_spending": monthly_spending,
    }


def get_required_value(record: dict[str, object], key: str) -> object:
    """读取必须存在的字典字段。"""
    return record[key]


def merge_monthly_sales(
    january: dict[str, float],
    february: dict[str, float],
) -> dict[str, float]:
    """合计两个月的商品销售额。"""
    for amount in january.values():
        if amount < 0:
            raise ValueError("销售额不能小于 0")
    for amount in february.values():
        if amount < 0:
            raise ValueError("销售额不能小于 0")

    totals = january.copy()
    for product, amount in february.items():
        totals[product] = totals.get(product, 0) + amount
    return totals
