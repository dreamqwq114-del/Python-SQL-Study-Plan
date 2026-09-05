"""第 9 节答案：分类指标。"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def calculate_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
) -> dict[str, float]:
    if len(np.unique(y_true)) < 2:
        raise ValueError("计算 ROC AUC 时 y_true 必须包含两个类别")
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(
            precision_score(y_true, y_pred, zero_division=0)
        ),
        "recall": float(
            recall_score(y_true, y_pred, zero_division=0)
        ),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
    }


def calculate_threshold_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
) -> dict[str, float]:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold 必须在 0 和 1 之间")
    y_pred = (y_prob >= threshold).astype(int)
    return {
        "precision": float(
            precision_score(y_true, y_pred, zero_division=0)
        ),
        "recall": float(
            recall_score(y_true, y_pred, zero_division=0)
        ),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }


def calculate_specificity(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:
    tn, fp, _, _ = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()
    denominator = tn + fp
    if denominator == 0:
        return 0.0
    return float(tn / denominator)
