"""第 11 节答案：模型比较。"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.tree import DecisionTreeClassifier


def compare_models(
    X_train: np.ndarray,
    X_validation: np.ndarray,
    y_train: np.ndarray,
    y_validation: np.ndarray,
) -> pd.DataFrame:
    models = [
        (
            "Logistic",
            LogisticRegression(max_iter=1000, random_state=42),
        ),
        (
            "Tree",
            DecisionTreeClassifier(max_depth=3, random_state=42),
        ),
    ]
    rows = []
    for name, model in models:
        model.fit(X_train, y_train)
        predictions = model.predict(X_validation)
        probabilities = model.predict_proba(X_validation)[:, 1]
        rows.append(
            {
                "model": name,
                "accuracy": float(
                    accuracy_score(y_validation, predictions)
                ),
                "roc_auc": float(
                    roc_auc_score(y_validation, probabilities)
                ),
            }
        )
    return pd.DataFrame(
        rows,
        columns=["model", "accuracy", "roc_auc"],
    )


def rank_models(
    results: pd.DataFrame,
    metric: str,
) -> pd.DataFrame:
    if metric not in results.columns:
        raise KeyError(metric)
    return results.sort_values(
        metric,
        ascending=False,
        kind="stable",
    ).reset_index(drop=True)


def select_best_model_name(
    results: pd.DataFrame,
    metric: str,
) -> str:
    if results.empty:
        raise ValueError("results 不能为空")
    if "model" not in results.columns:
        raise KeyError("model")
    if metric not in results.columns:
        raise KeyError(metric)
    best_index = results[metric].idxmax()
    return str(results.loc[best_index, "model"])
