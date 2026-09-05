"""第 14 节练习：肘部法。"""

import numpy as np
import pandas as pd


def calculate_inertias(X: np.ndarray, k_values: list[int]) -> list[float]:
    """
    题目背景：
        选择聚类数前，要比较不同 k 下样本到聚类中心的总平方距离。

    学生需要完成什么：
        对每个 k 训练 KMeans(random_state=42, n_init=10)，按输入顺序
        返回 float inertia_ 列表。

    参数：
        X：聚类数值特征。
        k_values：要评估的聚类数。

    返回值：
        与 k_values 等长的 inertia 列表。

    输入输出示例：
        k=[2,3,4] -> 返回 3 个数
        同一数据增加 k -> inertia 通常不增加

    特殊情况：
        k_values 为空返回空列表；无效 k 保留 KMeans 的 ValueError。

    提示：
        在循环中 fit 模型，然后读取 float(model.inertia_)。
    """
    # TODO: 计算每个 k 的 inertia。
    raise NotImplementedError("TODO: 实现 calculate_inertias")


def calculate_inertia_drops(
    inertias: list[float],
) -> list[float]:
    """
    题目背景：
        肘部法关注 k 每增加 1 时 inertia 减少了多少。

    学生需要完成什么：
        返回相邻差值 previous - current。

    参数：
        inertias：按 k 升序得到的 inertia。

    返回值：
        长度比输入少 1 的下降量列表。

    输入输出示例：
        [100,60,45] -> [40,15]
        [] 或 [100] -> []

    特殊情况：
        inertia 若出现负数或后一个大于前一个时抛出 ValueError。

    提示：
        使用 range(1, len(inertias)) 比较相邻项。
    """
    # TODO: 计算合法 inertia 序列的相邻下降量。
    raise NotImplementedError("TODO: 实现 calculate_inertia_drops")


def build_elbow_table(
    X: np.ndarray,
    k_values: list[int],
) -> pd.DataFrame:
    """
    题目背景：
        画肘部图前要把 k 和 inertia 整理成两列表格。

    学生需要完成什么：
        按输入顺序训练固定随机参数 KMeans，返回列为 k、inertia 的 DataFrame。

    参数：
        X：聚类特征。
        k_values：评估的 k。

    返回值：
        每个 k 一行的表。

    输入输出示例：
        k=[2,3] -> 返回 2 行
        返回列顺序 -> ["k","inertia"]

    特殊情况：
        空 k_values 返回有两列但零行的 DataFrame。

    提示：
        先得到 inertia 列表，再创建 DataFrame。
    """
    # TODO: 生成肘部法结果表。
    raise NotImplementedError("TODO: 实现 build_elbow_table")
