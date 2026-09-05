"""计算不同聚类数对应的 inertia。"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def build_elbow_table() -> pd.DataFrame:
    """返回 k=2 至 5 的 inertia 表。"""
    X, _ = make_blobs(
        n_samples=60,
        centers=3,
        cluster_std=0.45,
        random_state=42,
    )
    rows = []
    for k in range(2, 6):
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        ).fit(X)
        rows.append({"k": k, "inertia": model.inertia_})
    return pd.DataFrame(rows)


def main() -> None:
    table = build_elbow_table()
    print(table["k"].tolist())
    print(table["inertia"].is_monotonic_decreasing)
    print(table.round(2).to_dict("records"))


if __name__ == "__main__":
    main()
