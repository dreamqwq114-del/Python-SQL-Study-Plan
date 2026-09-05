"""Pandas《Pandas 03：在分析前查看和检查数据》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_03_summarize_structure(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"age": [20, 30], "city": ["A", "B"]})
    result = module.summarize_structure(source)
    assert result == {
        "rows": 2,
        "columns": ["age", "city"],
        "dtypes": {
            "age": str(source["age"].dtype),
            "city": str(source["city"].dtype),
        },
    }
    assert module.summarize_structure(source.iloc[:0])["rows"] == 0

def check_03_preview_rows(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"value": [10, 20, 30]})
    pd.testing.assert_frame_equal(module.preview_rows(source, 2), source.head(2))
    assert module.preview_rows(source, 0).empty
    assert len(module.preview_rows(source, 10)) == 3
    with pytest.raises(ValueError):
        module.preview_rows(source, -1)

def check_03_count_column_values(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"contract": ["A", "A", "B", None]})
    result = module.count_column_values(source, "contract")
    assert result.to_dict() == {"A": 2, "B": 1}
    result_with_missing = module.count_column_values(
        source, "contract", include_missing=True
    )
    assert result_with_missing.sum() == 4
    assert result_with_missing[result_with_missing.index.isna()].iloc[0] == 1
    with pytest.raises(KeyError):
        module.count_column_values(source, "unknown")

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_03_summarize_structure", answer, check_03_summarize_structure),
    ("answer_03_preview_rows", answer, check_03_preview_rows),
    ("answer_03_count_column_values", answer, check_03_count_column_values),
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
