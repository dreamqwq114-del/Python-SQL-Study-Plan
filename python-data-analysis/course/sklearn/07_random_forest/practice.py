"""第 7 节练习：随机森林。"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_forest(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    题目背景：
        单棵树可能对训练数据过于敏感，使用多棵树共同投票提高稳定性。

    学生需要完成什么：
        创建 RandomForestClassifier(n_estimators=50, random_state=42)，
        拟合 X、y 并返回。

    参数：
        X：训练特征。
        y：训练标签。

    返回值：
        已拟合随机森林。

    输入输出示例：
        model.n_estimators -> 50
        训练后 len(model.estimators_) -> 50

    特殊情况：
        数据无效时保留 scikit-learn 的 ValueError。

    提示：
        n_estimators 表示森林中决策树数量。
    """
    # TODO: 训练固定 50 棵树的随机森林。
    raise NotImplementedError("TODO: 实现 train_forest")


def train_forest_with_estimators(
    X: np.ndarray,
    y: np.ndarray,
    n_estimators: int,
) -> RandomForestClassifier:
    """
    题目背景：
        实验要比较不同树数量的随机森林。

    学生需要完成什么：
        验证 n_estimators 为正整数，使用 random_state=42 拟合模型。

    参数：
        X：训练特征。
        y：训练标签。
        n_estimators：树的数量。

    返回值：
        已拟合随机森林。

    输入输出示例：
        n_estimators=10 -> len(model.estimators_) == 10
        n_estimators=100 -> model.n_estimators == 100

    特殊情况：
        n_estimators<=0 时抛出 ValueError。

    提示：
        固定 random_state 才能公平比较实验。
    """
    # TODO: 使用指定树数量训练随机森林。
    raise NotImplementedError("TODO: 实现 train_forest_with_estimators")


def forest_importance_table(
    model: RandomForestClassifier,
    feature_names: list[str],
) -> pd.DataFrame:
    """
    题目背景：
        报告需要展示随机森林最重视哪些输入特征。

    学生需要完成什么：
        用 feature_importances_ 建立 feature、importance 两列，
        按 importance 降序并重置索引。

    参数：
        model：已拟合随机森林。
        feature_names：特征名称。

    返回值：
        排序后的重要性表。

    输入输出示例：
        四个输入特征 -> 返回 4 行
        importance 最大的特征 -> 位于第 0 行

    特殊情况：
        未拟合抛出 NotFittedError；名称数量不匹配抛出 ValueError。

    提示：
        实现结构与上一节树重要性表相似。
    """
    # TODO: 整理随机森林特征重要性。
    raise NotImplementedError("TODO: 实现 forest_importance_table")
