"""第 6 节答案：处理缺失值。"""

import pandas as pd


def count_missing(dataframe: pd.DataFrame) -> pd.Series:
    return dataframe.isna().sum()


def fill_missing_scores(
    dataframe: pd.DataFrame, fill_value: float
) -> pd.DataFrame:
    result = dataframe.copy()
    result["satisfaction_score"] = result["satisfaction_score"].fillna(fill_value)
    return result


def drop_incomplete_rows(
    dataframe: pd.DataFrame, required_columns: list[str]
) -> pd.DataFrame:
    return dataframe.dropna(subset=required_columns).reset_index(drop=True)
