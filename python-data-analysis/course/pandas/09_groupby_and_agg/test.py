"""Pandas《Pandas 09：按城市或合同分组汇总》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_09_summarize_by_city(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C2", "C3"],
            "city": ["A", "A", "A", "B"],
            "monthly_spending": [100.0, 300.0, 300.0, 50.0],
        }
    )
    result = module.summarize_by_city(source)
    assert result.to_dict("records") == [
        {"city": "A", "customer_count": 2, "average_spending": 700 / 3},
        {"city": "B", "customer_count": 1, "average_spending": 50.0},
    ]

def check_09_summarize_orders_by_customer(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3"],
            "customer_id": ["C1", "C1", "C2"],
            "quantity": [2, 1, 3],
            "unit_price": [50, 60, 10],
        }
    )
    result = module.summarize_orders_by_customer(source)
    assert result.to_dict("records") == [
        {"customer_id": "C1", "order_count": 2, "total_spending": 160},
        {"customer_id": "C2", "order_count": 1, "total_spending": 30},
    ]
    assert "order_total" not in source.columns

def check_09_calculate_churn_rate(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "contract_type": ["Monthly", "Monthly", "Yearly"],
            "churn": [1, 0, 0],
        }
    )
    result = module.calculate_churn_rate_by_contract(source)
    assert result.to_dict("records") == [
        {"contract_type": "Monthly", "customer_count": 2, "churn_rate": 0.5},
        {"contract_type": "Yearly", "customer_count": 1, "churn_rate": 0.0},
    ]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_09_summarize_by_city", answer, check_09_summarize_by_city),
    ("answer_09_summarize_orders_by_customer", answer, check_09_summarize_orders_by_customer),
    ("answer_09_calculate_churn_rate", answer, check_09_calculate_churn_rate),
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
