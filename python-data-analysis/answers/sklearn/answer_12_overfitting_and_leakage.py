"""第 12 节答案：过拟合与数据泄漏。"""

from typing import Any

import numpy as np
from sklearn.preprocessing import StandardScaler


def compare_train_test_accuracy(
    model: Any,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> tuple[float, float]:
    train_accuracy = float(model.score(X_train, y_train))
    test_accuracy = float(model.score(X_test, y_test))
    return train_accuracy, test_accuracy


def detect_overfitting(
    train_accuracy: float,
    test_accuracy: float,
    maximum_gap: float,
) -> bool:
    values = [train_accuracy, test_accuracy, maximum_gap]
    if any(value < 0 or value > 1 for value in values):
        raise ValueError("准确率和差距必须在 0 和 1 之间")
    return train_accuracy - test_accuracy > maximum_gap


def scale_without_leakage(
    X_train: np.ndarray,
    X_test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler.transform(X_train), scaler.transform(X_test)
