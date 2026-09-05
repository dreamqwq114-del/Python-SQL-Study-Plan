"""第 6 节答案：决策树。"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.validation import check_is_fitted


def train_tree(
    X: np.ndarray,
    y: np.ndarray,
) -> DecisionTreeClassifier:
    model = DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
    )
    model.fit(X, y)
    return model


def train_tree_with_depth(
    X: np.ndarray,
    y: np.ndarray,
    max_depth: int,
) -> DecisionTreeClassifier:
    if max_depth <= 0:
        raise ValueError("max_depth 必须大于 0")
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=42,
    )
    model.fit(X, y)
    return model


def tree_importance_table(
    model: DecisionTreeClassifier,
    feature_names: list[str],
) -> pd.DataFrame:
    check_is_fitted(model)
    importances = model.feature_importances_
    if len(feature_names) != len(importances):
        raise ValueError("feature_names 数量必须与模型特征数一致")
    result = pd.DataFrame(
        {"feature": feature_names, "importance": importances}
    )
    return result.sort_values(
        "importance",
        ascending=False,
    ).reset_index(drop=True)
