"""训练深度受限的客户分类决策树。"""

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier


def train_tree() -> DecisionTreeClassifier:
    """训练 max_depth=3 的确定性决策树。"""
    X, y = make_classification(
        n_samples=60,
        n_features=3,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )
    return DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
    ).fit(X, y)


def main() -> None:
    model = train_tree()
    print((model.max_depth, model.random_state))
    print(model.get_depth())
    print(round(float(model.feature_importances_.sum()), 3))


if __name__ == "__main__":
    main()
