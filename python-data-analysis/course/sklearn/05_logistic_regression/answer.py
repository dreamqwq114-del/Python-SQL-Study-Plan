"""第 5 节答案：逻辑回归。"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import check_is_fitted


def train_logistic(
    X: np.ndarray,
    y: np.ndarray,
) -> LogisticRegression:
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
    )
    model.fit(X, y)
    return model


def train_logistic_with_strength(
    X: np.ndarray,
    y: np.ndarray,
    regularization_strength: float,
) -> LogisticRegression:
    if regularization_strength <= 0:
        raise ValueError("regularization_strength 必须大于 0")
    model = LogisticRegression(
        C=regularization_strength,
        random_state=42,
        max_iter=1000,
    )
    model.fit(X, y)
    return model


def logistic_coefficient_table(
    model: LogisticRegression,
    feature_names: list[str],
) -> pd.DataFrame:
    check_is_fitted(model)
    coefficients = model.coef_[0]
    if len(feature_names) != len(coefficients):
        raise ValueError("feature_names 数量必须与模型特征数一致")
    result = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
        }
    )
    result["absolute_coefficient"] = result["coefficient"].abs()
    return result.sort_values(
        "absolute_coefficient",
        ascending=False,
    ).reset_index(drop=True)
