"""第 15 节练习：轮廓系数。"""

import numpy as np
import pandas as pd


def calculate_silhouette_scores(X: np.ndarray, k_values: list[int]) -> dict[int, float]:
    """
    题目背景：
        除 inertia 外，还要衡量客户与本组是否紧密、与其他组是否分离。

    学生需要完成什么：
        对每个 k 使用 KMeans(random_state=42, n_init=10) 得到标签，
        计算 silhouette_score(X, labels)，按输入 k 存入字典。

    参数：
        X：聚类特征。
        k_values：要评估的聚类数。

    返回值：
        {k: score} 字典。

    输入输出示例：
        k=[2,3] -> 字典键为 2、3
        每个分数 -> 范围 -1 到 1

    特殊情况：
        k 必须至少 2 且小于样本数；无效情况保留 ValueError；空列表返回空字典。

    提示：
        model.fit_predict(X) 后调用 silhouette_score。
    """
    # TODO: 计算每个 k 的轮廓系数。
    raise NotImplementedError("TODO: 实现 calculate_silhouette_scores")


def select_best_silhouette_k(scores: dict[int, float]) -> int:
    """
    题目背景：
        自动选择候选 k 时，可先找到轮廓系数最高的聚类数。

    学生需要完成什么：
        返回分数最大对应的 k；并列时返回较小 k。

    参数：
        scores：k 到轮廓系数的字典。

    返回值：
        最佳 k 整数。

    输入输出示例：
        {2:0.4,3:0.6} -> 3
        {2:0.5,3:0.5} -> 2

    特殊情况：
        空字典抛出 ValueError。

    提示：
        可以按 (-score, k) 排序，或用 max 的元组规则谨慎处理并列。
    """
    # TODO: 选择轮廓系数最高且并列时较小的 k。
    raise NotImplementedError("TODO: 实现 select_best_silhouette_k")


def build_cluster_evaluation(
    X: np.ndarray,
    k_values: list[int],
) -> pd.DataFrame:
    """
    题目背景：
        最终选 k 不能只看一个指标，需要把 inertia 和 silhouette 放在同一表。

    学生需要完成什么：
        对每个 k 训练固定随机参数 KMeans，返回 k、inertia、
        silhouette 三列，顺序与 k_values 一致。

    参数：
        X：聚类特征。
        k_values：候选聚类数。

    返回值：
        聚类评估 DataFrame。

    输入输出示例：
        k=[2,3] -> 2 行 3 列
        silhouette 列 -> 每个值在 -1 到 1

    特殊情况：
        空列表返回固定三列空表；无效 k 保留 ValueError。

    提示：
        每个 k 只需 fit_predict 一次，再读取 inertia_ 和计算轮廓系数。
    """
    # TODO: 同时生成两项聚类评估指标。
    raise NotImplementedError("TODO: 实现 build_cluster_evaluation")
