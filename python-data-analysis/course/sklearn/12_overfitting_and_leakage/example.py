"""比较训练/测试分数，并只用训练集拟合缩放器。"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def evaluate_tree() -> tuple[float, float, float]:
    """返回训练分数、测试分数和泄漏安全的测试缩放值。"""
    X, y = make_classification(
        n_samples=80,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )
    model = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
    scaler = StandardScaler().fit(X_train)
    scaled_test = scaler.transform(X_test)
    return (
        model.score(X_train, y_train),
        model.score(X_test, y_test),
        float(np.mean(scaled_test)),
    )


def main() -> None:
    train_score, test_score, test_mean = evaluate_tree()
    print((round(train_score, 3), round(test_score, 3)))
    print(round(train_score - test_score, 3))
    print(round(test_mean, 3))


if __name__ == "__main__":
    main()
