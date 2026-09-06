"""第 14 节练习：保存数据。"""

from pathlib import Path

import pandas as pd

def save_processed(dataframe: pd.DataFrame, path: Path) -> None:
    """
    题目背景：
        清洗后的客户表要保存到一个可能尚不存在的输出目录。

    学生需要完成什么：
        创建 path 的父目录，以 UTF-8 CSV 保存 dataframe，不写入索引。

    参数：
        dataframe：要保存的数据表。
        path：目标 CSV 路径。

    返回值：
        None。

    输入输出示例：
        path=output/customers.csv -> 自动创建 output 并写入文件
        两行 DataFrame -> 重新读取后仍有两行，不出现 Unnamed: 0

    特殊情况：
        已存在文件可覆盖；空 DataFrame 也要写出列标题。
    """
    # TODO: 创建目录并保存完整表。
    raise NotImplementedError("TODO: 实现 save_processed")


def save_selected_columns(
    dataframe: pd.DataFrame, path: Path, columns: list[str]
) -> None:
    """
    题目背景：
        对外报告只允许输出指定列，不能保存内部字段。

    学生需要完成什么：
        创建父目录，按 columns 顺序选择列，以 UTF-8 CSV 保存且不写索引。

    参数：
        dataframe：来源数据表。
        path：目标 CSV 路径。
        columns：允许输出的列名及顺序。

    返回值：
        None。

    输入输出示例：
        columns=["city"] -> 文件只有 city 一列
        columns=["age", "customer_id"] -> 文件列顺序相同

    特殊情况：
        列不存在时抛出 KeyError；不得修改原表。
    """
    # TODO: 只保存指定列。
    raise NotImplementedError("TODO: 实现 save_selected_columns")


def save_city_summary(dataframe: pd.DataFrame, path: Path) -> None:
    """
    题目背景：
        经理只需要每个城市的客户数，而不是逐行客户明细。

    学生需要完成什么：
        按 city 分组统计行数，结果列名为 city、customer_count；
        创建父目录并保存为不含索引的 UTF-8 CSV。

    参数：
        dataframe：含 city 列的客户表。
        path：汇总 CSV 的目标路径。

    返回值：
        None。

    输入输出示例：
        city=["A", "A", "B"] -> A 为 2、B 为 1
        空客户表但有 city 列 -> 写出只有标题的空汇总

    特殊情况：
        缺失 city 不建立分组；缺少 city 列时抛出 KeyError。
    """
    # TODO: 生成城市计数汇总并保存。
    raise NotImplementedError("TODO: 实现 save_city_summary")
