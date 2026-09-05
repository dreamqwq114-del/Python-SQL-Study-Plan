"""Python《04. 条件判断与循环：让分析规则重复执行》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_classify_spending(module: ModuleType, tmp_path: Path) -> None:
    assert module.classify_spending(99.0) == "low"
    assert module.classify_spending(100.0) == "medium"
    assert module.classify_spending(499.99) == "medium"
    assert module.classify_spending(500.0) == "high"
    with pytest.raises(ValueError):
        module.classify_spending(-0.01)

def check_count_churned(module: ModuleType, tmp_path: Path) -> None:
    assert module.count_churned(["Yes", "No", "Yes"]) == 2
    assert module.count_churned([]) == 0
    with pytest.raises(ValueError):
        module.count_churned(["yes"])

def check_calculate_valid_average(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_valid_average([4, None, 2]) == pytest.approx(3.0)
    assert module.calculate_valid_average([5]) == pytest.approx(5.0)
    with pytest.raises(ValueError):
        module.calculate_valid_average([])
    with pytest.raises(ValueError):
        module.calculate_valid_average([None, None])

def check_find_first_large_order(module: ModuleType, tmp_path: Path) -> None:
    assert module.find_first_large_order([20, 150, 80], 100) == 1
    assert module.find_first_large_order([20, 100], 100) is None
    assert module.find_first_large_order([], 0) is None
    with pytest.raises(ValueError):
        module.find_first_large_order([10, -1], 5)
    with pytest.raises(ValueError):
        module.find_first_large_order([10], -1)

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_04_classify_spending", answer, check_classify_spending),
    ("answer_04_count_churned", answer, check_count_churned),
    ("answer_04_valid_average", answer, check_calculate_valid_average),
    ("answer_04_first_large_order", answer, check_find_first_large_order),
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
