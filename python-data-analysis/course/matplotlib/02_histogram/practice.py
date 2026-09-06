"""第 2 节练习：直方图。"""

from pathlib import Path

import pandas as pd


def plot_age_histogram(dataframe: pd.DataFrame, output_path: Path) -> None:
    """
    题目背景：
        客户经理想了解年龄集中在哪些区间，而不是逐个查看年龄。

    学生需要完成什么：
        安全地把 age 转为数值，删除转换失败和缺失值，使用 5 个箱绘制
        直方图。标题 Customer Age Distribution，横轴 Age，
        纵轴 Customer Count。创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 age 列的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        age=[20, 21, 40] -> 三个有效年龄进入 5 个区间
        age=["20", "bad", None] -> 只有 20 进入直方图

    特殊情况：
        无有效年龄时仍保存空图；不修改原表；缺列时抛出 KeyError。
    """
    # TODO: 清理年龄并绘制 5 箱直方图。
    raise NotImplementedError("TODO: 实现 plot_age_histogram")


def plot_spending_histogram(
    dataframe: pd.DataFrame,
    output_path: Path,
    bins: int,
) -> None:
    """
    题目背景：
        分析师希望自己决定消费金额分布被切成多少个区间。

    学生需要完成什么：
        验证 bins 为正整数；安全转换 monthly_spending 并删除缺失，
        使用指定 bins 绘制直方图。标题 Monthly Spending Distribution，
        横轴 Monthly Spending，纵轴 Customer Count。创建父目录，保存并关闭 Figure。

    参数：
        dataframe：包含 monthly_spending 的客户表。
        output_path：输出图片路径。
        bins：直方图箱数。

    返回值：
        None。

    输入输出示例：
        spending=[100, 200, 300]、bins=3 -> 绘制 3 个区间
        spending=["100", "bad"]、bins=2 -> 只有 100 参与绘图

    特殊情况：
        bins<=0 时主动抛出 ValueError，且不得创建图片；不修改原表。
    """
    # TODO: 验证箱数并绘制消费直方图。
    raise NotImplementedError("TODO: 实现 plot_spending_histogram")


def plot_age_histograms_by_churn(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        挽留团队想比较流失客户与未流失客户的年龄分布。

    学生需要完成什么：
        安全转换 age；分别取 churn==0 和 churn==1 的有效年龄，
        在同一 Axes 上各画一个 5 箱、半透明直方图，标签为 Stayed 和
        Churned。添加标题 Age Distribution by Churn、轴标签和图例，
        创建父目录，保存并关闭 Figure。

    参数：
        dataframe：包含 age、churn 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        churn=[0, 1] -> 图例包含 Stayed、Churned
        某一组没有数据 -> 仍保存图片并保留两组标签

    特殊情况：
        无效年龄不绘制；不修改原表；缺少 age 或 churn 时抛出 KeyError。
    """
    # TODO: 叠加两组年龄直方图。
    raise NotImplementedError("TODO: 实现 plot_age_histograms_by_churn")
