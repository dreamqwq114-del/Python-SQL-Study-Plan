"""使用固定随机种子进行分层训练/测试划分。"""

import pandas as pd
from sklearn.model_selection import train_test_split


def split_customer_data(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """按 75%/25% 分层划分数据。"""
    return train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )


def main() -> None:
    X = pd.DataFrame({"customer_number": range(40)})
    y = pd.Series([0, 1] * 20, name="churn")
    X_train, X_test, y_train, y_test = split_customer_data(X, y)
    print((len(X_train), len(X_test)))
    print((y_train.mean(), y_test.mean()))
    print(sorted(X_test["customer_number"].tolist())[:3])


if __name__ == "__main__":
    main()
