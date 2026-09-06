"""第 4 节练习：数值标准化。"""

import numpy as np
import pandas as pd


def scale_features(train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    题目背景：
        年龄和消费金额量纲不同，需要用训练集均值和标准差标准化。

    学生需要完成什么：
        只在 train 上拟合 StandardScaler，再转换 train 和 test。

    参数：
        train：二维训练特征数组。
        test：列数相同的二维测试数组。

    返回值：
        (train_scaled, test_scaled)。

    输入输出示例：
        train=[[1],[2],[3]] -> 标准化训练列均值约为 0
        test=[[4]] -> 使用训练集参数转换，shape 仍为 (1,1)

    特殊情况：
        不在 test 上 fit；列数不一致时保留 scikit-learn 的 ValueError。
    """
    # TODO: 用训练集参数标准化两组数据。
    raise NotImplementedError("TODO: 实现 scale_features")


def scale_dataframe_columns(
    train: pd.DataFrame,
    test: pd.DataFrame,
    columns: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    题目背景：
        客户表只有 age 和 monthly_spending 需要标准化，其他列要原样保留。

    学生需要完成什么：
        返回两张副本，只用训练集拟合指定 columns，并把转换结果写回这些列。

    参数：
        train：训练 DataFrame。
        test：测试 DataFrame。
        columns：要标准化的数值列。

    返回值：
        (scaled_train, scaled_test) 两张 DataFrame。

    输入输出示例：
        columns=["age"] -> age 改变，city 保持不变
        训练 age=[10,20,30] -> 训练 age 平均值约为 0

    特殊情况：
        columns 为空时返回两张副本；不修改输入；缺列时抛出 KeyError。
    """
    # TODO: 只标准化指定 DataFrame 列。
    raise NotImplementedError("TODO: 实现 scale_dataframe_columns")


def summarize_scaled_training(
    scaled_train: np.ndarray,
) -> dict[str, np.ndarray]:
    """
    题目背景：
        标准化后需要检查每列均值是否接近 0、标准差是否接近 1。

    学生需要完成什么：
        按列计算 mean 和 std（NumPy 默认总体标准差），放入字典返回。

    参数：
        scaled_train：二维标准化训练数组。

    返回值：
        {"mean": 一维数组, "std": 一维数组}。

    输入输出示例：
        标准化两列 -> mean.shape == (2,)
        完全标准化的非恒定列 -> mean 约 0、std 约 1

    特殊情况：
        必须是非空二维数组，否则抛出 ValueError。
    """
    # TODO: 计算标准化训练数据的列均值和列标准差。
    raise NotImplementedError("TODO: 实现 summarize_scaled_training")
