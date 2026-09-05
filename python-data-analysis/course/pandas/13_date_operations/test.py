"""Pandas《Pandas 13：解析日期并制作月度订单汇总》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_13_add_date_parts(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"join_date": ["2025-01-12", "2024/03/18", "wrong"]}
    )
    result = module.add_date_parts(source)
    assert result.loc[0, "join_year"] == 2025
    assert result.loc[1, "join_month"] == 3
    assert pd.isna(result.loc[2, "join_date"])
    assert pd.api.types.is_datetime64_any_dtype(result["join_date"])

def check_13_filter_orders_by_date(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3", "O4"],
            "order_date": ["2025-01-01", "2025-01-31", "2025-02-01", "wrong"],
        }
    )
    result = module.filter_orders_by_date(source, "2025-01-01", "2025-01-31")
    assert result["order_id"].tolist() == ["O1", "O2"]
    with pytest.raises(ValueError):
        module.filter_orders_by_date(source, "bad", "2025-01-31")
    with pytest.raises(ValueError):
        module.filter_orders_by_date(source, "2025-02-01", "2025-01-01")

def check_13_monthly_order_totals(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "order_date": ["2025-01-01", "2025/01/10", "2025-02-01", "wrong"],
            "quantity": [2, 1, 1, 99],
            "unit_price": [50, 50, 80, 99],
        }
    )
    result = module.monthly_order_totals(source)
    assert result.to_dict("records") == [
        {"order_month": "2025-01", "order_total": 150},
        {"order_month": "2025-02", "order_total": 80},
    ]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_13_add_date_parts", answer, check_13_add_date_parts),
    ("answer_13_filter_orders_by_date", answer, check_13_filter_orders_by_date),
    ("answer_13_monthly_order_totals", answer, check_13_monthly_order_totals),
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
