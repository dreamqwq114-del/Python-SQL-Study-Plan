"""第 2 节练习：读取 CSV。"""

from pathlib import Path

import pandas as pd

def load_customers(path: Path) -> pd.DataFrame:
    """
    题目背景：
        客户记录保存在 UTF-8 编码的 CSV 文件中，需要读入 pandas。

    学生需要完成什么：
        使用 pd.read_csv() 读取 path 并返回完整 DataFrame。

    参数：
        path：CSV 文件路径。

    返回值：
        文件中的完整客户 DataFrame。

    输入输出示例：
        文件有 2 行、3 列 -> load_customers(path).shape == (2, 3)
        文件首列为 customer_id -> 返回表首列仍为 customer_id

    特殊情况：
        文件不存在时让 pandas 抛出 FileNotFoundError；不要吞掉错误。

    提示：
        把 path 直接传给 pd.read_csv()。
    """
    # TODO: 读取完整 CSV。
    raise NotImplementedError("TODO: 实现 load_customers")


def load_customer_columns(path: Path, columns: list[str]) -> pd.DataFrame:
    """
    题目背景：
        大型客户表列很多，当前报告只需要其中几列。

    学生需要完成什么：
        读取 CSV，只返回 columns 指定的列，并保持 columns 给出的顺序。

    参数：
        path：CSV 文件路径。
        columns：需要返回的列名列表。

    返回值：
        只含指定列的 DataFrame。

    输入输出示例：
        columns=["city"] -> 返回一列 city
        columns=["age", "customer_id"] -> 列顺序为 age、customer_id

    特殊情况：
        columns=[] 时返回行数不变的零列表；列不存在时抛出 KeyError。

    提示：
        先读取完整表，再使用 dataframe.loc[:, columns]。
    """
    # TODO: 读取后按指定顺序选择列。
    raise NotImplementedError("TODO: 实现 load_customer_columns")


def load_orders_with_dates(path: Path) -> pd.DataFrame:
    """
    题目背景：
        订单日期从 CSV 读入后是文本，不能直接进行日期分析。

    学生需要完成什么：
        读取 CSV，把 order_date 转成 pandas 日期类型并返回新表。
        无法识别的日期应变成 NaT（日期缺失值）。

    参数：
        path：订单 CSV 文件路径。

    返回值：
        order_date 已转换为日期类型的 DataFrame。

    输入输出示例：
        "2025-01-15" -> Timestamp("2025-01-15")
        "not-a-date" -> NaT

    特殊情况：
        缺少 order_date 列时抛出 KeyError；文件不存在时抛出 FileNotFoundError。

    提示：
        使用 pd.to_datetime(..., errors="coerce", format="mixed")。
    """
    # TODO: 读取订单并转换 order_date。
    raise NotImplementedError("TODO: 实现 load_orders_with_dates")
