"""Python《02. 列表、元组、集合与切片》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_unique_recent_items(module: ModuleType, tmp_path: Path) -> None:
    items = ["Pen", "Book", "Pen", "Mouse"]
    assert module.unique_recent_items(items, 1) == {"Book", "Pen", "Mouse"}
    assert module.unique_recent_items(items, 4) == set()
    assert module.unique_recent_items(items, -2) == {"Pen", "Mouse"}
    assert items == ["Pen", "Book", "Pen", "Mouse"]

def check_calculate_average_score(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_average_score([80, 90, 70]) == pytest.approx(80.0)
    assert module.calculate_average_score([88.5]) == pytest.approx(88.5)
    with pytest.raises(ValueError):
        module.calculate_average_score([])

def check_unpack_order(module: ModuleType, tmp_path: Path) -> None:
    assert module.unpack_order(("Notebook", 2, 12.5)) == "Notebook：2 × 12.50"
    assert module.unpack_order(("Pen", 0, 3.0)) == "Pen：0 × 3.00"
    with pytest.raises(ValueError):
        module.unpack_order(("Pen", -1, 3.0))
    with pytest.raises(ValueError):
        module.unpack_order(("Pen", 1, -3.0))

def check_find_common_customers(module: ModuleType, tmp_path: Path) -> None:
    first = {"C1", "C2"}
    second = {"C2", "C3"}
    assert module.find_common_customers(first, second) == {"C2"}
    assert module.find_common_customers(set(), second) == set()
    assert first == {"C1", "C2"}
    assert second == {"C2", "C3"}

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_02_unique_recent_items", answer, check_unique_recent_items),
    ("answer_02_average_score", answer, check_calculate_average_score),
    ("answer_02_unpack_order", answer, check_unpack_order),
    ("answer_02_common_customers", answer, check_find_common_customers),
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
