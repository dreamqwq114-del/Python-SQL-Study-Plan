"""第 3 节练习：查看与检查数据。"""

import pandas as pd

def summarize_structure(dataframe: pd.DataFrame) -> dict[str, object]:
    """
    题目背景：
        分析前要先确认表有多少行、哪些列以及各列的数据类型。

    学生需要完成什么：
        返回包含 rows、columns、dtypes 的字典。rows 是行数，
        columns 是列名列表，dtypes 是“列名: 类型名称字符串”的字典。

    参数：
        dataframe：要检查的数据表。

    返回值：
        结构摘要字典。

    输入输出示例：
        2 行表 -> summary["rows"] == 2
        int64 的 age 列 -> summary["dtypes"]["age"] == "int64"

    特殊情况：
        空表的 rows 为 0；不修改原表。

    提示：
        shape、columns.tolist() 和 dtype 的 str() 可以完成任务。
    """
    # TODO: 生成 rows、columns、dtypes。
    raise NotImplementedError("TODO: 实现 summarize_structure")


def preview_rows(dataframe: pd.DataFrame, count: int) -> pd.DataFrame:
    """
    题目背景：
        数据表可能有几万行，检查时只想查看开头的少量记录。

    学生需要完成什么：
        返回前 count 行的副本。

    参数：
        dataframe：要预览的数据表。
        count：需要查看的行数。

    返回值：
        前 count 行组成的 DataFrame。

    输入输出示例：
        5 行表、count=2 -> 返回前 2 行
        2 行表、count=10 -> 返回全部 2 行

    特殊情况：
        count=0 返回空表；count<0 时主动抛出 ValueError。

    提示：
        先检查 count，再使用 head(count).copy()。
    """
    # TODO: 验证 count 并返回表头副本。
    raise NotImplementedError("TODO: 实现 preview_rows")


def count_column_values(
    dataframe: pd.DataFrame, column: str, include_missing: bool = False
) -> pd.Series:
    """
    题目背景：
        你想快速知道每种合同类型出现了多少次。

    学生需要完成什么：
        统计 column 中每个值的出现次数；include_missing=True 时也统计缺失值。

    参数：
        dataframe：来源数据表。
        column：要统计的列名。
        include_missing：是否把缺失值也作为一类。

    返回值：
        value_counts() 生成的计数 Series。

    输入输出示例：
        ["A", "A", "B"] -> A 为 2、B 为 1
        ["A", None] 且 include_missing=True -> 两类计数都为 1

    特殊情况：
        列不存在时抛出 KeyError；空列返回空 Series。

    提示：
        value_counts() 的 dropna 参数控制是否忽略缺失值。
    """
    # TODO: 返回指定列的频数统计。
    raise NotImplementedError("TODO: 实现 count_column_values")
