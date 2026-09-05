"""把分类结果整理为混淆矩阵与四个计数。"""

import numpy as np
from sklearn.metrics import confusion_matrix


def build_counts() -> tuple[np.ndarray, dict[str, int]]:
    """返回固定示例的矩阵和 TN/FP/FN/TP。"""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 0, 1])
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    counts = {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }
    return matrix, counts


def main() -> None:
    matrix, counts = build_counts()
    print(matrix.tolist())
    print(counts)
    print(matrix.shape)


if __name__ == "__main__":
    main()
