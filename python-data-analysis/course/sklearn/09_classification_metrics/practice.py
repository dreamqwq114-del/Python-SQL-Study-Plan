"""第 9 节练习：分类指标。"""

import numpy as np


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray) -> dict[str, float]:
    """
    题目背景：
        单看准确率可能忽略少数流失客户，需要同时计算多种指标。

    学生需要完成什么：
        返回 accuracy、precision、recall、f1、roc_auc 五个浮点指标；
        precision 和 recall 使用 zero_division=0。

    参数：
        y_true：真实 0/1 标签。
        y_pred：预测 0/1 标签。
        y_prob：正类概率。

    返回值：
        五个固定键的字典。

    输入输出示例：
        4 个样本预测对 3 个 -> accuracy=0.75
        所有指标 -> 理论范围通常为 0 到 1

    特殊情况：
        y_true 只有一个类别时主动抛出 ValueError，避免不同版本返回 NaN。

    提示：
        从 sklearn.metrics 分别导入五个函数。
    """
    # TODO: 计算五项分类指标。
    raise NotImplementedError("TODO: 实现 calculate_metrics")


def calculate_threshold_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
) -> dict[str, float]:
    """
    题目背景：
        改变风险阈值会改变 precision、recall 和 f1。

    学生需要完成什么：
        验证阈值，按概率生成标签，返回 precision、recall、f1，
        三项都使用 zero_division=0。

    参数：
        y_true：真实标签。
        y_prob：正类概率。
        threshold：0 到 1 的阈值。

    返回值：
        三项指标字典。

    输入输出示例：
        prob=[0.2,0.8]、threshold=0.5 -> 预测 [0,1]
        没有正类预测 -> precision 返回 0 而不报除零错误

    特殊情况：
        阈值越界抛出 ValueError；输入长度不一致保留指标函数异常。

    提示：
        先生成 y_pred，再调用三个指标函数。
    """
    # TODO: 计算指定阈值下的三项指标。
    raise NotImplementedError("TODO: 实现 calculate_threshold_metrics")


def calculate_specificity(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:
    """
    题目背景：
        团队还想知道模型正确识别未流失客户的比例。

    学生需要完成什么：
        从 labels=[0,1] 的混淆矩阵取得 TN 和 FP，返回 TN/(TN+FP)。

    参数：
        y_true：真实标签。
        y_pred：预测标签。

    返回值：
        specificity 浮点数。

    输入输出示例：
        两个真实负类都判断正确 -> 1.0
        一个真负、一个假正 -> 0.5

    特殊情况：
        没有真实负类时返回 0.0；长度不一致保留 ValueError。

    提示：
        confusion_matrix(..., labels=[0,1]).ravel() 得到 tn,fp,fn,tp。
    """
    # TODO: 计算负类召回率 specificity。
    raise NotImplementedError("TODO: 实现 calculate_specificity")
