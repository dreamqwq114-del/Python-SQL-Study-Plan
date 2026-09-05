"""第 10 节答案：混淆矩阵。"""

import numpy as np
from sklearn.metrics import confusion_matrix


def build_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> np.ndarray:
    return confusion_matrix(y_true, y_pred, labels=[0, 1])


def confusion_counts(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, int]:
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()
    return {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def normalized_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> np.ndarray:
    return confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
        normalize="true",
    )
