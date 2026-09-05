"""第 8 节练习：预测标签与概率。"""

from typing import Any

import numpy as np
import pandas as pd


def predict_labels_and_probabilities(model: Any, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    题目背景：
        业务既要最终 0/1 判断，也要每位客户流失的风险概率。

    学生需要完成什么：
        返回 model.predict(X) 的标签，以及 model.predict_proba(X)[:, 1]
        的正类概率。

    参数：
        model：已拟合且支持 predict、predict_proba 的分类器。
        X：待预测特征。

    返回值：
        (labels, positive_probabilities) 两个一维数组。

    输入输出示例：
        X 有 5 行 -> 两个结果 shape 都为 (5,)
        正类概率 -> 每个值在 0 到 1 之间

    特殊情况：
        模型未拟合或不支持 predict_proba 时保留相应异常。

    提示：
        predict_proba 的第 0 列是类 0 概率，第 1 列是类 1 概率。
    """
    # TODO: 返回标签和正类概率。
    raise NotImplementedError("TODO: 实现 predict_labels_and_probabilities")


def predict_with_threshold(
    model: Any,
    X: np.ndarray,
    threshold: float,
) -> np.ndarray:
    """
    题目背景：
        挽留团队可以调整风险阈值，决定哪些客户被标记为流失。

    学生需要完成什么：
        验证阈值在 0 到 1 之间；取得正类概率，概率 >= threshold 返回 1，
        否则返回 0，结果为整数数组。

    参数：
        model：已拟合概率分类器。
        X：待预测特征。
        threshold：分类阈值。

    返回值：
        0/1 NumPy 数组。

    输入输出示例：
        probabilities=[0.2,0.8]、threshold=0.5 -> [0,1]
        probability=0.5、threshold=0.5 -> 1

    特殊情况：
        threshold<0 或 >1 时抛出 ValueError。

    提示：
        布尔数组可用 .astype(int) 转成 0/1。
    """
    # TODO: 按自定义概率阈值生成标签。
    raise NotImplementedError("TODO: 实现 predict_with_threshold")


def build_prediction_table(
    customer_ids: list[str],
    labels: np.ndarray,
    probabilities: np.ndarray,
) -> pd.DataFrame:
    """
    题目背景：
        预测结果要与客户编号对应，才能交给业务团队。

    学生需要完成什么：
        创建 customer_id、predicted_churn、churn_probability 三列 DataFrame。

    参数：
        customer_ids：客户编号列表。
        labels：预测 0/1 标签。
        probabilities：正类概率。

    返回值：
        三列预测结果表。

    输入输出示例：
        一个客户 -> 返回一行
        ids=["C1","C2"] -> customer_id 顺序保持不变

    特殊情况：
        三个输入长度不一致时抛出 ValueError；不修改输入。

    提示：
        先比较 len()，再把三列放进 pd.DataFrame 字典。
    """
    # TODO: 将客户编号、标签和概率组合成表。
    raise NotImplementedError("TODO: 实现 build_prediction_table")
