"""第 13 节答案：K-Means 聚类。"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def fit_kmeans(X: np.ndarray, n_clusters: int) -> KMeans:
    if n_clusters <= 0:
        raise ValueError("n_clusters 必须大于 0")
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10,
    )
    model.fit(X)
    return model


def cluster_customers(
    X: np.ndarray,
    n_clusters: int,
) -> np.ndarray:
    if n_clusters <= 0:
        raise ValueError("n_clusters 必须大于 0")
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10,
    )
    return model.fit_predict(X)


def cluster_centers_table(
    model: KMeans,
    feature_names: list[str],
) -> pd.DataFrame:
    centers = model.cluster_centers_
    if len(feature_names) != centers.shape[1]:
        raise ValueError("feature_names 数量必须与中心列数一致")
    result = pd.DataFrame(centers, columns=feature_names)
    result.insert(0, "cluster", range(model.n_clusters))
    return result
