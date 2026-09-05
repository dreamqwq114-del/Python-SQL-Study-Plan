"""Pandas《Pandas 04：准确选择需要的行和列》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_04_select_customer_columns(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "city": ["A"],
            "monthly_spending": [100.0],
            "customer_id": ["C1"],
        }
    )
    original = source.copy()
    result = module.select_customer_columns(source)
    assert result.columns.tolist() == ["customer_id", "monthly_spending"]
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.select_customer_columns(pd.DataFrame({"customer_id": ["C1"]}))

def check_04_select_rows_by_labels(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"value": [10, 20]}, index=["C1", "C2"])
    result = module.select_rows_by_labels(source, ["C2", "C1"])
    assert result.index.tolist() == ["C2", "C1"]
    assert module.select_rows_by_labels(source, []).empty
    with pytest.raises(KeyError):
        module.select_rows_by_labels(source, ["C9"])

def check_04_select_data_block(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"city": ["A", "B", "C"], "age": [20, 30, 40]})
    result = module.select_data_block(source, ["age"], 2)
    pd.testing.assert_frame_equal(result, source[["age"]].head(2))
    assert module.select_data_block(source, ["city"], 0).shape == (0, 1)
    with pytest.raises(ValueError):
        module.select_data_block(source, ["city"], -1)
    with pytest.raises(KeyError):
        module.select_data_block(source, ["unknown"], 1)

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_04_select_customer_columns", answer, check_04_select_customer_columns),
    ("answer_04_select_rows_by_labels", answer, check_04_select_rows_by_labels),
    ("answer_04_select_data_block", answer, check_04_select_data_block),
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
