"""Python《09. 基础类：把数据和相关操作放在一起》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_customer_class(module: ModuleType, tmp_path: Path) -> None:
    customer = module.Customer("Alice", 188.5)
    assert customer.describe() == "Alice: 188.50"
    assert customer.annual_spending() == pytest.approx(2262.0)
    with pytest.raises(ValueError):
        module.Customer("", 10)
    with pytest.raises(ValueError):
        module.Customer("Alice", -1)

def check_order_class(module: ModuleType, tmp_path: Path) -> None:
    order = module.Order("Pen", 3, 2.5)
    assert order.total() == pytest.approx(7.5)
    assert order.describe() == "Pen × 3 = 7.50"
    zero_order = module.Order("Book", 0, 12)
    assert zero_order.total() == pytest.approx(0.0)
    with pytest.raises(ValueError):
        module.Order("", 1, 1)
    with pytest.raises(ValueError):
        module.Order("Pen", -1, 1)

def check_score_summary_class(module: ModuleType, tmp_path: Path) -> None:
    source_scores = [60, 80, 100]
    summary = module.ScoreSummary(source_scores)
    source_scores.append(0)
    assert summary.average() == pytest.approx(80.0)
    assert summary.highest() == pytest.approx(100.0)
    with pytest.raises(ValueError):
        module.ScoreSummary([])
    with pytest.raises(ValueError):
        module.ScoreSummary([101])

def check_build_customers(module: ModuleType, tmp_path: Path) -> None:
    customers = module.build_customers([("A", 10), ("B", 20)])
    assert [customer.describe() for customer in customers] == ["A: 10.00", "B: 20.00"]
    assert module.build_customers([]) == []
    with pytest.raises(ValueError):
        module.build_customers([("", 10)])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_09_customer", answer, check_customer_class),
    ("answer_09_order", answer, check_order_class),
    ("answer_09_score_summary", answer, check_score_summary_class),
    ("answer_09_build_customers", answer, check_build_customers),
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
