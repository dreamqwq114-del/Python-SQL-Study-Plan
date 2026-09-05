"""第 13 节答案：日期操作。"""

import pandas as pd


def add_date_parts(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["join_date"] = pd.to_datetime(
        result["join_date"],
        errors="coerce",
        format="mixed",
    )
    result["join_year"] = result["join_date"].dt.year
    result["join_month"] = result["join_date"].dt.month
    return result


def filter_orders_by_date(
    dataframe: pd.DataFrame, start: str, end: str
) -> pd.DataFrame:
    start_date = pd.to_datetime(start, errors="coerce")
    end_date = pd.to_datetime(end, errors="coerce")
    if pd.isna(start_date) or pd.isna(end_date):
        raise ValueError("start 和 end 必须是有效日期")
    if start_date > end_date:
        raise ValueError("start 不能晚于 end")

    result = dataframe.copy()
    result["order_date"] = pd.to_datetime(
        result["order_date"],
        errors="coerce",
        format="mixed",
    )
    mask = result["order_date"].between(start_date, end_date)
    return result.loc[mask].reset_index(drop=True)


def monthly_order_totals(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["order_date"] = pd.to_datetime(
        result["order_date"],
        errors="coerce",
        format="mixed",
    )
    result["order_total"] = result["quantity"] * result["unit_price"]
    result = result.dropna(subset=["order_date"]).copy()
    result["order_month"] = result["order_date"].dt.strftime("%Y-%m")
    return (
        result.groupby("order_month", as_index=False)["order_total"]
        .sum()
        .sort_values("order_month")
        .reset_index(drop=True)
    )
