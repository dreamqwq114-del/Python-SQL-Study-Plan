"""第 10 节答案：合并与拼接。"""

import pandas as pd


def merge_customers_orders(
    customers: pd.DataFrame, orders: pd.DataFrame
) -> pd.DataFrame:
    return customers.merge(
        orders,
        on="customer_id",
        how="left",
    )


def concat_order_batches(batches: list[pd.DataFrame]) -> pd.DataFrame:
    if not batches:
        return pd.DataFrame()
    return pd.concat(batches, ignore_index=True)


def find_orders_without_customer(
    customers: pd.DataFrame, orders: pd.DataFrame
) -> pd.DataFrame:
    mask = ~orders["customer_id"].isin(customers["customer_id"])
    return orders.loc[mask].reset_index(drop=True)
