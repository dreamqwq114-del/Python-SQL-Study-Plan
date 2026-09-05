"""Python《01. 变量与数据类型》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_convert_age(module: ModuleType, tmp_path: Path) -> None:
    assert module.convert_age("21") == 21
    assert module.convert_age(" 0 ") == 0
    for invalid in ("-1", "21.5", "twenty", ""):
        with pytest.raises(ValueError):
            module.convert_age(invalid)

def check_convert_price(module: ModuleType, tmp_path: Path) -> None:
    assert module.convert_price("39.90") == pytest.approx(39.9)
    assert module.convert_price(" 0 ") == pytest.approx(0.0)
    for invalid in ("-0.01", "39.90元", "", "free"):
        with pytest.raises(ValueError):
            module.convert_price(invalid)

def check_calculate_order_amount(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_order_amount("12.50", "4") == pytest.approx(50.0)
    assert module.calculate_order_amount("8", "0") == pytest.approx(0.0)
    for price, quantity in (("-1", "2"), ("10", "-2"), ("10", "2.5"), ("bad", "2")):
        with pytest.raises(ValueError):
            module.calculate_order_amount(price, quantity)

def check_build_order_summary(module: ModuleType, tmp_path: Path) -> None:
    assert module.build_order_summary("Notebook", "2", "12.50") == (
        "商品：Notebook，数量：2，单价：12.50 元，总金额：25.00 元"
    )
    assert module.build_order_summary("Pen", "0", "3") == (
        "商品：Pen，数量：0，单价：3.00 元，总金额：0.00 元"
    )
    for quantity, price in (("-1", "12.50"), ("2", "-1"), ("two", "12.50")):
        with pytest.raises(ValueError):
            module.build_order_summary("Notebook", quantity, price)

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_01_convert_age", answer, check_convert_age),
    ("answer_01_convert_price", answer, check_convert_price),
    ("answer_01_order_amount", answer, check_calculate_order_amount),
    ("answer_01_order_summary", answer, check_build_order_summary),
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
