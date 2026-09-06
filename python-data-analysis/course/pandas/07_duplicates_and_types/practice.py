"""第 7 节练习：重复值与数据类型。"""

import pandas as pd

def clean_duplicates_and_spending(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        客户表可能重复导入，同一客户出现多次，消费金额也可能是文本。

    学生需要完成什么：
        按 customer_id 保留第一次出现的记录，把 monthly_spending 用
        安全方式转成数字，失败值变成 NaN，最后重置索引。

    参数：
        dataframe：客户数据表。

    返回值：
        已去重且消费列为数值的新 DataFrame。

    输入输出示例：
        customer_id=["C1", "C1"] -> 只保留第一条 C1
        monthly_spending=["100", "bad"] -> 数字 100.0 和缺失值

    特殊情况：
        不修改原表；缺少所需列时抛出 KeyError。
    """
    # TODO: 按客户去重并安全转换消费列。
    raise NotImplementedError("TODO: 实现 clean_duplicates_and_spending")


def convert_customer_types(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        年龄和消费金额从表格读入后可能都是字符串。

    学生需要完成什么：
        返回副本，把 age 安全转换为 pandas 可空整数 Int64，
        把 monthly_spending 安全转换为浮点数字；失败值变成缺失值。

    参数：
        dataframe：客户表。

    返回值：
        两列类型已修正的新 DataFrame。

    输入输出示例：
        age=["21", "bad"] -> [21, <NA>] 且 dtype 为 Int64
        monthly_spending=["19.5", "bad"] -> [19.5, NaN]

    特殊情况：
        不修改原表；缺少 age 或 monthly_spending 时抛出 KeyError。
    """
    # TODO: 转换 age 和 monthly_spending。
    raise NotImplementedError("TODO: 实现 convert_customer_types")


def keep_latest_customer_records(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        同一客户有多次更新，表中最后出现的记录代表最新状态。

    学生需要完成什么：
        按 customer_id 去重，保留最后一次出现的记录并重置索引。

    参数：
        dataframe：按导入顺序排列的客户表。

    返回值：
        每个客户只保留最新一条记录的新 DataFrame。

    输入输出示例：
        C1 金额依次为 100、120 -> 保留金额 120
        C1、C2 各一条 -> 两条都保留

    特殊情况：
        空表返回空表；缺少 customer_id 时抛出 KeyError。
    """
    # TODO: 保留每位客户最后一条记录。
    raise NotImplementedError("TODO: 实现 keep_latest_customer_records")
