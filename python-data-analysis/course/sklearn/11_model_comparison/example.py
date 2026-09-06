"""在相同验证集上比较逻辑回归和决策树。"""

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def demo_compare_models() -> pd.DataFrame:
    """用自带模拟数据演示训练/验证/测试划分下的两模型比较流程。

    这里的数据由 make_classification 生成、函数无参数，仅演示完整流程；
    练习题 compare_models 需要接收外部传入的训练集和验证集。
    """
    X, y = make_classification(
        n_samples=80,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )
    X_development, X_test, y_development, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )
    X_train, X_validation, y_train, y_validation = train_test_split(
        X_development,
        y_development,
        test_size=0.25,
        stratify=y_development,
        random_state=42,
    )
    _ = X_test, y_test
    models = {
        "Logistic": LogisticRegression(max_iter=1000, random_state=42),
        "Tree": DecisionTreeClassifier(max_depth=3, random_state=42),
    }
    rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        rows.append(
            {
                "model": name,
                "accuracy": accuracy_score(
                    y_validation,
                    model.predict(X_validation),
                ),
                "roc_auc": roc_auc_score(
                    y_validation,
                    model.predict_proba(X_validation)[:, 1],
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(
        "roc_auc",
        ascending=False,
    )


def main() -> None:
    results = demo_compare_models()
    print(results["model"].tolist())
    print(results[["accuracy", "roc_auc"]].round(3).to_dict("records"))


if __name__ == "__main__":
    main()
