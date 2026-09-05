"""输出分类标签、正类概率和客户预测表。"""

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression


def build_predictions() -> pd.DataFrame:
    """训练模型并返回前五位客户的预测表。"""
    X, y = make_classification(
        n_samples=50,
        n_features=3,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
    ).fit(X, y)
    labels = model.predict(X[:5])
    probabilities = model.predict_proba(X[:5])[:, 1]
    return pd.DataFrame(
        {
            "customer_id": [f"C{i:03d}" for i in range(1, 6)],
            "predicted_churn": labels,
            "churn_probability": probabilities,
        }
    )


def main() -> None:
    predictions = build_predictions()
    print(predictions.shape)
    print(predictions["predicted_churn"].tolist())
    print(predictions["churn_probability"].between(0, 1).all())


if __name__ == "__main__":
    main()
