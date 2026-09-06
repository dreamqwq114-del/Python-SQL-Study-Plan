"""第 10 节练习：合并与拼接。"""

import pandas as pd

def merge_customers_orders(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        客户资料和订单明细分开保存，需要把订单信息接到客户表后面。

    学生需要完成什么：
        按 customer_id 执行左连接，保留所有客户。

    参数：
        customers：左侧客户表。
        orders：右侧订单表。

    返回值：
        左连接后的 DataFrame。

    输入输出示例：
        C1 有两单 -> 合并后 C1 出现两行
        C2 没有订单 -> C2 仍保留，订单列为缺失

    特殊情况：
        任一表缺少 customer_id 时抛出 KeyError；不修改输入表。
    """
    # TODO: 左连接客户表和订单表。
    raise NotImplementedError("TODO: 实现 merge_customers_orders")


def concat_order_batches(batches: list[pd.DataFrame]) -> pd.DataFrame:
    """
    题目背景：
        一月和二月的订单表列结构相同，需要上下拼成一张全年明细。

    学生需要完成什么：
        按列表顺序纵向拼接所有 DataFrame，并生成连续的 0 开始索引。

    参数：
        batches：若干结构相同的订单 DataFrame。

    返回值：
        拼接后的 DataFrame。

    输入输出示例：
        两张各 2 行的表 -> 返回 4 行
        [表A, 表B] -> 表A 的行在表B 之前

    特殊情况：
        batches=[] 时返回空 DataFrame；不修改任何输入表。
    """
    # TODO: 处理空列表并拼接订单批次。
    raise NotImplementedError("TODO: 实现 concat_order_batches")


def find_orders_without_customer(
    customers: pd.DataFrame, orders: pd.DataFrame
) -> pd.DataFrame:
    """
    题目背景：
        数据质量检查要找出客户主表中不存在的“孤立订单”。

    学生需要完成什么：
        返回 orders 中 customer_id 未出现在 customers 的行，
        保持 orders 的全部原列并重置索引。

    参数：
        customers：客户主表。
        orders：订单明细表。

    返回值：
        无法匹配客户的订单 DataFrame。

    输入输出示例：
        customers 有 C1，orders 有 C1、C9 -> 只返回 C9 订单
        所有订单都能匹配 -> 返回零行且保留订单列

    特殊情况：
        缺少 customer_id 时抛出 KeyError；不修改输入表。
    """
    # TODO: 筛选孤立订单。
    raise NotImplementedError("TODO: 实现 find_orders_without_customer")
