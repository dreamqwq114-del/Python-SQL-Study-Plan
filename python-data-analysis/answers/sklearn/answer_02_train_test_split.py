"""第 2 节答案：训练集与测试集。"""

import pandas as pd
from sklearn.model_selection import train_test_split


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    return train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )


def split_with_test_size(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    if not 0 < test_size < 1:
        raise ValueError("test_size 必须在 0 和 1 之间")
    return train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=42,
    )


def summarize_split_balance(
    y_train: pd.Series,
    y_test: pd.Series,
) -> dict[str, float]:
    if y_train.empty or y_test.empty:
        raise ValueError("训练标签和测试标签都不能为空")
    return {
        "train_positive_rate": float(y_train.mean()),
        "test_positive_rate": float(y_test.mean()),
    }
