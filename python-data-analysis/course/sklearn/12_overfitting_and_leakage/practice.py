"""第 12 节练习：过拟合与数据泄漏。"""

from typing import Any

import numpy as np


def compare_train_test_accuracy(model: Any, X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> tuple[float, float]:
    """
    题目背景：
        训练分数很高但测试分数明显较低，可能表示模型过拟合。

    学生需要完成什么：
        使用 model.score 分别计算训练集和测试集准确率并转成 float。

    参数：
        model：已拟合分类模型。
        X_train、X_test：两组特征。
        y_train、y_test：对应标签。

    返回值：
        (train_accuracy, test_accuracy)。

    输入输出示例：
        完全正确训练预测 -> train_accuracy=1.0
        两个分数 -> 都在 0 到 1 之间

    特殊情况：
        模型未拟合保留 NotFittedError；不重新 fit 模型。
    """
    # TODO: 分别评估训练集和测试集。
    raise NotImplementedError("TODO: 实现 compare_train_test_accuracy")


def detect_overfitting(
    train_accuracy: float,
    test_accuracy: float,
    maximum_gap: float,
) -> bool:
    """
    题目背景：
        团队用一个明确差距阈值标记可能过拟合的实验。

    学生需要完成什么：
        验证两个准确率和 maximum_gap 都在 0 到 1；
        当 train_accuracy - test_accuracy > maximum_gap 时返回 True。

    参数：
        train_accuracy：训练准确率。
        test_accuracy：测试准确率。
        maximum_gap：允许的最大差距。

    返回值：
        是否超过阈值。

    输入输出示例：
        0.95、0.75、gap=0.1 -> True
        0.85、0.80、gap=0.1 -> False

    特殊情况：
        等于 maximum_gap 时返回 False；任一值越界抛出 ValueError。
    """
    # TODO: 按明确阈值标记过拟合风险。
    raise NotImplementedError("TODO: 实现 detect_overfitting")


def scale_without_leakage(
    X_train: np.ndarray,
    X_test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    题目背景：
        如果缩放器看过测试集均值，就把未来信息泄漏进训练流程。

    学生需要完成什么：
        只在 X_train 拟合 StandardScaler，再分别转换训练集和测试集。

    参数：
        X_train：训练特征。
        X_test：测试特征。

    返回值：
        (scaled_train, scaled_test)。

    输入输出示例：
        训练列 [1,2,3] -> 缩放后均值约 0
        测试值 100 -> 使用训练均值转换，不会变成 0

    特殊情况：
        禁止把两组先拼接再 fit；列数不同保留 ValueError。
    """
    # TODO: 实现不接触测试分布的缩放。
    raise NotImplementedError("TODO: 实现 scale_without_leakage")
