"""第三章练习：使用字典组织和汇总表格数据。"""


def count_categories(values: list[str]) -> dict[str, int]:
    """统计每个类别出现的次数。

    题目背景：
        客户合同类型从表格的一列读出，需要统计 Monthly、Yearly 等类别分别
        出现多少次。

    学生需要完成什么：
        遍历 values，用字典保存“类别 -> 次数”并返回。

    参数：
        values：类别文本组成的列表，大小写不同视为不同类别。

    返回值：
        键为类别、值为出现次数的字典。

    输入输出示例：
        count_categories(["A", "B", "A"]) -> {"A": 2, "B": 1}
        count_categories([]) -> {}

    特殊情况：
        空列表返回空字典；不要改变原列表。
    """
    # TODO: 遍历列表并累计每个类别的次数。
    raise NotImplementedError("TODO: 实现 count_categories")


def build_customer_record(
    customer_id: str,
    city: str,
    monthly_spending: float,
) -> dict[str, object]:
    """把三个客户字段组织成一条字典记录。

    题目背景：
        表格中的一行数据常用字典表示，列名是键，该行中的数据是值。

    学生需要完成什么：
        返回包含 customer_id、city、monthly_spending 三个键的字典。

    参数：
        customer_id：客户编号，不能为空。
        city：客户所在城市。
        monthly_spending：客户月消费，不能小于 0。

    返回值：
        保存三个字段的字典。

    输入输出示例：
        build_customer_record("C1", "Suzhou", 120.5)
        -> {"customer_id": "C1", "city": "Suzhou", "monthly_spending": 120.5}
        build_customer_record("C2", "", 0)
        -> {"customer_id": "C2", "city": "", "monthly_spending": 0}

    特殊情况：
        customer_id 为空或 monthly_spending 为负数时产生 ValueError。
    """
    # TODO: 检查输入并创建客户字典。
    raise NotImplementedError("TODO: 实现 build_customer_record")


def get_required_value(record: dict[str, object], key: str) -> object:
    """读取字典中必须存在的字段。

    题目背景：
        分析代码依赖 customer_id 等关键字段。如果字段不存在，应该立即暴露
        问题，而不是静默返回错误结果。

    学生需要完成什么：
        使用方括号根据 key 读取并返回对应值。

    参数：
        record：一条字典记录。
        key：必须存在的字段名。

    返回值：
        字典中 key 对应的值。

    输入输出示例：
        get_required_value({"city": "Suzhou"}, "city") -> "Suzhou"
        get_required_value({"score": 0}, "score") -> 0

    特殊情况：
        key 不存在时应由 Python 产生 KeyError；不要改用默认值掩盖错误。
    """
    # TODO: 用必须存在字段的方式读取字典。
    raise NotImplementedError("TODO: 实现 get_required_value")


def merge_monthly_sales(
    january: dict[str, float],
    february: dict[str, float],
) -> dict[str, float]:
    """合并两个月的商品销售额。

    题目背景：
        两个月的销售额分别保存在字典中，同一商品可能同时出现在两个月，也可能
        只出现在其中一个月。

    学生需要完成什么：
        创建新字典，累加同名商品的销售额并返回。

    参数：
        january：一月的“商品 -> 销售额”字典。
        february：二月的“商品 -> 销售额”字典。

    返回值：
        两个月合计后的新字典。

    输入输出示例：
        merge_monthly_sales({"Pen": 10}, {"Pen": 5, "Book": 20})
        -> {"Pen": 15, "Book": 20}
        merge_monthly_sales({}, {"Book": 8}) -> {"Book": 8}

    特殊情况：
        任意销售额为负数时产生 ValueError；不能修改传入的两个字典。
    """
    # TODO: 检查金额并合并两个销售字典。
    raise NotImplementedError("TODO: 实现 merge_monthly_sales")
