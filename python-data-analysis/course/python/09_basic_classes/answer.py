"""第九章四道练习的参考答案。"""


class Customer:
    """保存客户名称和月消费。"""

    def __init__(self, name: str, monthly_spending: float) -> None:
        if name == "":
            raise ValueError("客户名称不能为空")
        if monthly_spending < 0:
            raise ValueError("月消费不能小于 0")
        self.name = name
        self.monthly_spending = monthly_spending

    def annual_spending(self) -> float:
        """返回十二个月的消费金额。"""
        return self.monthly_spending * 12

    def describe(self) -> str:
        """返回固定格式的客户描述。"""
        return f"{self.name}: {self.monthly_spending:.2f}"


class Order:
    """保存订单字段并计算总金额。"""

    def __init__(self, product_name: str, quantity: int, unit_price: float) -> None:
        if product_name == "":
            raise ValueError("商品名不能为空")
        if quantity < 0:
            raise ValueError("数量不能小于 0")
        if unit_price < 0:
            raise ValueError("单价不能小于 0")
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    def total(self) -> float:
        """返回订单总金额。"""
        return self.quantity * self.unit_price

    def describe(self) -> str:
        """返回固定格式的订单描述。"""
        return f"{self.product_name} × {self.quantity} = {self.total():.2f}"


class ScoreSummary:
    """保存一组成绩并提供统计方法。"""

    def __init__(self, scores: list[float]) -> None:
        if len(scores) == 0:
            raise ValueError("成绩列表不能为空")
        for score in scores:
            if score < 0 or score > 100:
                raise ValueError("成绩必须在 0 到 100 之间")
        self.scores = list(scores)

    def average(self) -> float:
        """返回平均分。"""
        return sum(self.scores) / len(self.scores)

    def highest(self) -> float:
        """返回最高分。"""
        return max(self.scores)


def build_customers(rows: list[tuple[str, float]]) -> list[Customer]:
    """把多行数据转换为 Customer 对象。"""
    customers: list[Customer] = []
    for name, spending in rows:
        customers.append(Customer(name, spending))
    return customers
