"""Matplotlib《Matplotlib 06：可靠保存图片并释放 Figure》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from .._figure_helpers import assert_image, capture_saved_figures
from . import answer
from . import practice

Check = Callable[[ModuleType, Path, pytest.MonkeyPatch], None]

def check_06_save_churn_figure(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"churn": [0, 1, 0, None]})
    path = tmp_path / "nested" / "churn.png"
    records = capture_saved_figures(monkeypatch)
    module.save_churn_figure(source, path)
    assert_image(path)
    assert records[0]["kwargs"]["dpi"] >= 120
    assert records[0]["kwargs"]["bbox_inches"] == "tight"
    assert records[0]["axes"][0]["patch_heights"] == [2, 1]

def check_06_save_transparent_spending_scatter(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"age": [20, 30], "monthly_spending": [100, 200]}
    )
    path = tmp_path / "transparent" / "spending.png"
    records = capture_saved_figures(monkeypatch)
    module.save_transparent_spending_scatter(source, path)
    assert_image(path)
    assert records[0]["kwargs"]["dpi"] == 200
    assert records[0]["kwargs"]["transparent"] is True
    assert records[0]["kwargs"]["bbox_inches"] == "tight"

def check_06_save_city_figure_formats(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"city": ["B", "A", "A"]})
    output_directory = tmp_path / "formats"
    records = capture_saved_figures(monkeypatch)
    paths = module.save_city_figure_formats(source, output_directory)
    assert paths == [
        output_directory / "city_counts.png",
        output_directory / "city_counts.pdf",
    ]
    assert len(records) == 2
    for path in paths:
        assert_image(path)
    assert [record["filename"].suffix for record in records] == [".png", ".pdf"]
    assert all(record["kwargs"]["dpi"] == 150 for record in records)
    assert records[0]["axes"][0]["patch_heights"] == [2, 1]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_06_save_churn_figure", answer, check_06_save_churn_figure),
    ("answer_06_save_transparent_spending_scatter", answer, check_06_save_transparent_spending_scatter),
    ("answer_06_save_city_figure_formats", answer, check_06_save_city_figure_formats),
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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    check(module, tmp_path, monkeypatch)


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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    try:
        check(module, tmp_path, monkeypatch)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
