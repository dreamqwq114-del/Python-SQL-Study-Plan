"""Pandas《Pandas 01：用 Series 和 DataFrame 表示表格数据》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_01_build_customer_frame(module: ModuleType, _: Path) -> None:
    result = module.build_customer_frame()
    expected = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "city": ["Suzhou", "Shanghai"],
            "monthly_spending": [188.5, 420.0],
        }
    )
    pd.testing.assert_frame_equal(result, expected)
    result.loc[0, "city"] = "Changed"
    assert module.build_customer_frame().loc[0, "city"] == "Suzhou"

def check_01_build_order_series(module: ModuleType, _: Path) -> None:
    result = module.build_order_series()
    expected = pd.Series(
        [1, 2, 3],
        index=["O001", "O002", "O003"],
        name="quantity",
    )
    pd.testing.assert_series_equal(result, expected)

def check_01_add_order_total(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"quantity": [2, 0, 3], "unit_price": [50, 99, 10]})
    original = source.copy()
    result = module.add_order_total(source)
    assert result["order_total"].tolist() == [100, 0, 30]
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.add_order_total(pd.DataFrame({"quantity": [1]}))

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_01_build_customer_frame", answer, check_01_build_customer_frame),
    ("answer_01_build_order_series", answer, check_01_build_order_series),
    ("answer_01_add_order_total", answer, check_01_add_order_total),
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
