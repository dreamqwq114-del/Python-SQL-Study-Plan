"""第 8 节答案：预测标签与概率。"""

from typing import Any

import numpy as np
import pandas as pd


def predict_labels_and_probabilities(
    model: Any,
    X: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    labels = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]
    return labels, probabilities


def predict_with_threshold(
    model: Any,
    X: np.ndarray,
    threshold: float,
) -> np.ndarray:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold 必须在 0 和 1 之间")
    probabilities = model.predict_proba(X)[:, 1]
    return (probabilities >= threshold).astype(int)


def build_prediction_table(
    customer_ids: list[str],
    labels: np.ndarray,
    probabilities: np.ndarray,
) -> pd.DataFrame:
    if not (
        len(customer_ids) == len(labels) == len(probabilities)
    ):
        raise ValueError("三个输入的长度必须一致")
    return pd.DataFrame(
        {
            "customer_id": customer_ids,
            "predicted_churn": labels,
            "churn_probability": probabilities,
        }
    )
