"""第 7 节答案：重复值与数据类型。"""

import pandas as pd


def clean_duplicates_and_spending(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.drop_duplicates(
        subset="customer_id",
        keep="first",
    ).copy()
    result["monthly_spending"] = pd.to_numeric(
        result["monthly_spending"],
        errors="coerce",
    )
    return result.reset_index(drop=True)


def convert_customer_types(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["age"] = pd.to_numeric(
        result["age"],
        errors="coerce",
    ).astype("Int64")
    result["monthly_spending"] = pd.to_numeric(
        result["monthly_spending"],
        errors="coerce",
    )
    return result


def keep_latest_customer_records(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.drop_duplicates(
        subset="customer_id",
        keep="last",
    ).reset_index(drop=True)
