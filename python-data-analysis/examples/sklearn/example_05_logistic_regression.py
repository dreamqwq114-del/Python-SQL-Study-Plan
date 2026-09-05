"""训练逻辑回归并查看预测与系数。"""

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression


def train_model() -> tuple[LogisticRegression, object, object]:
    """创建确定性数据并训练逻辑回归。"""
    X, y = make_classification(
        n_samples=60,
        n_features=3,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
    ).fit(X, y)
    return model, X, y


def main() -> None:
    model, X, y = train_model()
    print((model.random_state, model.max_iter))
    print(model.coef_.shape)
    print(round(model.score(X, y), 3))


if __name__ == "__main__":
    main()
