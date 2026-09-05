"""第 6 节练习：决策树。"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def train_tree(X: np.ndarray, y: np.ndarray) -> DecisionTreeClassifier:
    """
    题目背景：
        需要一个能通过一系列“是否大于某阈值”规则分类客户的模型。

    学生需要完成什么：
        创建 DecisionTreeClassifier(max_depth=3, random_state=42)，
        拟合 X、y 并返回模型。

    参数：
        X：训练特征数组。
        y：0/1 标签。

    返回值：
        已拟合决策树。

    输入输出示例：
        训练后 hasattr(model, "tree_") -> True
        model.max_depth -> 3

    特殊情况：
        数据为空或长度不一致时保留 scikit-learn 的 ValueError。

    提示：
        创建分类器后调用 fit(X, y)。
    """
    # TODO: 训练深度受限的决策树。
    raise NotImplementedError("TODO: 实现 train_tree")


def train_tree_with_depth(
    X: np.ndarray,
    y: np.ndarray,
    max_depth: int,
) -> DecisionTreeClassifier:
    """
    题目背景：
        实验要比较浅树和深树，观察复杂度变化。

    学生需要完成什么：
        验证 max_depth 为正整数，使用 random_state=42 创建并拟合决策树。

    参数：
        X：训练特征。
        y：训练标签。
        max_depth：允许的最大树深度。

    返回值：
        已拟合模型。

    输入输出示例：
        max_depth=1 -> model.max_depth == 1
        max_depth=5 -> model.max_depth == 5

    特殊情况：
        max_depth<=0 时抛出 ValueError。

    提示：
        限制深度是控制模型复杂度的一种方法。
    """
    # TODO: 使用指定最大深度训练决策树。
    raise NotImplementedError("TODO: 实现 train_tree_with_depth")


def tree_importance_table(
    model: DecisionTreeClassifier,
    feature_names: list[str],
) -> pd.DataFrame:
    """
    题目背景：
        训练后要查看哪些特征更常被树用于有效分裂。

    学生需要完成什么：
        建立 feature、importance 两列，按 importance 降序并重置索引。

    参数：
        model：已拟合决策树。
        feature_names：与输入列对应的名称。

    返回值：
        特征重要性 DataFrame。

    输入输出示例：
        两个特征 -> 返回 2 行
        importance=[0.2,0.8] -> 第二个特征排第一

    特殊情况：
        未拟合模型抛出 NotFittedError；名称数量不一致抛出 ValueError。

    提示：
        使用 model.feature_importances_。
    """
    # TODO: 整理并排序决策树特征重要性。
    raise NotImplementedError("TODO: 实现 tree_importance_table")
