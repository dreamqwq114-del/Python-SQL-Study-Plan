"""第 3 节答案：查看与检查数据。"""

import pandas as pd


def summarize_structure(dataframe: pd.DataFrame) -> dict[str, object]:
    dtypes = {
        column: str(dtype)
        for column, dtype in dataframe.dtypes.items()
    }
    return {
        "rows": dataframe.shape[0],
        "columns": dataframe.columns.tolist(),
        "dtypes": dtypes,
    }


def preview_rows(dataframe: pd.DataFrame, count: int) -> pd.DataFrame:
    if count < 0:
        raise ValueError("count 不能小于 0")
    return dataframe.head(count).copy()


def count_column_values(
    dataframe: pd.DataFrame, column: str, include_missing: bool = False
) -> pd.Series:
    return dataframe[column].value_counts(dropna=not include_missing)
