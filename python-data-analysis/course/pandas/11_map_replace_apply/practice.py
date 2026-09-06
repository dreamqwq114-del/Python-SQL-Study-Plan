"""第 11 节练习：map、replace 与 apply。"""

import pandas as pd

def add_churn_and_annual_spending(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        报告需要把 0/1 流失编码变成人能读懂的文字，并估算年消费。

    学生需要完成什么：
        返回副本，新增 churn_label：0 映射为 Stayed，1 映射为 Churned；
        新增 annual_spending：monthly_spending * 12。

    参数：
        dataframe：含 churn 和 monthly_spending 的客户表。

    返回值：
        新增两列后的 DataFrame。

    输入输出示例：
        churn=1、monthly_spending=100 -> Churned、1200
        churn=0、monthly_spending=50 -> Stayed、600

    特殊情况：
        其他 churn 值映射为缺失值；不得修改原表。
    """
    # TODO: 添加文字标签和年消费。
    raise NotImplementedError("TODO: 实现 add_churn_and_annual_spending")


def replace_contract_labels(
    dataframe: pd.DataFrame, labels: dict[str, str]
) -> pd.DataFrame:
    """
    题目背景：
        报表中要把内部合同名称替换成更友好的显示名称。

    学生需要完成什么：
        返回副本，使用 labels 替换 contract_type 中能匹配的值。

    参数：
        dataframe：客户表。
        labels：旧名称到新名称的映射字典。

    返回值：
        合同名称替换后的 DataFrame。

    输入输出示例：
        ["Monthly"]、{"Monthly": "月付"} -> ["月付"]
        ["Yearly"]、{"Monthly": "月付"} -> ["Yearly"]

    特殊情况：
        字典中没有的值保持不变；空字典不改变数据；不修改原表。
    """
    # TODO: 在副本中替换合同标签。
    raise NotImplementedError("TODO: 实现 replace_contract_labels")


def add_spending_band(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        营销团队把客户分为 Low、Medium、High 三个消费档。

    学生需要完成什么：
        返回副本并新增 spending_band。monthly_spending < 200 为 Low，
        200 <= 金额 < 400 为 Medium，金额 >= 400 为 High；
        缺失金额标记为 Unknown。

    参数：
        dataframe：含 monthly_spending 的客户表。

    返回值：
        新增 spending_band 的 DataFrame。

    输入输出示例：
        [199, 200, 400] -> ["Low", "Medium", "High"]
        [None] -> ["Unknown"]

    特殊情况：
        边界 200 属于 Medium，400 属于 High；不修改原表。
    """
    # TODO: 使用 apply 添加消费档位。
    raise NotImplementedError("TODO: 实现 add_spending_band")
