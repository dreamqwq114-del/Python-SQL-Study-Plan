"""第 4 节答案：选择行和列。"""

import pandas as pd


def select_customer_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[["customer_id", "monthly_spending"]].copy()


def select_rows_by_labels(
    dataframe: pd.DataFrame, labels: list[object]
) -> pd.DataFrame:
    return dataframe.loc[labels].copy()


def select_data_block(
    dataframe: pd.DataFrame, columns: list[str], row_count: int
) -> pd.DataFrame:
    if row_count < 0:
        raise ValueError("row_count 不能小于 0")
    return dataframe.loc[:, columns].head(row_count).copy()
