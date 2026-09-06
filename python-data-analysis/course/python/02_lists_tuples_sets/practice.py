"""第二章练习：列表、元组、集合与切片。"""


def unique_recent_items(items: list[str], start: int) -> set[str]:
    """截取指定位置之后的数据并去重。

    题目背景：
        客户最近浏览商品保存在列表中，同一商品可能出现多次。分析时只想保留
        从某个位置开始出现过的不同商品。

    学生需要完成什么：
        使用切片取得 items[start:]，再把结果转换成集合并返回。

    参数：
        items：按时间顺序保存的商品名称列表。
        start：切片开始位置，可以是 0、正数或负数。

    返回值：
        从 start 开始出现过的不同商品组成的集合。

    输入输出示例：
        unique_recent_items(["Pen", "Book", "Pen"], 1) -> {"Book", "Pen"}
        unique_recent_items(["A", "B"], 2) -> set()

    特殊情况：
        空列表或超出列表右边界的 start 返回空集合；负数 start 按 Python
        切片规则从末尾计算。
    """
    # TODO: 对列表切片并去重。
    raise NotImplementedError("TODO: 实现 unique_recent_items")


def calculate_average_score(scores: list[float]) -> float:
    """计算一组成绩的平均值。

    题目背景：
        一门课的成绩已整理成列表，需要计算班级平均分。

    学生需要完成什么：
        使用 sum() 和 len() 计算平均值并返回。

    参数：
        scores：由整数或浮点数组成的非空成绩列表。

    返回值：
        浮点数形式的平均分。

    输入输出示例：
        calculate_average_score([80, 90, 70]) -> 80.0
        calculate_average_score([88.5]) -> 88.5

    特殊情况：
        空列表没有平均值，应产生 ValueError。
    """
    # TODO: 检查空列表并计算平均值。
    raise NotImplementedError("TODO: 实现 calculate_average_score")


def unpack_order(order: tuple[str, int, float]) -> str:
    """解包一条订单元组并生成摘要。

    题目背景：
        一条简化订单使用“商品名、数量、单价”三个固定位置保存，元组适合表示
        这种结构不会改变的记录。

    学生需要完成什么：
        把元组解包为三个变量，检查数量和单价非负，再生成指定文本。

    参数：
        order：格式固定为 (商品名, 数量, 单价) 的三项元组。

    返回值：
        格式为“商品名：数量 × 单价”的字符串，单价显示两位小数。

    输入输出示例：
        unpack_order(("Notebook", 2, 12.5)) -> "Notebook：2 × 12.50"
        unpack_order(("Pen", 0, 3.0)) -> "Pen：0 × 3.00"

    特殊情况：
        数量或单价小于 0 时产生 ValueError。元组项数不为 3 时，Python
        解包本身会产生 ValueError。
    """
    # TODO: 解包元组、检查数值并生成文本。
    raise NotImplementedError("TODO: 实现 unpack_order")


def find_common_customers(
    first_group: set[str],
    second_group: set[str],
) -> set[str]:
    """找出同时出现在两个客户组中的客户。

    题目背景：
        市场部门分别整理了“高消费客户”和“高满意度客户”，现在要找出同时满足
        两个条件的人。

    学生需要完成什么：
        使用集合交集返回两个集合共有的客户编号。

    参数：
        first_group：第一组客户编号。
        second_group：第二组客户编号。

    返回值：
        同时存在于两个集合中的客户编号集合。

    输入输出示例：
        find_common_customers({"C1", "C2"}, {"C2", "C3"}) -> {"C2"}
        find_common_customers({"C1"}, {"C2"}) -> set()

    特殊情况：
        任意一个集合为空时返回空集合；不能修改传入的原集合。
    """
    # TODO: 返回两个客户集合的交集。
    raise NotImplementedError("TODO: 实现 find_common_customers")
