"""第 14 节答案：保存数据。"""

from pathlib import Path

import pandas as pd


def save_processed(dataframe: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False, encoding="utf-8")


def save_selected_columns(
    dataframe: pd.DataFrame, path: Path, columns: list[str]
) -> None:
    selected = dataframe.loc[:, columns]
    path.parent.mkdir(parents=True, exist_ok=True)
    selected.to_csv(path, index=False, encoding="utf-8")


def save_city_summary(dataframe: pd.DataFrame, path: Path) -> None:
    summary = (
        dataframe.groupby("city")
        .size()
        .reset_index(name="customer_count")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False, encoding="utf-8")
