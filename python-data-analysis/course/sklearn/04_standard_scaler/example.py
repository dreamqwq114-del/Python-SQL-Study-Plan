"""用训练集参数标准化训练和测试特征。"""

import numpy as np
from sklearn.preprocessing import StandardScaler


def scale_train_and_test(
    train: np.ndarray,
    test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """只在训练数组上拟合缩放器。"""
    scaler = StandardScaler()
    return scaler.fit_transform(train), scaler.transform(test)


def main() -> None:
    train = np.array([[20.0, 100.0], [30.0, 200.0], [40.0, 300.0]])
    test = np.array([[50.0, 400.0]])
    train_scaled, test_scaled = scale_train_and_test(train, test)
    print(np.round(train_scaled.mean(axis=0), 6).tolist())
    print(np.round(train_scaled.std(axis=0), 6).tolist())
    print(np.round(test_scaled, 3).tolist())


if __name__ == "__main__":
    main()
