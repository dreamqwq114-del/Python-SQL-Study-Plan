"""第八章练习：发现错误、抛出异常与处理异常。"""

from pathlib import Path


def parse_positive_amount(text: str) -> float:
    """把文本转换为严格大于 0 的金额。

    题目背景：
        用户输入或 CSV 字段可能不是有效金额，需要在进入计算前进行保护。

    学生需要完成什么：
        使用 float() 转换文本；转换结果小于或等于 0 时主动抛出 ValueError。

    参数：
        text：字符串形式的金额。

    返回值：
        严格大于 0 的浮点数金额。

    输入输出示例：
        parse_positive_amount("12.5") -> 12.5
        parse_positive_amount(" 1 ") -> 1.0

    特殊情况：
        "0"、负数、空字符串和非数字文本都应产生 ValueError。

    提示：
        float() 已经会为无法转换的文本产生 ValueError。
    """
    # TODO: 转换文本并检查金额严格为正。
    raise NotImplementedError("TODO: 实现 parse_positive_amount")


def parse_optional_score(text: str) -> float | None:
    """解析允许缺失的百分制成绩。

    题目背景：
        成绩列使用空字符串或 "NA" 表示缺失，其余值必须是 0 到 100 的数字。

    学生需要完成什么：
        清理文本；缺失标记返回 None；其他文本转换为 float 并检查范围。

    参数：
        text：成绩文本，可能包含两边空格。

    返回值：
        0 到 100 的浮点数，或表示缺失的 None。

    输入输出示例：
        parse_optional_score("88.5") -> 88.5
        parse_optional_score(" NA ") -> None

    特殊情况：
        空字符串也返回 None；范围外数值或其他文本产生 ValueError。

    提示：
        先处理缺失标记，再调用 float()，可以避免对 "NA" 进行转换。
    """
    # TODO: 处理缺失标记并验证成绩范围。
    raise NotImplementedError("TODO: 实现 parse_optional_score")


def safe_divide(numerator: float, denominator: float) -> float:
    """安全地完成除法。

    题目背景：
        计算平均金额或转化率时，分母可能是 0，需要给出清楚的错误。

    学生需要完成什么：
        分母为 0 时主动抛出 ValueError，否则返回除法结果。

    参数：
        numerator：分子。
        denominator：分母。

    返回值：
        numerator / denominator 的浮点数结果。

    输入输出示例：
        safe_divide(10, 2) -> 5.0
        safe_divide(0, 5) -> 0.0

    特殊情况：
        denominator 为 0 或 0.0 时产生 ValueError。

    提示：
        使用 if 检查分母，再执行除法。
    """
    # TODO: 防止除以 0 并返回结果。
    raise NotImplementedError("TODO: 实现 safe_divide")


def read_required_text(file_path: Path) -> str:
    """读取一个必须存在且不能为空的文本文件。

    题目背景：
        配置或字段说明是分析流程的必需输入，希望把底层文件错误转换成更统一的
        ValueError。

    学生需要完成什么：
        尝试以 UTF-8 读取文件；文件不存在时捕获 FileNotFoundError 并抛出
        ValueError；内容去除两边空白后为空也抛出 ValueError。

    参数：
        file_path：必需文本文件的路径。

    返回值：
        去除文件首尾空白后的非空文本。

    输入输出示例：
        内容为 " customer_id \\n" 时返回 "customer_id"
        文件不存在时产生 ValueError

    特殊情况：
        空文件或只有空白字符的文件产生 ValueError。

    提示：
        使用 try/except 捕获 FileNotFoundError，并用 raise ValueError(...) from error。
    """
    # TODO: 捕获文件缺失并验证内容非空。
    raise NotImplementedError("TODO: 实现 read_required_text")
