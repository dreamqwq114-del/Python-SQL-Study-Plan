"""第 15 节答案：轮廓系数。"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def calculate_silhouette_scores(
    X: np.ndarray,
    k_values: list[int],
) -> dict[int, float]:
    scores = {}
    for k in k_values:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )
        labels = model.fit_predict(X)
        scores[k] = float(silhouette_score(X, labels))
    return scores


def select_best_silhouette_k(scores: dict[int, float]) -> int:
    if not scores:
        raise ValueError("scores 不能为空")
    return min(scores, key=lambda k: (-scores[k], k))


def build_cluster_evaluation(
    X: np.ndarray,
    k_values: list[int],
) -> pd.DataFrame:
    rows = []
    for k in k_values:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )
        labels = model.fit_predict(X)
        rows.append(
            {
                "k": k,
                "inertia": float(model.inertia_),
                "silhouette": float(silhouette_score(X, labels)),
            }
        )
    return pd.DataFrame(
        rows,
        columns=["k", "inertia", "silhouette"],
    )
