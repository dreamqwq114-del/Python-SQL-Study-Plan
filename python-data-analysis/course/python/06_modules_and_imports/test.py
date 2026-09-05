"""Python《06. 模块与导入：把项目代码分到不同文件》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_build_data_path(module: ModuleType, tmp_path: Path) -> None:
    path = module.build_data_path("sample_customers.csv")
    assert path.name == "sample_customers.csv"
    assert path.parent.name == "data"
    for invalid in ("", "customers.txt", "folder/customers.csv"):
        with pytest.raises(ValueError):
            module.build_data_path(invalid)

def check_build_processed_path(module: ModuleType, tmp_path: Path) -> None:
    path = module.build_processed_path("clean.csv")
    assert path.name == "clean.csv"
    assert path.parent.name == "processed"
    with pytest.raises(ValueError):
        module.build_processed_path("clean.xlsx")
    with pytest.raises(ValueError):
        module.build_processed_path("nested/clean.csv")

def check_build_figure_path(module: ModuleType, tmp_path: Path) -> None:
    path = module.build_figure_path("sales.png")
    assert path.name == "sales.png"
    assert path.parent.name == "figures"
    with pytest.raises(ValueError):
        module.build_figure_path("sales.jpg")
    with pytest.raises(ValueError):
        module.build_figure_path("nested/sales.png")

def check_get_project_directories(module: ModuleType, tmp_path: Path) -> None:
    directories = module.get_project_directories()
    assert set(directories) == {"root", "data", "processed", "figures"}
    assert directories["data"].parent == directories["root"]
    assert directories["processed"].parent == directories["data"]
    assert directories["figures"].parent == directories["root"]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_06_data_path", answer, check_build_data_path),
    ("answer_06_processed_path", answer, check_build_processed_path),
    ("answer_06_figure_path", answer, check_build_figure_path),
    ("answer_06_directories", answer, check_get_project_directories),
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
