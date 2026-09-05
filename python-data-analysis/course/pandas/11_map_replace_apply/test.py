"""Pandas《Pandas 11：转换类别、名称和消费档位》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_11_add_churn_and_annual_spending(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"churn": [1, 0, 9], "monthly_spending": [100.0, 50.0, 10.0]}
    )
    original = source.copy()
    result = module.add_churn_and_annual_spending(source)
    assert result["churn_label"].iloc[:2].tolist() == ["Churned", "Stayed"]
    assert pd.isna(result.loc[2, "churn_label"])
    assert result["annual_spending"].tolist() == [1200.0, 600.0, 120.0]
    pd.testing.assert_frame_equal(source, original)

def check_11_replace_contract_labels(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"contract_type": ["Monthly", "Yearly"]})
    result = module.replace_contract_labels(source, {"Monthly": "月付"})
    assert result["contract_type"].tolist() == ["月付", "Yearly"]
    unchanged = module.replace_contract_labels(source, {})
    pd.testing.assert_frame_equal(unchanged, source)

def check_11_add_spending_band(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"monthly_spending": [199.0, 200.0, 399.0, 400.0, None]}
    )
    result = module.add_spending_band(source)
    assert result["spending_band"].tolist() == [
        "Low",
        "Medium",
        "Medium",
        "High",
        "Unknown",
    ]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_11_add_churn_and_annual_spending", answer, check_11_add_churn_and_annual_spending),
    ("answer_11_replace_contract_labels", answer, check_11_replace_contract_labels),
    ("answer_11_add_spending_band", answer, check_11_add_spending_band),
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
