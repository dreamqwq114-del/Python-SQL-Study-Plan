"""使用 K-Means 给小型客户数据分群。"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def fit_customer_clusters() -> KMeans:
    """创建三群数据并拟合 K-Means。"""
    X, _ = make_blobs(
        n_samples=30,
        centers=3,
        cluster_std=0.4,
        random_state=42,
    )
    return KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10,
    ).fit(X)


def main() -> None:
    model = fit_customer_clusters()
    counts = np.bincount(model.labels_)
    print((model.n_clusters, model.random_state, model.n_init))
    print(counts.tolist())
    print(model.cluster_centers_.shape)


if __name__ == "__main__":
    main()
