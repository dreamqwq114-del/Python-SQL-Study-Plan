"""从客户表中分离模型特征 X 和标签 y。"""

import pandas as pd


def select_model_data(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """选择两个数值特征和流失标签。"""
    X = dataframe[["age", "monthly_spending"]].copy()
    y = dataframe["churn"].copy()
    return X, y


def main() -> None:
    customers = pd.DataFrame(
        {
            "age": [23, 41, 35, 29],
            "monthly_spending": [188.5, 420.0, 315.8, 250.0],
            "city": ["Suzhou", "Shanghai", "Nanjing", "Suzhou"],
            "churn": [1, 0, 0, 1],
        }
    )
    X, y = select_model_data(customers)
    print(X.columns.tolist())
    print((X.shape, y.shape))
    print(y.value_counts().sort_index().to_dict())


if __name__ == "__main__":
    main()
