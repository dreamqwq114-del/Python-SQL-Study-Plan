"""第 1 节练习：Series 与 DataFrame。"""

import pandas as pd


def build_customer_frame() -> pd.DataFrame:
    """
    题目背景：
        你需要把两位客户的记录整理成一张小表，供后续分析使用。

    学生需要完成什么：
        创建并返回一个 DataFrame。列顺序必须是 customer_id、city、
        monthly_spending，数据依次为：
        C001、Suzhou、188.5
        C002、Shanghai、420.0

    参数：
        无。

    返回值：
        两行三列的 pandas DataFrame。

    输入输出示例：
        build_customer_frame().shape -> (2, 3)
        build_customer_frame()["customer_id"].tolist() -> ["C001", "C002"]

    特殊情况：
        不使用外部 CSV；每次调用都应返回一张新的 DataFrame。

    提示：
        把“列名: 一列数据”写进字典，再交给 pd.DataFrame()。
    """
    # TODO: 创建题目指定的客户 DataFrame。
    raise NotImplementedError("TODO: 实现 build_customer_frame")


def build_order_series() -> pd.Series:
    """
    题目背景：
        订单编号和购买数量需要组成一列带标签的数据。

    学生需要完成什么：
        创建数量为 1、2、3 的 Series，索引依次为 O001、O002、O003，
        Series 名称必须是 quantity。

    参数：
        无。

    返回值：
        一维 pandas Series。

    输入输出示例：
        build_order_series().loc["O002"] -> 2
        build_order_series().name -> "quantity"

    特殊情况：
        索引和数据顺序必须与题目一致。

    提示：
        pd.Series() 可以同时接收 data、index 和 name。
    """
    # TODO: 创建题目指定的订单数量 Series。
    raise NotImplementedError("TODO: 实现 build_order_series")


def add_order_total(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        订单表只有 quantity 和 unit_price，需要计算每行订单金额。

    学生需要完成什么：
        返回原表的副本，并新增 order_total 列：
        order_total = quantity * unit_price。

    参数：
        dataframe：至少包含 quantity 和 unit_price 两列的订单表。

    返回值：
        新增 order_total 列后的 DataFrame。

    输入输出示例：
        quantity=[2]、unit_price=[50] -> order_total=[100]
        quantity=[0, 3]、unit_price=[99, 10] -> order_total=[0, 30]

    特殊情况：
        不得修改传入的原 DataFrame；缺少所需列时保留 pandas 的 KeyError。

    提示：
        先使用 dataframe.copy()，再让两列直接相乘。
    """
    # TODO: 在副本中计算 order_total。
    raise NotImplementedError("TODO: 实现 add_order_total")
