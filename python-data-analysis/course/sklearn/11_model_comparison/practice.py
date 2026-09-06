"""第 11 节练习：模型比较。"""

import numpy as np
import pandas as pd


def compare_models(
    X_train: np.ndarray,
    X_validation: np.ndarray,
    y_train: np.ndarray,
    y_validation: np.ndarray,
) -> pd.DataFrame:
    """
    题目背景：
        同一份拟合数据和验证数据要公平比较逻辑回归和决策树；
        最终测试集不能参与这一步。

    学生需要完成什么：
        训练 LogisticRegression(max_iter=1000, random_state=42) 和
        DecisionTreeClassifier(max_depth=3, random_state=42)，在验证集计算
        accuracy 与正类概率 roc_auc，返回 model、accuracy、roc_auc 三列。

    参数：
        X_train、X_validation：拟合和验证特征。
        y_train、y_validation：拟合和验证标签。

    返回值：
        两行 DataFrame，model 名称固定为 Logistic、Tree。

    输入输出示例：
        两个模型 -> 返回 2 行
        返回列顺序 -> ["model","accuracy","roc_auc"]

    特殊情况：
        两个模型必须使用完全相同验证集；验证标签单类时 AUC 抛 ValueError；
        这里的分数用于选候选模型，不能冒充最终测试成绩。
    """
    # TODO: 在相同数据上训练并比较两个模型。
    raise NotImplementedError("TODO: 实现 compare_models")


def rank_models(
    results: pd.DataFrame,
    metric: str,
) -> pd.DataFrame:
    """
    题目背景：
        指标表要按指定指标从高到低排列，方便选择候选模型。

    学生需要完成什么：
        验证 metric 列存在，按该列降序排列并重置索引，返回副本。

    参数：
        results：至少含 model 和指标列的表。
        metric：排序指标列名。

    返回值：
        排序后的新 DataFrame。

    输入输出示例：
        accuracy=[0.7,0.9] -> 0.9 模型排第一
        相同分数 -> 保持 pandas 稳定排序结果

    特殊情况：
        metric 不存在时抛出 KeyError；不修改原表。
    """
    # TODO: 按选定指标排名模型。
    raise NotImplementedError("TODO: 实现 rank_models")


def select_best_model_name(
    results: pd.DataFrame,
    metric: str,
) -> str:
    """
    题目背景：
        自动化流程需要从指标表中取出最佳模型名称。

    学生需要完成什么：
        验证 results 非空且含 model、metric；找到 metric 最大值所在第一行，
        返回对应 model 的字符串。

    参数：
        results：模型指标表。
        metric：用于选择的指标。

    返回值：
        最佳模型名称。

    输入输出示例：
        AUC: Logistic=0.8、Tree=0.7 -> "Logistic"
        两者并列且 Logistic 先出现 -> "Logistic"

    特殊情况：
        空表抛出 ValueError；缺列抛出 KeyError。
    """
    # TODO: 返回指定指标最佳模型名称。
    raise NotImplementedError("TODO: 实现 select_best_model_name")
