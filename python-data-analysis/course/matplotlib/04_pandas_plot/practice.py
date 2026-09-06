"""第 4 节练习：Pandas 绘图入口。"""

from pathlib import Path

import pandas as pd


def plot_city_average(dataframe: pd.DataFrame, output_path: Path) -> None:
    """
    题目背景：
        区域经理需要比较每个城市的平均月消费，而不是绘制客户明细。

    学生需要完成什么：
        先按 city 计算 monthly_spending 平均值并按城市名称升序，
        再使用 pandas 的 Series.plot.bar() 绘制柱状图。
        标题 Average Spending by City，轴标签 City、Average Monthly Spending，
        创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 city、monthly_spending 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        A 城消费 100、300 -> A 柱高度 200
        A、B 两城 -> 按 A、B 顺序显示两根柱

    特殊情况：
        缺失城市不分组；不修改原表；缺列时抛出 KeyError。
    """
    # TODO: 先聚合，再使用 pandas 绘制柱状图。
    raise NotImplementedError("TODO: 实现 plot_city_average")


def plot_contract_churn_rate(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        挽留团队要比较不同合同类型的客户流失率。

    学生需要完成什么：
        按 contract_type 计算 0/1 churn 的平均值并降序排列，
        使用 pandas 绘制柱状图。标题 Churn Rate by Contract，
        轴标签 Contract Type、Churn Rate，纵轴范围固定为 0 到 1，
        创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 contract_type、churn 的客户表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        Monthly 的 churn=[1, 0] -> 柱高 0.5
        Yearly 的 churn=[0] -> 柱高 0.0

    特殊情况：
        缺失合同类型不分组；不修改原表；缺列时抛出 KeyError。
    """
    # TODO: 聚合并绘制合同流失率。
    raise NotImplementedError("TODO: 实现 plot_contract_churn_rate")


def plot_monthly_order_totals(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        财务经理想查看订单金额的月度变化趋势。

    学生需要完成什么：
        安全转换 order_date，计算 quantity * unit_price，排除无效日期，
        按 YYYY-MM 月份汇总金额并使用 pandas Series.plot() 绘制折线图。
        标题 Monthly Order Totals，轴标签 Month、Order Total，
        使用圆形 marker，创建父目录，以 150 dpi 保存并关闭 Figure。

    参数：
        dataframe：包含 order_date、quantity、unit_price 的订单表。
        output_path：输出图片路径。

    返回值：
        None。

    输入输出示例：
        一月两单 100、50 -> 一月点为 150
        二月一单 80 -> 二月点为 80

    特殊情况：
        无效日期不参与汇总；不修改原表；缺列时抛出 KeyError。
    """
    # TODO: 汇总并绘制月度订单金额。
    raise NotImplementedError("TODO: 实现 plot_monthly_order_totals")
