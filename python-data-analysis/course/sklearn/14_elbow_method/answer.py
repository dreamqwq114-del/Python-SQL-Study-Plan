"""第 14 节答案：肘部法。"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def calculate_inertias(
    X: np.ndarray,
    k_values: list[int],
) -> list[float]:
    inertias = []
    for k in k_values:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )
        model.fit(X)
        inertias.append(float(model.inertia_))
    return inertias


def calculate_inertia_drops(
    inertias: list[float],
) -> list[float]:
    if any(value < 0 for value in inertias):
        raise ValueError("inertia 不能为负数")
    drops = []
    for index in range(1, len(inertias)):
        if inertias[index] > inertias[index - 1]:
            raise ValueError("inertia 序列不能上升")
        drops.append(inertias[index - 1] - inertias[index])
    return drops


def build_elbow_table(
    X: np.ndarray,
    k_values: list[int],
) -> pd.DataFrame:
    inertias = calculate_inertias(X, k_values)
    return pd.DataFrame(
        {"k": k_values, "inertia": inertias},
        columns=["k", "inertia"],
    )
