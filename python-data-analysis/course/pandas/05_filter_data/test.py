"""Pandas《Pandas 05：用业务条件筛选客户》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_05_filter_customers(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C3", "C4"],
            "age": [35, 35, 29, 30],
            "churn": [1, 0, 1, 1],
        }
    )
    result = module.filter_customers(source)
    assert result["customer_id"].tolist() == ["C1", "C4"]
    assert module.filter_customers(source.assign(churn=0)).empty

def check_05_filter_by_cities(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"city": ["Suzhou", "Wuxi", "Shanghai"]})
    result = module.filter_by_cities(source, ["Wuxi", "Suzhou"])
    assert result["city"].tolist() == ["Suzhou", "Wuxi"]
    assert module.filter_by_cities(source, []).empty

def check_05_filter_spending_range(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"monthly_spending": [100.0, 200.0, 300.0, float("nan")]}
    )
    result = module.filter_spending_range(source, 100, 200)
    assert result["monthly_spending"].tolist() == [100.0, 200.0]
    with pytest.raises(ValueError):
        module.filter_spending_range(source, 300, 100)

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_05_filter_customers", answer, check_05_filter_customers),
    ("answer_05_filter_by_cities", answer, check_05_filter_by_cities),
    ("answer_05_filter_spending_range", answer, check_05_filter_spending_range),
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
