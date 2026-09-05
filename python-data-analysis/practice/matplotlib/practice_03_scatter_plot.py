"""第 3 节练习：散点图。"""

from pathlib import Path

import pandas as pd


def plot_age_spending(dataframe: pd.DataFrame, output_path: Path) -> None:
    """
    题目背景：
        分析师想观察年龄与月消费是否一起上升，以及是否存在离群客户。

    学生需要完成什么：
        安全转换 age 和 monthly_spending，只保留两列都有效的行，
        绘制散点图。标题 Age vs Monthly Spending，横轴 Age，
        纵轴 Monthly Spending。创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 age 和 monthly_spending 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        age=[20, 30]、spending=[100, 200] -> 两个散点
        age=["bad", 30]、spending=[100, 200] -> 只绘制第二个散点

    特殊情况：
        两列必须成对删除无效行；不修改原表；缺列时抛出 KeyError。

    提示：
        先组成含两列的临时 DataFrame，再 dropna()，避免横纵坐标错位。
    """
    # TODO: 清理成对数据并绘制散点图。
    raise NotImplementedError("TODO: 实现 plot_age_spending")


def plot_quantity_unit_price(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        订单分析要观察购买数量较高时，商品单价通常是高还是低。

    学生需要完成什么：
        使用 quantity 作为横轴、unit_price 作为纵轴绘制散点图。
        标题 Quantity vs Unit Price，轴标签 Quantity、Unit Price，
        网格透明度设为 0.3，创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 quantity、unit_price 的订单表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        quantity=[1, 2]、unit_price=[99, 50] -> 两个散点
        空表 -> 保存只有坐标轴的空图

    特殊情况：
        不修改原表；缺列时抛出 KeyError。

    提示：
        ax.scatter(dataframe["quantity"], dataframe["unit_price"])。
    """
    # TODO: 绘制数量与单价散点图。
    raise NotImplementedError("TODO: 实现 plot_quantity_unit_price")


def plot_income_spending_by_cluster(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        客户分群完成后，要在收入—消费得分平面上比较各个群组。

    学生需要完成什么：
        按 cluster 升序逐组绘制散点。横轴 annual_income，纵轴
        spending_score，每组标签格式为 Cluster 0、Cluster 1 等。
        标题 Customer Segments，添加图例，创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 annual_income、spending_score、cluster 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        cluster=[0, 1] -> 图例包含 Cluster 0 和 Cluster 1
        cluster=[2, 2] -> 只绘制一组 Cluster 2

    特殊情况：
        不修改原表；缺列时抛出 KeyError；空表仍保存空图。

    提示：
        for cluster in sorted(dataframe["cluster"].dropna().unique())。
    """
    # TODO: 按聚类编号绘制多组散点。
    raise NotImplementedError("TODO: 实现 plot_income_spending_by_cluster")
