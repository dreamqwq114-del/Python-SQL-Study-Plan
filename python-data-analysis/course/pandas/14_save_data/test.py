"""Pandas《Pandas 14：把清洗结果安全保存为 CSV》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_14_save_processed(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame({"customer_id": ["C1", "C2"], "city": ["A", "B"]})
    path = tmp_path / "nested" / "customers.csv"
    assert module.save_processed(source, path) is None
    result = pd.read_csv(path)
    pd.testing.assert_frame_equal(result, source)
    assert "Unnamed: 0" not in result.columns

def check_14_save_selected_columns(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1"], "age": [20], "city": ["A"]}
    )
    path = tmp_path / "report" / "selected.csv"
    assert module.save_selected_columns(
        source, path, ["age", "customer_id"]
    ) is None
    result = pd.read_csv(path)
    assert result.columns.tolist() == ["age", "customer_id"]
    with pytest.raises(KeyError):
        module.save_selected_columns(source, path, ["unknown"])

def check_14_save_city_summary(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame({"city": ["A", "A", "B", None]})
    path = tmp_path / "summary" / "city.csv"
    assert module.save_city_summary(source, path) is None
    result = pd.read_csv(path)
    assert result.to_dict("records") == [
        {"city": "A", "customer_count": 2},
        {"city": "B", "customer_count": 1},
    ]
    empty_path = tmp_path / "summary" / "empty.csv"
    module.save_city_summary(source.iloc[:0], empty_path)
    assert pd.read_csv(empty_path).empty

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_14_save_processed", answer, check_14_save_processed),
    ("answer_14_save_selected_columns", answer, check_14_save_selected_columns),
    ("answer_14_save_city_summary", answer, check_14_save_city_summary),
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
