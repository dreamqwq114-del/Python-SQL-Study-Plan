"""第 3 节答案：类别编码。"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def encode_city_feature(
    train: pd.DataFrame,
    test: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )
    train_encoded = encoder.fit_transform(train[["city"]])
    test_encoded = encoder.transform(test[["city"]])
    return train_encoded, test_encoded


def encode_categorical_features(
    train: pd.DataFrame,
    test: pd.DataFrame,
    columns: list[str],
) -> tuple[np.ndarray, np.ndarray]:
    if not columns:
        raise ValueError("columns 不能为空")
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )
    train_encoded = encoder.fit_transform(train.loc[:, columns])
    test_encoded = encoder.transform(test.loc[:, columns])
    return train_encoded, test_encoded


def get_encoded_feature_names(
    train: pd.DataFrame,
    columns: list[str],
) -> list[str]:
    if not columns:
        raise ValueError("columns 不能为空")
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )
    encoder.fit(train.loc[:, columns])
    return encoder.get_feature_names_out(columns).tolist()
