"""第七章四道练习的参考答案。"""

import csv
from pathlib import Path


def read_first_line(file_path: Path) -> str:
    """读取 UTF-8 文件的第一行。"""
    with file_path.open("r", encoding="utf-8") as file:
        return file.readline().rstrip("\r\n")


def read_nonempty_lines(file_path: Path) -> list[str]:
    """返回清理后的非空行。"""
    result: list[str] = []
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            cleaned = line.strip()
            if cleaned != "":
                result.append(cleaned)
    return result


def write_report(file_path: Path, lines: list[str]) -> None:
    """创建父目录并写入多行报告。"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines)
    if len(lines) > 0:
        content += "\n"
    file_path.write_text(content, encoding="utf-8")


def count_csv_rows(file_path: Path) -> int:
    """统计 CSV 中除表头外的数据行。"""
    with file_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if header is None:
            raise ValueError("CSV 文件没有表头")
        count = 0
        for _ in reader:
            count += 1
    return count
