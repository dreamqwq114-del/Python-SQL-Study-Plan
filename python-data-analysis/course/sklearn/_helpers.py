"""scikit-learn 多章测试共享的构造辅助函数。"""

import numpy as np
from sklearn.datasets import make_blobs, make_classification
from sklearn.model_selection import train_test_split

def comparison_split() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X, y = make_classification(
        n_samples=80,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )
    return train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )

def small_clusters() -> np.ndarray:
    X, _ = make_blobs(
        n_samples=30,
        centers=3,
        cluster_std=0.4,
        random_state=42,
    )
    return X

def tiny_classification() -> tuple[np.ndarray, np.ndarray]:
    return make_classification(
        n_samples=40,
        n_features=3,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )
