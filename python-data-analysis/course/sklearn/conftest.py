"""scikit-learn 各章共享的 pytest 配置与夹具。"""

import numpy as np
import pytest
from sklearn.datasets import make_blobs, make_classification
from sklearn.model_selection import train_test_split

@pytest.fixture(scope="module")
def classification_data() -> tuple[np.ndarray, np.ndarray]:
    return make_classification(
        n_samples=100,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )

@pytest.fixture(scope="module")
def split_classification_data(
    classification_data: tuple[np.ndarray, np.ndarray],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X, y = classification_data
    return train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )

@pytest.fixture(scope="module")
def cluster_data() -> np.ndarray:
    X, _ = make_blobs(
        n_samples=60,
        centers=3,
        cluster_std=0.45,
        random_state=42,
    )
    return X
