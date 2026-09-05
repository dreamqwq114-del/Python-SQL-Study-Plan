"""第 8 节答案：排序与描述统计。"""

import pandas as pd


def spending_statistics(dataframe: pd.DataFrame) -> dict[str, float]:
    spending = dataframe["monthly_spending"]
    return {
        "mean": float(spending.mean()),
        "median": float(spending.median()),
        "max": float(spending.max()),
    }


def sort_customers_by_spending(
    dataframe: pd.DataFrame, ascending: bool = False
) -> pd.DataFrame:
    return dataframe.sort_values(
        "monthly_spending",
        ascending=ascending,
    ).reset_index(drop=True)


def top_spending_customers(
    dataframe: pd.DataFrame, count: int
) -> pd.DataFrame:
    if count < 0:
        raise ValueError("count 不能小于 0")
    return dataframe.sort_values(
        "monthly_spending",
        ascending=False,
    ).head(count).reset_index(drop=True)
