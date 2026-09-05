"""Matplotlib《Matplotlib 02：用直方图查看数值分布》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from .._figure_helpers import assert_image, capture_saved_figures
from . import answer
from . import practice

Check = Callable[[ModuleType, Path, pytest.MonkeyPatch], None]

def check_02_plot_age_histogram(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"age": ["20", "bad", 40, None]})
    path = tmp_path / "nested" / "age.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_age_histogram(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Customer Age Distribution"
    assert len(axis["patch_heights"]) == 5
    assert sum(axis["patch_heights"]) == 2

def check_02_plot_spending_histogram(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"monthly_spending": ["100", "bad", 200, 300]}
    )
    path = tmp_path / "nested" / "spending.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_spending_histogram(source, path, 3)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert len(axis["patch_heights"]) == 3
    assert sum(axis["patch_heights"]) == 3
    invalid_path = tmp_path / "nested" / "invalid.png"
    with pytest.raises(ValueError):
        module.plot_spending_histogram(source, invalid_path, 0)
    assert not invalid_path.exists()

def check_02_plot_age_histograms_by_churn(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"age": [20, 30, 40, "bad"], "churn": [0, 1, 1, 0]}
    )
    path = tmp_path / "nested" / "age_churn.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_age_histograms_by_churn(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Age Distribution by Churn"
    assert axis["legend_labels"] == ["Stayed", "Churned"]
    assert sum(axis["patch_heights"]) == 3

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_02_plot_age_histogram", answer, check_02_plot_age_histogram),
    ("answer_02_plot_spending_histogram", answer, check_02_plot_spending_histogram),
    ("answer_02_plot_age_histograms_by_churn", answer, check_02_plot_age_histograms_by_churn),
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
