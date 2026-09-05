"""第 6 节练习：保存并关闭图像。"""

from pathlib import Path

import pandas as pd


def save_churn_figure(dataframe: pd.DataFrame, output_path: Path) -> None:
    """
    题目背景：
        流失类别图要作为报告文件保存，而不是只显示在屏幕上。

    学生需要完成什么：
        统计 churn 非缺失值并按类别升序绘制柱状图。标题
        Churn Category Distribution，轴标签 Churn、Customer Count。
        创建父目录，使用 150 dpi 和 bbox_inches="tight" 保存，
        然后关闭创建的 Figure。

    参数：
        dataframe：包含 churn 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        churn=[0, 1, 0] -> 两根柱高度 2、1
        output_path=reports/churn.png -> 自动创建 reports

    特殊情况：
        缺失 churn 不计数；不得调用 plt.show()；缺列时抛出 KeyError。

    提示：
        保存必须发生在 plt.close(fig) 之前。
    """
    # TODO: 以指定质量保存流失计数图并关闭 Figure。
    raise NotImplementedError("TODO: 实现 save_churn_figure")


def save_transparent_spending_scatter(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        设计师需要一张透明背景的年龄—消费散点图叠加到报告版面。

    学生需要完成什么：
        绘制 age 与 monthly_spending 散点图，标题 Spending by Age，
        轴标签 Age、Monthly Spending。创建父目录，使用 200 dpi、
        transparent=True、bbox_inches="tight" 保存并关闭 Figure。

    参数：
        dataframe：包含 age、monthly_spending 的客户表。
        output_path：PNG 输出路径。

    返回值：
        None。

    输入输出示例：
        两行有效数据 -> 保存含两个点的透明 PNG
        父目录不存在 -> 自动创建后保存

    特殊情况：
        不修改原表；缺列时抛出 KeyError；不得遗留打开的 Figure。

    提示：
        fig.savefig(..., dpi=200, transparent=True, bbox_inches="tight")。
    """
    # TODO: 保存透明背景散点图。
    raise NotImplementedError("TODO: 实现 save_transparent_spending_scatter")


def save_city_figure_formats(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> list[Path]:
    """
    题目背景：
        同一张城市客户数图既要用于网页 PNG，也要用于可缩放的 PDF 报告。

    学生需要完成什么：
        创建 output_directory，绘制按 city 名称升序的客户计数柱状图，
        标题 Customers by City，设置轴标签。把同一 Figure 以 150 dpi、
        bbox_inches="tight" 依次保存为 city_counts.png 和 city_counts.pdf，
        关闭 Figure，并按 PNG、PDF 顺序返回两个 Path。

    参数：
        dataframe：包含 city 的客户表。
        output_directory：两个输出文件所在目录。

    返回值：
        [PNG 路径, PDF 路径]。

    输入输出示例：
        output_directory=reports -> 返回 reports/city_counts.png 与 .pdf
        city=["A", "B"] -> 两个文件都存在且非空

    特殊情况：
        缺失 city 不计数；不得修改原表；缺列时抛出 KeyError。

    提示：
        只创建一个 Figure，对两个 Path 分别调用 fig.savefig()，最后关闭。
    """
    # TODO: 用同一 Figure 保存 PNG 和 PDF。
    raise NotImplementedError("TODO: 实现 save_city_figure_formats")
