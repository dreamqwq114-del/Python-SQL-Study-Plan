"""第 12 节练习：字符串操作。"""

import pandas as pd

def clean_text_fields(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        城市和合同字段含多余空格、大小写不统一，导致分组重复。

    学生需要完成什么：
        返回副本：city 去掉两端空格并转小写；
        contract_type 只去掉两端空格。

    参数：
        dataframe：客户表。

    返回值：
        两个文本字段已清理的 DataFrame。

    输入输出示例：
        city=" Suzhou " -> "suzhou"
        contract_type=" Monthly " -> "Monthly"

    特殊情况：
        缺失文本保持缺失；不修改原表；缺列时抛出 KeyError。

    提示：
        通过 Series.str 依次调用 strip() 和 lower()。
    """
    # TODO: 清理 city 和 contract_type。
    raise NotImplementedError("TODO: 实现 clean_text_fields")


def filter_products_by_keyword(
    dataframe: pd.DataFrame, keyword: str
) -> pd.DataFrame:
    """
    题目背景：
        商品分析需要找出名称中包含某个关键词的订单。

    学生需要完成什么：
        对 product_name 做不区分大小写的文字包含匹配，返回匹配行副本。
        keyword 应按普通文本处理，而不是正则表达式。

    参数：
        dataframe：订单表。
        keyword：搜索关键词。

    返回值：
        商品名包含关键词的订单 DataFrame。

    输入输出示例：
        ["USB Cable", "Mouse"]、keyword="usb" -> 只返回 USB Cable
        ["Phone Case"]、keyword="CASE" -> 返回 Phone Case

    特殊情况：
        缺失商品名不匹配；空关键词匹配所有非缺失商品名。

    提示：
        str.contains(keyword, case=False, na=False, regex=False)。
    """
    # TODO: 按普通文本关键词筛选商品。
    raise NotImplementedError("TODO: 实现 filter_products_by_keyword")


def add_product_key(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    题目背景：
        系统需要由商品名生成统一的小写键，方便后续匹配。

    学生需要完成什么：
        返回副本并新增 product_key：product_name 去掉两端空格、
        转小写，再把连续空白替换为一个下划线。

    参数：
        dataframe：订单表。

    返回值：
        新增 product_key 的 DataFrame。

    输入输出示例：
        " USB Cable " -> "usb_cable"
        "Phone   Case" -> "phone_case"

    特殊情况：
        缺失商品名得到缺失 product_key；不修改原表。

    提示：
        使用 str.strip().str.lower().str.replace(r"\\s+", "_", regex=True)。
    """
    # TODO: 生成规范化商品键。
    raise NotImplementedError("TODO: 实现 add_product_key")
