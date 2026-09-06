"""第 5 节练习：按条件筛选数据。"""

import pandas as pd

def filter_customers(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        客户挽留团队要查看年龄至少 30 岁且已经流失的客户。

    学生需要完成什么：
        保留 age >= 30 且 churn == 1 的行，并返回副本。

    参数：
        dataframe：含 age 和 churn 列的客户表。

    返回值：
        同时满足两个条件的客户 DataFrame。

    输入输出示例：
        age=35、churn=1 -> 保留
        age=35、churn=0 或 age=29、churn=1 -> 不保留

    特殊情况：
        没有符合项时返回列结构不变的空表；缺列时抛出 KeyError。
    """
    # TODO: 创建布尔条件并筛选。
    raise NotImplementedError("TODO: 实现 filter_customers")


def filter_by_cities(
    dataframe: pd.DataFrame, cities: list[str]
) -> pd.DataFrame:
    """
    题目背景：
        区域经理只负责若干指定城市。

    学生需要完成什么：
        保留 city 列出现在 cities 列表中的行并返回副本。

    参数：
        dataframe：客户表。
        cities：允许的城市名称列表，匹配区分大小写。

    返回值：
        指定城市的客户 DataFrame。

    输入输出示例：
        cities=["Suzhou"] -> 只保留 city 为 Suzhou 的行
        cities=["Suzhou", "Wuxi"] -> 保留两个城市

    特殊情况：
        cities=[] 返回空表；缺少 city 列时抛出 KeyError。
    """
    # TODO: 使用 isin 筛选城市。
    raise NotImplementedError("TODO: 实现 filter_by_cities")


def filter_spending_range(
    dataframe: pd.DataFrame, minimum: float, maximum: float
) -> pd.DataFrame:
    """
    题目背景：
        营销活动面向月消费处于指定区间的客户。

    学生需要完成什么：
        保留 monthly_spending 在 minimum 到 maximum 之间的行，
        两个边界都包括在内。

    参数：
        dataframe：客户表。
        minimum：最低月消费。
        maximum：最高月消费。

    返回值：
        消费位于闭区间内的客户 DataFrame。

    输入输出示例：
        金额 [100, 200, 300]、范围 100~200 -> 保留 100 和 200
        范围 150~250 -> 只保留 200

    特殊情况：
        minimum > maximum 时抛出 ValueError；缺失金额不会被保留。
    """
    # TODO: 验证范围并筛选月消费。
    raise NotImplementedError("TODO: 实现 filter_spending_range")
