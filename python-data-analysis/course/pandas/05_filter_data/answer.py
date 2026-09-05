"""第 5 节答案：按条件筛选数据。"""

import pandas as pd


def filter_customers(dataframe: pd.DataFrame) -> pd.DataFrame:
    mask = (dataframe["age"] >= 30) & (dataframe["churn"] == 1)
    return dataframe.loc[mask].copy()


def filter_by_cities(
    dataframe: pd.DataFrame, cities: list[str]
) -> pd.DataFrame:
    mask = dataframe["city"].isin(cities)
    return dataframe.loc[mask].copy()


def filter_spending_range(
    dataframe: pd.DataFrame, minimum: float, maximum: float
) -> pd.DataFrame:
    if minimum > maximum:
        raise ValueError("minimum 不能大于 maximum")
    mask = dataframe["monthly_spending"].between(minimum, maximum)
    return dataframe.loc[mask].copy()
