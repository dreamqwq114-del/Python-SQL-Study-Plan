"""第 9 节练习：分组与聚合。"""

import pandas as pd

def summarize_by_city(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        区域报告需要比较各城市的客户数量和平均月消费。

    学生需要完成什么：
        按 city 分组，计算 customer_id 的不重复数量 customer_count，
        以及 monthly_spending 的平均值 average_spending，返回普通列结构。

    参数：
        dataframe：客户表。

    返回值：
        列为 city、customer_count、average_spending 的 DataFrame。

    输入输出示例：
        A 城有 C1、C2 -> customer_count=2
        A 城消费 100、300 -> average_spending=200

    特殊情况：
        默认不生成缺失 city 的分组；缺列时抛出 KeyError。
    """
    # TODO: 生成城市汇总表。
    raise NotImplementedError("TODO: 实现 summarize_by_city")


def summarize_orders_by_customer(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        订单明细是一单一行，客户分析需要每位客户的订单数和总金额。

    学生需要完成什么：
        先计算 quantity * unit_price，再按 customer_id 分组；
        返回 order_count（order_id 不重复数量）和 total_spending（金额总和）。

    参数：
        dataframe：订单明细表。

    返回值：
        列为 customer_id、order_count、total_spending 的 DataFrame。

    输入输出示例：
        C1 有 O1、O2 -> order_count=2
        两单金额 100、60 -> total_spending=160

    特殊情况：
        不修改原表；缺少所需列时抛出 KeyError。
    """
    # TODO: 汇总每位客户的订单。
    raise NotImplementedError("TODO: 实现 summarize_orders_by_customer")


def calculate_churn_rate_by_contract(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        团队想比较不同合同类型的客户流失比例。

    学生需要完成什么：
        按 contract_type 分组，返回 customer_count（行数）和
        churn_rate（0/1 churn 列的平均值）。

    参数：
        dataframe：churn 已编码为 0 或 1 的客户表。

    返回值：
        列为 contract_type、customer_count、churn_rate 的 DataFrame。

    输入输出示例：
        Monthly 的 churn=[1, 0] -> churn_rate=0.5
        Yearly 的 churn=[0] -> customer_count=1、churn_rate=0.0

    特殊情况：
        churn 中的缺失值不进入平均值；缺列时抛出 KeyError。
    """
    # TODO: 生成合同类型流失汇总。
    raise NotImplementedError("TODO: 实现 calculate_churn_rate_by_contract")
