"""Python《07. 文件与路径：读取输入并保存分析结果》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_read_first_line(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "note.txt"
    path.write_text("first\nsecond\n", encoding="utf-8")
    assert module.read_first_line(path) == "first"
    empty = tmp_path / "empty.txt"
    empty.write_text("", encoding="utf-8")
    assert module.read_first_line(empty) == ""
    with pytest.raises(FileNotFoundError):
        module.read_first_line(tmp_path / "missing.txt")

def check_read_nonempty_lines(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "fields.txt"
    path.write_text(" age \n\n city\n  \n", encoding="utf-8")
    assert module.read_nonempty_lines(path) == ["age", "city"]
    empty = tmp_path / "empty_lines.txt"
    empty.write_text("", encoding="utf-8")
    assert module.read_nonempty_lines(empty) == []

def check_write_report(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "nested" / "report.txt"
    lines = ["A", "B"]
    assert module.write_report(path, lines) is None
    assert path.read_text(encoding="utf-8") == "A\nB\n"
    assert lines == ["A", "B"]
    empty_path = tmp_path / "empty_report.txt"
    module.write_report(empty_path, [])
    assert empty_path.read_text(encoding="utf-8") == ""

def check_count_csv_rows(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text('id,name\n1,"A, B"\n2,C\n', encoding="utf-8")
    assert module.count_csv_rows(path) == 2
    header_only = tmp_path / "header.csv"
    header_only.write_text("id,name\n", encoding="utf-8")
    assert module.count_csv_rows(header_only) == 0
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        module.count_csv_rows(empty)

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_07_first_line", answer, check_read_first_line),
    ("answer_07_nonempty_lines", answer, check_read_nonempty_lines),
    ("answer_07_write_report", answer, check_write_report),
    ("answer_07_count_csv", answer, check_count_csv_rows),
]

PRACTICE_CASES: list[tuple[str, ModuleType, Check]] = [
    (name.replace("answer_", "practice_"), practice, check)
    for name, _, check in ANSWER_CASES
]

@pytest.mark.parametrize(
    ("name", "module", "check"),
    ANSWER_CASES,
    ids=[case[0] for case in ANSWER_CASES],
)
def test_answer_contract(
    name: str,
    module: ModuleType,
    check: Check,
    tmp_path: Path,
) -> None:
    check(module, tmp_path)


@pytest.mark.parametrize(
    ("name", "module", "check"),
    PRACTICE_CASES,
    ids=[case[0] for case in PRACTICE_CASES],
)
def test_practice_contract(
    name: str,
    module: ModuleType,
    check: Check,
    tmp_path: Path,
) -> None:
    try:
        check(module, tmp_path)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
