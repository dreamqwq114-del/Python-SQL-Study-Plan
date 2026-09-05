"""第 8 节练习：排序与描述统计。"""

import pandas as pd

def spending_statistics(dataframe: pd.DataFrame) -> dict[str, float]:
    """
    题目背景：
        经理需要一眼看到客户月消费的平均数、中位数和最大值。

    学生需要完成什么：
        对 monthly_spending 计算 mean、median、max，并以同名键返回字典。

    参数：
        dataframe：monthly_spending 已是数值的客户表。

    返回值：
        {"mean": 浮点数, "median": 浮点数, "max": 浮点数}。

    输入输出示例：
        [100, 200, 300] -> mean=200、median=200、max=300
        [100, NaN, 300] -> 三项统计自动忽略 NaN

    特殊情况：
        空列返回的三项都是 NaN；缺列时抛出 KeyError。

    提示：
        pandas 的 mean()、median()、max() 默认忽略缺失值。
    """
    # TODO: 计算三项消费统计。
    raise NotImplementedError("TODO: 实现 spending_statistics")


def sort_customers_by_spending(
    dataframe: pd.DataFrame, ascending: bool = False
) -> pd.DataFrame:
    """
    题目背景：
        客户经理想从高消费客户开始查看名单。

    学生需要完成什么：
        按 monthly_spending 排序，方向由 ascending 决定，并重置索引。

    参数：
        dataframe：客户表。
        ascending：True 为从低到高，False 为从高到低。

    返回值：
        排序后的新 DataFrame。

    输入输出示例：
        金额 [100, 300, 200]、ascending=False -> [300, 200, 100]
        同一数据、ascending=True -> [100, 200, 300]

    特殊情况：
        不修改原表；缺失值保持在结果末尾。

    提示：
        sort_values() 可通过 ascending 控制方向。
    """
    # TODO: 排序并重置索引。
    raise NotImplementedError("TODO: 实现 sort_customers_by_spending")


def top_spending_customers(
    dataframe: pd.DataFrame, count: int
) -> pd.DataFrame:
    """
    题目背景：
        奖励活动只邀请消费最高的前 count 位客户。

    学生需要完成什么：
        按 monthly_spending 从高到低排序，返回前 count 行并重置索引。

    参数：
        dataframe：客户表。
        count：需要返回的客户数。

    返回值：
        高消费客户 DataFrame。

    输入输出示例：
        金额 [100, 300, 200]、count=2 -> [300, 200]
        count=0 -> 返回零行

    特殊情况：
        count<0 时抛出 ValueError；count 超过行数时返回全部行。

    提示：
        先 sort_values()，再 head(count)。
    """
    # TODO: 验证 count 并返回前几名。
    raise NotImplementedError("TODO: 实现 top_spending_customers")
