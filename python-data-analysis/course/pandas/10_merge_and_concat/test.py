"""Pandas《Pandas 10：连接客户表与订单表》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_10_merge_customers_orders(module: ModuleType, _: Path) -> None:
    customers = pd.DataFrame(
        {"customer_id": ["C1", "C2"], "city": ["A", "B"]}
    )
    orders = pd.DataFrame(
        {"customer_id": ["C1", "C1"], "order_id": ["O1", "O2"]}
    )
    result = module.merge_customers_orders(customers, orders)
    assert result["customer_id"].tolist() == ["C1", "C1", "C2"]
    assert pd.isna(result.loc[2, "order_id"])

def check_10_concat_order_batches(module: ModuleType, _: Path) -> None:
    first = pd.DataFrame({"order_id": ["O1", "O2"]})
    second = pd.DataFrame({"order_id": ["O3"]})
    result = module.concat_order_batches([first, second])
    assert result["order_id"].tolist() == ["O1", "O2", "O3"]
    assert result.index.tolist() == [0, 1, 2]
    assert module.concat_order_batches([]).empty

def check_10_find_orders_without_customer(module: ModuleType, _: Path) -> None:
    customers = pd.DataFrame({"customer_id": ["C1", "C2"]})
    orders = pd.DataFrame(
        {"order_id": ["O1", "O9"], "customer_id": ["C1", "C9"]}
    )
    result = module.find_orders_without_customer(customers, orders)
    assert result.to_dict("records") == [{"order_id": "O9", "customer_id": "C9"}]
    assert module.find_orders_without_customer(customers, orders.iloc[:1]).empty

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_10_merge_customers_orders", answer, check_10_merge_customers_orders),
    ("answer_10_concat_order_batches", answer, check_10_concat_order_batches),
    ("answer_10_find_orders_without_customer", answer, check_10_find_orders_without_customer),
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
