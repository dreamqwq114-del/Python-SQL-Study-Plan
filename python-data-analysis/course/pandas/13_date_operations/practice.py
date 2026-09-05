"""第 13 节练习：日期操作。"""

import pandas as pd

def add_date_parts(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        客户加入日期是文本，年度和月度分析需要先转成真正的日期。

    学生需要完成什么：
        返回副本，把 join_date 安全转换为日期，并新增 join_year、
        join_month 两列。无效日期转换为 NaT。

    参数：
        dataframe：客户表。

    返回值：
        日期已转换并拆分年月的新 DataFrame。

    输入输出示例：
        "2025-01-12" -> join_year=2025、join_month=1
        "not-a-date" -> join_date=NaT，年月为缺失

    特殊情况：
        混合日期格式应尽量识别；不修改原表。

    提示：
        pd.to_datetime(..., errors="coerce", format="mixed") 后使用 .dt。
    """
    # TODO: 转换 join_date 并提取年月。
    raise NotImplementedError("TODO: 实现 add_date_parts")


def filter_orders_by_date(
    dataframe: pd.DataFrame, start: str, end: str
) -> pd.DataFrame:
    """
    题目背景：
        月度报告只统计某个起止日期范围内的订单。

    学生需要完成什么：
        把 start、end 转为日期；把 order_date 安全转为日期；
        返回位于闭区间 [start, end] 的订单，并保留转换后的 order_date。

    参数：
        dataframe：订单表。
        start：开始日期文本。
        end：结束日期文本。

    返回值：
        日期范围内的订单 DataFrame，索引从 0 开始。

    输入输出示例：
        日期 1月1日、1月31日，范围相同 -> 两端都保留
        日期 2月1日，范围为一月 -> 不保留

    特殊情况：
        start 或 end 无效、或 start>end 时抛出 ValueError；
        无效 order_date 被排除。

    提示：
        先用 pd.to_datetime() 转边界，再用 between()。
    """
    # TODO: 验证边界并筛选订单日期。
    raise NotImplementedError("TODO: 实现 filter_orders_by_date")


def monthly_order_totals(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        财务报告要把订单金额按月份汇总。

    学生需要完成什么：
        安全转换 order_date，计算 quantity * unit_price；
        排除无效日期，按 YYYY-MM 的 order_month 分组求 order_total 总和。

    参数：
        dataframe：订单明细表。

    返回值：
        列为 order_month、order_total，且月份升序排列的 DataFrame。

    输入输出示例：
        2025-01 两单金额 100、50 -> 该月 order_total=150
        2025-02 一单金额 80 -> 另有一行 2025-02、80

    特殊情况：
        无效日期不参与分组；不修改原表。

    提示：
        日期列的 .dt.strftime("%Y-%m") 可生成月份文本。
    """
    # TODO: 计算并按月汇总订单金额。
    raise NotImplementedError("TODO: 实现 monthly_order_totals")
