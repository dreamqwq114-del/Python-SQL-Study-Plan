"""第 5 节练习：标题、图例与布局。"""

from pathlib import Path

import pandas as pd


def plot_order_status_lines(dataframe: pd.DataFrame, output_path: Path) -> None:
    """
    题目背景：
        订单报告要分别展示每种状态下订单金额出现的顺序。

    学生需要完成什么：
        按 status 名称升序逐组绘制 order_amount 折线，每组的横坐标从 1
        开始，图例标签就是状态名称。标题 Order Amount by Status，
        轴标签 Order Sequence、Order Amount，添加图例和网格，
        调用 tight_layout，创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 status、order_amount 的订单表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        status=["paid", "refunded"] -> 图例有 paid、refunded
        paid 金额 [50, 70] -> paid 折线横坐标为 1、2

    特殊情况：
        不修改原表；缺列时抛出 KeyError；空表仍保存图片。

    提示：
        groupby("status", sort=True) 后对每组调用 ax.plot(..., label=status)。
    """
    # TODO: 为每种订单状态绘制带标签的折线。
    raise NotImplementedError("TODO: 实现 plot_order_status_lines")


def plot_online_and_store_sales(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        销售报告要在同一张图中比较线上和门店两个渠道。

    学生需要完成什么：
        按 month 升序，绘制 online_sales 和 store_sales 两条带圆点折线，
        标签分别为 Online、Store。标题 Sales by Channel，轴标签 Month、
        Sales，添加图例和网格，使用 tight_layout，创建父目录，保存并关闭 Figure。

    参数：
        dataframe：包含 month、online_sales、store_sales 的销售表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        两个月数据 -> 每条线各有两个点
        month=[2, 1] -> 绘图顺序调整为 1、2

    特殊情况：
        不修改原表；缺列时抛出 KeyError；空表仍保存图。

    提示：
        对排序后的同一 Axes 调用两次 plot()，并分别设置 label。
    """
    # TODO: 绘制两个渠道的带图例折线。
    raise NotImplementedError("TODO: 实现 plot_online_and_store_sales")


def plot_customer_dashboard(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        一张管理看板要并排展示城市客户数和流失客户数。

    学生需要完成什么：
        创建一行两列子图。左图绘制按名称升序的 city 计数，标题
        Customers by City；右图绘制按 0、1 升序的 churn 计数，
        标题 Customers by Churn。Figure 总标题 Customer Overview，
        两图都有轴标签，调用 tight_layout，创建父目录，以 150 dpi 保存并关闭。

    参数：
        dataframe：包含 city、churn 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        两个城市和两类 churn -> 图片包含两个 Axes
        city=["A", "A"] -> 左图 A 柱高度为 2

    特殊情况：
        缺失值不计数；不修改原表；缺列时抛出 KeyError。

    提示：
        plt.subplots(1, 2) 后分别使用 value_counts().sort_index()。
    """
    # TODO: 创建带总标题和紧凑布局的双图看板。
    raise NotImplementedError("TODO: 实现 plot_customer_dashboard")
