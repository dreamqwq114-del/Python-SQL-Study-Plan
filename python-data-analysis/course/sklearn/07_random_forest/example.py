"""训练多棵树组成的随机森林。"""

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier


def train_forest() -> RandomForestClassifier:
    """训练 50 棵树的确定性随机森林。"""
    X, y = make_classification(
        n_samples=60,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )
    return RandomForestClassifier(
        n_estimators=50,
        random_state=42,
    ).fit(X, y)


def main() -> None:
    model = train_forest()
    print((model.n_estimators, model.random_state))
    print(len(model.estimators_))
    print(round(float(model.feature_importances_.sum()), 3))


if __name__ == "__main__":
    main()
