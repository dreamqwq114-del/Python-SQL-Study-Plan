"""第七章练习：使用 pathlib 读写文本与 CSV 文件。"""

import csv
from pathlib import Path


def read_first_line(file_path: Path) -> str:
    """读取 UTF-8 文本文件的第一行。

    题目背景：
        分析前常先读取说明文件的标题，以确认打开了正确文件。

    学生需要完成什么：
        以 UTF-8 编码读取文件，返回去除换行符后的第一行。

    参数：
        file_path：需要读取的文本文件路径。

    返回值：
        第一行文本，不包含行尾换行符。

    输入输出示例：
        内容为 "first\\nsecond\\n" 时返回 "first"
        内容为 "\\nsecond\\n" 时返回 ""

    特殊情况：
        文件不存在时保留 Python 的 FileNotFoundError；空文件返回空字符串。

    提示：
        可以使用 file_path.open() 和文件对象的 readline()。
    """
    # TODO: 以 UTF-8 读取并返回第一行。
    raise NotImplementedError("TODO: 实现 read_first_line")


def read_nonempty_lines(file_path: Path) -> list[str]:
    """读取并清理文件中的非空行。

    题目背景：
        报表字段清单可能混有空白行，需要在分析前去掉空行和两边空格。

    学生需要完成什么：
        读取所有行，对每行使用 strip()，只保留清理后非空的文本。

    参数：
        file_path：UTF-8 文本文件路径。

    返回值：
        按原顺序保存的非空文本列表。

    输入输出示例：
        内容为 " age \\n\\n city\\n" 时返回 ["age", "city"]
        空文件返回 []

    特殊情况：
        文件不存在时产生 FileNotFoundError；不能改变文件内容。

    提示：
        可以在列表推导式前先写普通 for 循环，理解后再决定是否简化。
    """
    # TODO: 读取、清理并筛选非空行。
    raise NotImplementedError("TODO: 实现 read_nonempty_lines")


def write_report(file_path: Path, lines: list[str]) -> None:
    """把多行报告写入 UTF-8 文本文件。

    题目背景：
        分析结果需要写入 outputs 子目录，而目标文件夹可能尚不存在。

    学生需要完成什么：
        创建父目录，把每个字符串写成一行，并保证文件末尾有换行符。

    参数：
        file_path：报告输出路径。
        lines：按顺序写入的文本列表。

    返回值：
        None。结果通过磁盘上的文件体现。

    输入输出示例：
        write_report(path, ["A", "B"]) 后文件内容为 "A\\nB\\n"
        write_report(path, []) 后创建内容为空的文件

    特殊情况：
        允许父目录不存在；不能修改传入的 lines 列表。

    提示：
        file_path.parent.mkdir(parents=True, exist_ok=True) 可创建父目录。
    """
    # TODO: 创建父目录并写入每行文本。
    raise NotImplementedError("TODO: 实现 write_report")


def count_csv_rows(file_path: Path) -> int:
    """统计 CSV 中除表头外的数据行数。

    题目背景：
        读取完整表格前，先用标准库快速确认 CSV 有多少条记录。

    学生需要完成什么：
        使用 csv.reader 读取文件，跳过第一行表头并统计剩余记录。

    参数：
        file_path：UTF-8 CSV 文件路径。

    返回值：
        不包括表头的数据行数量。

    输入输出示例：
        内容为 "id,name\\n1,A\\n2,B\\n" 时返回 2
        内容只有 "id,name\\n" 时返回 0

    特殊情况：
        完全空的文件没有表头，应产生 ValueError；文件不存在时产生
        FileNotFoundError。

    提示：
        先用 next(reader, None) 读取表头，再循环统计后续行。
    """
    # TODO: 使用 csv.reader 跳过表头并计数。
    raise NotImplementedError("TODO: 实现 count_csv_rows")
