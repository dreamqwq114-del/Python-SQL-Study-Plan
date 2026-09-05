"""第 1 节答案：Series 与 DataFrame。"""

import pandas as pd


def build_customer_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "city": ["Suzhou", "Shanghai"],
            "monthly_spending": [188.5, 420.0],
        }
    )


def build_order_series() -> pd.Series:
    return pd.Series(
        [1, 2, 3],
        index=["O001", "O002", "O003"],
        name="quantity",
    )


def add_order_total(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["order_total"] = result["quantity"] * result["unit_price"]
    return result
