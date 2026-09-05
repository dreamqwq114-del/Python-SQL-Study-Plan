"""Pandas《Pandas 08：排序客户并计算描述统计》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_08_spending_statistics(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"monthly_spending": [100.0, None, 300.0]})
    result = module.spending_statistics(source)
    assert result == {"mean": 200.0, "median": 200.0, "max": 300.0}
    empty_result = module.spending_statistics(source.iloc[:0])
    assert all(pd.isna(value) for value in empty_result.values())

def check_08_sort_customers_by_spending(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", "C2", "C3"], "monthly_spending": [100, 300, 200]}
    )
    original = source.copy()
    assert module.sort_customers_by_spending(source)["customer_id"].tolist() == [
        "C2",
        "C3",
        "C1",
    ]
    assert module.sort_customers_by_spending(
        source, ascending=True
    )["customer_id"].tolist() == ["C1", "C3", "C2"]
    pd.testing.assert_frame_equal(source, original)

def check_08_top_spending_customers(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", "C2", "C3"], "monthly_spending": [100, 300, 200]}
    )
    result = module.top_spending_customers(source, 2)
    assert result["customer_id"].tolist() == ["C2", "C3"]
    assert module.top_spending_customers(source, 0).empty
    assert len(module.top_spending_customers(source, 10)) == 3
    with pytest.raises(ValueError):
        module.top_spending_customers(source, -1)

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_08_spending_statistics", answer, check_08_spending_statistics),
    ("answer_08_sort_customers_by_spending", answer, check_08_sort_customers_by_spending),
    ("answer_08_top_spending_customers", answer, check_08_top_spending_customers),
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
