"""第五章练习：函数、参数与返回值。"""


def calculate_order_total(
    quantity: int,
    unit_price: float,
    discount: float = 0.0,
) -> float:
    """计算应用折扣后的订单金额。

    题目背景：
        多处订单分析都会用到相同的金额公式，应该把公式封装成函数。

    学生需要完成什么：
        返回 quantity * unit_price * (1 - discount)。

    参数：
        quantity：非负商品数量。
        unit_price：非负商品单价。
        discount：0 到 1 之间的小数，默认值为 0。

    返回值：
        折扣后的浮点数金额。

    输入输出示例：
        calculate_order_total(3, 20, 0.1) -> 54.0
        calculate_order_total(2, 15) -> 30.0

    特殊情况：
        数量或单价为负、折扣小于 0 或大于 1 时产生 ValueError。
    """
    # TODO: 验证参数并计算折扣后金额。
    raise NotImplementedError("TODO: 实现 calculate_order_total")


def calculate_growth_rate(old_value: float, new_value: float) -> float:
    """计算指标相对上一期的增长率。

    题目背景：
        月销售额从旧值变为新值，需要用百分比比较变化程度。

    学生需要完成什么：
        使用 (new_value - old_value) / old_value * 100 计算增长率。

    参数：
        old_value：上一期数值，必须大于 0。
        new_value：本期非负数值。

    返回值：
        百分数形式的增长率，例如 20.0 表示增长 20%。

    输入输出示例：
        calculate_growth_rate(100, 120) -> 20.0
        calculate_growth_rate(200, 150) -> -25.0

    特殊情况：
        old_value 小于或等于 0、new_value 小于 0 时产生 ValueError。
    """
    # TODO: 检查输入并计算百分比增长率。
    raise NotImplementedError("TODO: 实现 calculate_growth_rate")


def summarize_scores(scores: list[float]) -> tuple[float, float, float]:
    """一次返回最低分、最高分和平均分。

    题目背景：
        成绩报告需要三个统计值，函数可以用元组一次返回多个结果。

    学生需要完成什么：
        计算最低分、最高分和平均分，按这个顺序组成元组返回。

    参数：
        scores：非空成绩列表，每个成绩应在 0 到 100 之间。

    返回值：
        (最低分, 最高分, 平均分) 三项元组。

    输入输出示例：
        summarize_scores([60, 80, 100]) -> (60, 100, 80.0)
        summarize_scores([88.5]) -> (88.5, 88.5, 88.5)

    特殊情况：
        空列表或存在范围外成绩时产生 ValueError。
    """
    # TODO: 验证成绩并返回三个统计量。
    raise NotImplementedError("TODO: 实现 summarize_scores")


def format_customer_label(customer_id: str, city: str = "Unknown") -> str:
    """生成格式统一的客户标签。

    题目背景：
        报表中需要使用“客户编号 - 城市”的统一显示格式。

    学生需要完成什么：
        去掉 customer_id 和 city 两边的空格并返回“编号 - 城市”。

    参数：
        customer_id：客户编号，去除空格后不能为空。
        city：城市，默认值为 "Unknown"；去除空格后为空也使用 "Unknown"。

    返回值：
        格式为“客户编号 - 城市”的字符串。

    输入输出示例：
        format_customer_label(" C001 ", " Suzhou ") -> "C001 - Suzhou"
        format_customer_label("C002") -> "C002 - Unknown"

    特殊情况：
        customer_id 为空或只有空格时产生 ValueError。
    """
    # TODO: 清理文本并生成客户标签。
    raise NotImplementedError("TODO: 实现 format_customer_label")
