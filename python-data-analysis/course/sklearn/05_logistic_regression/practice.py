"""第 5 节练习：逻辑回归。"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


def train_logistic(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
    """
    题目背景：
        使用数值特征训练一个二分类流失模型。

    学生需要完成什么：
        创建 LogisticRegression(random_state=42, max_iter=1000)，
        在 X、y 上 fit 并返回已训练模型。

    参数：
        X：二维数值特征数组。
        y：0/1 标签数组。

    返回值：
        已拟合的 LogisticRegression。

    输入输出示例：
        训练后 hasattr(model, "coef_") -> True
        返回模型的 random_state -> 42

    特殊情况：
        y 只有一个类别或行数不一致时保留 scikit-learn 的 ValueError。

    提示：
        model = LogisticRegression(...); model.fit(X, y)。
    """
    # TODO: 创建并拟合固定参数逻辑回归。
    raise NotImplementedError("TODO: 实现 train_logistic")


def train_logistic_with_strength(
    X: np.ndarray,
    y: np.ndarray,
    regularization_strength: float,
) -> LogisticRegression:
    """
    题目背景：
        实验需要调整逻辑回归的正则化强度参数 C。

    学生需要完成什么：
        验证 regularization_strength > 0，把它作为 C，仍使用
        random_state=42、max_iter=1000，拟合并返回模型。

    参数：
        X：训练特征。
        y：训练标签。
        regularization_strength：传给 C 的正数。

    返回值：
        已拟合逻辑回归。

    输入输出示例：
        strength=0.5 -> model.C == 0.5
        strength=2.0 -> model.C == 2.0

    特殊情况：
        strength<=0 时主动抛出 ValueError。

    提示：
        scikit-learn 的 C 越小，正则化约束通常越强。
    """
    # TODO: 使用指定 C 训练逻辑回归。
    raise NotImplementedError("TODO: 实现 train_logistic_with_strength")


def logistic_coefficient_table(
    model: LogisticRegression,
    feature_names: list[str],
) -> pd.DataFrame:
    """
    题目背景：
        模型训练后要把每个特征的系数整理成可读表格。

    学生需要完成什么：
        取二分类模型 coef_[0]，建立 feature、coefficient、
        absolute_coefficient 三列，按 absolute_coefficient 降序并重置索引。

    参数：
        model：已拟合的二分类 LogisticRegression。
        feature_names：与系数一一对应的名称。

    返回值：
        排序后的 DataFrame。

    输入输出示例：
        两个特征 -> 返回 2 行 3 列
        系数 [-2, 0.5] -> 绝对值 2 的特征排第一

    特殊情况：
        模型未拟合时抛出 NotFittedError；名称数量不匹配时抛出 ValueError。

    提示：
        先检查 len(feature_names) 与 model.coef_.shape[1]。
    """
    # TODO: 生成按绝对系数排序的解释表。
    raise NotImplementedError("TODO: 实现 logistic_coefficient_table")
