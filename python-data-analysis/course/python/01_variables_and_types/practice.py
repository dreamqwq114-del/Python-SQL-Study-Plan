"""第一章练习：变量、数据类型、类型转换与 f-string。"""


def convert_age(age_text: str) -> int:
    """把客户年龄从字符串转换为整数。

    题目背景：
        CSV 或网页表格中的年龄可能以字符串形式读入，例如 "21"。

    学生需要完成什么：
        把 age_text 转换为 int 并返回。年龄不能小于 0。

    参数：
        age_text：表示客户年龄的字符串，字符串两边可能有空格。

    返回值：
        转换后的非负整数年龄。

    输入输出示例：
        convert_age("21") -> 21
        convert_age(" 0 ") -> 0

    特殊情况：
        负数、带小数的文本或非数字文本都应产生 ValueError。
    """
    # TODO: 把年龄文本转换为非负整数。
    raise NotImplementedError("TODO: 实现 convert_age")


def convert_price(price_text: str) -> float:
    """把商品价格从字符串转换为浮点数。

    题目背景：
        表格中的商品价格可能是 "39.90"，计算前需要变成真正的数字。

    学生需要完成什么：
        把 price_text 转换为 float 并返回。价格不能小于 0。

    参数：
        price_text：表示商品价格的字符串，字符串两边可能有空格。

    返回值：
        转换后的非负浮点数价格。

    输入输出示例：
        convert_price("39.90") -> 39.9
        convert_price(" 0 ") -> 0.0

    特殊情况：
        负数、空字符串、非数字文本或带有“元”等单位的文本应产生 ValueError。
    """
    # TODO: 把价格文本转换为非负浮点数。
    raise NotImplementedError("TODO: 实现 convert_price")


def calculate_order_amount(unit_price_text: str, quantity_text: str) -> float:
    """根据字符串形式的单价和数量计算订单金额。

    题目背景：
        一行订单数据把单价和数量都保存成了字符串，需要先转换再计算。

    学生需要完成什么：
        把 unit_price_text 转成 float，把 quantity_text 转成 int，
        检查二者都不是负数，然后返回“单价 × 数量”。

    参数：
        unit_price_text：字符串形式的商品单价。
        quantity_text：字符串形式的商品数量。

    返回值：
        浮点数形式的订单总金额。

    输入输出示例：
        calculate_order_amount("12.50", "4") -> 50.0
        calculate_order_amount("8", "0") -> 0.0

    特殊情况：
        负单价、负数量、非整数数量或无法转换的文本应产生 ValueError。
    """
    # TODO: 转换单价和数量，检查非负，然后计算总金额。
    raise NotImplementedError("TODO: 实现 calculate_order_amount")


def build_order_summary(
    product_name: str,
    quantity_text: str,
    unit_price_text: str,
) -> str:
    """使用 f-string 生成一条格式固定的订单摘要。

    题目背景：
        订单计算完成后，需要生成一行可以直接展示或写入报告的文本。

    学生需要完成什么：
        转换数量和单价，计算总金额，并使用 f-string 返回指定格式。
        单价和总金额都必须显示两位小数。

    参数：
        product_name：商品名称。
        quantity_text：字符串形式的商品数量。
        unit_price_text：字符串形式的商品单价。

    返回值：
        格式为
        “商品：商品名，数量：数量，单价：0.00 元，总金额：0.00 元”的字符串。

    输入输出示例：
        build_order_summary("Notebook", "2", "12.50")
        -> "商品：Notebook，数量：2，单价：12.50 元，总金额：25.00 元"

        build_order_summary("Pen", "0", "3")
        -> "商品：Pen，数量：0，单价：3.00 元，总金额：0.00 元"

    特殊情况：
        数量或单价是负数、格式错误时，应产生 ValueError。
        商品名按传入内容原样显示。
    """
    # TODO: 转换数据、计算金额，并使用 f-string 生成指定文本。
    raise NotImplementedError("TODO: 实现 build_order_summary")
