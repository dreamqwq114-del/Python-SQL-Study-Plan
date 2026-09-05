"""第 4 节答案：数值标准化。"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_features(
    train: np.ndarray,
    test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train)
    test_scaled = scaler.transform(test)
    return train_scaled, test_scaled


def scale_dataframe_columns(
    train: pd.DataFrame,
    test: pd.DataFrame,
    columns: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_result = train.copy()
    test_result = test.copy()
    if not columns:
        return train_result, test_result
    scaler = StandardScaler()
    train_result[columns] = scaler.fit_transform(train.loc[:, columns])
    test_result[columns] = scaler.transform(test.loc[:, columns])
    return train_result, test_result


def summarize_scaled_training(
    scaled_train: np.ndarray,
) -> dict[str, np.ndarray]:
    if scaled_train.ndim != 2 or scaled_train.size == 0:
        raise ValueError("scaled_train 必须是非空二维数组")
    return {
        "mean": np.mean(scaled_train, axis=0),
        "std": np.std(scaled_train, axis=0),
    }
