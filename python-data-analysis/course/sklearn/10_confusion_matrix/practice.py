"""第 10 节练习：混淆矩阵。"""

import numpy as np


def build_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    题目背景：
        团队要知道预测错误分别是假警报还是漏掉流失客户。

    学生需要完成什么：
        使用 labels=[0,1] 返回固定 2×2 混淆矩阵。

    参数：
        y_true：真实标签。
        y_pred：预测标签。

    返回值：
        布局为 [[TN, FP], [FN, TP]] 的整数数组。

    输入输出示例：
        true=[0,1]、pred=[0,1] -> [[1,0],[0,1]]
        true=[0,1]、pred=[1,0] -> [[0,1],[1,0]]

    特殊情况：
        即使某个类别未出现也必须保持 2×2；长度不一致抛出 ValueError。
    """
    # TODO: 创建固定顺序的二分类混淆矩阵。
    raise NotImplementedError("TODO: 实现 build_confusion_matrix")


def confusion_counts(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, int]:
    """
    题目背景：
        报告文字需要直接引用 TN、FP、FN、TP 四个数量。

    学生需要完成什么：
        构建 labels=[0,1] 的混淆矩阵并返回四个整数键。

    参数：
        y_true：真实标签。
        y_pred：预测标签。

    返回值：
        {"tn":..., "fp":..., "fn":..., "tp":...}。

    输入输出示例：
        完全正确的 [0,1] -> tn=1、tp=1
        完全相反的 [0,1] -> fp=1、fn=1

    特殊情况：
        某类不存在时相应计数为 0；固定返回四个键。
    """
    # TODO: 把混淆矩阵拆成四个业务计数。
    raise NotImplementedError("TODO: 实现 confusion_counts")


def normalized_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> np.ndarray:
    """
    题目背景：
        两类样本数量不同，团队希望按每个真实类别查看预测比例。

    学生需要完成什么：
        返回 labels=[0,1]、normalize="true" 的 2×2 浮点混淆矩阵。

    参数：
        y_true：真实标签。
        y_pred：预测标签。

    返回值：
        每个存在的真实类别行之和为 1 的数组。

    输入输出示例：
        每类一对一正确 -> [[1,0],[0,1]]
        真实负类两个、一个误报 -> 第一行 [0.5,0.5]

    特殊情况：
        某真实类别没有样本时该行是 0；长度不一致抛出 ValueError。
    """
    # TODO: 返回按真实类别归一化的矩阵。
    raise NotImplementedError("TODO: 实现 normalized_confusion_matrix")
