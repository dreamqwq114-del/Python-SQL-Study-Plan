"""第 7 节答案：随机森林。"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.validation import check_is_fitted


def train_forest(
    X: np.ndarray,
    y: np.ndarray,
) -> RandomForestClassifier:
    model = RandomForestClassifier(
        n_estimators=50,
        random_state=42,
    )
    model.fit(X, y)
    return model


def train_forest_with_estimators(
    X: np.ndarray,
    y: np.ndarray,
    n_estimators: int,
) -> RandomForestClassifier:
    if n_estimators <= 0:
        raise ValueError("n_estimators 必须大于 0")
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=42,
    )
    model.fit(X, y)
    return model


def forest_importance_table(
    model: RandomForestClassifier,
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
