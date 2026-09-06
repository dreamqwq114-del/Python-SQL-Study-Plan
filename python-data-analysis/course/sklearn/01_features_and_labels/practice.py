"""第 1 节练习：特征 X 与标签 y。"""

import pandas as pd


def select_features_and_label(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    题目背景：
        流失分类模型要用年龄和月消费预测客户是否流失。

    学生需要完成什么：
        按 age、monthly_spending 的顺序返回特征表 X，并返回 churn 标签 y；
        X 和 y 都必须是副本。

    参数：
        dataframe：至少包含 age、monthly_spending、churn 的客户表。

    返回值：
        (X, y)，X 是两列 DataFrame，y 是 Series。

    输入输出示例：
        2 行客户表 -> X.shape == (2, 2)，y.shape == (2,)
        原表列顺序不同 -> X 列仍为 age、monthly_spending

    特殊情况：
        不修改原表；缺少任一必需列时抛出 KeyError。
    """
    # TODO: 分离固定特征 X 与标签 y。
    raise NotImplementedError("TODO: 实现 select_features_and_label")


def select_mixed_features(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    题目背景：
        第二个模型还要使用城市这个类别特征。

    学生需要完成什么：
        按 age、monthly_spending、city 的顺序返回 X，返回 churn 作为 y，
        两者均为副本。

    参数：
        dataframe：包含三个特征列和 churn 的客户表。

    返回值：
        (X, y)。

    输入输出示例：
        一行表 -> X.shape == (1, 3)
        city=["A", "B"] -> X["city"].tolist() == ["A", "B"]

    特殊情况：
        city 仍保持文本，不在本题编码；缺列时抛出 KeyError。
    """
    # TODO: 分离包含城市的混合特征与标签。
    raise NotImplementedError("TODO: 实现 select_mixed_features")


def count_target_classes(target: pd.Series) -> dict[int, int]:
    """
    题目背景：
        划分数据前要确认流失标签是否只有 0 和 1，以及两类各有多少。

    学生需要完成什么：
        验证所有非缺失标签都属于 0、1；返回两个键都存在的计数字典
        {0: 未流失数, 1: 流失数}。

    参数：
        target：0/1 流失标签 Series。

    返回值：
        dict[int, int]。

    输入输出示例：
        [0, 1, 0] -> {0: 2, 1: 1}
        [0, 0] -> {0: 2, 1: 0}

    特殊情况：
        有缺失值或 0/1 之外的值时抛出 ValueError；空 Series 返回两个 0。
    """
    # TODO: 验证并统计二分类标签。
    raise NotImplementedError("TODO: 实现 count_target_classes")
