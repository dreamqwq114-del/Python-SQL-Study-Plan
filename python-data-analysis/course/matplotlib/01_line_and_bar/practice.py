"""第 1 节练习：折线图与柱状图。"""

from pathlib import Path

import pandas as pd


def plot_city_counts(dataframe: pd.DataFrame, output_path: Path) -> None:
    """
    题目背景：
        区域经理需要用柱状图比较不同城市的客户数量。

    学生需要完成什么：
        统计 city 的非缺失值数量，按城市名称升序排列，绘制柱状图。
        标题为 Customers by City，横轴为 City，纵轴为 Customer Count。
        创建父目录，以 150 dpi 保存图片并关闭 Figure。

    参数：
        dataframe：至少包含 city 列的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        city=["A", "A", "B"] -> A、B 两根柱，高度 2、1
        output_path=reports/city.png -> 自动创建 reports 并保存图片

    特殊情况：
        缺失 city 不计数；不得修改原 DataFrame；缺列时抛出 KeyError。

    提示：
        value_counts().sort_index() 得到计数，使用 ax.bar() 绘图。
    """
    # TODO: 统计城市并保存柱状图。
    raise NotImplementedError("TODO: 实现 plot_city_counts")


def plot_monthly_sales(dataframe: pd.DataFrame, output_path: Path) -> None:
    """
    题目背景：
        销售经理想观察销售额随月份的变化趋势。

    学生需要完成什么：
        按 month 升序排列，使用折线图绘制 month 和 sales，
        数据点使用圆形 marker。标题为 Monthly Sales Trend，
        横轴为 Month，纵轴为 Sales。创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 month 和 sales 的月度销售表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        month=[2, 1]、sales=[150, 120] -> 折线顺序为 1、2
        一行数据 -> 仍保存含一个圆点的图片

    特殊情况：
        不得修改原表；缺列时抛出 KeyError；空表也应保存带坐标轴的图。

    提示：
        sort_values("month") 后使用 ax.plot(..., marker="o")。
    """
    # TODO: 绘制月度销售折线图。
    raise NotImplementedError("TODO: 实现 plot_monthly_sales")


def plot_sales_and_city_counts(
    sales: pd.DataFrame,
    customers: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        一页报告要同时展示月度销售趋势和城市客户数量。

    学生需要完成什么：
        创建一行两列子图。左图按 month 升序绘制 sales 折线，
        标题 Monthly Sales；右图绘制按城市名称升序的客户计数柱状图，
        标题 Customers by City。两图都设置轴标签，使用 tight_layout，
        创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        sales：包含 month、sales 的销售表。
        customers：包含 city 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        3 个月销售、2 个城市 -> 图片包含 2 个 Axes
        city=["A", "A", "B"] -> 右图柱高 2、1

    特殊情况：
        不修改两个输入表；任一必需列缺失时抛出 KeyError。

    提示：
        fig, axes = plt.subplots(1, 2)，分别使用 axes[0] 和 axes[1]。
    """
    # TODO: 在两个子图中组合折线图和柱状图。
    raise NotImplementedError("TODO: 实现 plot_sales_and_city_counts")
