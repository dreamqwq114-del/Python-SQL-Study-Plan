"""第四章练习：条件判断与循环。"""


def classify_spending(amount: float) -> str:
    """根据月消费金额划分客户等级。

    题目背景：
        业务人员希望把客户分为低、中、高消费三组。

    学生需要完成什么：
        amount 小于 100 返回 "low"；100 到 499.99 返回 "medium"；
        500 及以上返回 "high"。

    参数：
        amount：非负月消费金额。

    返回值：
        "low"、"medium" 或 "high"。

    输入输出示例：
        classify_spending(99) -> "low"
        classify_spending(500) -> "high"

    特殊情况：
        100 应归为 "medium"；负数金额应产生 ValueError。

    提示：
        先处理错误输入，再按从小到大的边界写 if/elif/else。
    """
    # TODO: 检查金额并按边界分类。
    raise NotImplementedError("TODO: 实现 classify_spending")


def count_churned(statuses: list[str]) -> int:
    """统计已经流失的客户数量。

    题目背景：
        客户流失列使用 "Yes" 和 "No" 表示状态，需要统计 "Yes" 的数量。

    学生需要完成什么：
        遍历列表，每遇到一个 "Yes" 就把计数加 1。

    参数：
        statuses：只应包含 "Yes" 或 "No" 的状态列表。

    返回值：
        "Yes" 出现的次数。

    输入输出示例：
        count_churned(["Yes", "No", "Yes"]) -> 2
        count_churned([]) -> 0

    特殊情况：
        出现 "yes"、空字符串或其他未知值时产生 ValueError。

    提示：
        循环中可以先验证当前值，再使用 if 判断是否需要计数。
    """
    # TODO: 验证状态并统计 Yes。
    raise NotImplementedError("TODO: 实现 count_churned")


def calculate_valid_average(values: list[float | None]) -> float:
    """忽略缺失值并计算平均数。

    题目背景：
        满意度列表中可能使用 None 表示缺失，平均值只能使用实际存在的数字。

    学生需要完成什么：
        循环收集或累计不是 None 的数值，再计算平均值。

    参数：
        values：浮点数和 None 组成的列表。

    返回值：
        非缺失数字的平均值。

    输入输出示例：
        calculate_valid_average([4, None, 2]) -> 3.0
        calculate_valid_average([5]) -> 5.0

    特殊情况：
        空列表或全部是 None 时产生 ValueError。

    提示：
        同时维护 total 和 count，只有值不是 None 时才更新它们。
    """
    # TODO: 跳过 None 并计算有效数据平均值。
    raise NotImplementedError("TODO: 实现 calculate_valid_average")


def find_first_large_order(
    amounts: list[float],
    threshold: float,
) -> int | None:
    """查找第一笔超过阈值的订单位置。

    题目背景：
        风控人员按时间检查订单，希望尽快找到第一笔超过指定金额的订单。

    学生需要完成什么：
        按顺序循环 amounts，返回第一笔严格大于 threshold 的索引。

    参数：
        amounts：按时间排序的非负订单金额列表。
        threshold：非负判断阈值。

    返回值：
        第一笔大额订单的整数索引；没有找到时返回 None。

    输入输出示例：
        find_first_large_order([20, 150, 80], 100) -> 1
        find_first_large_order([20, 100], 100) -> None

    特殊情况：
        threshold 或任意订单金额为负数时产生 ValueError；等于阈值不算超过。

    提示：
        enumerate() 能同时得到索引和金额，找到后可以立即 return。
    """
    # TODO: 验证金额并查找第一个超过阈值的索引。
    raise NotImplementedError("TODO: 实现 find_first_large_order")
