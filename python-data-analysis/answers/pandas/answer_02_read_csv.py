"""第 2 节答案：读取 CSV。"""

from pathlib import Path

import pandas as pd


def load_customers(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8")


def load_customer_columns(path: Path, columns: list[str]) -> pd.DataFrame:
    dataframe = pd.read_csv(path, encoding="utf-8")
    return dataframe.loc[:, columns].copy()


def load_orders_with_dates(path: Path) -> pd.DataFrame:
    dataframe = pd.read_csv(path, encoding="utf-8")
    dataframe["order_date"] = pd.to_datetime(
        dataframe["order_date"],
        errors="coerce",
        format="mixed",
    )
    return dataframe
