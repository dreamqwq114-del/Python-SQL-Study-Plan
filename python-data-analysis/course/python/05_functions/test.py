"""Python《05. 函数：把重复分析步骤变成可复用工具》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_calculate_order_total(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_order_total(3, 20.0, 0.1) == pytest.approx(54.0)
    assert module.calculate_order_total(2, 15.0) == pytest.approx(30.0)
    assert module.calculate_order_total(0, 15.0, 1.0) == pytest.approx(0.0)
    for arguments in ((-1, 10.0, 0.0), (1, -1.0, 0.0), (1, 10.0, 1.1)):
        with pytest.raises(ValueError):
            module.calculate_order_total(*arguments)

def check_calculate_growth_rate(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_growth_rate(100, 120) == pytest.approx(20.0)
    assert module.calculate_growth_rate(200, 150) == pytest.approx(-25.0)
    assert module.calculate_growth_rate(100, 0) == pytest.approx(-100.0)
    with pytest.raises(ValueError):
        module.calculate_growth_rate(0, 10)
    with pytest.raises(ValueError):
        module.calculate_growth_rate(10, -1)

def check_summarize_scores(module: ModuleType, tmp_path: Path) -> None:
    assert module.summarize_scores([60, 80, 100]) == pytest.approx((60, 100, 80))
    assert module.summarize_scores([88.5]) == pytest.approx((88.5, 88.5, 88.5))
    with pytest.raises(ValueError):
        module.summarize_scores([])
    with pytest.raises(ValueError):
        module.summarize_scores([101])

def check_format_customer_label(module: ModuleType, tmp_path: Path) -> None:
    assert module.format_customer_label(" C001 ", " Suzhou ") == "C001 - Suzhou"
    assert module.format_customer_label("C002") == "C002 - Unknown"
    assert module.format_customer_label("C003", "  ") == "C003 - Unknown"
    with pytest.raises(ValueError):
        module.format_customer_label("  ", "Suzhou")

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_05_order_total", answer, check_calculate_order_total),
    ("answer_05_growth_rate", answer, check_calculate_growth_rate),
    ("answer_05_summarize_scores", answer, check_summarize_scores),
    ("answer_05_customer_label", answer, check_format_customer_label),
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
