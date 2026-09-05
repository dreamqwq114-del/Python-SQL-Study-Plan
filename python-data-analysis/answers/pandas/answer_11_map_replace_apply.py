"""第 11 节答案：map、replace 与 apply。"""

import pandas as pd


def add_churn_and_annual_spending(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["churn_label"] = result["churn"].map(
        {0: "Stayed", 1: "Churned"}
    )
    result["annual_spending"] = result["monthly_spending"] * 12
    return result


def replace_contract_labels(
    dataframe: pd.DataFrame, labels: dict[str, str]
) -> pd.DataFrame:
    result = dataframe.copy()
    result["contract_type"] = result["contract_type"].replace(labels)
    return result


def add_spending_band(dataframe: pd.DataFrame) -> pd.DataFrame:
    def to_band(value: float) -> str:
        if pd.isna(value):
            return "Unknown"
        if value < 200:
            return "Low"
        if value < 400:
            return "Medium"
        return "High"

    result = dataframe.copy()
    result["spending_band"] = result["monthly_spending"].apply(to_band)
    return result
