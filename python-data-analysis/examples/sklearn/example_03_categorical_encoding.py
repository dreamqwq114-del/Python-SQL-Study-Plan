"""只用训练集拟合城市独热编码器。"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def encode_cities(
    train: pd.DataFrame,
    test: pd.DataFrame,
) -> tuple[list[str], list[list[float]], list[list[float]]]:
    """返回编码列名以及训练/测试编码。"""
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )
    train_encoded = encoder.fit_transform(train[["city"]])
    test_encoded = encoder.transform(test[["city"]])
    names = encoder.get_feature_names_out(["city"]).tolist()
    return names, train_encoded.tolist(), test_encoded.tolist()


def main() -> None:
    train = pd.DataFrame({"city": ["Suzhou", "Shanghai", "Suzhou"]})
    test = pd.DataFrame({"city": ["Shanghai", "Wuxi"]})
    names, train_encoded, test_encoded = encode_cities(train, test)
    print(names)
    print(train_encoded)
    print(test_encoded)


if __name__ == "__main__":
    main()
