"""使用 pathlib 读写 UTF-8 文件示例。"""

from pathlib import Path
from tempfile import TemporaryDirectory


def write_report(file_path: Path, lines: list[str]) -> None:
    """创建父目录并写入多行报告。"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_nonempty_lines(file_path: Path) -> list[str]:
    """返回清理后的非空行。"""
    result: list[str] = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip()
        if cleaned:
            result.append(cleaned)
    return result


def main() -> None:
    with TemporaryDirectory() as temporary_directory:
        report_path = Path(temporary_directory) / "outputs" / "summary.txt"
        write_report(report_path, ["客户数：3", "流失数：1"])

        print("文件存在：", report_path.exists())
        print("文件名：", report_path.name)
        print("报告内容：", read_nonempty_lines(report_path))


if __name__ == "__main__":
    main()
