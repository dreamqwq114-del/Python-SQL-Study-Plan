"""第 1 节答案：特征 X 与标签 y。"""

import pandas as pd


def select_features_and_label(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    X = dataframe[["age", "monthly_spending"]].copy()
    y = dataframe["churn"].copy()
    return X, y


def select_mixed_features(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    X = dataframe[["age", "monthly_spending", "city"]].copy()
    y = dataframe["churn"].copy()
    return X, y


def count_target_classes(target: pd.Series) -> dict[int, int]:
    if target.isna().any() or not target.isin([0, 1]).all():
        raise ValueError("target 必须只包含 0 和 1，且不能缺失")
    counts = target.value_counts()
    return {
        0: int(counts.get(0, 0)),
        1: int(counts.get(1, 0)),
    }
