"""综合客户项目：串联读取、清洗、合并、绘图和分类。"""

from pathlib import Path
from typing import Any

import pandas as pd


def load_datasets(
    customer_path: Path,
    order_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    题目背景：
        客户资料和订单记录分别保存在两张 CSV 表中，分析前要先读取它们。

    学生需要完成什么：
        用 pandas 读取两个路径，按“客户表、订单表”的顺序返回。

    参数：
        customer_path：客户 CSV 的 Path。
        order_path：订单 CSV 的 Path。

    返回值：
        (customers, orders)，两项都是 DataFrame。

    输入输出示例：
        两个各有 2 行的 CSV -> 返回两张 shape 为 (2, 列数) 的表。
        客户 CSV 只有表头 -> customers.empty 为 True，订单表仍正常读取。

    特殊情况：
        路径不存在时保留 pandas 抛出的 FileNotFoundError；不要创建假数据。
    """
    # TODO: 读取并按固定顺序返回两张原始数据表。
    raise NotImplementedError("TODO: 实现 load_datasets")


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        客户表存在重复客户、大小写和空格不统一、数字文本、坏日期及缺失值，
        不能直接用于统计或建模。

    学生需要完成什么：
        返回原表副本；先规范化 customer_id 并拒绝缺失或空编号，
        再按规范化后的 customer_id 保留第一条记录并重置索引；
        gender 去空格后转小写，city 去空格后转首字母大写，
        contract_type 去空格后转小写；
        age、monthly_spending、satisfaction_score 用 pd.to_numeric(errors="coerce")
        转换，保留转换产生的缺失值，供分类 Pipeline 只用训练集学习中位数；
        join_date 用 pd.to_datetime(format="mixed", errors="coerce", dayfirst=True)
        转换；churn 去空格、转小写并把 no/yes 映射为 0/1 整数。

    参数：
        customers：至少包含 customer_id、age、gender、city、monthly_spending、
        contract_type、join_date、churn、satisfaction_score 的客户表。

    返回值：
        清洗后的新 DataFrame，原表不得改变。

    输入输出示例：
        city=[" suzhou ", "NANJING"] -> ["Suzhou", "Nanjing"]。
        churn=["Yes", " no "] -> [1, 0]。

    特殊情况：
        缺少必需列时抛出 KeyError；customer_id 缺失或为空时抛出 ValueError；
        出现 yes/no 之外的非缺失 churn 时抛出
        ValueError；任一数值列整列都无法转换时也抛出 ValueError。
    """
    # TODO: 清理客户表并返回新对象。
    raise NotImplementedError("TODO: 实现 clean_customers")


def summarize_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        一位客户可能有多笔订单。建模需要每位客户一行的已完成订单统计。

    学生需要完成什么：
        在副本中把 quantity、unit_price 转成数字；拒绝缺失或无穷数值；
        验证数量是非负整数且单价非负；
        order_status 去空格并忽略大小写，只保留 Completed；
        计算 order_total = quantity * unit_price；按 customer_id 汇总
        order_count（不同 order_id 数）、total_order_spending（总金额）和
        average_order_value（平均订单金额），并按 customer_id 升序排列。

    参数：
        orders：包含 order_id、customer_id、quantity、unit_price、order_status 的表。

    返回值：
        每位有已完成订单客户一行的 DataFrame，列顺序固定为
        customer_id、order_count、total_order_spending、average_order_value。

    输入输出示例：
        C001 两笔 Completed，金额 20 和 30 -> count=2、total=50、average=25。
        只有 Cancelled 订单 -> 返回具有固定四列的空 DataFrame。

    特殊情况：
        缺列时抛出 KeyError；数字无法转换、数值缺失或无穷、数量不是整数、数量或单价为负时抛出
        ValueError；不得修改原表。
    """
    # TODO: 计算并汇总已完成订单。
    raise NotImplementedError("TODO: 实现 summarize_orders")


def merge_customer_summary(
    customers: pd.DataFrame,
    order_summary: pd.DataFrame,
) -> pd.DataFrame:
    """
    题目背景：
        客户属性和订单统计要合成一张分析表；没有已完成订单的客户也必须保留。

    学生需要完成什么：
        按 customer_id 做一对一左连接；用 0 填充缺失的 order_count、
        total_order_spending、average_order_value，并把 order_count 转为整数。

    参数：
        customers：每位客户一行的清洗客户表。
        order_summary：summarize_orders() 返回的每客户订单统计。

    返回值：
        行数和客户顺序与 customers 相同的新 DataFrame。

    输入输出示例：
        客户 C001 有订单 -> 合并后保留对应统计。
        客户 C002 无订单 -> 三个订单统计都为 0。

    特殊情况：
        任一表缺少 customer_id 时抛出 KeyError；任一表 customer_id 重复时让
        pandas 的一对一连接检查抛出 MergeError；不修改输入表。
    """
    # TODO: 左连接客户与订单汇总，并填充无订单客户。
    raise NotImplementedError("TODO: 实现 merge_customer_summary")


def create_customer_figure(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    题目背景：
        分析结果要以图片交付：左图比较各城市平均月消费，右图比较流失人数。

    学生需要完成什么：
        验证 city、monthly_spending、churn 三列；创建 1 行 2 列 Figure；
        左侧画按 city 分组的平均 monthly_spending 柱状图，右侧画 churn 的
        0/1 计数柱状图；添加英文标题和轴标签；自动创建输出父目录；
        tight_layout 后保存为非空图片，并关闭本函数创建的 Figure。

    参数：
        dataframe：已清洗、合并的客户分析表。
        output_path：图片保存路径。

    返回值：
        None。

    输入输出示例：
        output_path=Path("figures/report.png") -> 文件存在且大小大于 0。
        父目录尚不存在 -> 函数自动创建目录后保存。

    特殊情况：
        缺少绘图列时抛出 KeyError；即使保存失败，也要在 finally 中关闭 Figure；
        不得调用 plt.show()。
    """
    # TODO: 保存双子图客户分析图片并可靠关闭 Figure。
    raise NotImplementedError("TODO: 实现 create_customer_figure")


def train_churn_classifier(
    dataframe: pd.DataFrame,
) -> tuple[Any, dict[str, float]]:
    """
    题目背景：
        公司希望利用客户属性和订单行为预测 churn，并用未参与训练的客户评价模型。

    学生需要完成什么：
        使用 age、monthly_spending、satisfaction_score、order_count、
        total_order_spending、average_order_value 六个数值特征，以及 gender、
        city、contract_type 三个分类特征；churn 是 0/1 标签。
        按 75%/25% 分层划分，random_state=42；数值管道用中位数填补和
        StandardScaler，分类管道用众数填补和
        OneHotEncoder(handle_unknown="ignore")；通过 ColumnTransformer 和
        Pipeline 训练 LogisticRegression(max_iter=1000, random_state=42)。
        在测试集返回 accuracy、precision、recall、f1、roc_auc 五个指标。

    参数：
        dataframe：clean_customers 与 merge_customer_summary 产生的分析表。

    返回值：
        (model, metrics)。model 是已拟合 Pipeline；metrics 是五个 float 的字典。

    输入输出示例：
        30 行且两类充足的数据 -> model 可 predict，五个指标都在 0 到 1。
        特征中有数值缺失 -> 由训练集拟合的中位数填补后仍可训练。

    特殊情况：
        缺少任何必需列时抛出 KeyError；标签含缺失、非 0/1、只有一个类别，
        或任一类别不足以分层划分时抛出 ValueError；不得在划分前拟合预处理器。
    """
    # TODO: 用无泄漏管道训练并评价客户流失分类器。
    raise NotImplementedError("TODO: 实现 train_churn_classifier")
