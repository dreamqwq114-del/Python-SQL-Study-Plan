"""第 13 节练习：K-Means 聚类。"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def fit_kmeans(X: np.ndarray, n_clusters: int) -> KMeans:
    """
    题目背景：
        没有流失标签时，希望按收入和消费相似性把客户分组。

    学生需要完成什么：
        验证 n_clusters 为正整数，训练
        KMeans(n_clusters=n_clusters, random_state=42, n_init=10)。

    参数：
        X：二维数值特征数组。
        n_clusters：聚类数量。

    返回值：
        已拟合 KMeans。

    输入输出示例：
        n_clusters=3 -> model.n_clusters == 3
        X 有 20 行 -> model.labels_.shape == (20,)

    特殊情况：
        n_clusters<=0 主动抛 ValueError；聚类数大于样本数保留模型异常。
    """
    # TODO: 训练可复现的 K-Means。
    raise NotImplementedError("TODO: 实现 fit_kmeans")


def cluster_customers(
    X: np.ndarray,
    n_clusters: int,
) -> np.ndarray:
    """
    题目背景：
        分群结果要作为每位客户的新标签写回数据表。

    学生需要完成什么：
        使用 random_state=42、n_init=10 的 KMeans，返回 fit_predict(X)
        得到的一维整数聚类编号。

    参数：
        X：客户数值特征。
        n_clusters：聚类数量。

    返回值：
        每行客户对应的 cluster labels。

    输入输出示例：
        X 有 6 行 -> labels.shape == (6,)
        n_clusters=2 -> 不同标签数量不超过 2

    特殊情况：
        聚类编号 0、1 只是名称，不代表排名；n_clusters<=0 抛 ValueError。
    """
    # TODO: 训练并返回客户聚类标签。
    raise NotImplementedError("TODO: 实现 cluster_customers")


def cluster_centers_table(
    model: KMeans,
    feature_names: list[str],
) -> pd.DataFrame:
    """
    题目背景：
        要解释各群组，需要查看每个聚类中心在各特征上的坐标。

    学生需要完成什么：
        用 cluster_centers_ 建立列名为 feature_names 的 DataFrame，
        再在最前面插入 cluster 列 0 到 n_clusters-1。

    参数：
        model：已拟合 KMeans。
        feature_names：中心每一列对应的业务名称。

    返回值：
        每个聚类一行的中心表。

    输入输出示例：
        3 个聚类、2 个特征 -> shape 为 (3,3)
        cluster 列 -> [0,1,2]

    特殊情况：
        未拟合抛 AttributeError；名称数不匹配抛 ValueError。
    """
    # TODO: 将聚类中心整理成业务表。
    raise NotImplementedError("TODO: 实现 cluster_centers_table")
