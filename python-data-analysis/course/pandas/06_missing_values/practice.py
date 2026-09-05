"""第 6 节练习：处理缺失值。"""

import pandas as pd

def count_missing(dataframe: pd.DataFrame) -> pd.Series:
    """
    题目背景：
        客户表中可能缺少年龄或满意度，清洗前先统计每列缺了多少。

    学生需要完成什么：
        返回每一列的缺失值数量。

    参数：
        dataframe：要检查的数据表。

    返回值：
        索引为列名、值为缺失数量的 Series。

    输入输出示例：
        age=[20, None] -> age 的缺失数为 1
        city=["A", "B"] -> city 的缺失数为 0

    特殊情况：
        空表仍返回每列 0；不得修改原表。

    提示：
        先用 isna() 得到真假表，再按列 sum()。
    """
    # TODO: 统计每列缺失值。
    raise NotImplementedError("TODO: 实现 count_missing")


def fill_missing_scores(
    dataframe: pd.DataFrame, fill_value: float
) -> pd.DataFrame:
    """
    题目背景：
        满意度缺失时，业务决定使用一个指定分数补齐。

    学生需要完成什么：
        返回原表副本，用 fill_value 填充 satisfaction_score 中的缺失值。

    参数：
        dataframe：客户表。
        fill_value：用于补齐的分数。

    返回值：
        满意度已填充的新 DataFrame。

    输入输出示例：
        scores=[5, None]、fill_value=3 -> [5, 3]
        scores=[4, 2]、fill_value=0 -> [4, 2]

    特殊情况：
        不修改原表；缺少 satisfaction_score 列时抛出 KeyError。

    提示：
        先 copy()，再对指定列使用 fillna()。
    """
    # TODO: 在副本中填充满意度。
    raise NotImplementedError("TODO: 实现 fill_missing_scores")


def drop_incomplete_rows(
    dataframe: pd.DataFrame, required_columns: list[str]
) -> pd.DataFrame:
    """
    题目背景：
        某项分析要求客户编号和城市都不能缺失。

    学生需要完成什么：
        删除 required_columns 中任意一列缺失的行，重置为 0 开始的索引，
        并返回副本。

    参数：
        dataframe：来源数据表。
        required_columns：必须有值的列名。

    返回值：
        删除不完整记录后的 DataFrame。

    输入输出示例：
        required_columns=["city"] -> 删除 city 缺失的行
        required_columns=["id", "city"] -> 任一列缺失都删除

    特殊情况：
        required_columns=[] 时不删除任何行；列不存在时抛出 KeyError。

    提示：
        dropna(subset=...) 可只检查指定列，之后 reset_index(drop=True)。
    """
    # TODO: 删除关键列不完整的行。
    raise NotImplementedError("TODO: 实现 drop_incomplete_rows")
