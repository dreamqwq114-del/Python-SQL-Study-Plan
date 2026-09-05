"""Pandas《Pandas 02：从 CSV 读取客户和订单数据》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_02_load_customers(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame({"customer_id": ["C1", "C2"], "city": ["A", "B"]})
    path = tmp_path / "customers.csv"
    source.to_csv(path, index=False)
    pd.testing.assert_frame_equal(module.load_customers(path), source)
    with pytest.raises(FileNotFoundError):
        module.load_customers(tmp_path / "missing.csv")

def check_02_load_customer_columns(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", "C2"], "age": [20, 30], "city": ["A", "B"]}
    )
    path = tmp_path / "customers.csv"
    source.to_csv(path, index=False)
    result = module.load_customer_columns(path, ["age", "customer_id"])
    pd.testing.assert_frame_equal(result, source[["age", "customer_id"]])
    empty_columns = module.load_customer_columns(path, [])
    assert empty_columns.shape == (2, 0)
    with pytest.raises(KeyError):
        module.load_customer_columns(path, ["unknown"])

def check_02_load_orders_with_dates(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame(
        {"order_id": ["O1", "O2"], "order_date": ["2025-01-15", "wrong"]}
    )
    path = tmp_path / "orders.csv"
    source.to_csv(path, index=False)
    result = module.load_orders_with_dates(path)
    assert result.loc[0, "order_date"] == pd.Timestamp("2025-01-15")
    assert pd.isna(result.loc[1, "order_date"])
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_02_load_customers", answer, check_02_load_customers),
    ("answer_02_load_customer_columns", answer, check_02_load_customer_columns),
    ("answer_02_load_orders_with_dates", answer, check_02_load_orders_with_dates),
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
