"""用轮廓系数辅助选择聚类数量。"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score


def build_evaluation_table() -> pd.DataFrame:
    """同时计算 inertia 和 silhouette。"""
    X, _ = make_blobs(
        n_samples=60,
        centers=3,
        cluster_std=0.45,
        random_state=42,
    )
    rows = []
    for k in [2, 3, 4]:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )
        labels = model.fit_predict(X)
        rows.append(
            {
                "k": k,
                "inertia": model.inertia_,
                "silhouette": silhouette_score(X, labels),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    table = build_evaluation_table()
    best_k = int(table.loc[table["silhouette"].idxmax(), "k"])
    print(table["k"].tolist())
    print(best_k)
    print(table["silhouette"].between(-1, 1).all())


if __name__ == "__main__":
    main()
