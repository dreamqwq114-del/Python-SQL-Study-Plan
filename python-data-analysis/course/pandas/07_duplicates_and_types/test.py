"""Pandas《Pandas 07：去除重复记录并修正数据类型》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_07_clean_duplicates_and_spending(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C1", "C2"],
            "monthly_spending": ["100", "120", "bad"],
        }
    )
    original = source.copy()
    result = module.clean_duplicates_and_spending(source)
    assert result["customer_id"].tolist() == ["C1", "C2"]
    assert result.loc[0, "monthly_spending"] == 100
    assert pd.isna(result.loc[1, "monthly_spending"])
    pd.testing.assert_frame_equal(source, original)

def check_07_convert_customer_types(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"age": ["21", "bad"], "monthly_spending": ["19.5", "bad"]}
    )
    result = module.convert_customer_types(source)
    assert str(result["age"].dtype) == "Int64"
    assert result["age"].tolist()[0] == 21
    assert pd.isna(result["age"].tolist()[1])
    assert result.loc[0, "monthly_spending"] == 19.5
    assert pd.isna(result.loc[1, "monthly_spending"])

def check_07_keep_latest_customer_records(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C1"],
            "monthly_spending": [100, 200, 120],
        }
    )
    result = module.keep_latest_customer_records(source)
    assert result.to_dict("records") == [
        {"customer_id": "C2", "monthly_spending": 200},
        {"customer_id": "C1", "monthly_spending": 120},
    ]
    assert result.index.tolist() == [0, 1]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_07_clean_duplicates_and_spending", answer, check_07_clean_duplicates_and_spending),
    ("answer_07_convert_customer_types", answer, check_07_convert_customer_types),
    ("answer_07_keep_latest_customer_records", answer, check_07_keep_latest_customer_records),
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
