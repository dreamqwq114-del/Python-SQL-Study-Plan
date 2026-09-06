"""第 2 节练习：训练集与测试集。"""

import pandas as pd


def split_data(X: pd.DataFrame, y: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    题目背景：
        模型必须在未参与训练的数据上接受测试。

    学生需要完成什么：
        按 75%/25% 划分 X 和 y，使用 stratify=y 保持类别比例，
        random_state 固定为 42。

    参数：
        X：特征 DataFrame。
        y：与 X 行数相同的标签 Series。

    返回值：
        (X_train, X_test, y_train, y_test)。

    输入输出示例：
        40 行数据 -> 30 行训练、10 行测试
        y 中 0/1 各半 -> 训练和测试中仍各半

    特殊情况：
        X、y 长度不一致或某类样本太少时保留 scikit-learn 的 ValueError。
    """
    # TODO: 固定随机种子进行分层划分。
    raise NotImplementedError("TODO: 实现 split_data")


def split_with_test_size(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    题目背景：
        不同实验可能需要 20% 或 30% 测试数据。

    学生需要完成什么：
        验证 0 < test_size < 1，再使用分层划分和 random_state=42。

    参数：
        X：特征表。
        y：标签。
        test_size：测试集比例。

    返回值：
        四个训练/测试对象，顺序与 train_test_split 一致。

    输入输出示例：
        20 行、test_size=0.2 -> 测试集 4 行
        20 行、test_size=0.5 -> 训练和测试各 10 行

    特殊情况：
        test_size<=0 或 >=1 时主动抛出 ValueError。
    """
    # TODO: 根据调用者比例进行可复现分层划分。
    raise NotImplementedError("TODO: 实现 split_with_test_size")


def summarize_split_balance(
    y_train: pd.Series,
    y_test: pd.Series,
) -> dict[str, float]:
    """
    题目背景：
        划分后要核对训练集与测试集的流失比例是否接近。

    学生需要完成什么：
        返回 train_positive_rate 和 test_positive_rate，即两个集合中
        1 标签的平均值。

    参数：
        y_train：训练标签。
        y_test：测试标签。

    返回值：
        含两个浮点比例的字典。

    输入输出示例：
        y_train=[0,1]、y_test=[0,1] -> 两个比例都是 0.5
        y_train=[0,0]、y_test=[1,0] -> 0.0 和 0.5

    特殊情况：
        任一输入为空时抛出 ValueError；不修改输入。
    """
    # TODO: 汇总两个集合的正类比例。
    raise NotImplementedError("TODO: 实现 summarize_split_balance")
