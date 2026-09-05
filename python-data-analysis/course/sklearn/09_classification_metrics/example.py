"""计算多项二分类指标。"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def calculate_metrics() -> dict[str, float]:
    """对固定预测结果计算五项指标。"""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 1, 1])
    y_prob = np.array([0.1, 0.6, 0.7, 0.9])
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_prob),
    }


def main() -> None:
    metrics = calculate_metrics()
    print(list(metrics))
    print({name: round(value, 3) for name, value in metrics.items()})


if __name__ == "__main__":
    main()
