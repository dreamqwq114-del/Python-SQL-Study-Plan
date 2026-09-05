"""第 3 节练习：类别编码。"""

import numpy as np
import pandas as pd


def encode_city_feature(train: pd.DataFrame, test: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """
    题目背景：
        模型不能直接使用城市文本，需要把每个训练集中已知城市变成 0/1 列。

    学生需要完成什么：
        创建 OneHotEncoder(handle_unknown="ignore", sparse_output=False)，
        只在 train[["city"]] 上拟合，再转换 train 和 test。

    参数：
        train：训练客户表。
        test：测试客户表。

    返回值：
        (train_encoded, test_encoded) 两个二维 NumPy 数组。

    输入输出示例：
        train 城市 A、B -> 编码后有 2 列
        test 出现新城市 C -> 不报错，对已知城市列全为 0

    特殊情况：
        绝不能在 test 上 fit；缺少 city 时抛出 KeyError。

    提示：
        encoder.fit_transform(train[["city"]])，然后 encoder.transform(test[["city"]])。
    """
    # TODO: 只用训练集拟合城市编码器。
    raise NotImplementedError("TODO: 实现 encode_city_feature")


def encode_categorical_features(
    train: pd.DataFrame,
    test: pd.DataFrame,
    columns: list[str],
) -> tuple[np.ndarray, np.ndarray]:
    """
    题目背景：
        模型同时需要 city 和 contract_type 等多个类别字段。

    学生需要完成什么：
        使用同一 OneHotEncoder 只在训练集指定 columns 上拟合，
        再分别转换训练集与测试集。

    参数：
        train：训练表。
        test：测试表。
        columns：要编码的类别列名及顺序。

    返回值：
        两个列数一致的二维数组。

    输入输出示例：
        columns=["city"] -> 行数分别等于 train、test 行数
        columns=["city","contract"] -> 同时编码两个字段

    特殊情况：
        columns 为空时抛出 ValueError；未知测试类别被忽略；缺列抛出 KeyError。

    提示：
        先检查 columns，再用 train.loc[:, columns]。
    """
    # TODO: 编码多个类别特征。
    raise NotImplementedError("TODO: 实现 encode_categorical_features")


def get_encoded_feature_names(
    train: pd.DataFrame,
    columns: list[str],
) -> list[str]:
    """
    题目背景：
        编码后的数组没有直观列名，解释模型时需要知道每列代表哪个类别。

    学生需要完成什么：
        在训练集指定列上拟合 OneHotEncoder，并返回
        get_feature_names_out(columns) 生成的名称列表。

    参数：
        train：训练表。
        columns：类别列名。

    返回值：
        编码后特征名称字符串列表。

    输入输出示例：
        city 含 A、B -> ["city_A", "city_B"]
        contract 含 Monthly -> 名称包含 "contract_Monthly"

    特殊情况：
        columns 为空时抛出 ValueError；名称顺序由编码器决定。

    提示：
        拟合后调用 encoder.get_feature_names_out(columns).tolist()。
    """
    # TODO: 返回训练类别对应的编码列名。
    raise NotImplementedError("TODO: 实现 get_encoded_feature_names")
