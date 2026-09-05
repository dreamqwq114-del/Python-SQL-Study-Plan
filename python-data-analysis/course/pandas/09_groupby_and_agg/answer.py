"""第 9 节答案：分组与聚合。"""

import pandas as pd


def summarize_by_city(dataframe: pd.DataFrame) -> pd.DataFrame:
    return (
        dataframe.groupby("city")
        .agg(
            customer_count=("customer_id", "nunique"),
            average_spending=("monthly_spending", "mean"),
        )
        .reset_index()
    )


def summarize_orders_by_customer(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["order_total"] = result["quantity"] * result["unit_price"]
    return (
        result.groupby("customer_id")
        .agg(
            order_count=("order_id", "nunique"),
            total_spending=("order_total", "sum"),
        )
        .reset_index()
    )


def calculate_churn_rate_by_contract(dataframe: pd.DataFrame) -> pd.DataFrame:
    return (
        dataframe.groupby("contract_type")
        .agg(
            customer_count=("churn", "size"),
            churn_rate=("churn", "mean"),
        )
        .reset_index()
    )
