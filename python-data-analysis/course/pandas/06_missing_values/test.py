"""Pandas《Pandas 06：识别、填充和删除缺失值》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_06_count_missing(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"age": [20, None], "city": ["A", "B"]})
    result = module.count_missing(source)
    assert result.to_dict() == {"age": 1, "city": 0}
    assert module.count_missing(source.iloc[:0]).to_dict() == {"age": 0, "city": 0}

def check_06_fill_missing_scores(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"satisfaction_score": [5.0, None, 2.0]})
    original = source.copy()
    result = module.fill_missing_scores(source, 3.0)
    assert result["satisfaction_score"].tolist() == [5.0, 3.0, 2.0]
    pd.testing.assert_frame_equal(source, original)

def check_06_drop_incomplete_rows(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", None, "C3"], "city": ["A", "B", None]}
    )
    result = module.drop_incomplete_rows(source, ["customer_id", "city"])
    assert result.to_dict("records") == [{"customer_id": "C1", "city": "A"}]
    pd.testing.assert_frame_equal(
        module.drop_incomplete_rows(source, []),
        source.reset_index(drop=True),
    )
    with pytest.raises(KeyError):
        module.drop_incomplete_rows(source, ["unknown"])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_06_count_missing", answer, check_06_count_missing),
    ("answer_06_fill_missing_scores", answer, check_06_fill_missing_scores),
    ("answer_06_drop_incomplete_rows", answer, check_06_drop_incomplete_rows),
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
