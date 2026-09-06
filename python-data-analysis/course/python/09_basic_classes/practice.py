"""第九章练习：用基础类表示客户、订单和成绩摘要。"""


class Customer:
    """练习 1：保存客户状态并提供描述方法。

    题目背景：
        客户编号和月消费属于同一个客户对象，方法可以使用对象内部的数据。

    学生需要完成什么：
        __init__ 保存 name 和非负 monthly_spending；annual_spending() 返回
        月消费乘以 12；describe() 返回“name: 188.50”格式。

    参数：
        name：非空客户名称。
        monthly_spending：非负月消费。

    返回值：
        构造方法没有返回值；其他方法分别返回浮点数和字符串。

    输入输出示例：
        Customer("Alice", 100).annual_spending() -> 1200
        Customer("Alice", 188.5).describe() -> "Alice: 188.50"

    特殊情况：
        name 为空或 monthly_spending 为负数时产生 ValueError。
    """

    def __init__(self, name: str, monthly_spending: float) -> None:
        """验证并保存客户名称与非负月消费。"""
        # TODO: 验证并保存客户属性。
        raise NotImplementedError("TODO: 实现 Customer.__init__")

    def annual_spending(self) -> float:
        """返回十二个月的消费金额。"""
        # TODO: 返回十二个月的消费金额。
        raise NotImplementedError("TODO: 实现 Customer.annual_spending")

    def describe(self) -> str:
        """返回类说明中规定格式的客户描述。"""
        # TODO: 返回固定格式的客户描述。
        raise NotImplementedError("TODO: 实现 Customer.describe")


class Order:
    """练习 2：把订单数据和金额计算放进同一个类。

    题目背景：
        每条订单都有商品、数量和单价，订单对象可以自己计算总金额。

    学生需要完成什么：
        保存三个属性；total() 返回数量乘单价；describe() 返回固定文本。

    参数：
        product_name：非空商品名。
        quantity：非负整数数量。
        unit_price：非负单价。

    返回值：
        total() 返回浮点数；describe() 返回“商品 × 数量 = 金额”文本。

    输入输出示例：
        Order("Pen", 3, 2.5).total() -> 7.5
        Order("Book", 2, 12).describe() -> "Book × 2 = 24.00"

    特殊情况：
        商品名为空、数量或单价为负数时产生 ValueError。
    """

    def __init__(self, product_name: str, quantity: int, unit_price: float) -> None:
        """验证并保存商品名称、数量和单价。"""
        # TODO: 验证并保存订单属性。
        raise NotImplementedError("TODO: 实现 Order.__init__")

    def total(self) -> float:
        """返回该订单的总金额。"""
        # TODO: 返回订单总金额。
        raise NotImplementedError("TODO: 实现 Order.total")

    def describe(self) -> str:
        """返回类说明中规定格式的订单描述。"""
        # TODO: 返回固定格式的订单描述。
        raise NotImplementedError("TODO: 实现 Order.describe")


class ScoreSummary:
    """练习 3：让对象保存一组成绩并计算统计量。

    题目背景：
        同一组成绩会被多次查询平均分和最高分，可以由对象保存这组数据。

    学生需要完成什么：
        保存成绩列表的副本；average() 返回平均分；highest() 返回最高分。

    参数：
        scores：非空且每项在 0 到 100 之间的成绩列表。

    返回值：
        average() 和 highest() 都返回数字。

    输入输出示例：
        ScoreSummary([60, 80, 100]).average() -> 80.0
        ScoreSummary([88.5]).highest() -> 88.5

    特殊情况：
        空列表或范围外成绩产生 ValueError；对象不能直接保存外部列表引用。
    """

    def __init__(self, scores: list[float]) -> None:
        """验证成绩并保存列表副本。"""
        # TODO: 验证成绩并保存列表副本。
        raise NotImplementedError("TODO: 实现 ScoreSummary.__init__")

    def average(self) -> float:
        """返回已保存成绩的平均值。"""
        # TODO: 返回平均分。
        raise NotImplementedError("TODO: 实现 ScoreSummary.average")

    def highest(self) -> float:
        """返回已保存成绩中的最高值。"""
        # TODO: 返回最高分。
        raise NotImplementedError("TODO: 实现 ScoreSummary.highest")


def build_customers(rows: list[tuple[str, float]]) -> list[Customer]:
    """练习 4：把多行原始数据转换为 Customer 对象。

    题目背景：
        表格数据读出后常表现为多行元组，需要逐行创建业务对象。

    学生需要完成什么：
        遍历 rows，为每个 (name, monthly_spending) 创建 Customer 并返回列表。

    参数：
        rows：客户名称和月消费组成的二项元组列表。

    返回值：
        与输入顺序一致的 Customer 对象列表。

    输入输出示例：
        build_customers([("A", 10)])[0].describe() -> "A: 10.00"
        build_customers([]) -> []

    特殊情况：
        任意一行数据无效时，由 Customer 产生 ValueError。
    """
    # TODO: 逐行创建 Customer 对象。
    raise NotImplementedError("TODO: 实现 build_customers")
