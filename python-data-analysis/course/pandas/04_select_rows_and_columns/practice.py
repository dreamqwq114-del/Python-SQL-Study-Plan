"""第 4 节练习：选择行和列。"""

import pandas as pd

def select_customer_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        消费报告只需要客户编号和月消费两列。

    学生需要完成什么：
        按 customer_id、monthly_spending 的顺序返回这两列的副本。

    参数：
        dataframe：客户 DataFrame。

    返回值：
        两列 DataFrame。

    输入输出示例：
        3 行客户表 -> 返回 shape 为 (3, 2)
        原列顺序相反 -> 返回列顺序仍为 customer_id、monthly_spending

    特殊情况：
        缺列时抛出 KeyError；不得修改原表。
    """
    # TODO: 选择固定的两列。
    raise NotImplementedError("TODO: 实现 select_customer_columns")


def select_rows_by_labels(
    dataframe: pd.DataFrame, labels: list[object]
) -> pd.DataFrame:
    """
    题目背景：
        数据表索引可能是客户编号，需要按索引标签找出指定客户。

    学生需要完成什么：
        使用 labels 按给定顺序选择行并返回副本。

    参数：
        dataframe：带索引标签的数据表。
        labels：要选择的索引标签列表。

    返回值：
        选中行的 DataFrame。

    输入输出示例：
        索引 ["C1", "C2"]、labels=["C2"] -> 返回 C2
        labels=["C2", "C1"] -> 返回顺序为 C2、C1

    特殊情况：
        labels=[] 返回零行；标签不存在时抛出 KeyError。
    """
    # TODO: 使用 loc 选择索引标签。
    raise NotImplementedError("TODO: 实现 select_rows_by_labels")


def select_data_block(
    dataframe: pd.DataFrame, columns: list[str], row_count: int
) -> pd.DataFrame:
    """
    题目背景：
        检查报告时，只需看指定列的前几行。

    学生需要完成什么：
        按 columns 给定顺序选择列，再返回前 row_count 行的副本。

    参数：
        dataframe：来源数据表。
        columns：需要的列名。
        row_count：需要的前几行。

    返回值：
        指定数据块。

    输入输出示例：
        3 行表、columns=["city"]、row_count=2 -> 2 行 1 列
        row_count=0 -> 保留指定列但没有数据行

    特殊情况：
        row_count<0 时抛出 ValueError；列不存在时抛出 KeyError。
    """
    # TODO: 验证行数并选择数据块。
    raise NotImplementedError("TODO: 实现 select_data_block")
