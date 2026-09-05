"""Python《03. 字典：用字段名组织一条数据》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_count_categories(module: ModuleType, tmp_path: Path) -> None:
    assert module.count_categories(["A", "B", "A"]) == {"A": 2, "B": 1}
    assert module.count_categories([]) == {}
    assert module.count_categories(["a", "A"]) == {"a": 1, "A": 1}

def check_build_customer_record(module: ModuleType, tmp_path: Path) -> None:
    assert module.build_customer_record("C1", "Suzhou", 120.5) == {
        "customer_id": "C1",
        "city": "Suzhou",
        "monthly_spending": 120.5,
    }
    assert module.build_customer_record("C2", "", 0)["monthly_spending"] == 0
    with pytest.raises(ValueError):
        module.build_customer_record("", "Suzhou", 10)
    with pytest.raises(ValueError):
        module.build_customer_record("C1", "Suzhou", -1)

def check_get_required_value(module: ModuleType, tmp_path: Path) -> None:
    assert module.get_required_value({"city": "Suzhou"}, "city") == "Suzhou"
    assert module.get_required_value({"score": 0}, "score") == 0
    with pytest.raises(KeyError):
        module.get_required_value({}, "customer_id")

def check_merge_monthly_sales(module: ModuleType, tmp_path: Path) -> None:
    january = {"Pen": 10.0}
    february = {"Pen": 5.0, "Book": 20.0}
    assert module.merge_monthly_sales(january, february) == {"Pen": 15.0, "Book": 20.0}
    assert january == {"Pen": 10.0}
    assert module.merge_monthly_sales({}, {"Book": 8.0}) == {"Book": 8.0}
    with pytest.raises(ValueError):
        module.merge_monthly_sales({"Pen": -1.0}, {})

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_03_count_categories", answer, check_count_categories),
    ("answer_03_customer_record", answer, check_build_customer_record),
    ("answer_03_required_value", answer, check_get_required_value),
    ("answer_03_merge_sales", answer, check_merge_monthly_sales),
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
